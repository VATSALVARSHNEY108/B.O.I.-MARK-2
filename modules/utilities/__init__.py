"""
Utilities Module
Various utility functions for the AI Desktop Automation Controller
"""

from .notepad_writer import (
    write_to_notepad,
    write_code_to_notepad,
    write_letter_to_notepad
)

from .timer_stopwatch import TimerStopwatch
from .quick_reminders import QuickReminders
from .habit_tracker import HabitTracker
from .color_tools import ColorTools
from .qr_code_tools import QRCodeTools
from .screenshot_annotator import ScreenshotAnnotator
from .image_resizer import ImageResizer

__all__ = [
    'write_to_notepad',
    'write_code_to_notepad',
    'write_letter_to_notepad',
    'TimerStopwatch',
    'QuickReminders',
    'HabitTracker',
    'ColorTools',
    'QRCodeTools',
    'ScreenshotAnnotator',
    'ImageResizer'
]
