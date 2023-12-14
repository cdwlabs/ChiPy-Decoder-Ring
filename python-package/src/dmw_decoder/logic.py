import csv
import importlib.resources
import pathlib

import httpx


class Decoder:
    def __init__(
        self,
        api_key: str,
        site_csv: pathlib.Path = importlib.resources.files("dmw_decoder.data")
        / "Buildings.csv",
        client=httpx.Client(),
    ):
        self.api_key = api_key
        self.site_csv = site_csv
        self.client = client

    def read_csv(self) -> dict:
        addresses = {}
        with open(self.site_csv) as file:
            for line in csv.DictReader(file):
                building_id = self.normalize_building_id(line["Building ID"])
                addresses[building_id] = line
        return addresses

    def get_address_by_building_id(self, csv_data: dict, building_id: str) -> str:
        normalized_building_id = self.normalize_building_id(building_id)
        try:
            return csv_data[normalized_building_id]["Address"]
        except KeyError:
            raise KeyError(f"The value {building_id} is not in lookup csv.")

    def geo_lookup_by_address(self, lookup_address: str) -> dict:
        base_url = "https://api.geoapify.com/v1/geocode/search?text="
        params = f"&format=json&apiKey={self.api_key}"
        response = self.client.get(f"{base_url}{lookup_address}{params}")
        response.raise_for_status()
        return response.json()

    def get_timezone_by_address(self, lookup_address: str) -> str:
        geo_data = self.geo_lookup_by_address(lookup_address)
        # If confidence is > 45% return first result's timezone
        if geo_data["results"][0]["rank"]["confidence"] > 0.45:
            return geo_data["results"][0]["timezone"]["abbreviation_STD"]
        else:
            return "TBD"

    def normalize_building_id(self, building_id: str) -> str:
        try:
            id = int(building_id)
        except ValueError as e:
            print(f"The value {building_id} is not an integer. Error: {e}")
            raise
        if id >= 100:
            print(f"The value {building_id} is larger than 99.")
            raise ValueError
        elif id < 10 and len(building_id) < 2:
            padded_id = "0" + building_id
            return padded_id
        else:
            return building_id

    def format_device_function(self, device: str) -> str:
        device = device.lower().strip()
        # Potential pitfall!
        # We wanted to use a newer Python feature (match statement)
        # but for our supported version of Ansible we need to allow
        # for Python 3.9 users to run this code.
        """
        match device:
            case "server":
                return "s"
            case "network":
                return "n"
            case "virtualized":
                return "v"
            case "app":
                return "a"
            case "other":
                return "o"
            case _:
                raise ValueError("Invalid option")
        """
        if "server" in device:
            return "s"
        elif "network" in device:
            return "n"
        elif "virtualized" in device:
            return "v"
        elif "app" in device:
            return "a"
        elif "other" in device:
            return "o"
        else:
            raise ValueError("Invalid option")

    def netbios_compatibility_check(self, name: str) -> None:
        disallowed = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        min_length = 1
        max_length = 15
        if any(item in name for item in disallowed):
            raise ValueError("Name contains disallowed character")
        if len(name) < min_length:
            raise ValueError("Name does not meet minimum length")
        if len(name) > max_length:
            raise ValueError("Name exceeds maximum length")

    def entity_check(self, name: str) -> str:
        min_length = 3
        max_length = 7
        if len(name) < min_length:
            raise ValueError("Name does not meet minimum length")
        if len(name) > max_length:
            raise ValueError("Name exceeds maximum length")
        else:
            return name

    def truncate_component(self, component: str, name: str) -> str:
        max_length = 15
        remaining_chars = max_length - len(name)
        if remaining_chars == 0:
            return ""
        elif remaining_chars < 0:
            raise ValueError("Name exceeds maximum length")
        else:
            leftovers = component[:remaining_chars]
            return leftovers

    def create_netbios_compatible_name(
        self, building_id: str, device_function: str, entity: str, component: str
    ) -> str:
        sites = self.read_csv()
        normal_building_id = self.normalize_building_id(building_id)
        formatted_device_function = self.format_device_function(device_function)
        address = self.get_address_by_building_id(sites, building_id)
        timezone = self.get_timezone_by_address(address)
        checked_entity = self.entity_check(entity)
        partial_name = (
            f"{normal_building_id}{formatted_device_function}{timezone}{checked_entity}"
        )
        formatted_component = self.truncate_component(component, partial_name)
        final_name = partial_name + formatted_component
        self.netbios_compatibility_check(final_name)
        return final_name
