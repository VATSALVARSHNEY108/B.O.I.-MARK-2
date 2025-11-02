"""
AI Features Module
Consolidated AI functionality including chatbots, code generation, vision AI, and automation
"""

from modules.ai_features.ai_features import AIFeatures
from modules.ai_features.chatbots import SimpleChatbot
from modules.ai_features.code_generation import generate_code, generate_letter, list_letter_types
from modules.ai_features.vision_ai import MultiModalAI, create_multimodal_ai
from modules.ai_features.automation_ai import AdvancedAIAutomation, AdvancedAIIntegration

__all__ = [
    'AIFeatures',
    'SimpleChatbot',
    'generate_code',
    'generate_letter',
    'list_letter_types',
    'MultiModalAI',
    'create_multimodal_ai',
    'AdvancedAIAutomation',
    'AdvancedAIIntegration',
]
