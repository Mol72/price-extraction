def read_txt_file_line_by_line(file_path: str):
    """
        Reads a TXT file line by line and returns a list of strings, where each string
        is a line from the file.
    Args:
        file_path: The path to the TXT file.
    Returns:
        A list of strings, each representing a line in the file.
    """
    try:
        lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())  # Remove leading/trailing whitespace
        return lines
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
    return None
