"""
Batch Form Filler Module
Automatically fills web forms, desktop forms, and applications using templates
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    pyperclip = None

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None


class BatchFormFiller:
    """Intelligent batch form filling with multiple strategies"""
    
    def __init__(self):
        self.templates_file = "form_templates.json"
        self.templates = self.load_templates()
        self.driver = None
        self.fill_history = []
        self.field_mappings = self.get_field_mappings()
        self.selenium_available = SELENIUM_AVAILABLE
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        self.pandas_available = PANDAS_AVAILABLE
        self.pyperclip_available = PYPERCLIP_AVAILABLE
        
    def load_templates(self) -> Dict:
        """Load form templates from JSON"""
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_templates(self):
        """Save form templates to JSON"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
    
    def get_field_mappings(self) -> Dict[str, List[str]]:
        """Common field name variations for intelligent matching"""
        return {
            'email': ['email', 'e-mail', 'mail', 'email_address', 'user_email', 'contact_email'],
            'first_name': ['first_name', 'firstname', 'fname', 'given_name', 'forename'],
            'last_name': ['last_name', 'lastname', 'lname', 'surname', 'family_name'],
            'full_name': ['full_name', 'name', 'fullname', 'your_name', 'user_name'],
            'phone': ['phone', 'telephone', 'mobile', 'cell', 'phone_number', 'contact_number'],
            'address': ['address', 'street', 'address_line1', 'street_address', 'address1'],
            'city': ['city', 'town', 'locality'],
            'state': ['state', 'province', 'region', 'county'],
            'zip': ['zip', 'zipcode', 'postal', 'postcode', 'postal_code', 'zip_code'],
            'country': ['country', 'nation', 'country_code'],
            'company': ['company', 'organization', 'employer', 'company_name'],
            'job_title': ['job_title', 'title', 'position', 'role'],
            'message': ['message', 'comments', 'feedback', 'description', 'details', 'notes'],
            'subject': ['subject', 'topic', 'regarding'],
            'username': ['username', 'user', 'login', 'account_name'],
            'password': ['password', 'pass', 'pwd'],
            'date_of_birth': ['date_of_birth', 'dob', 'birthdate', 'birth_date', 'birthday']
        }
    
    def find_field_value(self, field_name: str, template_data: Dict) -> Optional[str]:
        """Intelligently find the value for a field using fuzzy matching"""
        field_lower = field_name.lower().replace('-', '_').replace(' ', '_')
        
        # Direct match
        if field_lower in template_data:
            return str(template_data[field_lower])
        
        # Check field mappings
        for key, variations in self.field_mappings.items():
            if field_lower in variations and key in template_data:
                return str(template_data[key])
        
        # Partial match
        for key in template_data:
            if field_lower in key.lower() or key.lower() in field_lower:
                return str(template_data[key])
        
        return None
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check which dependencies are available"""
        return {
            'selenium': self.selenium_available,
            'pyautogui': self.pyautogui_available,
            'pandas': self.pandas_available,
            'pyperclip': self.pyperclip_available
        }
    
    def get_missing_dependencies_message(self, required: List[str]) -> str:
        """Get helpful message about missing dependencies"""
        missing = [dep for dep in required if not getattr(self, f'{dep}_available', False)]
        if not missing:
            return ""
        
        install_commands = {
            'selenium': 'pip install selenium',
            'pyautogui': 'pip install pyautogui',
            'pandas': 'pip install pandas openpyxl',
            'pyperclip': 'pip install pyperclip'
        }
        
        msg = f"Missing required dependencies: {', '.join(missing)}\n"
        msg += "Install with:\n"
        for dep in missing:
            msg += f"  {install_commands.get(dep, f'pip install {dep}')}\n"
        
        if 'selenium' in missing:
            msg += "\nNote: Selenium also requires ChromeDriver or another WebDriver.\n"
            msg += "For Replit, consider using desktop or clipboard mode instead.\n"
        
        return msg
    
    def _init_webdriver(self) -> Optional[Any]:
        """Initialize WebDriver with proper error handling"""
        if not SELENIUM_AVAILABLE:
            return None
        
        try:
            options = ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')
            
            try:
                driver = webdriver.Chrome(options=options)
                return driver
            except Exception as e:
                print(f"ChromeDriver not available: {e}")
                print("Attempting to use Firefox...")
                try:
                    driver = webdriver.Firefox()
                    return driver
                except Exception:
                    return None
        except Exception:
            return None
    
    def fill_web_form_selenium(self, url: str, template_name: str, submit: bool = False) -> Dict:
        """Fill web form using Selenium with intelligent field detection"""
        if not self.selenium_available:
            return {
                "success": False,
                "error": "Selenium not available",
                "help": self.get_missing_dependencies_message(['selenium'])
            }
        
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        template_data = self.templates[template_name]
        
        try:
            # Initialize Selenium
            if not self.driver:
                self.driver = self._init_webdriver()
                if not self.driver:
                    return {
                        "success": False,
                        "error": "WebDriver initialization failed",
                        "help": "ChromeDriver or other WebDriver not configured.\nConsider using desktop_form_pyautogui() or fill_form_clipboard() instead."
                    }
            
            self.driver.get(url)
            time.sleep(2)
            
            filled_fields = []
            errors = []
            
            # Find all input fields
            input_elements = self.driver.find_elements(By.TAG_NAME, 'input')
            textarea_elements = self.driver.find_elements(By.TAG_NAME, 'textarea')
            select_elements = self.driver.find_elements(By.TAG_NAME, 'select')
            
            all_fields = input_elements + textarea_elements + select_elements
            
            for element in all_fields:
                field_name = "unknown"
                try:
                    # Get field identifiers
                    field_name = element.get_attribute('name') or element.get_attribute('id') or element.get_attribute('placeholder') or "unknown"
                    field_type = element.get_attribute('type')
                    
                    if not field_name or field_name == "unknown":
                        continue
                    
                    # Skip hidden and submit buttons
                    if field_type in ['hidden', 'submit', 'button']:
                        continue
                    
                    # Find matching value
                    value = self.find_field_value(field_name, template_data)
                    
                    if value:
                        # Handle different field types
                        if element.tag_name == 'select':
                            # Select dropdown
                            from selenium.webdriver.support.ui import Select
                            select = Select(element)
                            try:
                                select.select_by_visible_text(value)
                            except:
                                select.select_by_value(value)
                        elif field_type == 'checkbox':
                            if value.lower() in ['true', 'yes', '1']:
                                if not element.is_selected():
                                    element.click()
                        elif field_type == 'radio':
                            if element.get_attribute('value') == value:
                                element.click()
                        else:
                            # Text input
                            element.clear()
                            element.send_keys(value)
                        
                        filled_fields.append(field_name)
                
                except Exception as e:
                    errors.append(f"Error filling {field_name}: {str(e)}")
            
            # Submit if requested
            if submit:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
                    submit_button.click()
                    time.sleep(2)
                except:
                    errors.append("Could not find or click submit button")
            
            result = {
                "success": True,
                "filled_fields": filled_fields,
                "total_fields": len(filled_fields),
                "errors": errors,
                "template_used": template_name,
                "url": url
            }
            
            self.fill_history.append(result)
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fill_desktop_form_pyautogui(self, template_name: str, delay: float = 0.5) -> Dict:
        """Fill desktop form using PyAutoGUI with tab navigation"""
        if not self.pyautogui_available:
            return {
                "success": False,
                "error": "PyAutoGUI not available",
                "help": self.get_missing_dependencies_message(['pyautogui'])
            }
        
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        template_data = self.templates[template_name]
        
        try:
            print(f"Starting form fill in 3 seconds. Click on the first field...")
            time.sleep(3)
            
            filled_count = 0
            
            for field_name, value in template_data.items():
                # Type the value
                pyautogui.write(str(value), interval=0.05)
                time.sleep(delay)
                
                # Tab to next field
                pyautogui.press('tab')
                time.sleep(delay)
                
                filled_count += 1
            
            return {
                "success": True,
                "filled_fields": filled_count,
                "template_used": template_name,
                "method": "desktop_tab_navigation"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fill_form_clipboard(self, template_name: str) -> Dict:
        """Fill form by copying values to clipboard for manual paste"""
        if not self.pyperclip_available:
            return {
                "success": False,
                "error": "Pyperclip not available",
                "help": self.get_missing_dependencies_message(['pyperclip'])
            }
        
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        template_data = self.templates[template_name]
        
        try:
            print("Clipboard Form Filler Active!")
            print("Values will be copied to clipboard. Press Enter to copy next value.")
            print("Press 'q' and Enter to quit.\n")
            
            for field_name, value in template_data.items():
                print(f"\n{field_name}: {value}")
                user_input = input("Press Enter to copy (or 'q' to quit): ")
                
                if user_input.lower() == 'q':
                    break
                
                pyperclip.copy(str(value))
                print("✓ Copied to clipboard! You can now paste it.")
            
            return {
                "success": True,
                "template_used": template_name,
                "method": "clipboard"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def batch_fill_from_csv(self, csv_file: str, url: str, submit: bool = False) -> List[Dict]:
        """Fill multiple forms from CSV data"""
        if not self.pandas_available:
            return [{
                "success": False,
                "error": "Pandas not available",
                "help": self.get_missing_dependencies_message(['pandas'])
            }]
        
        if not self.selenium_available:
            return [{
                "success": False,
                "error": "Selenium not available",
                "help": self.get_missing_dependencies_message(['selenium'])
            }]
        
        results = []
        
        try:
            df = pd.read_csv(csv_file)
            
            for idx, row in df.iterrows():
                # Create temporary template
                row_num = int(idx) if isinstance(idx, (int, float)) else 0
                temp_template = f"batch_temp_{row_num}"
                self.templates[temp_template] = row.to_dict()
                
                # Fill form
                result = self.fill_web_form_selenium(url, temp_template, submit)
                result['row_number'] = row_num + 1
                results.append(result)
                
                # Clean up
                del self.templates[temp_template]
                
                # Delay between forms
                time.sleep(2)
            
            return results
            
        except Exception as e:
            return [{"success": False, "error": str(e)}]
    
    def batch_fill_from_excel(self, excel_file: str, url: str, sheet_name: Any = 0, submit: bool = False) -> List[Dict]:
        """Fill multiple forms from Excel data"""
        if not self.pandas_available:
            return [{
                "success": False,
                "error": "Pandas not available",
                "help": self.get_missing_dependencies_message(['pandas'])
            }]
        
        if not self.selenium_available:
            return [{
                "success": False,
                "error": "Selenium not available",
                "help": self.get_missing_dependencies_message(['selenium'])
            }]
        
        results = []
        
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            for idx, row in df.iterrows():
                # Create temporary template
                row_num = int(idx) if isinstance(idx, (int, float)) else 0
                temp_template = f"batch_temp_{row_num}"
                self.templates[temp_template] = row.to_dict()
                
                # Fill form
                result = self.fill_web_form_selenium(url, temp_template, submit)
                result['row_number'] = row_num + 1
                results.append(result)
                
                # Clean up
                del self.templates[temp_template]
                
                # Delay between forms
                time.sleep(2)
            
            return results
            
        except Exception as e:
            return [{"success": False, "error": str(e)}]
    
    def create_custom_template(self, template_name: str, data: Dict) -> Dict:
        """Create a new custom template"""
        self.templates[template_name] = data
        self.save_templates()
        
        return {
            "success": True,
            "message": f"Template '{template_name}' created successfully",
            "fields": len(data)
        }
    
    def update_template(self, template_name: str, updates: Dict) -> Dict:
        """Update an existing template"""
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        self.templates[template_name].update(updates)
        self.save_templates()
        
        return {
            "success": True,
            "message": f"Template '{template_name}' updated successfully"
        }
    
    def delete_template(self, template_name: str) -> Dict:
        """Delete a template"""
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        del self.templates[template_name]
        self.save_templates()
        
        return {
            "success": True,
            "message": f"Template '{template_name}' deleted successfully"
        }
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.templates.keys())
    
    def get_template(self, template_name: str) -> Optional[Dict]:
        """Get a specific template"""
        return self.templates.get(template_name)
    
    def export_template_to_csv(self, template_name: str, output_file: str) -> Dict:
        """Export template to CSV for batch editing"""
        if not self.pandas_available:
            return {
                "success": False,
                "error": "Pandas not available",
                "help": self.get_missing_dependencies_message(['pandas'])
            }
        
        if template_name not in self.templates:
            return {"success": False, "error": f"Template '{template_name}' not found"}
        
        try:
            df = pd.DataFrame([self.templates[template_name]])
            df.to_csv(output_file, index=False)
            
            return {
                "success": True,
                "message": f"Template exported to {output_file}",
                "file": output_file
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_fill_history(self) -> List[Dict]:
        """Get history of filled forms"""
        return self.fill_history
    
    def close_browser(self):
        """Close Selenium browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None


# CLI interface for testing
if __name__ == "__main__":
    filler = BatchFormFiller()
    
    print("=" * 60)
    print("BATCH FORM FILLER")
    print("=" * 60)
    print(f"\nAvailable templates: {len(filler.list_templates())}")
    for template in filler.list_templates():
        print(f"  - {template}")
    
    print("\nExample usage:")
    print("1. Fill web form: filler.fill_web_form_selenium(url, 'job_application')")
    print("2. Fill desktop form: filler.fill_desktop_form_pyautogui('contact_form')")
    print("3. Clipboard mode: filler.fill_form_clipboard('registration_form')")
    print("4. Batch from CSV: filler.batch_fill_from_csv('data.csv', url)")
