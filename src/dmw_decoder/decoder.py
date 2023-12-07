import csv

import httpx

def read_csv(filename: str) -> dict:
    addresses = {}
    with open(filename) as file:
        for line in csv.DictReader(file):
            building_id = normalize_building_id(line["Building ID"])
            addresses[building_id] = line
    return addresses


def get_address_by_building_id(csv_data: dict, building_id: str) -> str:
    normalized_building_id = normalize_building_id(building_id)
    try:
        return csv_data[normalized_building_id]["Address"]
    except KeyError:
        raise KeyError(f"The value {building_id} is not in lookup csv.")


def geo_lookup_by_address(lookup_address: str, api_key: str, client = httpx.Client()) -> dict:
    base_url = "https://api.geoapify.com/v1/geocode/search?text="
    params = f"&format=json&apiKey={api_key}"
    response = client.get(f"{base_url}{lookup_address}{params}")
    response.raise_for_status()
    return response.json()


def get_timezone_by_address(lookup_address: str, api_key: str, client = httpx.Client()) -> str:
    geo_data = geo_lookup_by_address(lookup_address, api_key, client)
    # If confidence is > 45% return first result's timezone
    if geo_data["results"][0]["rank"]["confidence"] > 0.45:
        return geo_data["results"][0]["timezone"]["abbreviation_STD"]
    else:
        return "TBD"


def normalize_building_id(building_id: str) -> str:
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


def format_device_function(device: str) -> str:
    device = device.lower().strip()
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


def netbios_compatibility_check(name: str) -> None:
    disallowed = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    min_length = 1
    max_length = 15
    if any(item in name for item in disallowed):
        raise ValueError("Name contains disallowed character")
    if len(name) < min_length:
        raise ValueError("Name does not meet minimum length")
    if len(name) > max_length:
        raise ValueError("Name exceeds maximum length")


def entity_check(name: str) -> str:
    min_length = 3
    max_length = 7
    if len(name) < min_length:
        raise ValueError("Name does not meet minimum length")
    if len(name) > max_length:
        raise ValueError("Name exceeds maximum length")
    else:
        return name


def truncate_component(component: str, name: str) -> str:
    max_length = 15
    remaining_chars = max_length - len(name)
    if remaining_chars == 0:
        return ""
    elif remaining_chars < 0:
        raise ValueError("Name exceeds maximum length")
    else:
        leftovers = component[:remaining_chars]
        return leftovers


def create_netbios_compatible_name(building_id: str, device_function: str, entity: str, component: str, api_key: str, site_csv: str = 'Buildings.csv', client = httpx.Client()) -> str:
    sites = read_csv(site_csv)
    normal_building_id = normalize_building_id(building_id)
    formatted_device_function = format_device_function(device_function)
    address = get_address_by_building_id(sites, building_id)
    timezone = get_timezone_by_address(address, api_key, client=client)
    checked_entity = entity_check(entity)
    partial_name = f"{normal_building_id}{formatted_device_function}{timezone}{checked_entity}"
    formatted_component = truncate_component(component, partial_name)
    final_name = partial_name + formatted_component
    netbios_compatibility_check(final_name)
    return final_name

def main(**kwargs) -> str:
    return create_netbios_compatible_name(**kwargs)

if __name__ == "__main__":
    main()