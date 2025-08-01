import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Takes a file path and content, if the file already exists it gets overwritten otherwise a new file is created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file that should be written, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file that was specified",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_abs, file_path))

    if not target_file.startswith(working_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(target_file)):
        try:
            os.makedirs(os.path.dirname(target_file))
        except Exception as e:
            return f"Error: Could not create the file {file_path}: {e}"
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: Unable to write to {file_path}: {e}"
