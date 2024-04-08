"""
ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher

It starts off with a format like `\\033[XXXm` where `XXX` is a semicolon separated list of commands

The important ones here relate to colour.

`30-37` are black, red, green, yellow, blue, magenta, cyan and white in that order

`40-47` are the same except for the background

`90-97` are the same but "bright" foreground

`100-107` are the same as the bright ones but for the background.

`1` means bold, `2` means dim, `0` means reset, and `4` means underline.

Another way of writing `\\033` would be `\\x1b`.
"""

# ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
# It starts off with a format like \033[XXXm where XXX is a semicolon separated list of commands
# The important ones here relate to colour.
# 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
# 40-47 are the same except for the background
# 90-97 are the same but "bright" foreground
# 100-107 are the same as the bright ones but for the background.
# 1 means bold, 2 means dim, 0 means reset, and 4 means underline.
# Another way of writing \033 would be \x1b.

__all__ = (
    # Formatting
    "reset",
    "bold",
    "dim",
    "underline",
    
    # Colors
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    
    # Bright colors
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    
    # Background colors
    "bg_black",
    "bg_red",
    "bg_green",
    "bg_yellow",
    "bg_blue",
    "bg_magenta",
    "bg_cyan",
    "bg_white",
    
    # Bright background colors
    "bg_bright_black",
    "bg_bright_red",
    "bg_bright_green",
    "bg_bright_yellow",
    "bg_bright_blue",
    "bg_bright_magenta",
    "bg_bright_cyan",
    "bg_bright_white",
    
    # Custom colors
    "lime",
)

def ansi(code: int) -> str:
    return f"\033[{code}m"

def rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def hex(hex: int) -> str:
    r = hex >> 16
    g = hex >> 8 & 0xFF
    b = hex & 0xFF
    return rgb(r, g, b)

lime = rgb(0, 255, 128)

reset = ansi(0)
bold = ansi(1)
dim = ansi(2)
underline = ansi(4)

black = ansi(30)
red = ansi(31)
green = ansi(32)
yellow = ansi(33)
blue = ansi(34)
magenta = ansi(35)
cyan = ansi(36)
white = ansi(37)

bright_black = ansi(90)
bright_red = ansi(91)
bright_green = ansi(92)
bright_yellow = ansi(93)
bright_blue = ansi(94)
bright_magenta = ansi(95)
bright_cyan = ansi(96)
bright_white = ansi(97)

bg_black = ansi(40)
bg_red = ansi(41)
bg_green = ansi(42)
bg_yellow = ansi(43)
bg_blue = ansi(44)
bg_magenta = ansi(45)
bg_cyan = ansi(46)
bg_white = ansi(47)

bg_bright_black = ansi(100)
bg_bright_red = ansi(101)
bg_bright_green = ansi(102)
bg_bright_yellow = ansi(103)
bg_bright_blue = ansi(104)
bg_bright_magenta = ansi(105)
bg_bright_cyan = ansi(106)
bg_bright_white = ansi(107)
