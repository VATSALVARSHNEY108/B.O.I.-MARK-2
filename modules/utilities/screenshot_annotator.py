"""
Screenshot Annotator Module
Add text, arrows, highlights, and shapes to screenshots
"""

from PIL import Image, ImageDraw, ImageFont
import pyautogui
import os
from datetime import datetime

class ScreenshotAnnotator:
    def __init__(self):
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        self.current_screenshot = None
        self.current_image = None
    
    def take_screenshot(self, filename=None):
        """Take a new screenshot"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            self.current_screenshot = filepath
            self.current_image = Image.open(filepath)
            
            return f"📸 Screenshot saved: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to take screenshot: {str(e)}"
    
    def load_screenshot(self, filepath):
        """Load an existing screenshot for annotation"""
        try:
            if not os.path.exists(filepath):
                return f"❌ File not found: {filepath}"
            
            self.current_screenshot = filepath
            self.current_image = Image.open(filepath)
            
            return f"✅ Loaded screenshot: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to load screenshot: {str(e)}"
    
    def add_text(self, text, x, y, color="red", size=30, filename=None):
        """Add text annotation to screenshot"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            img = self.current_image.copy()
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                font = ImageFont.load_default()
            
            draw.text((x, y), text, fill=color, font=font)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Added text: '{text}' at ({x}, {y})\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to add text: {str(e)}"
    
    def add_arrow(self, start_x, start_y, end_x, end_y, color="red", width=3, filename=None):
        """Add arrow annotation to screenshot"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            img = self.current_image.copy()
            draw = ImageDraw.Draw(img)
            
            draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
            
            import math
            angle = math.atan2(end_y - start_y, end_x - start_x)
            arrow_length = 20
            arrow_angle = math.pi / 6
            
            arrow_point1 = (
                end_x - arrow_length * math.cos(angle - arrow_angle),
                end_y - arrow_length * math.sin(angle - arrow_angle)
            )
            arrow_point2 = (
                end_x - arrow_length * math.cos(angle + arrow_angle),
                end_y - arrow_length * math.sin(angle + arrow_angle)
            )
            
            draw.line([arrow_point1, (end_x, end_y)], fill=color, width=width)
            draw.line([arrow_point2, (end_x, end_y)], fill=color, width=width)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Added arrow from ({start_x}, {start_y}) to ({end_x}, {end_y})\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to add arrow: {str(e)}"
    
    def add_rectangle(self, x, y, width, height, color="red", outline_width=3, fill=False, filename=None):
        """Add rectangle highlight to screenshot"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            img = self.current_image.copy()
            draw = ImageDraw.Draw(img)
            
            x2, y2 = x + width, y + height
            
            if fill:
                fill_color = color if isinstance(color, tuple) else color
                draw.rectangle([x, y, x2, y2], fill=fill_color, outline=color, width=outline_width)
            else:
                draw.rectangle([x, y, x2, y2], outline=color, width=outline_width)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Added rectangle at ({x}, {y}), size {width}x{height}\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to add rectangle: {str(e)}"
    
    def add_circle(self, center_x, center_y, radius, color="red", outline_width=3, fill=False, filename=None):
        """Add circle highlight to screenshot"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            img = self.current_image.copy()
            draw = ImageDraw.Draw(img)
            
            bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
            
            if fill:
                draw.ellipse(bbox, fill=color, outline=color, width=outline_width)
            else:
                draw.ellipse(bbox, outline=color, width=outline_width)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Added circle at ({center_x}, {center_y}), radius {radius}\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to add circle: {str(e)}"
    
    def add_highlight(self, x, y, width, height, color=(255, 255, 0, 100), filename=None):
        """Add semi-transparent highlight to screenshot"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            img = self.current_image.copy()
            
            overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            x2, y2 = x + width, y + height
            draw.rectangle([x, y, x2, y2], fill=color)
            
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Added highlight at ({x}, {y}), size {width}x{height}\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to add highlight: {str(e)}"
    
    def blur_area(self, x, y, width, height, blur_amount=10, filename=None):
        """Blur a specific area (for privacy)"""
        try:
            if self.current_image is None:
                return "⚠️ No screenshot loaded. Take or load a screenshot first."
            
            from PIL import ImageFilter
            
            img = self.current_image.copy()
            
            x2, y2 = x + width, y + height
            region = img.crop((x, y, x2, y2))
            
            blurred_region = region.filter(ImageFilter.GaussianBlur(blur_amount))
            
            img.paste(blurred_region, (x, y))
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"annotated_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            self.current_image = img
            self.current_screenshot = filepath
            
            return f"✅ Blurred area at ({x}, {y}), size {width}x{height}\nSaved to: {filepath}"
        
        except Exception as e:
            return f"❌ Failed to blur area: {str(e)}"
    
    def list_screenshots(self):
        """List all screenshots"""
        try:
            if not os.path.exists(self.screenshots_dir):
                return "ℹ️ No screenshots directory found"
            
            files = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
            
            if not files:
                return "ℹ️ No screenshots found"
            
            result = f"📸 Screenshots:\n" + "=" * 60 + "\n"
            
            for filename in sorted(files, reverse=True)[:20]:
                filepath = os.path.join(self.screenshots_dir, filename)
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                result += f"\n• {filename}\n"
                result += f"  Size: {size/1024:.2f} KB\n"
                result += f"  Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n"
            
            result += "=" * 60
            return result
        
        except Exception as e:
            return f"❌ Failed to list screenshots: {str(e)}"

if __name__ == "__main__":
    annotator = ScreenshotAnnotator()
    
    print("Testing Screenshot Annotator...")
    print(annotator.take_screenshot("test"))
    print(annotator.add_text("Test Annotation", 100, 100))
    print(annotator.list_screenshots())
