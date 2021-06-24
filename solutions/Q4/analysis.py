import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
from os.path import join as J

def read_dataset(dataset_path):
    organizations = {}
    practitioners = {}
    patients = {}
    encounters = {}
    observations = {}

    for objects, filename, klass in [
        (organizations, "organizations", Organization),
        (practitioners, "practitioners", Practitioner),
        (patients, "patients", Patient),
        (encounters, "encounters", Encounter),
        (observations, "observations", Observation),
    ]:
        # print("Reading file", filename)

        with open(J(dataset_path, filename + ".json"), "r") as f:
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

    return {
        "organizations": organizations,
        "practitioners": practitioners,
        "patients": patients,
        "encounters": encounters,
        "observations": observations,
    }

data = read_dataset("dataset/build")

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

in_data = open("solutions/Q4/1.in", "r").readlines()[2:]
out_data = open("solutions/Q4/1.out", "r").readlines()[1:]

# https://stackoverflow.com/a/18391039
curr_pos = 0

fig = plt.figure()
ax = fig.add_subplot(111)

def draw(index):
    # ax.plot([100, 160], [150, 170])
    cur_index = 0
    for i, l in enumerate(out_data):
        if l[0] != "C":
            cur_index += 1
            if cur_index > index:
                data_index = i
                break
    n_rects = int(out_data[data_index])
    patients = in_data[index].split()
    for r in range(n_rects):
        c, d, p, *c_patients = out_data[data_index + r+1].split()
        mlx, mly, mhx, mhy = min(vals[pat][0] for pat in c_patients), min(vals[pat][1] for pat in c_patients), max(vals[pat][0] for pat in c_patients), max(vals[pat][1] for pat in c_patients)
        ax.add_patch(Rectangle((mlx, mly), mhx-mlx, mhy-mly, facecolor="green", edgecolor="pink", alpha=0.3, fill=True, lw=1))
    ax.scatter([vals[pat][0] for pat in patients], [vals[pat][1] for pat in patients], s=5)
    fig.canvas.draw()


def key_event(e):
    global curr_pos

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(in_data)

    ax.cla()
    print(curr_pos)
    draw(curr_pos)

fig.canvas.mpl_connect('key_press_event', key_event)
draw(0)
plt.show()