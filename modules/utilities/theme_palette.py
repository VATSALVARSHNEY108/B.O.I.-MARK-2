#!/usr/bin/env python3
"""
Theme Palette for VATSAL AI Desktop Automation
Provides modern, eye-comforting color schemes with cyber aesthetic
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class ColorScheme:
    """Color scheme definition"""
    bg_base: str
    bg_secondary: str
    bg_tertiary: str
    bg_card: str
    
    accent_primary: str
    accent_secondary: str
    accent_tertiary: str
    
    text_primary: str
    text_secondary: str
    text_tertiary: str
    
    border_primary: str
    border_secondary: str
    
    success: str
    warning: str
    error: str
    
    hover_primary: str
    hover_secondary: str


class ThemePalette:
    """Centralized theme palette manager"""
    
    LIGHT_THEME = ColorScheme(
        bg_base="#F6F5F0",
        bg_secondary="#FAFAF8",
        bg_tertiary="#E8E7E2",
        bg_card="#FFFFFF",
        
        accent_primary="#00F2A6",
        accent_secondary="#A65BFF",
        accent_tertiary="#3ED1E0",
        
        text_primary="#1E1E1E",
        text_secondary="#4A4A4A",
        text_tertiary="#7A7A7A",
        
        border_primary="#D4D3CE",
        border_secondary="#E8E7E2",
        
        success="#00F2A6",
        warning="#FFB84D",
        error="#FF6B6B",
        
        hover_primary="#02C08A",
        hover_secondary="#8343D0"
    )
    
    DARK_THEME = ColorScheme(
        bg_base="#000000",
        bg_secondary="#0a0a0a",
        bg_tertiary="#1a1a1a",
        bg_card="#111111",
        
        accent_primary="#00d4ff",
        accent_secondary="#b19cd9",
        accent_tertiary="#00ff88",
        
        text_primary="#ffffff",
        text_secondary="#cccccc",
        text_tertiary="#999999",
        
        border_primary="#333333",
        border_secondary="#ffffff",
        
        success="#00ff88",
        warning="#ffaa00",
        error="#ff0080",
        
        hover_primary="#00ff88",
        hover_secondary="#ff0080"
    )
    
    def __init__(self, theme: str = "light"):
        """Initialize theme palette
        
        Args:
            theme: 'light' or 'dark'
        """
        self.current_theme = theme
        self._theme = self.LIGHT_THEME if theme == "light" else self.DARK_THEME
    
    def switch_theme(self, theme: str):
        """Switch between light and dark themes
        
        Args:
            theme: 'light' or 'dark'
        """
        self.current_theme = theme
        self._theme = self.LIGHT_THEME if theme == "light" else self.DARK_THEME
    
    @property
    def bg_base(self) -> str:
        return self._theme.bg_base
    
    @property
    def bg_secondary(self) -> str:
        return self._theme.bg_secondary
    
    @property
    def bg_tertiary(self) -> str:
        return self._theme.bg_tertiary
    
    @property
    def bg_card(self) -> str:
        return self._theme.bg_card
    
    @property
    def accent_primary(self) -> str:
        return self._theme.accent_primary
    
    @property
    def accent_secondary(self) -> str:
        return self._theme.accent_secondary
    
    @property
    def accent_tertiary(self) -> str:
        return self._theme.accent_tertiary
    
    @property
    def text_primary(self) -> str:
        return self._theme.text_primary
    
    @property
    def text_secondary(self) -> str:
        return self._theme.text_secondary
    
    @property
    def text_tertiary(self) -> str:
        return self._theme.text_tertiary
    
    @property
    def border_primary(self) -> str:
        return self._theme.border_primary
    
    @property
    def border_secondary(self) -> str:
        return self._theme.border_secondary
    
    @property
    def success(self) -> str:
        return self._theme.success
    
    @property
    def warning(self) -> str:
        return self._theme.warning
    
    @property
    def error(self) -> str:
        return self._theme.error
    
    @property
    def hover_primary(self) -> str:
        return self._theme.hover_primary
    
    @property
    def hover_secondary(self) -> str:
        return self._theme.hover_secondary
    
    def get_gradient(self, start_color: str = None, end_color: str = None) -> tuple:
        """Get gradient colors for backgrounds
        
        Returns:
            Tuple of (start_color, end_color)
        """
        if start_color and end_color:
            return (start_color, end_color)
        
        if self.current_theme == "light":
            return (self.bg_secondary, self.bg_tertiary)
        else:
            return (self.bg_secondary, self.bg_tertiary)
    
    def to_dict(self) -> Dict[str, str]:
        """Convert theme to dictionary"""
        return {
            'bg_base': self.bg_base,
            'bg_secondary': self.bg_secondary,
            'bg_tertiary': self.bg_tertiary,
            'bg_card': self.bg_card,
            'accent_primary': self.accent_primary,
            'accent_secondary': self.accent_secondary,
            'accent_tertiary': self.accent_tertiary,
            'text_primary': self.text_primary,
            'text_secondary': self.text_secondary,
            'text_tertiary': self.text_tertiary,
            'border_primary': self.border_primary,
            'border_secondary': self.border_secondary,
            'success': self.success,
            'warning': self.warning,
            'error': self.error,
            'hover_primary': self.hover_primary,
            'hover_secondary': self.hover_secondary
        }


def create_theme_palette(theme: str = "light") -> ThemePalette:
    """Factory function to create theme palette
    
    Args:
        theme: 'light' or 'dark'
    
    Returns:
        ThemePalette instance
    """
    return ThemePalette(theme)
