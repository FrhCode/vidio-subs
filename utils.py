import os

def extract_file_name(input_file):
    base_name = os.path.basename(input_file)
    file_name, _ = os.path.splitext(base_name)
    return file_name