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