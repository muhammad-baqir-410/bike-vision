def get_key_from_value(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

def get_keys_from_file(file_path, categories):
    """
    Reads values from a given text file, one per line, and returns a list of keys
    from the categories dictionary corresponding to those values.
    
    Parameters:
    - file_path (str): The path to the text file containing the values.
    - categories (dict): The dictionary to search for keys based on the values.
    
    Returns:
    - list: A list of keys corresponding to the values read from the file. If a value
            is not found, it is skipped.
    """
    keys = []
    with open(file_path, 'r') as file:
        for line in file:
            value = line.strip()  # Remove any leading/trailing whitespace
            key = get_key_from_value(categories, value)
            if key is not None:
                keys.append(key)
    return keys

def find_unique_class_counts(data):
    result = {}
    for tracking_id, values in data.items():
        if values not in result:
            result[values] = 1
        else:
            result[values] += 1

    return result
    # print(result)