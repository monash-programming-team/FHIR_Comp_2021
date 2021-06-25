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

        # Ranges from 10-40
        # Distribution is uniform.

        # 60 tests, 3% of population,  Worth 20%, 0.3333% each
        # 20 tests, 30% of population, Worth 30%, 1.5% each
        # 10 tests, 98% of population, Worth 50%, 5% each

        tests = 60 + 20 + 10
        interactor.writeln(tests)

        correct = 0

        for x in range(tests):
            while True:
                if x < 60:
                    length = (random.random() * 1.5 + 1.5) / 100 * 30
                elif x < 80:
                    length = (random.random() * 15 + 15) / 100 * 30
                else:
                    length = (random.random() * 2 + 96) / 100 * 30
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
            # TODO: Change this to a specific value so that at 98% 4/9ths solution fails.
            expected_queries = math.log((r - l + 1) * (r - l) / 2, 3) + 3

            while True:
                query = interactor.readtoken().decode('utf-8')
                if query == "A":
                    r1 = interactor.readtoken().decode('utf-8')
                    r2 = interactor.readtoken().decode('utf-8')
                    if (r1 == in_data[first][0] and r2 == in_data[second][0]) or (r1 == in_data[second][0] and r2 == in_data[first][0]):
                        if n_queries < expected_queries:
                            if x < 60:
                                correct += 0.3333
                            elif x < 80:
                                correct += 1.5
                            else:
                                correct += 5
                    break
                if query == "Q":
                    n_queries += 1
                    a1 = interactor.readint()
                    a2 = interactor.readint()
                    ids1 = [interactor.readtoken().decode('utf-8') for _ in range(a1)]
                    ids2 = [interactor.readtoken().decode('utf-8') for _ in range(a2)]
                    if n_queries > 1000:
                        interactor.writeln("FINISH")
                        break
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

        correct = max(correct, 0)
        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}\%")
