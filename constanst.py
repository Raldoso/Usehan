import os

DIRPATH = os.path.dirname(__file__)
import os
from functions import relpath


DIRPATH = os.path.dirname(__file__)
DELETE_URL = relpath(r"Images\Trash.png")
SESSION_SETTINGS = relpath(r"Images\SessionSettings.png")
CHECK_URL = relpath(r"Images\CheckURL.png")
UNCHECK_URL = relpath(r"Images\UnCheckURL.png")