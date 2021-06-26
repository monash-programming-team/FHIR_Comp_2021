import datetime
import decimal

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

data = read_dataset("/problems/data/dataset")

vals = {
    _id: [
        min([
            (datetime.datetime.fromisoformat(obs.effective), obs.component[x]["valueQuantity"]["value"]) 
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == "55284-4"
        ])[1]
        for x in range(2)
    ]
    for _id in data['patients']
}

import os, sys
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")[1:]
        out_data = case.output_data().decode('utf-8').split("\n")[1:]

        # [0] = number of test cases
        # [1:] = test case inputs

        # 5 tests, 10 patients, worth 20%: 4% p test
        # 3 tests, 25 patients, worth 30%: 10% p test
        # 2 tests, 40 patients, worth 50%: 25% p test

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        interactor.writeln(in_data[0])

        correct = 0
        tests = int(in_data[0])
        cur_sol_index = 0

        for x in range(tests):
            interactor.writeln(in_data[x+1])
            covered = {
                id_: False
                for id_ in in_data[x+1].split()
            }
            # Read all the rectangles
            n_rects = interactor.readint()
            total_cost = 0
            for r in range(n_rects):
                line = interactor.readln().decode("utf-8").split()
                if line[0] != "C":
                    return CheckerResult(False, 0, f"Expected token C, got {line[0]}")
                distance = float(line[1])
                total_cost += 10 + pow(distance, 1.5)
                if line[2] != "P":
                    return CheckerResult(False, 0, f"Expected token P, got {c}")
                for pat in line[3:]:
                    covered[pat] = True
                # Make sure it fits.
                mav0, miv0, mav1, miv1 = max(vals[pat][0] for pat in line[3:]), min(vals[pat][0] for pat in line[3:]), max(vals[pat][1] for pat in line[3:]), min(vals[pat][1] for pat in line[3:])
                if mav0 - miv0 + mav1 - miv1 > distance + 1e-9:
                    return CheckerResult(False, 0, "Invalid selection of patients given.")
            for key in covered:
                if covered[key] is False:
                    return CheckerResult(False, 0, "Not all patients covered by scheme.")
            # Calculate the cost of the solution data.
            n_sol_rects = int(out_data[cur_sol_index])
            cur_sol_index += 1
            sol_cost = 0
            for r in range(n_sol_rects):
                sol_cost += 10 + pow(float(out_data[cur_sol_index].split()[1]), 1.5)
                cur_sol_index += 1
            # Higher cost than sol = bad.
            # Assume that 95% of sol cost is best, and 125% of sol is 0 score. And linearly interpolate.
            pct = (1.25 * sol_cost - total_cost) / (0.3 * sol_cost)
            pct = max(min(pct, 1), 0)
            if x < 5:
                correct += 4 * pct
            elif x < 8:
                correct += 10 * pct
            else:
                correct += 25 * pct

        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}%")
