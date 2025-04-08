def todo_function(file_content):
    # Example TODO function that checks for the presence of the word "TODO"
    if "TODO" in file_content:
        return False  # Fail the commit if "TODO" is found
    return True  # Allow the commit if "TODO" is not found


def read_file_contents(file_paths):
    contents = {}
    for path in file_paths:
        with open(path, "r") as file:
            contents[path] = file.read()
    return contents
