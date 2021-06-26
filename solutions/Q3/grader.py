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

import os, sys, math
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")[1:]
        out_data = case.output_data().decode('utf-8').split("\n")[1:]

        # [0] = number of test cases
        # [1:] = test case inputs

        # 50 tests, 3%, worth 20%: 0.4% p test
        # 20 tests, 30%, worth 30%: 1.5% p test
        # 5 tests, 98%, worth 50%: 10% p test

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        print(in_data[0], file=sys.stderr)
        interactor.writeln(in_data[0])

        correct = 0
        tests = int(in_data[0])
        cur_sol_index = 0

        for x in range(tests):
            d = float(in_data[2*x+1].split()[0])
            interactor.writeln(in_data[2*x+1])
            interactor.writeln(in_data[2*x+2])
            patients = in_data[2*x+2].split()
            sorted_values = sorted([
                (min([
                    (datetime.datetime.fromisoformat(obs.effective), obs.value["value"]) 
                    for obs_id in data['patients'][_id].observations 
                    if (obs := data['observations'][obs_id]).code == "8302-2"
                ])[1], _id)
                for _id in patients
            ])[::-1]

            vals = {
                _id: (i, v)
                for i, (v, _id) in enumerate(sorted_values)
            }
            # Read all the rectangles
            n_gens = interactor.readint()
            total_cost = 0
            cur_shortest = 0
            for r in range(n_gens):
                pat1 = interactor.readtoken().decode("utf-8")
                pat2 = interactor.readtoken().decode("utf-8")

                if pat1 not in vals or pat2 not in vals:
                    return CheckerResult(False, 0, "Invalid selection of patients given.")
                if vals[pat1][0] > cur_shortest and vals[pat2][0] > cur_shortest:
                    print(vals[pat1][0], vals[pat2][0], file=sys.stderr)
                    return CheckerResult(False, 0, "Both patients given have not been generalised for yet.")
                cur_shortest = max(vals[pat1][0], vals[pat2][0])
                total_cost += math.log(
                    # Difference in height
                    abs(vals[pat1][1] - vals[pat2][1]) / 
                    # d * (difference in position + 1)
                    (d * (abs(vals[pat1][0] - vals[pat2][0]) + 1))
                )
            if cur_shortest != len(vals.keys()) - 1:
                return CheckerResult(False, 0, "Not every patient covered after generalisation.")

            # Calculate the cost of the solution data.
            n_sol_gens = int(out_data[cur_sol_index])
            cur_sol_index += 1
            sol_cost = 0
            for r in range(n_sol_gens):
                pat1, pat2 = out_data[cur_sol_index].split()
                sol_cost += math.log(
                    # Difference in height
                    abs(vals[pat1][1] - vals[pat2][1]) / 
                    # d * (difference in position + 1)
                    (d * (abs(vals[pat1][0] - vals[pat2][0]) + 1))
                )
                cur_sol_index += 1
            # Higher cost than sol = bad.
            # Assume that 97% of sol cost is best, and 115% of sol is 0 score. And linearly interpolate.
            print(sol_cost + len(patients), total_cost + len(patients), file=sys.stderr)
            pct = (1.15 * (sol_cost + len(patients)) - total_cost - len(patients)) / (0.18 * (sol_cost + len(patients)))
            pct = max(min(pct, 1), 0)
            if x < 50:
                correct += 0.4 * pct
            elif x < 70:
                correct += 1.5 * pct
            else:
                correct += 10 * pct

        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}%")
