"""
BOI Modules Package - AI Desktop Automation Controller
Provides centralized access to all 410+ features
"""

__version__ = "4.0"
__author__ = "BOI Team"

# Core modules
from modules.core.command_executor import CommandExecutor, create_command_executor
from modules.core.gui_app import ModernBOIGUI
from modules.core.gemini_controller import parse_command, chat_response, get_ai_suggestion
from modules.core.future_tech_core import FutureTechCore, create_future_tech_core

# Factory functions for all major features
from modules.core.multimodal_control import create_multimodal_control
from modules.automation.self_operating_computer import SelfOperatingComputer
from modules.automation.comprehensive_desktop_controller import ComprehensiveDesktopController
from modules.ai_features.vision_ai import create_multimodal_ai
from modules.ai_features.ai_features import create_ai_features
from modules.communication.email_sender import create_email_sender
from modules.communication.phone_dialer import create_phone_dialer
from modules.communication.whatsapp_automation import create_whatsapp_automation
from modules.voice.voice_commander import create_voice_commander
from modules.voice.voice_assistant import VoiceAssistant
from modules.utilities.youtube_automation import create_youtube_automation
from modules.system.system_control import SystemController
from modules.security.security_enhancements import create_security_enhancements
from modules.intelligence.desktop_rag import create_desktop_rag
from modules.intelligence.persona_response_service import create_persona_service
from modules.monitoring.visual_chat_monitor import create_visual_chat_monitor
from modules.monitoring.chat_monitor import ChatMonitor

# Utilities and productivity
from modules.utilities.password_vault import PasswordVault
from modules.utilities.calendar_manager import CalendarManager
from modules.utilities.quick_notes import QuickNotes
from modules.utilities.weather_news_service import WeatherNewsService
from modules.communication.translation_service import TranslationService
from modules.productivity.productivity_monitor import ProductivityMonitor

__all__ = [
    'CommandExecutor',
    'create_command_executor',
    'ModernBOIGUI',
    'parse_command',
    'chat_response',
    'FutureTechCore',
    'create_future_tech_core',
    'create_multimodal_control',
    'SelfOperatingComputer',
    'ComprehensiveDesktopController',
    'create_multimodal_ai',
    'create_ai_features',
    'create_email_sender',
    'create_phone_dialer',
    'create_whatsapp_automation',
    'create_voice_commander',
    'VoiceAssistant',
    'create_youtube_automation',
    'SystemController',
    'create_security_enhancements',
    'create_desktop_rag',
    'create_persona_service',
    'create_visual_chat_monitor',
    'ChatMonitor',
]
