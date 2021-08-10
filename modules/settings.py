"""
Global Settings Classes for storing informations about the applications

The database during open time is always open in a python dictionary object reducing file handling.
Future plan is implementing a paralell process that saves the informations in fixed time intervals.
"""

from dataclasses import dataclass

@dataclass
class LinkSettings():
    launcable = False

@dataclass
class SessionSettings():
    launchAtStartup: bool
    browser: str
    activeWindow: str
@dataclass
class AppSettings():
    launchAtStartup: bool
    theme: str