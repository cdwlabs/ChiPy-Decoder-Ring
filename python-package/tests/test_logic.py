import httpx
import pytest
from pytest_httpx import HTTPXMock

from src.dmw_decoder.logic import Decoder

mock_csv_dict = {
    "01": {
        "Building Name": "HQ",
        "Building ID": "1",
        "Address": "625 W Adams St, Chicago, IL  60661, United States",
    },
    "22": {
        "Building Name": "Denver",
        "Building ID": "22",
        "Address": "206 E 13th Ave, Denver, CO 80203",
    },
    "07": {
        "Building Name": "Grape City",
        "Building ID": "7",
        "Address": "3070 Limestone Way Suite C, Paso Robles, CA 93446",
    },
    "15": {
        "Building Name": "Targhee",
        "Building ID": "15",
        "Address": "3300 Ski Hill Rd, Alta, WY 83414",
    },
    "53": {
        "Building Name": "Vancouver",
        "Building ID": "53",
        "Address": "530 Robson St, Vancouver, BC V6B 2B7, Canada",
    },
    "82": {
        "Building Name": "Wren",
        "Building ID": "82",
        "Address": "94 St Aldate's, Oxford OX1 1BT, United Kingdom",
    },
    "02": {
        "Building Name": "Aran",
        "Building ID": "2",
        "Address": "2 Chome-5-8 Higashishinagawa, Shinagawa City, Tokyo 140-0002, Japan",
    },
    "09": {
        "Building Name": "Greenhouse",
        "Building ID": "9",
        "Address": "2655 South Park Ave, Buffalo, NY 14218",
    },
}


def test_normalize_building_id():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    assert decode.normalize_building_id("5") == "05"
    assert decode.normalize_building_id("15") == "15"
    with pytest.raises(ValueError):
        decode.normalize_building_id("not a number")
    with pytest.raises(ValueError):
        decode.normalize_building_id(150)


def test_format_device_function():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    assert decode.format_device_function("server") == "s"
    assert decode.format_device_function("network") == "n"
    assert decode.format_device_function("virtualized") == "v"
    assert decode.format_device_function("app") == "a"
    assert decode.format_device_function("other") == "o"
    assert decode.format_device_function("sErVeR") == "s"
    assert decode.format_device_function("Network   ") == "n"
    assert decode.format_device_function("  virtualized") == "v"
    assert decode.format_device_function("  other ") == "o"
    assert decode.format_device_function(" seRver ") == "s"
    with pytest.raises(ValueError):
        decode.format_device_function("cluster")


@pytest.mark.parametrize("disallowed", ["\\", "/", ":", "*", "?", '"', "<", ">", "|"])
def test_netbios_compatibility_check_disallowed(disallowed):
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    with pytest.raises(ValueError) as e_char:
        decode.netbios_compatibility_check(disallowed)
    assert str(e_char.value) == "Name contains disallowed character"
    with pytest.raises(ValueError) as e_min:
        decode.netbios_compatibility_check("")
    assert str(e_min.value) == "Name does not meet minimum length"


def test_netbios_compatibility_check_min():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    with pytest.raises(ValueError) as e_char:
        decode.netbios_compatibility_check("")
    assert str(e_char.value) == "Name does not meet minimum length"


def test_netbios_compatibility_check_max():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    with pytest.raises(ValueError) as e_char:
        decode.netbios_compatibility_check("Too long for NetBIOS I'm afraid")
    assert str(e_char.value) == "Name exceeds maximum length"


@pytest.mark.parametrize(
    "test_name, test_component, expected",
    [
        ("09sCSTserver", "01ABC", "01A"),
        ("10sCSTserv", "ABC123", "ABC12"),
        ("99sCSTb", "1", "1"),
        ("09sESTcore-sw01", "ZXY", ""),
    ],
)
def test_truncate_component(test_name, test_component, expected):
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    result = decode.truncate_component(name=test_name, component=test_component)
    assert len(result) + len(test_name) <= 15
    assert result == expected


def test_truncate_component_got_long_name():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    with pytest.raises(ValueError) as e_char:
        decode.truncate_component(name="This name is too long", component="NA")
    assert str(e_char.value) == "Name exceeds maximum length"


@pytest.mark.parametrize(
    "id, expected_address",
    [
        ("01", mock_csv_dict["01"]["Address"]),
        ("22", mock_csv_dict["22"]["Address"]),
        ("07", mock_csv_dict["07"]["Address"]),
        ("15", mock_csv_dict["15"]["Address"]),
        ("53", mock_csv_dict["53"]["Address"]),
        ("82", mock_csv_dict["82"]["Address"]),
        ("02", mock_csv_dict["02"]["Address"]),
        ("09", mock_csv_dict["09"]["Address"]),
    ],
)
def test_get_address_by_building_id(id, expected_address):
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    address = decode.get_address_by_building_id(mock_csv_dict, id)
    assert address == expected_address


