"""
BOI Modules Package - AI Desktop Automation Controller
Provides centralized access to all 410+ features

This package provides lazy-loaded imports with fallback support.
All features can work independently or interconnected.
"""

__version__ = "4.0"
__author__ = "BOI Team"


def _import_with_fallback(module_path, name):
    """Safely import a module with fallback"""
    try:
        parts = module_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[parts[-1] if len(parts) > 1 else name])
        return getattr(module, name, None)
    except (ImportError, AttributeError):
        return None


# Lazy-loaded core modules (with fallbacks)
__all__ = [
    'get_command_executor',
    'get_gui',
    'get_gemini_controller',
    'get_future_tech_core',
]


def get_command_executor():
    """Get CommandExecutor with graceful fallback"""
    try:
        from modules.core.command_executor import CommandExecutor
        return CommandExecutor
    except ImportError:
        return None


def get_gui():
    """Get GUI App with graceful fallback"""
    try:
        from modules.core.gui_app import ModernBOIGUI
        return ModernBOIGUI
    except ImportError:
        return None


def get_gemini_controller():
    """Get Gemini Controller functions"""
    try:
        from modules.core import gemini_controller
        return {
            'parse_command': getattr(gemini_controller, 'parse_command', None),
            'chat_response': getattr(gemini_controller, 'chat_response', None),
            'get_ai_suggestion': getattr(gemini_controller, 'get_ai_suggestion', None),
        }
    except ImportError:
        return {}


def get_future_tech_core():
    """Get Future-Tech Core with graceful fallback"""
    try:
        from modules.core.future_tech_core import create_future_tech_core
        return create_future_tech_core()
    except ImportError:
        return None
