import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        
        dir_content = os.listdir(target_dir)
        string_dir_content = ""
        
        for name in dir_content:
            curr_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(curr_path)
            is_dir = os.path.isdir(curr_path)
            string_dir_content += f'- {name}: file_size={file_size} bytes, is_dir={is_dir}\n'

        return string_dir_content

    except Exception as e:
        return f'Error: {e}'