import os

def get_file_content(working_directory, file_path):
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_abs,file_path))

    if not target_file.startswith(working_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'