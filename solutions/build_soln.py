import sys

def main(filepath):

    new_file_string = ""

    with open("solutions/data_types.py", "r") as f:
        new_file_string = new_file_string + f.read() + "\n"

    with open("solutions/read_data.py", "r") as f:
        new_file_string = new_file_string + f.read() + "\n"

    with open(filepath, "r") as f:
        new_file_string = new_file_string + f.read() + "\n"

    with open(filepath.replace(".py", "_compiled.py"), "w") as f:
        f.write(new_file_string)

if __name__ == "__main__":
    main(sys.argv[1])
