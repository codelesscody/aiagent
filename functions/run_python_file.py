import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    full_path = os.path.join(working_directory, file_path)
    if working_directory not in os.path.normpath(full_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(['python', full_path]+args, capture_output=True, text=True, timeout=30)
        if result.stdout == '' and result.stderr == '':
            return 'No output produced.'
        if result.returncode != 0:
            f'STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nProcess exited with code {result.returncode}'
        return f'STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}'
    except Exception as e:
        return f'Error: executing Python file: {str(e)}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python .py file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python .py file to run, relative to the working directory.",
            ),
        },
    ),
)