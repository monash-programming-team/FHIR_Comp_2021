import os
from dmoj.result import CheckerResult
from dmoj.graders.interactive import InteractiveGrader

class Grader(InteractiveGrader):
    def interact(self, case, interactor):

        in_data = case.input_data().decode('utf-8').split("\n")[1:]
        out_data = case.output_data().decode('utf-8').split("\n")

        # [0] = number of test cases
        # [1:] = test case inputs

        # First 50 test case := 3% of patients
        # Middle 20 test case := 30% of patients
        # Last 5 test case := 98% of patients

        # Solving 3%s: 20%
        # Solving 30%s: 60%
        # 50 test cases worth 20%: 1 test case worth 0.4%.
        # 20 test cases worth 40%: 1 test case worth 2%
        # 5 test case worth 40%: 1 test case worth 8%

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
            interactor.writeln(in_data[x+1])
            if abs(interactor.readfloat() - float(out_data[x])) <= 2e-8:
                if x < 50:
                    correct += 0.4
                elif x < 70:
                    correct += 2
                else:
                    correct += 8

        return CheckerResult(True, case.points * correct / 100, f"Earned {correct:.2f}%")
