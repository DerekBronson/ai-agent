import os

def get_files_info(working_directory, directory="."):
    working_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_abs,directory))
    if not target_dir.startswith(working_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    if not os.path.isdir(working_abs):
        return f'Error: "{working_directory}" is not a directory'
    
    try:
        results_string=""
            
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir,item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            results_string += f"- {item}: filze_size={size}, is_dir={is_dir}\n"
        return results_string
    except Exception as e:
        return f"Error listing files: {e}"