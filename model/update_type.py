from enum import Enum


class UpdateType(Enum):
    """
    Enumeration for informs the change type
    """
    CREATED = 0
    UPDATED = 1
    DELETED = 2
