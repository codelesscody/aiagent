import os
from config import *

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if working_directory not in os.path.normpath(full_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)  # Limit to first MAX_CUARS characters
        return file_content_string
    except Exception as e:
        return f'Error: {str(e)}'
    