import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(absolute_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]

        if args is not None:
            command.extend(args)

        complete_process = subprocess.run(
            command, cwd = working_dir_abs, capture_output = True, text = True, timeout = 30
        )

        output_string = ""

        if complete_process.returncode != 0:
            output_string += f"Process exited with code {complete_process.returncode}\n"

        if complete_process.stderr == None and complete_process.stdout == None:
            output_string += "No output produced\n"

        if complete_process.stdout != "":
            output_string += f"STDOUT: {complete_process.stdout}"

        if complete_process.stderr != "":
            output_string += f"STDERR: {complete_process.stderr}"

        return output_string
    
    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a specified python file in the working directory, providing STDOUT and STDERR",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Specific argument to the function"
                    },
                    "description": "List of arguments to the function (default is None)"
                }
            },
            "required": ["file_path"]
        },
    },
}