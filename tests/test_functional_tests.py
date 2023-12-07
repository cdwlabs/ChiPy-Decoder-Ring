import pytest
import os
from dotenv import load_dotenv
import decoder
import json

load_dotenv()

api_key = os.getenv('GEOAPIFY')

with open('tests/functional_test_permutations.json') as file:
    permutations = json.load(file)


@pytest.mark.parametrize("params, expected_result", permutations)
def test_functional_testing_for_all_valid_options(params, expected_result):
    params['api_key'] = api_key
    assert decoder.main(**params) == expected_result 
