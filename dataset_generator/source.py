import math
import numpy as np
import random
from random_word import RandomWords

r = RandomWords()

# TOTAL AMOUNTS
NUMBER_PATIENTS = 2000
# This is the maximum number of practitioners it seems?
NUMBER_OF_PRACTITIONERS = 200
NUMBER_OF_ORGANIZATIONS = 30

# MAPPING AMOUNTS
ENCOUNTERS_PER_PATIENT = [1.01, 2]

# MAXIMUM REQUIRED QUERIES
MAX_NUMBER_ENCOUNTERS = int((ENCOUNTERS_PER_PATIENT[0] + 0.66 * (ENCOUNTERS_PER_PATIENT[1] - ENCOUNTERS_PER_PATIENT[0])) * NUMBER_PATIENTS)

PRACS_PER_PATIENT = [1, 3]
PRACS_PER_ENCOUNTER = [1, 3.5]
ORGS_PER_PRAC = [1, 5.5]

########### OBSERVATIONS ####################
def distribution(x):
    up_the_line = random.random()
    up_the_line *= up_the_line
    mag = random.random()
    mag *= mag
    mag = (1 - up_the_line) * (1 - mag)
    flip1 = random.random() > 0.5
    flip2 = random.random() > 0.5
    line_point = (up_the_line, -up_the_line) if flip1 else (-up_the_line, up_the_line)
    bottom_left = (100, 150)
    size = (40, 20)
    relative = (line_point[0] + mag, line_point[1] + mag) if flip2 else (line_point[0] - mag, line_point[1] - mag)
    return [
        (relative[0] + 1)/2 * size[0] + bottom_left[0],
        (relative[1] + 1)/2 * size[1] + bottom_left[1]
    ]
    
OBSERVATION_PRESSURE = ["55284-4", "Blood_Pressure", [1.3, 2.4], {
    "value_generator": (lambda x: distribution(x))
}]
OBSERVATION_SMOKING = ["72166-2", "Tobacco Smoking Status", [0.5, 1.5], {}]
OBSERVATION_PLATELET = [
    "32623-1",
    "Platelet Mean Volume",
    [1.01, 3.5],
    {"value_generator": (lambda x: np.random.normal(15, 5))},
]
def bionic_map(obj, v):
    obj["code"]["coding"][0]["code"] = "94235-3"
    obj["code"]["coding"][0]["display"] = "Bionic preffered enhancement"
    obj["code"]["text"] = "Bionic preffered enhancement"
    obj["valueQuantity"] = {"value": v}
    return obj

RANDOM_BIONIC_CHOICES = [r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun") for _ in range(math.ceil(math.sqrt(NUMBER_PATIENTS)))]

BIONIC_DATA = ["718-7", "Bionic Enhancement", [1.01, 1.01], {"value_generator": (lambda x: random.choice(RANDOM_BIONIC_CHOICES)), "object_map": bionic_map}]

BODY_WEIGHT = ["29463-7", "Body Weight", [1.01, 2.5], {"value_generator": (lambda x: 45 + random.random() * 120)}]

HEMOGLOBIN = ["718-7", "Hemoglobin [Mass/volume] in Blood", [1.01, 1.01], {"value_generator": (lambda x: 10 + random.random() * 30)}]

# Example of correlating two observations, using a shared random generator.
"""shared_value = {}
def get_random(_id):
    if _id not in shared_value:
        shared_value[_id] = random.random()
    return shared_value[_id]
OBSERVATION_PLATELET = [
    "32623-1",
    "Platelet Mean Volume",
    [0.5, 3.5],
    {"value_generator": (lambda x: get_random(x) * 15 - 4)},
]
OBSERVATION_PRESSURE = ["55284-4", "Blood_Pressure", [0.8, 1.8], {"value_generator": (lambda x: get_random(x) * 5 + 20)}]"""

OBSERVATION_LIST = [OBSERVATION_PLATELET, BIONIC_DATA, OBSERVATION_PRESSURE, BODY_WEIGHT, HEMOGLOBIN]
#############################################

API_TOKEN = "b6ai0PI8aEEGrUGnMA18zAZsfqaBbFdD"
API_URL = "https://syntheticmass.mitre.org/v1/fhir/"

import os
import shutil
from .randomisation import RandomGenerator

def main():

    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "dataset"
    )

    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)
    os.mkdir(dataset_path)

    os.mkdir(os.path.join(dataset_path, "all_practitioners"))

    # Generate organizations, and practitioners for each organization.

    from .organizations import generate_organizations

    RandomGenerator.set_all_orgs(
        generate_organizations(NUMBER_OF_ORGANIZATIONS, API_URL, API_TOKEN, dataset_path)
    )

    from .practitioners import generate_practitioners

    RandomGenerator.set_all_pracs(
        generate_practitioners(NUMBER_OF_PRACTITIONERS, ORGS_PER_PRAC, API_URL, API_TOKEN, dataset_path)
    )

    # Generate patients, give them an organization, and pick some practitioners from that organization.

    from .patients import generate_patients

    generate_patients(NUMBER_PATIENTS, PRACS_PER_PATIENT, API_URL, API_TOKEN, dataset_path)

    # Generate encounters for a particular patient

    from .encounters import generate_encounters

    generate_encounters(
        ENCOUNTERS_PER_PATIENT,
        MAX_NUMBER_ENCOUNTERS,
        PRACS_PER_ENCOUNTER,
        API_URL,
        API_TOKEN,
        dataset_path,
    )

    # Generate observations for each encounter

    from .observations import generate_observations

    generate_observations(
        OBSERVATION_LIST, MAX_NUMBER_ENCOUNTERS, API_URL, API_TOKEN, dataset_path
    )

    from .validator import validate_unique_patients

    uniqueness = validate_unique_patients(dataset_path)
    if not uniqueness[0]:
        print("Duplicate Patients!")
    else:
        print("{} unique patients checked.".format(uniqueness[1]))
        # OUTPUT WAS: 193100 unique patients checked.

    from .combine import combine_all
    combine_all(dataset_path)

    # combined_dataset_path = os.path.join(dataset_path, 'build')
    # from replace_practitioner import merge_big_practitioners
    # merge_big_practitioners(combined_dataset_path)

if __name__ == "__main__":
    main()
