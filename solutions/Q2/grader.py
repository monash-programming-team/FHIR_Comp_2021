import os, sys
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")[1:]
        out_data = case.output_data().decode('utf-8').split("\n")

        # [0] = number of test cases
        # [1:] = test case inputs

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
                correct += 1

        return CheckerResult(True, case.points * correct / tests, f"Solved {100 * correct / tests:.2f}\%")
