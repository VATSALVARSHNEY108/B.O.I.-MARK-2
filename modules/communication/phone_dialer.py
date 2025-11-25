       "message": f"📱 Calling {phone_number} via Phone Link",
                                    "phone": phone_number,
                                    "method": "phone_link_auto_visual",
                                    "auto_call": True
                                }
                        except Exception as img_error:
                            print(f"ℹ️ Visual button detection not available: {img_error}")
                        
                        # Strategy 2: Try to find "Call" button using OCR
                        try:
                            import pytesseract
                            from PIL import ImageGrab
                            import numpy as np
                            
                            # Take a screenshot to find "Call" button
                            screenshot = ImageGrab.grab()
                            
                            # Use pytesseract to find text on screen
                            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                            
                            # Look for "Call" text
                            for i, text in enumerate(data['text']):
                                if text.strip().lower() in ['call', 'dial']:
                                    # Found the Call button text, click it
                                    x = data['left'][i] + data['width'][i] // 2
                                    y = data['top'][i] + data['height'][i] // 2
                                    pyautogui.click(x, y)
                                    print("✅ Call button clicked via OCR!")
                                    
                                    return {
                                        "success": True,
                                        "message": f"📱 Calling {phone_number} via Phone Link",
                                        "phone": phone_number,
                                        "method": "phone_link_auto_ocr",
                                        "auto_call": True
                                    }
                        except Exception as ocr_error:
                            print(f"ℹ️ OCR detection not available: {ocr_error}")
                        
                        # Strategy 3: Click the call button at bottom of screen
                        print("📞 Attempting to click Call button...")
                        
                        # Check if we have a calibrated position
                        import json
                        calibrated = False
                        try:
                            with open("config/phone_link_button.json", 'r') as f:
                                config = json.load(f)
                                cal_x = config.get("call_button_x")
                                cal_y = config.get("call_button_y")
                                
                                if cal_x and cal_y:
                                    print(f"   Using calibrated position: ({cal_x}, {cal_y})")
                                    pyautogui.click(cal_x, cal_y)
                                    time.sleep(0.5)
                                    calibrated = True
                                    print("✅ Clicked at calibrated position!")
                        except FileNotFoundError:
                            print("   No calibration found. Using Phone Link layout positions...")
                        except Exception as e:
                            print(f"   Calibration error: {e}")
                        
                        # If no calibration, try Phone Link's actual button positions
                        if not calibrated:
                            # Get screen size
                            screen_width, screen_height = pyautogui.size()
                            
                            # Based on Phone Link UI: Call button is at the BOTTOM
                            # Usually at bottom-center or bottom-right of the Phone Link window
                            # Phone Link window is typically on the right side of screen
                            
                            click_positions = [
                                # Bottom center-right (most likely for call button)
                                (int(screen_width * 0.85), int(screen_height * 0.92)),  # Bottom right area
                                (int(screen_width * 0.5), int(screen_height * 0.95)),   # Bottom center
                                (int(screen_width * 0.75), int(screen_height * 0.90)),  # Bottom center-right
                                (int(screen_width * 0.85), int(screen_height * 0.85)),  # Right side, lower
                                # Also try dial pad area (right side of screen)
                                (int(screen_width * 0.88), int(screen_height * 0.70)),  # Dial pad area
                            ]
                            
                            for i, (x, y) in enumerate(click_positions):
                                print(f"   Trying position {i+1}/5: ({x}, {y})")
                                pyautogui.click(x, y)
                                time.sleep(0.5)
                            
                            print("✅ Click commands sent!")
                            print()
                            print("   💡 TIP: Run 'python scripts/calibrate_phone_link_button.py'")
                            print("      to find the exact Call button position on your screen!")
                        
                        # Also try keyboard shortcuts as backup
                        print("   Backup: Trying keyboard shortcuts...")
                        pyautogui.press('enter')
                        time.sleep(0.2)
                        pyautogui.press('space')
                        time.sleep(0.2)
                        
                        # Try Tab navigation as final backup
                        for i in range(2):
                            pyautogui.press('tab')
                            time.sleep(0.1)
                        pyautogui.press('enter')
                        
                        return {
                            "success": True,
                            "message": f"📱 Calling {phone_number} via Phone Link (tried multiple click positions)",
                            "phone": phone_number,
                            "method": "phone_link_auto_multiclick",
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
