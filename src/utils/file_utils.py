import os
import pathlib
from typing import Any


def format_template(template_path: str, **data) -> str:
    """
    Take a path to a template text file and fill it out

    WARNING: this function does arbitrary code execution. Only use it for files you have written or 100% trust
    Otherwise can pass in stuff like `{__import__('os').system('install ransomware or something')}`

    The template must be formatted so the only variables it references are referenced through data["var_name"]

    Args:
        template_path: the path to the template file to fill
        data: the variables to set in the template

    Returns:
        the template, filled out with the given data
    """
    with open(template_path, "r") as file:
        text_to_format = file.read()

    return eval(f'f"""{text_to_format}"""')


def path_to_file(dunder_file: str, *rel_path: str) -> str:
    """
    Get the absolute path to a file given __file__ and the relative path from the folder containing the file that
    called __file__

    Args:
        dunder_file: the result of __file__
        rel_path: the relative path of the target file from the folder that called __file__

    Returns:
        the absolute path of the specified file
    """
    folder_path = pathlib.Path(dunder_file).parent
    return "/".join([str(folder_path), *rel_path])
