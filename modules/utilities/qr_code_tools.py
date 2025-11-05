"""
QR Code Generator & Reader Module
Create QR codes and scan them from screen or files
"""

import qrcode
from PIL import Image
import os
from datetime import datetime
import pyautogui

try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

class QRCodeTools:
    def __init__(self):
        self.output_dir = "data/qr_codes"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_qr(self, data, filename=None, size=10, border=4, color="black", bg_color="white"):
        """Generate a QR code from text/URL"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color=color, back_color=bg_color)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"qr_code_{timestamp}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)
            
            result = f"\n{'='*60}\n"
            result += f"📱 QR CODE GENERATED\n"
            result += f"{'='*60}\n\n"
            result += f"Data: {data[:50]}{'...' if len(data) > 50 else ''}\n"
            result += f"Saved to: {filepath}\n"
            result += f"Size: {size}x{size} pixels per box\n"
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to generate QR code: {str(e)}"
    
    def generate_qr_url(self, url, filename=None):
        """Generate QR code for URL"""
        return self.generate_qr(url, filename)
    
    def generate_qr_text(self, text, filename=None):
        """Generate QR code for text"""
        return self.generate_qr(text, filename)
    
    def generate_qr_contact(self, name, phone, email=None, filename=None):
        """Generate QR code for contact (vCard format)"""
        try:
            vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\n"
            if email:
                vcard += f"EMAIL:{email}\n"
            vcard += "END:VCARD"
            
            return self.generate_qr(vcard, filename or f"contact_{name.replace(' ', '_')}.png")
        except Exception as e:
            return f"❌ Failed to generate contact QR: {str(e)}"
    
    def generate_qr_wifi(self, ssid, password, security="WPA", hidden=False, filename=None):
        """Generate QR code for WiFi connection"""
        try:
            wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
            
            return self.generate_qr(wifi_string, filename or f"wifi_{ssid}.png")
        except Exception as e:
            return f"❌ Failed to generate WiFi QR: {str(e)}"
    
    def read_qr_from_file(self, filepath):
        """Read QR code from image file"""
        try:
            if not PYZBAR_AVAILABLE:
                return "❌ pyzbar library not available. QR code reading requires additional system dependencies."
            
            if not os.path.exists(filepath):
                return f"❌ File not found: {filepath}"
            
            img = Image.open(filepath)
            decoded_objects = decode(img)
            
            if not decoded_objects:
                return "⚠️ No QR code found in image"
            
            result = f"\n{'='*60}\n"
            result += f"📱 QR CODE READER\n"
            result += f"{'='*60}\n\n"
            result += f"File: {filepath}\n"
            result += f"Found {len(decoded_objects)} QR code(s)\n\n"
            
            for i, obj in enumerate(decoded_objects, 1):
                data = obj.data.decode('utf-8')
                qr_type = obj.type
                
                result += f"QR Code {i}:\n"
                result += f"  Type: {qr_type}\n"
                result += f"  Data: {data}\n\n"
            
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to read QR code: {str(e)}"
    
    def read_qr_from_screen(self):
        """Take screenshot and read QR code from it"""
        try:
            if not PYZBAR_AVAILABLE:
                return "❌ pyzbar library not available. QR code reading requires additional system dependencies."
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.output_dir, f"qr_screenshot_{timestamp}.png")
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            img = Image.open(screenshot_path)
            decoded_objects = decode(img)
            
            if not decoded_objects:
                return "⚠️ No QR code found on screen"
            
            result = f"\n{'='*60}\n"
            result += f"📱 QR CODE SCANNER (Screen)\n"
            result += f"{'='*60}\n\n"
            result += f"Screenshot saved: {screenshot_path}\n"
            result += f"Found {len(decoded_objects)} QR code(s)\n\n"
            
            for i, obj in enumerate(decoded_objects, 1):
                data = obj.data.decode('utf-8')
                qr_type = obj.type
                
                result += f"QR Code {i}:\n"
                result += f"  Type: {qr_type}\n"
                result += f"  Data: {data}\n\n"
            
            result += f"{'='*60}\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to scan screen: {str(e)}"
    
    def list_qr_codes(self):
        """List all generated QR codes"""
        try:
            if not os.path.exists(self.output_dir):
                return "ℹ️ No QR codes directory found"
            
            qr_files = [f for f in os.listdir(self.output_dir) if f.endswith('.png')]
            
            if not qr_files:
                return "ℹ️ No QR codes found"
            
            result = f"📱 Generated QR Codes:\n" + "=" * 60 + "\n"
            
            for filename in sorted(qr_files, reverse=True):
                filepath = os.path.join(self.output_dir, filename)
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                result += f"\n• {filename}\n"
                result += f"  Size: {size/1024:.2f} KB\n"
                result += f"  Created: {mtime.strftime('%Y-%m-%d %H:%M')}\n"
            
            result += "=" * 60
            return result
        
        except Exception as e:
            return f"❌ Failed to list QR codes: {str(e)}"
    
    def delete_qr(self, filename):
        """Delete a generated QR code"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return f"✅ Deleted QR code: {filename}"
            else:
                return f"⚠️ QR code not found: {filename}"
        
        except Exception as e:
            return f"❌ Failed to delete QR code: {str(e)}"
    
    def generate_qr_batch(self, data_list, prefix="batch"):
        """Generate multiple QR codes from a list"""
        try:
            results = []
            
            for i, data in enumerate(data_list, 1):
                filename = f"{prefix}_{i}.png"
                result = self.generate_qr(data, filename)
                results.append(f"{i}. {filename}")
            
            summary = f"\n{'='*60}\n"
            summary += f"📱 BATCH QR CODE GENERATION\n"
            summary += f"{'='*60}\n\n"
            summary += f"Generated {len(data_list)} QR codes:\n\n"
            summary += "\n".join(results)
            summary += f"\n\n{'='*60}\n"
            
            return summary
        
        except Exception as e:
            return f"❌ Failed to generate batch QR codes: {str(e)}"

if __name__ == "__main__":
    qr_tools = QRCodeTools()
    
    print("Testing QR Code Tools...")
    print(qr_tools.generate_qr_url("https://www.example.com", "test_url"))
    print(qr_tools.generate_qr_text("Hello, World!", "test_text"))
    print(qr_tools.list_qr_codes())
