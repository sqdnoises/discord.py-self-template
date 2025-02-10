"""
## `discord.py-self` bot template
a discord.py-self bot template that might come in handy for some people.

Copyright (c) 2025-present SqdNoises
Licensed under the MIT License
For more information, please check the provided LICENSE file.
"""

from .bot        import start
from .termcolors import *

if __name__ == "__main__":
    start()
    print(f"{bold}{blue}> {yellow}cya later {green}alligator {magenta}:3{reset}", flush=True)