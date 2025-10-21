import os
import platform
import webbrowser
from gui_automation import GUIAutomation
from contact_manager import ContactManager
from messaging_service import MessagingService

class CommandExecutor:
    """Executes parsed commands using the GUI automation module"""
    
    def __init__(self):
        self.gui = GUIAutomation()
        self.contact_manager = ContactManager()
        self.messaging = MessagingService(self.contact_manager)
    
    def execute(self, command_dict: dict) -> dict:
        """
        Execute a command dictionary returned by Gemini.
        Returns a result dict with success status and message.
        """
        if not command_dict:
            return {"success": False, "message": "No command provided"}
        
        action = command_dict.get("action", "")
        parameters = command_dict.get("parameters", {})
        steps = command_dict.get("steps", [])
        description = command_dict.get("description", "")
        
        print(f"\n📋 Task: {description}")
        
        if steps:
            return self.execute_workflow(steps)
        else:
            return self.execute_single_action(action, parameters)
    
    def execute_workflow(self, steps: list) -> dict:
        """Execute a multi-step workflow"""
        print(f"\n🔄 Executing workflow with {len(steps)} steps...")
        
        results = []
        for i, step in enumerate(steps, 1):
            action = step.get("action", "")
            parameters = step.get("parameters", {})
            
            print(f"\n  Step {i}/{len(steps)}: {action}")
            result = self.execute_single_action(action, parameters)
            results.append(result)
            
            if not result["success"]:
                return {
                    "success": False,
                    "message": f"Workflow failed at step {i}: {result['message']}"
                }
        
        return {
            "success": True,
            "message": f"Workflow completed successfully ({len(steps)} steps)"
        }
    
    def execute_single_action(self, action: str, parameters: dict) -> dict:
        """Execute a single action"""
        try:
            if action == "open_app":
                app_name = parameters.get("app_name", "")
                success = self.gui.open_application(app_name)
                return {
                    "success": success,
                    "message": f"Opened {app_name}" if success else f"Failed to open {app_name}"
                }
            
            elif action == "type_text":
                text = parameters.get("text", "")
                interval = parameters.get("interval", 0.05)
                success = self.gui.type_text(text, interval)
                return {
                    "success": success,
                    "message": f"Typed text" if success else "Failed to type text"
                }
            
            elif action == "click":
                x = parameters.get("x")
                y = parameters.get("y")
                button = parameters.get("button", "left")
                success = self.gui.click(x, y, button)
                return {
                    "success": success,
                    "message": "Clicked" if success else "Failed to click"
                }
            
            elif action == "move_mouse":
                x = parameters.get("x", 0)
                y = parameters.get("y", 0)
                success = self.gui.move_mouse(x, y)
                return {
                    "success": success,
                    "message": f"Moved mouse to ({x}, {y})" if success else "Failed to move mouse"
                }
            
            elif action == "press_key":
                key = parameters.get("key", "")
                success = self.gui.press_key(key)
                return {
                    "success": success,
                    "message": f"Pressed {key}" if success else f"Failed to press {key}"
                }
            
            elif action == "hotkey":
                keys = parameters.get("keys", [])
                if isinstance(keys, list):
                    success = self.gui.hotkey(*keys)
                    return {
                        "success": success,
                        "message": f"Pressed {'+'.join(keys)}" if success else "Failed to press hotkey"
                    }
                else:
                    return {"success": False, "message": "Keys must be a list"}
            
            elif action == "screenshot":
                filename = parameters.get("filename", "screenshot.png")
                success = self.gui.screenshot(filename)
                return {
                    "success": success,
                    "message": f"Screenshot saved as {filename}" if success else "Failed to take screenshot"
                }
            
            elif action == "copy":
                text = parameters.get("text", "")
                success = self.gui.copy_to_clipboard(text)
                return {
                    "success": success,
                    "message": "Copied to clipboard" if success else "Failed to copy"
                }
            
            elif action == "paste":
                success = self.gui.paste_from_clipboard()
                return {
                    "success": success,
                    "message": "Pasted from clipboard" if success else "Failed to paste"
                }
            
            elif action == "wait":
                seconds = parameters.get("seconds", 1)
                success = self.gui.wait(seconds)
                return {
                    "success": success,
                    "message": f"Waited {seconds} seconds" if success else "Failed to wait"
                }
            
            elif action == "search_web":
                query = parameters.get("query", "")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                return {
                    "success": True,
                    "message": f"Opened web search for: {query}"
                }
            
            elif action == "create_file":
                filename = parameters.get("filename", "")
                content = parameters.get("content", "")
                try:
                    with open(filename, 'w') as f:
                        f.write(content)
                    return {
                        "success": True,
                        "message": f"Created file: {filename}"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "message": f"Failed to create file: {str(e)}"
                    }
            
            elif action == "send_sms":
                contact_name = parameters.get("contact_name")
                phone = parameters.get("phone")
                message = parameters.get("message", "")
                result = self.messaging.send_sms(contact_name=contact_name, phone=phone, message=message)
                return result
            
            elif action == "send_email":
                contact_name = parameters.get("contact_name")
                email = parameters.get("email")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                result = self.messaging.send_email(contact_name=contact_name, email=email, subject=subject, body=body)
                return result
            
            elif action == "send_file":
                contact_name = parameters.get("contact_name", "")
                file_path = parameters.get("file_path", "")
                message = parameters.get("message", "")
                method = parameters.get("method", "auto")
                result = self.messaging.send_file(contact_name, file_path, message, method)
                return result
            
            elif action == "add_contact":
                name = parameters.get("name", "")
                phone = parameters.get("phone")
                email = parameters.get("email")
                success = self.contact_manager.add_contact(name, phone, email)
                return {
                    "success": success,
                    "message": f"Added contact: {name}" if success else f"Failed to add contact: {name}"
                }
            
            elif action == "list_contacts":
                contacts = self.contact_manager.list_contacts()
                if contacts:
                    contact_list = "\n".join([
                        f"  • {c['name']} - Phone: {c['phone'] or 'N/A'}, Email: {c['email'] or 'N/A'}"
                        for c in contacts
                    ])
                    return {
                        "success": True,
                        "message": f"Contacts:\n{contact_list}"
                    }
                else:
                    return {
                        "success": True,
                        "message": "No contacts found. Use 'add contact' to create one."
                    }
            
            elif action == "get_contact":
                name = parameters.get("name", "")
                contact = self.contact_manager.get_contact(name)
                if contact:
                    return {
                        "success": True,
                        "message": f"Contact: {contact['name']}\n  Phone: {contact['phone'] or 'N/A'}\n  Email: {contact['email'] or 'N/A'}"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Contact not found: {name}"
                    }
            
            elif action == "error":
                error_msg = parameters.get("error", "Unknown error")
                return {
                    "success": False,
                    "message": f"Command parsing error: {error_msg}"
                }
            
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
