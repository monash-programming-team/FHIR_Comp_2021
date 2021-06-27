import os, sys
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")

        # [0] = number of test cases
        # [1:] = test case inputs

        tests = len(in_data)
        interactor.writeln(tests)

        correct = 0

        for x in range(tests):
            interactor.writeln(in_data[x])
            if interactor.readint() == int(in_data[x]):
                correct += 1

        return CheckerResult(True, case.points * correct / tests, f"Earned {100 * correct / tests:.2f}%")
