import sys
import math
import random
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        # In data: list of patients, with blood values.
        in_data = list(map(lambda x: (x.split(" ")[0], float(x.split(" ")[1])), filter(bool, case.input_data().decode('utf-8').split("\n"))))
        print(len(in_data), file=sys.stderr)

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        # Body weigth ranges from 45 to 165.
        # Distribution is uniform.

        # 60 tests, 3% of population,  Worth 20%, 0.3333% each
        # 20 tests, 30% of population, Worth 30%, 1.5% each
        # 10 tests, 98% of population, Worth 50%, 5% each

        tests = 60 + 20 + 10
        interactor.writeln(tests)
        print(tests, file=sys.stderr)

        correct = 0

        v_mapping = {
            d[0]: d[1]
            for d in in_data
        }
        print(len(v_mapping.keys()), file=sys.stderr)

        lying = [random.randint(0, 1) for _ in range(7)]

        for x in range(tests):
            while True:
                if x < 60:
                    length = (random.random() * 1.5 + 1.5) / 100 * 120
                elif x < 80:
                    length = (random.random() * 15 + 15) / 100 * 120
                else:
                    length = (random.random() * 2 + 96) / 100 * 120
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
            print(f"{start} {start+length}", file=sys.stderr)

            n_queries = 0
            expected_queries = 30

            while True:
                query = interactor.readtoken().decode('utf-8')
                if query == "A":
                    print("GUESS", file=sys.stderr)
                    patient = interactor.readtoken().decode('utf-8')
                    if (patient == in_data[best][0]):
                        if x < 60:
                            correct += 0.3333
                        elif x < 80:
                            correct += 1.5
                        else:
                            correct += 5
                    break
                elif query == "Q":
                    n_queries += 1
                    patient = interactor.readtoken().decode('utf-8')
                    if n_queries > expected_queries:
                        interactor.writeln("FINISH")
                        print("FINISH", file=sys.stderr)
                        break
                    if patient not in v_mapping:
                        print(len([key for key in v_mapping.keys() if key.startswith(patient[:2])]), file=sys.stderr)
                        return CheckerResult(False, 0, f"Unknown patient {patient}")
                    if int(v_mapping[patient] <= in_data[best][1] + 1e-9) + int(lying[n_queries % 7]) == 1:
                        interactor.writeln("DANGEROUS")
                        print("DANGEROUS", file=sys.stderr)
                    else:
                        interactor.writeln("SAFE")
                        print("SAFE", file=sys.stderr)
                else:
                    return CheckerResult(False, 0, f"Expected Q or A, got {query}")

        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}%")
