import os
from . import constants
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns up to 10000 characters from a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_abs, file_path))

    if not target_file.startswith(working_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(constants.MAX_CHAR)
        return file_content_string
    except Exception as e:
        return f"Error processing {file_path}: {e}"
