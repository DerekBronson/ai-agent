import os


def get_files_info(working_directory, directory="."):
    try:
        if os.path.abspath(directory) not in os.path.abspath(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        if not os.path.isdir(working_directory):
            return f'Error: "{working_directory}" is not a directory'
        full_path = os.path.join(working_directory, directory)
    except:
        return f'Error: parsing the working directory {working_directory} and the directory {directory}'
    results_string=""
        
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path,item)
        size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)
        results_string += f"- {item}: filze_size={size}, is_dir={is_dir}\n"
        # except:
        #     return f'Error: gathering information for {item}'

    return results_string