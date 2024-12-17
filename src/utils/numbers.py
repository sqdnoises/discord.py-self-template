"""
Number related utilities.
"""

__all__ = (
    "rgb",
    "hex",
    "int_to_rgb",
    "int_to_hex",
    "rgb_to_hex",
    "hex_to_rgb",
    "format_number"
)

def rgb(r: int = 0, g: int = 0, b: int = 0) -> int:
    """Convert RGB to an int hex code."""
    return r << 16 | g << 8 | b

def hex(hex_str: str) -> int:
    """Convert a hex code to an int hex code."""
    hex_str = hex_str.lstrip("#").lower()  # remove leading # and convert to lower case
    
    if len(hex_str) not in (3, 6):
        raise ValueError("Invalid hex code length, it must be 3 or 6 characters long.")
        
    for char in hex_str:
        if char not in "0123456789abcdef":
            raise ValueError("Invalid character in hex code.")

    if len(hex_str) == 3:
        hex_str = hex_str[0] * 2 + hex_str[1] * 2 + hex_str[2] * 2 # expand 3 character string to 6 character string

    return int(hex_str, 16)

def int_to_rgb(int_hex: int) -> tuple[int, int, int]:
    """Convert an int hex code to a `(r, g, b)` tuple."""
    r = int_hex >> 16
    g = int_hex >> 8 & 0xFF
    b = int_hex & 0xFF
    return (r, g, b)

def int_to_hex(int_hex: int, upper: bool = True) -> str:
    """Convert an int hex code to string hex code."""
    return f"#{int_hex:06X}" if upper else f"#{int_hex:06x}"

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert a `(r, g, b)` tuple to a hex code."""
    return int_to_hex(rgb(r, g, b))

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert a hex code to a `(r, g, b)` tuple."""
    return int_to_rgb(hex(hex_str))

def format_number(number: int, decimal_points: int = 0, *, pad_decimal: bool = False) -> str:
    """
    Formats a large number with suffixes like K, M, B, etc. based on its magnitude.
    
    Parameters:
    - number (int): The number to be formatted.
    - decimal_points (int): The number of decimal places to display. Default is 0.
    - pad_decimal (bool): If True, adds trailing zeroes to decimals if needed. Default is False.
    
    Returns:
    - str: The formatted string with appropriate suffix and decimal places.
    
    Example:
    >>> format_number(1000000)
    '1M'
    >>> format_number(123456, decimal_points=2)
    '123.46K'
    >>> format_number(123000, decimal_points=2, pad_decimal=False)
    '123K'
    """
    
    if number < 1000:
        return str(number)
    
    suffixes = ["K", "M", "B", "T"]
    magnitude = 0
    num = number
    
    while num >= 1000 and magnitude < len(suffixes):
        magnitude += 1
        num /= 1000
    
    # Round the number to the specified decimal places
    if decimal_points:
        formatted_number = f"{num:.{decimal_points}f}"
    else:
        formatted_number = str(int(num))
    
    # Remove trailing decimals if pad_decimal is False
    if not pad_decimal and decimal_points:
        formatted_number = formatted_number.rstrip("0").rstrip(".")
    
    return f"{formatted_number}{suffixes[magnitude-1]}"