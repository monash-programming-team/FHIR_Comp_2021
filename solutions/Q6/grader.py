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
                first = random.randint(l, r)
                while True:
                    second = random.randint(l, r)
                    if second != first: break
                break
            interactor.writeln(f"{start} {start+length}")

            n_queries = 0
            expected_queries = math.log((r - l + 1) * (r - l) / 2, 3)

            while True:
                query = interactor.readtoken().decode('utf-8')
                if query == "A":
                    r1 = interactor.readtoken().decode('utf-8')
                    r2 = interactor.readtoken().decode('utf-8')
                    if (r1 == in_data[first][0] and r2 == in_data[second][0]) or (r1 == in_data[second][0] and r2 == in_data[first][0]):
                        print(n_queries, expected_queries, r - l + 1, file=sys.stderr)
                        correct += 1 - (n_queries - expected_queries)/((r - l + 1) - expected_queries)
                    break
                if query == "Q":
                    n_queries += 1
                    a1 = interactor.readint()
                    a2 = interactor.readint()
                    ids1 = [interactor.readtoken().decode('utf-8') for _ in range(a1)]
                    ids2 = [interactor.readtoken().decode('utf-8') for _ in range(a2)]
                    if len(set(ids1 + ids2)) != len(ids1 + ids2):
                        return CheckerResult(False, 0, f"Non-unique weighing given.")
                    if len(ids1) > len(ids2):
                        interactor.writeln("LEFT")
                    elif len(ids1) < len(ids2):
                        interactor.writeln("RIGHT")
                    else:
                        if in_data[first][0] in ids1:
                            if in_data[second][0] in ids2:
                                interactor.writeln("EQUAL")
                            else:
                                interactor.writeln("LEFT")
                        elif in_data[first][0] in ids2:
                            if in_data[second][0] in ids1:
                                interactor.writeln("EQUAL")
                            else:
                                interactor.writeln("RIGHT")
                        else:
                            if in_data[second][0] in ids1:
                                interactor.writeln("LEFT")
                            elif in_data[second][0] in ids2:
                                interactor.writeln("RIGHT")
                            else:
                                interactor.writeln("EQUAL")

        correct = min(correct, tests)
        correct = max(correct, 0)
        return CheckerResult(True, case.points * correct / tests, f"Scored {100 * correct / tests:.2f}\%")
