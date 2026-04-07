from enum import Enum


class Role(str, Enum):
    viewer = "Viewer"
    analyst = "Analyst"
    admin = "Admin"
