import os
import json
import shutil
import re

def create_bundle(filepath, data):
    with open(os.path.join(filepath.replace("/", "\\")), "w") as f:
        bundle = """\
{
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [\
    """
        f.write(bundle)
        f.write("".join(data))
        end = """
  ]
}\
"""
        f.write(end)

def combine_all(directory_path):
    print("=== Combining all data files")
    build_path = os.path.join(directory_path, "build")
    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    os.mkdir(build_path)

    # Create a new empty file
    for key in ["organizations", "practitioners", "patients", "encounters", "observations"]:
        os.mkdir("{}/{}".format(build_path, key))

    org_counter = 0
    org_string = []
    enc_counter = 0
    enc_string = []
    pat_counter = 0
    pat_string = []
    obs_counter = 0
    obs_string = []
    pra_counter = 0
    pra_string = []

    organizations = list(
        filter(
            lambda x: os.path.isdir(os.path.join(directory_path, "organizations", x)),
            os.listdir(os.path.join(directory_path, "organizations")),
        )
    )
    for org_index, organization in enumerate(organizations):
        print("O", (org_index + 1) / len(organizations) * 100)
        org_path = os.path.join(directory_path, "organizations", organization)
        with open("{}/{}.json".format(org_path, organization), "r") as f:
            org_object = json.loads(f.read())
            org_object["request"] = {"method": "POST", "url": "Organization"}

        text = json.dumps(org_object, indent=2)
        org_string.append("\n    " + "\n    ".join(text.split("\n")) + ",")
        if len(org_string) == 1000:
            create_bundle("{}/organizations/{}.json".format(build_path, org_counter), org_string)
            org_string = []
            org_counter += 1

        patients = list(
            filter(
                lambda x: os.path.isdir(os.path.join(org_path, "patients", x)),
                os.listdir(os.path.join(org_path, "patients")),
            )
        )
        for pat_index, patient in enumerate(patients):
            if (pat_index % 100 == 0):
                print("P", (pat_index + 1) / len(patients) * 100)
            patient_path = os.path.join(org_path, "patients", patient)
            with open("{}/{}.json".format(patient_path, patient), "r") as f:
                patient_object = json.loads(f.read())
                patient_object["request"] = {"method": "POST", "url": "Patient"}
            text = json.dumps(patient_object, indent=2)
            pat_string.append("\n    " + "\n    ".join(text.split("\n")) + ",")
            if len(pat_string) == 1000:
                create_bundle("{}/patients/{}.json".format(build_path, pat_counter), pat_string)
                pat_string = []
                pat_counter += 1

            encs = list(
                filter(
                    lambda x: os.path.isdir(os.path.join(patient_path, "encounters", x)),
                    os.listdir(os.path.join(patient_path, "encounters")),
                )
            )
            for encounter in encs:
                encounter_path = os.path.join(patient_path, "encounters", encounter)
                with open("{}/{}.json".format(encounter_path, encounter), "r") as f:
                    encounter_object = json.loads(f.read())
                    encounter_object["request"] = {
                        "method": "POST",
                        "url": "Encounter",
                    }
                text = json.dumps(encounter_object, indent=2)
                enc_string.append("\n    " + "\n    ".join(text.split("\n")) + ",")
                if len(enc_string) == 1000:
                    create_bundle("{}/encounters/{}.json".format(build_path, enc_counter), enc_string)
                    enc_string = []
                    enc_counter += 1

                obss = list(os.listdir(os.path.join(encounter_path, "observations")))
                for observation in obss:
                    observation_path = os.path.join(encounter_path, "observations", observation)
                    with open(observation_path, "r") as f:
                        observation_object = json.loads(f.read())
                        observation_object["request"] = {
                            "method": "POST",
                            "url": "Observation",
                        }
                    text = json.dumps(observation_object, indent=2)
                    obs_string.append("\n    " + "\n    ".join(text.split("\n")) + ",")
                    if len(obs_string) == 1000:
                        create_bundle("{}/observations/{}.json".format(build_path, obs_counter), obs_string)
                        obs_string = []
                        obs_counter += 1

    pracs = os.listdir(os.path.join(directory_path, "all_practitioners"))

    for prac in pracs:
        prac_path = os.path.join(directory_path, "all_practitioners", prac)
        with open(prac_path, "r") as f:
            prac_object = json.loads(f.read())
            prac_object["request"] = {"method": "POST", "url": "Practitioner"}

        text = json.dumps(prac_object, indent=2)
        pra_string.append("\n    " + "\n    ".join(text.split("\n")) + ",")
        if len(pra_string) == 1000:
            create_bundle("{}/practitioners/{}.json".format(build_path, pra_counter), pra_string)
            pra_string = []
            pra_counter += 1

    if obs_string:
        create_bundle("{}/observations/{}.json".format(build_path, obs_counter), obs_string)
    if enc_string:
        create_bundle("{}/encounters/{}.json".format(build_path, enc_counter), enc_string)
    if pat_string:
        create_bundle("{}/patients/{}.json".format(build_path, pat_counter), pat_string)
    if org_string:
        create_bundle("{}/organizations/{}.json".format(build_path, org_counter), org_string)
    if pra_string:
        create_bundle("{}/practitioners/{}.json".format(build_path, pra_counter), pra_string)

    for key in ["organizations", "practitioners", "patients", "encounters", "observations"]:
        for fname in os.listdir("{}\\{}".format(build_path, key)):
            json_file = open("{}\\{}\\{}".format(build_path, key, fname), "r+")
            fix_urn_data = re.sub(
                "[a-zA-Z]*https:\/\/syntheticmass.mitre.org\/v1\/fhir\/[a-zA-Z]*\/",
                "urn:uuid:",
                json_file.read(),
                flags=re.MULTILINE,
            )
            # Find the last comma and remove it
            for index in range(1, len(fix_urn_data) + 1):
                if fix_urn_data[-index] == ",":
                    fix_urn_data = fix_urn_data[:-index] + fix_urn_data[-(index - 1):]
                    break
            data = json.loads(fix_urn_data)
            json_file.seek(0)
            json_file.truncate()
            json_file.write(json.dumps(data, indent=2))
            json_file.close()

    print("Created, now removing intermediate files...")

    shutil.rmtree(os.path.join(directory_path, "organizations"))
    shutil.rmtree(os.path.join(directory_path, "all_practitioners"))
    print("Done.")
