import os


def get_files_info(working_directory, directory="."):

    files_info = []
    full_path = os.path.join(working_directory, directory)

    try:
        if working_directory not in os.path.normpath(full_path):
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