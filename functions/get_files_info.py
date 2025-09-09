import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    files_info = []
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    try:
        if working_path not in full_path:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(full_path):
            raise ValueError(f'Error: "{directory}" is not a directory')
    except Exception as e:
        return str(e)

    dir_contents = ""
    for name in os.listdir(full_path):
        full_filepath = os.path.join(full_path, name)
        dir_contents += f" - {name}: file_size={os.path.getsize(full_filepath)} bytes, is_dir={os.path.isdir(full_filepath)}\n"
    return dir_contents

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)