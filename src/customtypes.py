"""
Custom types that were defined for typing variables and function parameters.
"""

__all__ = (
    "MISSING",
)

class Missing:
    def __str__(self):
        return "MISSING"
    
    def __repr__(self):
        return "MISSING"

MISSING = Missing()