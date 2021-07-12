class Resource:
    def __init__(self, data, all_objects):
        self.id = data["resource"]["id"]
        if "active" in data["resource"] and not data["resource"]["active"]:
            print("Inactive {} found".format(data["resource"]["resourceType"]))


class Organization(Resource):
    def __init__(self, data, all_objects):
        super().__init__(data, all_objects)
        if len(data["resource"]["address"]) > 1:
            print("Organization found with more than one address")

        address = data["resource"]["address"][0]

        self.country = str(address["country"]).lower()
        self.state = str(address["state"]).lower()
        self.city = str(address["city"]).lower()
        self.post_code = str(address["postalCode"])

        self.name = data["resource"]["name"]

        self.practitioners = []
        self.patients = []


class Practitioner(Resource):
    def __init__(self, data, all_objects):
        super().__init__(data, all_objects)

        self.patients = []
        self.organizations = []


class Patient(Resource):
    def __init__(self, data, all_objects):
        super().__init__(data, all_objects)

        self.gender = data["resource"]["gender"]

        self.identifier = data['resource']['identifier']

        self.organization = data["resource"]["managingOrganization"]["reference"].split(":")[-1]
        self.practitioners = [
            obj["reference"].split(":")[-1]
            for obj in data["resource"]["generalPractitioner"]
        ]
        self.encounters = []
        self.observations = []
        all_objects["organizations"][self.organization].patients.append(self.id)
        for prac in self.practitioners:
            all_objects["practitioners"][prac].patients.append(self.id)
        for prac in self.practitioners:
            all_objects["organizations"][self.organization].practitioners.append(prac)
            all_objects["practitioners"][prac].organizations.append(self.organization)


class Encounter(Resource):
    def __init__(self, data, all_objects):
        super().__init__(data, all_objects)

        self.patient = data["resource"]["subject"]["reference"].split(":")[-1]
        self.practitioners = list(map(lambda x: x["individual"]["reference"].split(":")[-1], data["resource"]["participant"]))
        self.period_start = data["resource"]["period"]["start"]
        all_objects["patients"][self.patient].encounters.append(self.id)


class Observation(Resource):
    def __init__(self, data, all_objects):
        super().__init__(data, all_objects)

        self.code = data["resource"]["code"]["coding"][0]["code"]
        self.value = data["resource"].get("valueQuantity", None)

        try:
            self.valueCode = data['resource']['valueCodeableConcept']['coding'][0]['code']
        except Exception:
            self.valueCode = None

        self.effective = data["resource"]["effectiveDateTime"]
        self.component = data["resource"].get("component", [])

        self.encounter = data["resource"]["context"]["reference"].split("/")[1]
        self.patient = data["resource"]["subject"]["reference"].split(":")[-1]
        all_objects["patients"][self.patient].observations.append(self.id)
import json
from os import listdir
from os.path import join as J

def read_dataset(dataset_path):
    organizations = {}
    practitioners = {}
    patients = {}
    encounters = {}
    observations = {}

    for objects, dirname, klass in [
        (organizations, "organizations", Organization),
        (practitioners, "practitioners", Practitioner),
        (patients, "patients", Patient),
        (encounters, "encounters", Encounter),
        (observations, "observations", Observation),
    ]:
        # print("Reading file", dirname)

        for fname in listdir(J(dataset_path, dirname)):
            with open(J(dataset_path, dirname, fname), "r") as f:
                bundle_group = json.loads(f.read())["entry"]

            all_objects = list(map(lambda o: klass(o, {
                "organizations": organizations,
                "practitioners": practitioners,
                "patients": patients,
                "encounters": encounters,
                "observations": observations,
            }), bundle_group))
            for obj in all_objects:
                objects[obj.id] = obj

    # Make sure that org and practitioner relations are sets.
    for org_obj in organizations.values():
        org_obj.practitioners = list(set(org_obj.practitioners))
    for prac_obj in practitioners.values():
        prac_obj.organizations = list(set(prac_obj.organizations))

    """print(
        "Read data:\n{} Organizations\n{} Practitioners\n{} Patients\n{} Encounters\n{} Observations".format(
            len(organizations),
            len(practitioners),
            len(patients),
            len(encounters),
            len(observations),
        )
    )"""

    return {
        "organizations": organizations,
        "practitioners": practitioners,
        "patients": patients,
        "encounters": encounters,
        "observations": observations,
    }

data = read_dataset("dataset/build")

import random, math

n_easy = 50   # 3% patients
n_medium = 20 # 30% patients
n_hard = 5   # 98% patients

patients = list(data["patients"].keys())
pct = len(patients) // 100

with open("solutions/Q1/1.in", "w") as f:
    print("dataset/build", file=f)
    print(n_easy, file=f)
    for x in range(n_easy):
        start = random.randint(0, len(patients) - 3 * pct)
        n = random.randint(3 * pct - 5, 3 * pct + 5)
        print(n, 3 * pct, " ".join(patients[start: start+3 * pct]), file=f)

with open("solutions/Q1/2.in", "w") as f:
    print("dataset/build", file=f)
    print(n_medium, file=f)
    for x in range(n_medium):
        start = random.randint(0, len(patients) - 30 * pct)
        n = random.randint(30 * pct - 30, 30 * pct + 30)
        print(n, 30 * pct, " ".join(patients[start: start+30 * pct]), file=f)

with open("solutions/Q1/3.in", "w") as f:
    print("dataset/build", file=f)
    print(n_hard, file=f)
    for x in range(n_hard):
        start = random.randint(0, len(patients) - 2 * pct)
        n = random.randint(98 * pct - 100, 98 * pct + 100)
        print(n, len(patients) - 2 * pct, " ".join(patients[:start] + patients[start+2 * pct:]), file=f)

