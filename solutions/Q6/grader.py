import sys
import math
import random
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        # In data: list of patients, with blood values.
        in_data = case.input_data().decode('utf-8').split("\n")
        diff = in_data[0]
        in_data = in_data[1:]
        in_data = list(map(lambda x: (x.split(" ")[0], float(x.split(" ")[1])), filter(bool, in_data)))

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        # Ranges from 10-40
        # Distribution is uniform.

        if diff == "easy":
            tests = 60
        elif diff == "medium":
            tests = 20
        elif diff == "hard":
            tests = 10
        else:
            raise ValueError()
        interactor.writeln(tests)

        correct = 0

        for x in range(tests):
            while True:
                if diff == "easy":
                    length = math.floor(random.random() * len(in_data) * 0.01 + len(in_data) * 0.02)
                elif diff == "medium":
                    length = math.floor(random.random() * len(in_data) * 0.1 + len(in_data) * 0.2)
                else:
                    length = math.floor(random.random() * len(in_data) * 0.08 + len(in_data) * 0.9)
                l = random.randint(0, len(in_data) - length)
                r = l + length - 1
                if r - l < 1: continue
                if l == 0:
                    start = in_data[0][1] - 0.01
                else:
                    start = (in_data[l][1] + in_data[l-1][1]) / 2
                if r == len(in_data) - 1:
                    end = in_data[-1][1] + 0.01
                else:
                    end = (in_data[r][1] + in_data[r+1][1]) / 2
                first = random.randint(l, r)
                while True:
                    second = random.randint(l, r)
                    if second != first: break
                break
            interactor.writeln(f"{start} {end}")

            n_queries = 0
            expected_queries = math.log((r - l + 1) * (r - l) / 2, 3) + 3

            while True:
                query = interactor.readtoken().decode('utf-8')
                if query == "A":
                    r1 = interactor.readtoken().decode('utf-8')
                    r2 = interactor.readtoken().decode('utf-8')
                    if (r1 == in_data[first][0] and r2 == in_data[second][0]) or (r1 == in_data[second][0] and r2 == in_data[first][0]):
                        correct += 1
                    break
                elif query == "Q":
                    n_queries += 1
                    a1 = interactor.readint()
                    a2 = interactor.readint()
                    ids1 = [interactor.readtoken().decode('utf-8') for _ in range(a1)]
                    ids2 = [interactor.readtoken().decode('utf-8') for _ in range(a2)]
                    if n_queries > expected_queries:
                        interactor.writeln("FINISH")
                        break
                    if len(set(ids1 + ids2)) != len(ids1 + ids2):
                        return CheckerResult(False, 0, f"Non-unique weighing given.")
                    if in_data[first][0] in ids1:
                        if in_data[second][0] in ids2:
                            if len(ids1) > len(ids2):
                                interactor.writeln("RIGHT")
                            elif len(ids1) < len(ids2):
                                interactor.writeln("LEFT")
                            else:
                                interactor.writeln("EQUAL")
                        else:
                            interactor.writeln("LEFT")
                    elif in_data[first][0] in ids2:
                        if in_data[second][0] in ids1:
                            if len(ids1) > len(ids2):
                                interactor.writeln("RIGHT")
                            elif len(ids1) < len(ids2):
                                interactor.writeln("LEFT")
                            else:
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
                else:
                    return CheckerResult(False, 0, f"Got {query}")

        correct = max(correct, 0)
        return CheckerResult(True, case.points * correct / tests, f"Earned {correct / tests * 100:.2f}%")
