import pytest
import os
from dotenv import load_dotenv
from src.dmw_decoder.logic import Decoder
import json

load_dotenv()

api_key = os.getenv('GEOAPIFY')

with open('python-package/tests/functional_test_permutations.json') as file:
    permutations = json.load(file)


@pytest.mark.parametrize("params, expected_result", permutations)
# Warning, this test is somewhat fragile due to the way the csv is loaded
def test_functional_testing_for_all_valid_options(params, expected_result):
    decode = Decoder(api_key=api_key, site_csv='python-package/src/dmw_decoder/data/Buildings.csv')
    assert decode.create_netbios_compatible_name(**params) == expected_result
