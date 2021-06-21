"""Builds the dataset, compiles all solutions, creates test files, and zips test files."""
import argparse, os, sys
import subprocess
import runpy
from solutions.build_soln import main as compile_soln

parser = argparse.ArgumentParser()
parser.add_argument("--no-dataset", action="store_false", dest="dataset")

GRADING_FOLDERS = ["Q1", "Q2"]

def main():
    args = parser.parse_args(sys.argv[1:])
    
    if args.dataset:
        from dataset_generator.source import main as generate_data
        generate_data()

    for f in os.listdir("solutions"):
        f_p = os.path.join("solutions", f)
        if os.path.isdir(f_p):
            for f2 in os.listdir(f_p):
                if f2.endswith(".py") and "compiled" not in f2 and "solution" in f2:
                    # Compile solution
                    compile_soln(os.path.join(f_p, f2))
            # Generate test data
            if os.path.exists(os.path.join(f_p, "test_generator.py")):
                with open(f"solutions/{f}/1.in", "w") as test:
                    subprocess.run(f"python -m solutions.{f}.test_generator".split(), stdout=test)
            if f in GRADING_FOLDERS:
                with open(f"solutions/{f}/1.in", "r") as test_in:
                    with open(f"solutions/{f}/1.out", "w") as test_out:
                        subprocess.run(f"python -m solutions.{f}.solution_compiled".split(), stdin=test_in, stdout=test_out)

if __name__ == "__main__":
    main()
