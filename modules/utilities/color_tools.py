"""
Color Picker & Converter Module
Pick colors from screen, convert between formats (HEX, RGB, HSL, HSV)
"""

import colorsys
import re
from typing import Any

pyautogui: Any = None
PYAUTOGUI_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    PYAUTOGUI_AVAILABLE = False
    print(f"⚠️  PyAutoGUI not available (no display): {e}")

class ColorTools:
    def __init__(self):
        pass
    
    def pick_color_from_screen(self):
        """Pick a color from the current mouse position"""
        if not PYAUTOGUI_AVAILABLE:
            return "❌ Color picker not available in this environment (no display)"
        try:
            x, y = pyautogui.position()
            screenshot = pyautogui.screenshot()
            pixel = screenshot.getpixel((int(x), int(y)))
            
            r, g, b = pixel[:3]
            
            hex_color = self.rgb_to_hex(r, g, b)
            hsl = self.rgb_to_hsl(r, g, b)
            hsv = self.rgb_to_hsv(r, g, b)
            
            result = f"\n{'='*60}\n"
            result += f"🎨 COLOR PICKER\n"
            result += f"{'='*60}\n\n"
            result += f"Position: ({x}, {y})\n\n"
            result += f"HEX: {hex_color}\n"
            result += f"RGB: rgb({r}, {g}, {b})\n"
            result += f"HSL: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)\n"
            result += f"HSV: hsv({hsv[0]}, {hsv[1]}%, {hsv[2]}%)\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to pick color: {str(e)}"
    
    def hex_to_rgb(self, hex_color):
        """Convert HEX to RGB"""
        try:
            hex_color = hex_color.lstrip('#')
            
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            return (r, g, b)
        
        except Exception as e:
            return None
    
    def rgb_to_hex(self, r, g, b):
        """Convert RGB to HEX"""
        try:
            return f"#{r:02x}{g:02x}{b:02x}".upper()
        except Exception as e:
            return None
    
    def rgb_to_hsl(self, r, g, b):
        """Convert RGB to HSL"""
        try:
            r, g, b = r/255.0, g/255.0, b/255.0
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            
            h = int(h * 360)
            s = int(s * 100)
            l = int(l * 100)
            
            return (h, s, l)
        except Exception as e:
            return None
    
    def hsl_to_rgb(self, h, s, l):
        """Convert HSL to RGB"""
        try:
            h = h / 360.0
            s = s / 100.0
            l = l / 100.0
            
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            
            return (r, g, b)
        except Exception as e:
            return None
    
    def rgb_to_hsv(self, r, g, b):
        """Convert RGB to HSV"""
        try:
            r, g, b = r/255.0, g/255.0, b/255.0
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            
            h = int(h * 360)
            s = int(s * 100)
            v = int(v * 100)
            
            return (h, s, v)
        except Exception as e:
            return None
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        try:
            h = h / 360.0
            s = s / 100.0
            v = v / 100.0
            
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            
            return (r, g, b)
        except Exception as e:
            return None
    
    def convert_color(self, color_input, from_format="auto", to_format="all"):
        """Convert color between different formats"""
        try:
            r, g, b = None, None, None
            
            if from_format == "auto":
                if isinstance(color_input, str):
                    if color_input.startswith('#'):
                        from_format = "hex"
                    elif color_input.startswith('rgb'):
                        from_format = "rgb"
                    elif color_input.startswith('hsl'):
                        from_format = "hsl"
                    elif color_input.startswith('hsv'):
                        from_format = "hsv"
            
            if from_format == "hex":
                rgb = self.hex_to_rgb(color_input)
                if rgb:
                    r, g, b = rgb
            
            elif from_format == "rgb":
                match = re.findall(r'\d+', color_input)
                if len(match) >= 3:
                    r, g, b = int(match[0]), int(match[1]), int(match[2])
            
            elif from_format == "hsl":
                match = re.findall(r'\d+', color_input)
                if len(match) >= 3:
                    h, s, l = int(match[0]), int(match[1]), int(match[2])
                    rgb = self.hsl_to_rgb(h, s, l)
                    if rgb:
                        r, g, b = rgb
            
            elif from_format == "hsv":
                match = re.findall(r'\d+', color_input)
                if len(match) >= 3:
                    h, s, v = int(match[0]), int(match[1]), int(match[2])
                    rgb = self.hsv_to_rgb(h, s, v)
                    if rgb:
                        r, g, b = rgb
            
            if r is None or g is None or b is None:
                return "❌ Invalid color format"
            
            result = f"\n{'='*60}\n"
            result += f"🎨 COLOR CONVERTER\n"
            result += f"{'='*60}\n\n"
            result += f"Input: {color_input}\n\n"
            
            if to_format in ["all", "hex"]:
                hex_color = self.rgb_to_hex(r, g, b)
                result += f"HEX: {hex_color}\n"
            
            if to_format in ["all", "rgb"]:
                result += f"RGB: rgb({r}, {g}, {b})\n"
            
            if to_format in ["all", "hsl"]:
                hsl = self.rgb_to_hsl(r, g, b)
                if hsl:
                    result += f"HSL: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)\n"
            
            if to_format in ["all", "hsv"]:
                hsv = self.rgb_to_hsv(r, g, b)
                if hsv:
                    result += f"HSV: hsv({hsv[0]}, {hsv[1]}%, {hsv[2]}%)\n"
            
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to convert color: {str(e)}"
    
    def generate_palette(self, base_color, scheme="complementary"):
        """Generate color palette from base color"""
        try:
            rgb = None
            if base_color.startswith('#'):
                rgb = self.hex_to_rgb(base_color)
            else:
                match = re.findall(r'\d+', base_color)
                if len(match) >= 3:
                    rgb = (int(match[0]), int(match[1]), int(match[2]))
            
            if not rgb:
                return "❌ Invalid base color"
            
            r, g, b = rgb
            h, s, v = self.rgb_to_hsv(r, g, b)
            
            palette = []
            
            if scheme == "complementary":
                palette.append(rgb)
                comp_h = (h + 180) % 360
                palette.append(self.hsv_to_rgb(comp_h, s, v))
            
            elif scheme == "analogous":
                palette.append(self.hsv_to_rgb((h - 30) % 360, s, v))
                palette.append(rgb)
                palette.append(self.hsv_to_rgb((h + 30) % 360, s, v))
            
            elif scheme == "triadic":
                palette.append(rgb)
                palette.append(self.hsv_to_rgb((h + 120) % 360, s, v))
                palette.append(self.hsv_to_rgb((h + 240) % 360, s, v))
            
            elif scheme == "monochromatic":
                palette.append(self.hsv_to_rgb(h, s, max(0, v - 30)))
                palette.append(self.hsv_to_rgb(h, s, max(0, v - 15)))
                palette.append(rgb)
                palette.append(self.hsv_to_rgb(h, s, min(100, v + 15)))
                palette.append(self.hsv_to_rgb(h, s, min(100, v + 30)))
            
            result = f"\n{'='*60}\n"
            result += f"🎨 COLOR PALETTE - {scheme.upper()}\n"
            result += f"{'='*60}\n\n"
            result += f"Base Color: {base_color}\n\n"
            
            for i, color in enumerate(palette, 1):
                hex_color = self.rgb_to_hex(*color)
                result += f"{i}. {hex_color} - rgb{color}\n"
            
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to generate palette: {str(e)}"
    
    def lighten_color(self, color, amount=20):
        """Lighten a color by percentage"""
        try:
            rgb = None
            if color.startswith('#'):
                rgb = self.hex_to_rgb(color)
            else:
                match = re.findall(r'\d+', color)
                if len(match) >= 3:
                    rgb = (int(match[0]), int(match[1]), int(match[2]))
            
            if not rgb:
                return "❌ Invalid color"
            
            h, s, v = self.rgb_to_hsv(*rgb)
            v = min(100, v + amount)
            new_rgb = self.hsv_to_rgb(h, s, v)
            new_hex = self.rgb_to_hex(*new_rgb)
            
            return f"Lightened: {new_hex} - rgb{new_rgb}"
        
        except Exception as e:
            return f"❌ Failed to lighten color: {str(e)}"
    
    def darken_color(self, color, amount=20):
        """Darken a color by percentage"""
        try:
            rgb = None
            if color.startswith('#'):
                rgb = self.hex_to_rgb(color)
            else:
                match = re.findall(r'\d+', color)
                if len(match) >= 3:
                    rgb = (int(match[0]), int(match[1]), int(match[2]))
            
            if not rgb:
                return "❌ Invalid color"
            
            h, s, v = self.rgb_to_hsv(*rgb)
            v = max(0, v - amount)
            new_rgb = self.hsv_to_rgb(h, s, v)
            new_hex = self.rgb_to_hex(*new_rgb)
            
            return f"Darkened: {new_hex} - rgb{new_rgb}"
        
        except Exception as e:
            return f"❌ Failed to darken color: {str(e)}"

if __name__ == "__main__":
    color_tools = ColorTools()
    
    print("Testing Color Tools...")
    print(color_tools.convert_color("#FF5733"))
    print(color_tools.generate_palette("#3498db", "complementary"))
    print(color_tools.lighten_color("#3498db", 20))
