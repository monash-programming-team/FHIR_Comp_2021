import sys
import math
import random
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        # In data: list of patients, with blood values.
        in_data = list(map(lambda x: (x.split(" ")[0], float(x.split(" ")[1])), filter(bool, case.input_data().decode('utf-8').split("\n"))))

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        tests = 100

        interactor.writeln(tests)

        correct = 0

        v_mapping = {
            d[0]: d[1]
            for d in in_data
        }

        lying = [random.randint(0, 1) for _ in range(7)]

        for x in range(tests):
            while True:
                length = random.random() * (in_data[-1][1] - in_data[0][1])
                start = in_data[0][1] + random.random()*(in_data[-1][1] - in_data[0][1] - length)
                l, r = None, None
                for y in range(len(in_data)):
                    if in_data[y][1] >= start and l is None:
                        l = y
                    if in_data[y][1] <= start + length:
                        r = y
                if r - l < 1: continue
                # Must not include everyone
                if l == 0 and r == len(in_data): continue
                best = random.randint(l, r)
                break
            interactor.writeln(f"{start} {start+length}")

            n_queries = 0
            expected_queries = 30

            while True:
                query = interactor.readtoken().decode('utf-8')
                if query == "A":
                    patient = interactor.readtoken().decode('utf-8')
                    if (patient == best and n_queries < expected_queries):
                        correct += 1
                    break
                if query == "Q":
                    n_queries += 1
                    patient = interactor.readtoken().decode('utf-8')
                    if patient not in v_mapping:
                        return CheckerResult(False, 0, f"Non-unique weighing given.")
                    if int(v_mapping[patient] <= in_data[best][1]) + int(lying[n_queries % 7]) == 1:
                        interactor.writeln("SAFE")
                    else:
                        interactor.writeln("DANGEROUS")

        correct = min(correct, tests)
        correct = max(correct, 0)
        return CheckerResult(True, case.points * correct / tests, f"Scored {100 * correct / tests:.2f}\%")
