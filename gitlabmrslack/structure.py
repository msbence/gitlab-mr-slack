"""This module provides data structures to the app"""

from enum import Enum

class ActionType(Enum):
    """Possible action types on GitLab

    Parameters
    ----------
    Enum : enum.Enum
        The GitLab action type
    """
    COMMENT = 1
    APPROVE = 2
    UNAPPROVE = 3
    MERGE = 4
