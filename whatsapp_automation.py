"""
WhatsApp Automation Module
Send messages via WhatsApp Web
"""

import pywhatkit as pwk
import time


class WhatsAppAutomation:
    """Handles WhatsApp messaging automation"""
    
    def __init__(self):
        """Initialize WhatsApp automation"""
        print("📱 WhatsApp automation ready")
    
    def send_message_instantly(self, phone_number, message):
        """
        Send WhatsApp message instantly to a phone number.
        
        Args:
            phone_number: Phone number with country code (e.g., "+1234567890")
            message: Message text to send
        
        Returns:
            Success status and message
        """
        try:
            print(f"  📱 Sending WhatsApp message to {phone_number}")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message sent to {phone_number}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp message: {str(e)}"
            }
    
    def send_message_scheduled(self, phone_number, message, hour, minute):
        """
        Schedule a WhatsApp message for a specific time.
        
        Args:
            phone_number: Phone number with country code
            message: Message text to send
            hour: Hour in 24h format (0-23)
            minute: Minute (0-59)
        
        Returns:
            Success status and message
        """
        try:
            print(f"  📱 Scheduling WhatsApp message to {phone_number}")
            print(f"  ⏰ Scheduled for: {hour}:{minute:02d}")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg(
                phone_no=phone_number,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message scheduled for {hour}:{minute:02d}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error scheduling WhatsApp message: {str(e)}"
            }
    
    def send_to_group_instantly(self, group_id, message):
        """
        Send WhatsApp message to a group instantly.
        
        Args:
            group_id: WhatsApp group ID (from invite link)
            message: Message text to send
        
        Returns:
            Success status and message
        """
        try:
            print(f"  📱 Sending WhatsApp message to group")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg_to_group_instantly(
                group_id=group_id,
                message=message,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message sent to group"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp group message: {str(e)}"
            }
    
    def send_image(self, phone_number, image_path, caption=""):
        """
        Send an image via WhatsApp.
        
        Args:
            phone_number: Phone number with country code
            image_path: Path to the image file (JPG only, PNG not supported)
            caption: Optional image caption
        
        Returns:
            Success status and message
        """
        try:
            print(f"  📱 Sending WhatsApp image to {phone_number}")
            print(f"  🖼️  Image: {image_path}")
            if caption:
                print(f"  💬 Caption: {caption}")
            
            pwk.sendwhats_image(
                receiver=phone_number,
                img_path=image_path,
                caption=caption,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp image sent to {phone_number}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp image: {str(e)}"
            }


def create_whatsapp_automation():
    """
    Factory function to create WhatsAppAutomation instance.
    
    Returns:
        WhatsAppAutomation instance
    """
    return WhatsAppAutomation()
