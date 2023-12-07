import itertools
import json
import os
import sys
import time

from dotenv import load_dotenv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import src.dmw_decoder.logic as logic

'''
This "utility" creates all permutations for valid system names
and saves them in to a json file for easier loading via pytest's
parametrize
**Note** This expects the output of the script to be the source
of truth for testing. If introduced bugs cause bad values, these
tests may not fail properly and lead to bad test results. 
'''

load_dotenv()

api_key = os.getenv("GEOAPIFY")

buildings = ["1", "22", "7", "15", "53", "82", "2", "9"]
device_functions = ["server", "network", "virtualized", "app", "other"]
entity = ["--3", "four", "-five", "---six", "--seven"]
component = ["-01", "01-temp-fl2-goofy"]

all_permutations = list(
    itertools.product(buildings, device_functions, entity, component, [api_key])
)
everything = []
for i, tup in enumerate(all_permutations):
    total_permutations = len(all_permutations)
    single_test_data = ()
    params = {
        "building_id": tup[0],
        "device_function": tup[1],
        "entity": tup[2],
        "component": tup[3],
        "api_key": tup[4],
    }
    output = logic.main(**params)
    del params["api_key"]
    single_test_data = (params, output)
    everything.append(single_test_data)
    time.sleep(0.05)
    print(f'Item {i} of {total_permutations}')

json_object = json.dumps(everything)

with open("tests/functional_test_permutations.json", "w") as outfile:
    outfile.write(json_object)
