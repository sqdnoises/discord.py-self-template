"""
This module contains all the utilities that would be needed in the bot

Copyright (c) SqdNoises 2024-present
Licensed under the MIT License
https://github.com/sqdnoises/discord.py-bot-template
"""

import os
import re
import pkgutil
from typing import Any, List, Callable

__all__ = (
    "list_modules",
    "mprint",
    "strip_color",
    "code",
    "cleanup_code",
    "paginate",
    "detect_platform",
    "slice"
)

def list_modules(package: str | Any) -> list[str]:
    """List all modules in a package"""
    
    if type(package) == str:
        package = __import__(package)
    
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__+"."):
        modules.append(modname)
    
    return modules

def mprint(text: str = "", fillchar: str = " ", end: str = "\n", flush: bool = False):
    """Print text in the middle of the terminal if possible, and normally if not"""
    
    try:
        width = os.get_terminal_size().columns
    
    except:
        print(text, end=end, flush=flush)
    
    else:
        text = str(text)
        color_stripped = strip_color(text)
        
        centered_text = color_stripped.center(width, fillchar).replace(color_stripped, text)
        print(centered_text, end=end, flush=flush)

def strip_color(text: str) -> str:
    """Strip all color codes from a string"""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)

def code(text: str, language: str | None = None, ignore_whitespace: bool = False):
    """Return a code block version of the text provided"""
    if not ignore_whitespace and text.strip() == "":
        return ""
    
    return f"```{language or ''}\n{text}\n```"

def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    
    # remove `foo`
    return content.strip('` \n')

def paginate(array: list | tuple | set, count: int = 3, debug: bool = False, logger: Callable = print) -> list:
    """Efficient paginator for making a multiple lists out of a list which are sorted in a page-vise order.
    
    For example:
    ```py
    >>> abc = [1, 2, 3, 4, 5]
    >>> print(paginate(abc, count=2)
    [[1, 2], [3, 4], [5]]
    ```

    That was just the basic usage. By default the count variable is set to 3.
    """
    array = list(array)
    paginated = []
    
    temp = []
    for item in array:
        if len(temp) == count:
            paginated.append(temp)
            temp = []
        
        temp.append(item)
        
        if debug:
            logger(len(temp), item)
    
    if len(temp) > 0:
        paginated.append(temp)
    
    return paginated

def detect_platform():
    """Detect what platform the code is being run at"""

    if "ANDROID_ROOT" in os.environ:
        return "android"
    elif os.name == "nt":
        return "windows"
    elif os.name == "posix":
        return "linux"
    else:
        return "other"

def slice(text: str, max: int = 2000) -> List[str]:
    """Slice a message up into multiple messages"""
    return [text[i:i+max] for i in range(0, len(text), max)]