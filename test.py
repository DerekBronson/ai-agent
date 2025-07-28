from functions.get_files_info import get_files_info

#get_files_info(working_directory, directory=".")
directories_to_check = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator","../"]
]

for dir in directories_to_check:
    if dir[1] == ".":
        print (f"Result for current directory:")
    else:
        print (f"Result for '{dir[1]}' directory:")
    print (get_files_info(dir[0], dir[1]))