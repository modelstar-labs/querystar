import tokenize


def open_source_file(file_path: str):
    """
    Open a read-only Python file respecting PEP263 encoding. 
    If no encoding header is found, opens as utf-8.
    """

    if hasattr(tokenize, "open"):
        return tokenize.open(file_path)
    else:
        return open(file_path, "r", encoding="utf-8")
