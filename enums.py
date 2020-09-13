#!/usr/bin/python3

from enum import Enum

class EmailStatus(Enum):
    NEW_FLAT = 0
    LOWERED_FLAT = 1
    EMAIL_SENT = 2
