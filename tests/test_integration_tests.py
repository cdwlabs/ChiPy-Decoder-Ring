import os

from dotenv import load_dotenv

import src.dmw_decoder.decoder as decoder

load_dotenv()

api_key = os.getenv("GEOAPIFY")

expected_result = {
    "results": [
        {
            "datasource": {
                "sourcename": "openstreetmap",
                "attribution": "© OpenStreetMap contributors",
                "license": "Open Database License",
                "url": "https://www.openstreetmap.org/copyright",
            },
            "country": "United States",
            "country_code": "us",
            "state": "Illinois",
            "county": "Cook County",
            "city": "Chicago",
            "municipality": "West Chicago Township",
            "postcode": "60661",
            "district": "Greektown",
            "suburb": "Near West Side",
            "street": "West Adams Street",
            "housenumber": "625",
            "lon": -87.64356872182887,
            "lat": 41.8788457,
            "state_code": "IL",
            "formatted": "625 West Adams Street, Chicago, IL 60661, United States of America",
            "address_line1": "625 West Adams Street",
            "address_line2": "Chicago, IL 60661, United States of America",
            "category": "building",
            "timezone": {
                "name": "America/Chicago",
                "offset_STD": "-06:00",
                "offset_STD_seconds": -21600,
                "offset_DST": "-05:00",
                "offset_DST_seconds": -18000,
                "abbreviation_STD": "CST",
                "abbreviation_DST": "CDT",
            },
            "plus_code": "86HJV9H4+GH",
            "plus_code_short": "V9H4+GH Chicago, Cook County, United States",
            "result_type": "building",
            "rank": {
                "importance": 0.41000999999999993,
                "popularity": 7.6308646473839925,
                "confidence": 1,
                "confidence_city_level": 1,
                "confidence_street_level": 1,
                "match_type": "full_match",
            },
            "place_id": "51f23edd3a30e955c05978dd11047ef04440f00102f901c8c2dc0800000000c00203",
            "bbox": {
                "lon1": -87.6438186,
                "lat1": 41.8784333,
                "lon2": -87.6433173,
                "lat2": 41.8791768,
            },
        },
        {
            "datasource": {
                "sourcename": "openstreetmap",
                "attribution": "© OpenStreetMap contributors",
                "license": "Open Database License",
                "url": "https://www.openstreetmap.org/copyright",
            },
            "country": "United States",
            "country_code": "us",
            "state": "Illinois",
            "county": "Cook County",
            "city": "Chicago",
            "municipality": "West Chicago Township",
            "postcode": "60661",
            "district": "Greektown",
            "suburb": "Near West Side",
            "street": "West Adams Street",
            "housenumber": "625",
            "lon": -87.64284017600023,
            "lat": 41.879188450375,
            "state_code": "IL",
            "formatted": "625 West Adams Street, Chicago, IL 60661, United States of America",
            "address_line1": "625 West Adams Street",
            "address_line2": "Chicago, IL 60661, United States of America",
            "timezone": {
                "name": "America/Chicago",
                "offset_STD": "-06:00",
                "offset_STD_seconds": -21600,
                "offset_DST": "-05:00",
                "offset_DST_seconds": -18000,
                "abbreviation_STD": "CST",
                "abbreviation_DST": "CDT",
            },
            "plus_code": "86HJV9H4+MV",
            "plus_code_short": "V9H4+MV Chicago, Cook County, United States",
            "result_type": "building",
            "rank": {
                "importance": -0.74,
                "popularity": 7.7691629884648234,
                "confidence": 1,
                "confidence_city_level": 1,
                "confidence_street_level": 1,
                "match_type": "full_match",
            },
            "place_id": "51751e1f4b24e955c059d6b0443f89f04440f00102f9013ed3081300000000c00203",
            "bbox": {
                "lon1": -87.642890176,
                "lat1": 41.879138450375,
                "lon2": -87.642790176,
                "lat2": 41.879238450375,
            },
        },
    ],
    "query": {
        "text": "625 W Adams St, Chicago, IL  60661, United States",
        "parsed": {
            "housenumber": "625",
            "street": "w adams st",
            "postcode": "60661",
            "city": "chicago",
            "state": "il",
            "country": "united states",
            "expected_type": "building",
        },
    },
}

address = "625 W Adams St, Chicago, IL  60661, United States"


def test_geo_lookup_by_address_integration():
    assert decoder.geo_lookup_by_address(address, api_key) == expected_result
