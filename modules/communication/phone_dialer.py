"""
Phone Call Dialer for BOI
Make voice calls using Twilio integration or Phone Link
"""

import os
import platform
import webbrowser
import subprocess
from typing import Optional, Dict
from datetime import datetime
from modules.utilities.contact_manager import ContactManager


class PhoneDialer:
    """Make phone calls using Twilio"""
    
    def __init__(self):
        self.twilio_available = False
        self.demo_mode = True
        self.call_history = []
        self.is_windows = platform.system() == "Windows"
        self.contact_manager = ContactManager()
        
        self._check_twilio()
    
    def _check_twilio(self):
        """Check if Twilio credentials are available"""
        if (os.environ.get("TWILIO_ACCOUNT_SID") and 
            os.environ.get("TWILIO_AUTH_TOKEN") and
            os.environ.get("TWILIO_PHONE_NUMBER")):
            self.twilio_available = True
            self.demo_mode = False
            print("✅ Twilio phone dialer ready!")
        else:
            print("⚠️ Twilio not configured - phone dialer running in demo mode")
    
    def dial_call(self, phone_number: str, message: Optional[str] = None) -> Dict:
        """
        Dial a phone call to the specified number
        
        Args:
            phone_number: Phone number to call (with country code, e.g., +1234567890)
            message: Optional text-to-speech message to play when call is answered
        
        Returns:
            Dict with success status and details
        """
        if not phone_number:
            return {
                "success": False,
                "message": "No phone number provided"
            }
        
        # Normalize phone number
        phone_number = self._normalize_phone_number(phone_number)
        
        # Default message if none provided
        if not message:
            message = "This is an automated call from BOI (Barely Obeys Instructions) Assistant. This is a test call. Thank you."
        
        # Log the call attempt
        call_record = {
            "phone": phone_number,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        if self.demo_mode or not self.twilio_available:
            print(f"\n📞 [DEMO MODE] Making call to: {phone_number}")
            print(f"📝 Message: {message}")
            call_record["status"] = "demo"
            self.call_history.append(call_record)
            return {
                "success": True,
                "message": f"[DEMO] Call would be placed to {phone_number}",
                "demo": True,
                "phone": phone_number
            }
        
        try:
            from twilio.rest import Client
            
            # Initialize Twilio client
            client = Client(
                os.environ.get("TWILIO_ACCOUNT_SID"),
                os.environ.get("TWILIO_AUTH_TOKEN")
            )
            
            twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
            
            # Create TwiML for the call
            twiml_url = self._create_twiml_url(message)
            
            # Make the call
            call = client.calls.create(
                to=phone_number,
                from_=twilio_phone,
                url=twiml_url,
                method='GET'
            )
            
            call_record["status"] = "success"
            call_record["sid"] = call.sid
            self.call_history.append(call_record)
            
            print(f"✅ Call initiated to {phone_number}")
            print(f"📞 Call SID: {call.sid}")
            
            return {
                "success": True,
                "message": f"Call initiated to {phone_number}",
                "sid": call.sid,
                "phone": phone_number,
                "status": call.status
            }
            
        except Exception as e:
            call_record["status"] = "failed"
            call_record["error"] = str(e)
            self.call_history.append(call_record)
            
            return {
                "success": False,
                "message": f"Error making call: {str(e)}",
                "phone": phone_number
            }
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Normalize phone number to E.164 format"""
        # Remove common formatting characters
        phone = phone.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
        # Add + if not present
        if not phone.startswith("+"):
            # Assume US/Canada if 10 digits
            if len(phone) == 10:
                phone = "+1" + phone
            else:
                phone = "+" + phone
        
        return phone
    
    def _create_twiml_url(self, message: str) -> str:
        """
        Create a TwiML URL for the voice message using Twimlets
        Twimlets are simple, hosted TwiML apps from Twilio
        """
        from urllib.parse import quote
        
        # Encode the message for URL safety
        encoded_message = quote(message)
        
        # Use Twilio's Twimlets Message endpoint for text-to-speech
        # This will actually speak the message we provide
        twiml_url = f'http://twimlets.com/message?Message={encoded_message}'
        
        return twiml_url
    
    def make_call_with_twiml(self, phone_number: str, twiml_content: str) -> Dict:
        """
        Make a call with custom TwiML content
        
        Args:
            phone_number: Phone number to call
            twiml_content: Custom TwiML XML content
        
        Returns:
            Dict with success status and details
        """
        if self.demo_mode or not self.twilio_available:
            print(f"\n📞 [DEMO MODE] Making call to: {phone_number}")
            print(f"📝 TwiML: {twiml_content[:100]}...")
            return {
                "success": True,
                "message": f"[DEMO] Call with custom TwiML would be placed to {phone_number}",
                "demo": True
            }
        
        try:
            from twilio.rest import Client
            
            client = Client(
                os.environ.get("TWILIO_ACCOUNT_SID"),
                os.environ.get("TWILIO_AUTH_TOKEN")
            )
            
            twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
            
            # Make call with TwiML
            call = client.calls.create(
                to=phone_number,
                from_=twilio_phone,
                twiml=twiml_content
            )
            
            return {
                "success": True,
                "message": f"Call initiated to {phone_number}",
                "sid": call.sid,
                "status": call.status
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error making call: {str(e)}"
            }
    
    def get_call_status(self, call_sid: str) -> Dict:
        """
        Get the status of a call
        
        Args:
            call_sid: Twilio call SID
        
        Returns:
            Dict with call status information
        """
        if self.demo_mode or not self.twilio_available:
            return {
                "success": True,
                "message": "[DEMO] Call status check",
                "status": "completed",
                "demo": True
            }
        
        try:
            from twilio.rest import Client
            
            client = Client(
                os.environ.get("TWILIO_ACCOUNT_SID"),
                os.environ.get("TWILIO_AUTH_TOKEN")
            )
            
            call = client.calls(call_sid).fetch()
            
            return {
                "success": True,
                "sid": call.sid,
                "status": call.status,
                "duration": call.duration,
                "from": call.from_,
                "to": call.to,
                "direction": call.direction
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching call status: {str(e)}"
            }
    
    def get_call_history(self, limit: int = 10) -> list:
        """Get recent call history"""
        return self.call_history[-limit:]
    
    def quick_dial(self, name_or_number: str, message: Optional[str] = None, use_phone_link: bool = True) -> Dict:
        """
        Quick dial by name or number
        Supports both direct phone numbers and contact names
        Uses Phone Link by default for actual calling
        
        Args:
            name_or_number: Either a phone number or contact name
            message: Optional message to play (only for Twilio)
            use_phone_link: If True (default), use Phone Link. If False, use Twilio
        
        Returns:
            Dict with call status
        """
        # Check if it's a phone number (contains digits and common phone chars)
        if any(char.isdigit() for char in name_or_number) and any(c in name_or_number for c in ['+', '-', '(', ')', ' '] + list('0123456789')):
            # Looks like a phone number - use it directly
            phone_number = name_or_number
            contact_name = None
        else:
            # Try to look up contact by name
            phone_number = self.contact_manager.get_phone(name_or_number)
            contact_name = name_or_number
            
            if not phone_number:
                return {
                    "success": False,
                    "message": f"Contact '{name_or_number}' not found. Add contact or provide phone number."
                }
            
            print(f"📇 Found contact '{name_or_number}' → {phone_number}")
        
        # Use Phone Link by default (works on Windows without requiring Twilio)
        if use_phone_link and self.is_windows:
            result = self.dial_with_phone_link(phone_number, auto_call=True)
            # Add contact name to result if available
            if contact_name and result.get('success'):
                result['contact_name'] = contact_name
                result['message'] = f"📱 Calling {contact_name} ({phone_number})"
            return result
        else:
            # Fall back to Twilio (requires API credentials)
            return self.dial_call(phone_number, message)
    
    def call_contact(self, name: str, auto_call: bool = True) -> Dict:
        """
        Call a contact by name using Phone Link
        
        Args:
            name: Contact name to call
            auto_call: If True, automatically press call button
        
        Returns:
            Dict with success status and details
        """
        # Look up contact
        phone_number = self.contact_manager.get_phone(name)
        
        if not phone_number:
            # Try to find similar contacts
            similar = self.contact_manager.search_contacts(name)
            if similar:
                contacts_list = ", ".join([c['name'] for c in similar[:3]])
                return {
                    "success": False,
                    "message": f"Contact '{name}' not found. Did you mean: {contacts_list}?"
                }
            else:
                return {
                    "success": False,
                    "message": f"Contact '{name}' not found. Add contact first or provide phone number."
                }
        
        # Get full contact info for better logging
        contact = self.contact_manager.get_contact(name)
        contact_name = contact.get('name', name)
        
        print(f"📇 Calling {contact_name} at {phone_number}")
        
        # Call using Phone Link
        result = self.dial_with_phone_link(phone_number, auto_call=auto_call)
        
        # Update message to include contact name
        if result['success']:
            result['message'] = f"📱 Calling {contact_name} ({phone_number})"
            result['contact_name'] = contact_name
        
        return result
    
    def dial_with_phone_link(self, phone_number: str, auto_call: bool = True) -> Dict:
        """
        Dial a call using Windows Phone Link (Your Phone app)
        This opens Phone Link and initiates a call without needing Twilio
        
        Args:
            phone_number: Phone number to dial (any format)
            auto_call: If True, automatically click the call button (default: True)
        
        Returns:
            Dict with success status and details
        """
        if not phone_number:
            return {
                "success": False,
                "message": "No phone number provided"
            }
        
        # Clean the phone number (remove spaces, dashes, etc.)
        cleaned_number = phone_number.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
        
        try:
            # Log the call attempt
            call_record = {
                "phone": phone_number,
                "method": "phone_link",
                "timestamp": datetime.now().isoformat(),
                "status": "initiated"
            }
            self.call_history.append(call_record)
            
            if self.is_windows:
                # Use tel: URI protocol which Phone Link handles
                # This will automatically open Phone Link and dial the number
                tel_uri = f"tel:{cleaned_number}"
                
                # Try multiple methods to ensure it works
                try:
                    # Method 1: Use webbrowser to open tel: URI
                    webbrowser.open(tel_uri)
                    print(f"📞 Opening Phone Link to dial: {phone_number}")
                except:
                    # Method 2: Use subprocess with start command
                    subprocess.Popen(['start', tel_uri], shell=True)
                
                # Auto-click the call button if requested
                if auto_call:
                    try:
                        import pyautogui
                        import time
                        
                        print("⏳ Waiting for Phone Link to open...")
                        time.sleep(3)  # Wait for Phone Link to fully load
                        
                        # Try to find and click the "Call" button
                        # Phone Link usually has a green call button
                        print("🔍 Looking for Call button...")
                        
                        # Option 1: Try to find call button by image (if available)
                        # Option 2: Use keyboard shortcut - Enter key usually triggers call
                        print("📞 Pressing Enter to initiate call...")
                        pyautogui.press('enter')
                        time.sleep(0.5)
                        
                        # Backup: Try Alt+C (common shortcut for Call)
                        pyautogui.hotkey('alt', 'c')
                        
                        return {
                            "success": True,
                            "message": f"📱 Phone Link opened and calling {phone_number}",
                            "phone": phone_number,
                            "method": "phone_link_auto",
                            "auto_call": True
                        }
                    except ImportError:
                        # PyAutoGUI not available, just open Phone Link
                        return {
                            "success": True,
                            "message": f"📱 Phone Link opened with {phone_number} - Press Enter or click Call button",
                            "phone": phone_number,
                            "method": "phone_link_manual",
                            "auto_call": False,
                            "note": "Install pyautogui for automatic calling: pip install pyautogui"
                        }
                    except Exception as e:
                        print(f"⚠️ Auto-call failed: {e}")
                        return {
                            "success": True,
                            "message": f"📱 Phone Link opened with {phone_number} - Please click Call button manually",
                            "phone": phone_number,
                            "method": "phone_link_manual",
                            "auto_call": False,
                            "note": str(e)
                        }
                else:
                    return {
                        "success": True,
                        "message": f"📱 Phone Link opened with {phone_number} - Press Enter or click Call button",
                        "phone": phone_number,
                        "method": "phone_link_manual"
                    }
            else:
                # On non-Windows systems, try generic tel: URI
                tel_uri = f"tel:{cleaned_number}"
                webbrowser.open(tel_uri)
                
                return {
                    "success": True,
                    "message": f"📱 Opening default phone app to dial {phone_number}",
                    "phone": phone_number,
                    "method": "tel_uri"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error dialing with Phone Link: {str(e)}",
                "phone": phone_number
            }
    
    def open_phone_link(self) -> Dict:
        """
        Open Windows Phone Link app
        
        Returns:
            Dict with success status
        """
        try:
            if self.is_windows:
                # Open Phone Link using ms-yourphone: protocol
                try:
                    webbrowser.open("ms-yourphone:")
                    return {
                        "success": True,
                        "message": "📱 Opening Phone Link app..."
                    }
                except:
                    # Alternative: Use shell command
                    subprocess.Popen(['start', 'ms-yourphone:'], shell=True)
                    return {
                        "success": True,
                        "message": "📱 Opening Phone Link app..."
                    }
            else:
                return {
                    "success": False,
                    "message": "Phone Link is only available on Windows"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error opening Phone Link: {str(e)}"
            }


def create_phone_dialer():
    """Factory function to create PhoneDialer instance"""
    return PhoneDialer()
