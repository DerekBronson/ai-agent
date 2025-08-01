from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def test_get_files_info():
    # get_files_info(working_directory, directory=".")
    directories_to_check = [
        ["calculator", "."],
        ["calculator", "pkg"],
        ["calculator", "/bin"],
        ["calculator", "../"],
        ["calculator", "./functions"],
    ]

    for dir in directories_to_check:
        if dir[1] == ".":
            print("Result for current directory:")
        else:
            print(f"Result for '{dir[1]}' directory:")
        print(get_files_info(dir[0], dir[1]))


def test_get_file_content():
    # get_file_content(working_directory, file_path)
    files_to_check = [
        ["calculator", "main.py"],
        ["calculator", "pkg/calculator.py"],
        ["calculator", "/bin/cat"], # Should return an error
        ["calculator", "pkg/does_not_exist.py"],
    ]

    for file in files_to_check:
        print(f"Result for '{file[1]}' file:")
        print(get_file_content(file[0], file[1]))


def test_write_file():
    # write_file(working_directory, file_path, content)
    files_to_write = [
        ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
        ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["calculator", "/tmp/temp.txt", "this should not be allowed"],
    ]

    for file in files_to_write:
        print(f"Result for '{file[1]}' file:")
        print(write_file(file[0], file[1], file[2]))

def test_run_python():
    # run_python(working_directory, file_path, args=[])
    files_to_test = [
        ["calculator", "main.py"],
        ["calculator", "main.py", ["3 + 5"]],
        ["calculator", "../main.py"], # Should return an error
        ["calculator", "nonexistent.py"] # Should return an error
    ]

    for file in files_to_test:
        print(f"Result for '{file[1]}' file:")
        if len(file) == 3:
            print(run_python_file(file[0], file[1], file[2]))
        else:
            print(run_python_file(file[0],file[1]))


# test_get_file_content()
# test_write_file()
test_run_python()