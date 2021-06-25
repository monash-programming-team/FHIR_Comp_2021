import os, sys
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")[1:]
        out_data = case.output_data().decode('utf-8').split("\n")[1:]

        # [0] = number of test cases
        # [1:] = test case inputs

        # 10 tests, 10 practitioners, worth 20%: 2% p test
        # 5 tests, sqrt practitioners, worth 30%: 6% p test
        # 3 tests, all practitioners - 10, worth 50%: 16.66% p test

        dataset_path = "/problems/data/dataset"
        interactor.writeln(dataset_path)

        # Wait for a ready.
        read = interactor.readln().decode('utf-8')
        if "ready" not in read.lower():
            return CheckerResult(False, 0, feedback=f"Didn't Print Ready! Got {read}", extended_feedback=interactor.read().decode('utf-8'))

        interactor.writeln(in_data[0])

        correct = 0
        tests = int(in_data[0])

        for x in range(tests):
            interactor.writeln(in_data[2*x+1])
            interactor.writeln(in_data[2*x+2])
            if interactor.readint() == int(out_data[x]):
                if x < 10:
                    correct += 2
                elif x < 15:
                    correct += 6
                else:
                    correct += 16.6666

        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}%")