def test_get_address_by_bad_building_id():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    bad_building_id = "33"
    with pytest.raises(KeyError) as e_char:
        decode.get_address_by_building_id(mock_csv_dict, bad_building_id)
    assert e_char.value.args[0] == f"The value {bad_building_id} is not in lookup csv."


def test_entity_check():
    decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
    assert decode.entity_check("Valid") == "Valid"
    with pytest.raises(ValueError) as e_char:
        decode.entity_check("A")
    assert e_char.value.args[0] == "Name does not meet minimum length"
    with pytest.raises(ValueError) as e_char:
        decode.entity_check("This is more than seven chars")
    assert e_char.value.args[0] == "Name exceeds maximum length"


def test_geo_lookup_by_address(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"key1": "value1", "key2": "value2"})

    with httpx.Client() as mock_client:
        address = "address"
        api_key = "key"
        decode = Decoder(api_key='key', site_csv='src/dmw_decoder/data/Buildings.csv', client=mock_client)
        assert decode.geo_lookup_by_address(address) == {
            "key1": "value1",
            "key2": "value2",
        }

        httpx_mock.add_response(status_code=404)
        expected_error = ("Client error '404 Not Found' for url "
        "'https://api.geoapify.com/v1/geocode/search?text=address&format=json&apiKey=key'\n"
        "For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404")
        from httpx import HTTPStatusError

        with pytest.raises(HTTPStatusError) as e_char:
            decode.geo_lookup_by_address(address)
        assert e_char.value.args[0] == expected_error


def test_confident_get_timezone_by_address(httpx_mock: HTTPXMock):
    address = "address"
    key = "key"
    mocked_response = {
        "results": [
            {
                "timezone": {
                    "name": "America/Chicago",
                    "offset_STD": "-06:00",
                    "offset_STD_seconds": -21600,
                    "offset_DST": "-05:00",
                    "offset_DST_seconds": -18000,
                    "abbreviation_STD": "CST",
                    "abbreviation_DST": "CDT",
                },
                "rank": {
                    "importance": 0.41000999999999993,
                    "popularity": 7.6308646473839925,
                    "confidence": 1,
                    "confidence_city_level": 1,
                    "confidence_street_level": 1,
                    "match_type": "full_match",
                },
            },
        ],
    }
    httpx_mock.add_response(json=mocked_response)
    with httpx.Client() as client:
        decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
        assert decode.get_timezone_by_address(address) == "CST"


def test_uncertain_get_timezone_by_address(httpx_mock: HTTPXMock):
    address = "address"
    key = "key"
    mocked_response = {
        "results": [
            {
                "timezone": {
                    "name": "America/Chicago",
                    "offset_STD": "-06:00",
                    "offset_STD_seconds": -21600,
                    "offset_DST": "-05:00",
                    "offset_DST_seconds": -18000,
                    "abbreviation_STD": "CST",
                    "abbreviation_DST": "CDT",
                },
                "rank": {
                    "importance": 0.41000999999999993,
                    "popularity": 7.6308646473839925,
                    "confidence": 0.1,
                    "confidence_city_level": 0.1,
                    "confidence_street_level": 0.1,
                    "match_type": "full_match",
                },
            },
        ],
    }
    httpx_mock.add_response(json=mocked_response)
    with httpx.Client() as client:
        decode = Decoder(api_key='', site_csv='src/dmw_decoder/data/Buildings.csv')
        assert decode.get_timezone_by_address(address) == "TBD"


@pytest.fixture()
def site_csv(tmp_path):
    file_content = 'Building Name,Building ID,Address\nAran,2,"2 Chome-5-8 Higashishinagawa, Shinagawa City, Tokyo 140-0002, Japan"'
    directory = tmp_path / "sub"
    directory.mkdir()
    filename = directory / "sites.csv"
    filename.write_text(file_content)
    return filename

def test_read_csv(site_csv):
    expected_result = {
        "02": {
            "Building Name": "Aran",
            "Building ID": "2",
            "Address": "2 Chome-5-8 Higashishinagawa, Shinagawa City, Tokyo 140-0002, Japan",
        }
    }
    decode = Decoder(api_key='', site_csv=site_csv)
    assert decode.read_csv() == expected_result
    bad_filename = "bogus"
    decode_fail = Decoder(api_key='', site_csv=bad_filename)
    with pytest.raises(FileNotFoundError) as e_char:
        decode_fail.read_csv()
    assert e_char.value.strerror == "No such file or directory"

def test_create_netbios_compatible_name(site_csv, httpx_mock: HTTPXMock):
    mocked_response = {"results": [{"timezone": {"abbreviation_STD": "JST"}, "rank": {"confidence": 1}}]}
    httpx_mock.add_response(json=mocked_response)
    with httpx.Client() as mock_client:
        test_params = {'building_id': '2', 
                'device_function': 'virtualized', 
                'entity': 'csr', 
                'component': '-01-temp', 
                }
        decode = Decoder(api_key='', site_csv=site_csv, client=mock_client)
        assert decode.create_netbios_compatible_name(**test_params) == '02vJSTcsr-01-te'
