"""
Demo: Batch Form Filler System
Demonstrates all batch form filling capabilities
"""

import sys
import os
from modules.automation.batch_form_filler import BatchFormFiller


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_list_templates():
    """Demo: List all available templates"""
    print_header("AVAILABLE FORM TEMPLATES")
    
    filler = BatchFormFiller()
    
    # Show dependency status
    deps = filler.check_dependencies()
    print("\nDependency Status:")
    print(f"  • Selenium (web forms):    {'✓ Available' if deps['selenium'] else '✗ Not Available'}")
    print(f"  • PyAutoGUI (desktop):     {'✓ Available' if deps['pyautogui'] else '✗ Not Available'}")
    print(f"  • Pyperclip (clipboard):   {'✓ Available' if deps['pyperclip'] else '✗ Not Available'}")
    print(f"  • Pandas (batch CSV/Excel): {'✓ Available' if deps['pandas'] else '✗ Not Available'}")
    
    templates = filler.list_templates()
    
    print(f"\nTotal templates: {len(templates)}\n")
    
    for i, template_name in enumerate(templates, 1):
        template = filler.get_template(template_name)
        fields_count = len(template) if template else 0
        print(f"{i:2}. {template_name:<25} ({fields_count} fields)")
    
    return filler


def demo_view_template(filler, template_name):
    """Demo: View template details"""
    print_header(f"TEMPLATE: {template_name.upper()}")
    
    template = filler.get_template(template_name)
    
    if not template:
        print(f"❌ Template '{template_name}' not found!")
        return
    
    print(f"\nFields ({len(template)}):\n")
    
    for field, value in template.items():
        print(f"  • {field:<25} = {value}")


def demo_desktop_form_filling(filler):
    """Demo: Desktop form filling with tab navigation"""
    print_header("DESKTOP FORM FILLING (PyAutoGUI)")
    
    print("""
This mode fills desktop forms using keyboard automation:
1. Click on the first form field
2. The system will type each value and press Tab to move to next field
3. Works with any desktop application (PDF forms, desktop apps, etc.)

Example templates:
  • contact_form       - Simple contact forms
  • job_application    - Job applications  
  • registration_form  - User registration
  • survey_form        - Surveys and feedback
    """)
    
    print("\nExample command:")
    print("  filler.fill_desktop_form_pyautogui('contact_form', delay=0.5)")


def demo_clipboard_filling(filler):
    """Demo: Clipboard-based form filling"""
    print_header("CLIPBOARD FORM FILLING")
    
    print("""
This mode copies values to clipboard for manual pasting:
1. Each field value is displayed
2. Press Enter to copy it to clipboard
3. Paste it into the form manually
4. Great for secure forms or complex layouts

Example templates:
  • medical_form       - Medical/health forms
  • banking_form       - Banking applications
  • insurance_quote    - Insurance forms
    """)
    
    print("\nExample command:")
    print("  filler.fill_form_clipboard('medical_form')")


def demo_web_form_selenium(filler):
    """Demo: Web form filling with Selenium"""
    print_header("WEB FORM FILLING (Selenium)")
    
    print("""
This mode automatically fills web forms using intelligent field detection:
1. Opens the URL in a browser
2. Detects all input fields (text, email, phone, etc.)
3. Matches fields with template data using smart matching
4. Fills values automatically
5. Optionally submits the form

Smart field matching examples:
  • 'email', 'e-mail', 'user_email' → email field
  • 'fname', 'first_name', 'given_name' → first_name field
  • 'phone', 'mobile', 'telephone' → phone field

Example templates:
  • contact_form           - Contact forms
  • registration_form      - User registration
  • subscription_form      - Newsletter/subscription
  • event_registration     - Event signups
    """)
    
    print("\nExample command:")
    print("  filler.fill_web_form_selenium('https://example.com/contact', 'contact_form', submit=False)")


def demo_batch_csv_filling(filler):
    """Demo: Batch filling from CSV"""
    print_header("BATCH FILLING FROM CSV")
    
    print("""
This mode fills multiple forms using data from a CSV file:
1. Reads CSV file with multiple rows of data
2. Each row becomes a form submission
3. Automatically fills and submits forms
4. Returns detailed results for each submission

CSV Example (data/batch_form_example.csv):
  first_name,last_name,email,phone,company,message
  John,Doe,john@example.com,+1-555-0001,TechCo,Hello...
  Jane,Smith,jane@example.com,+1-555-0002,DevCorp,Hi...
  
Use cases:
  • Bulk job applications
  • Multiple event registrations
  • Mass contact form submissions
  • Lead generation forms
    """)
    
    print("\nExample command:")
    print("  results = filler.batch_fill_from_csv('data/batch_form_example.csv', 'https://example.com/contact', submit=True)")


def demo_batch_excel_filling(filler):
    """Demo: Batch filling from Excel"""
    print_header("BATCH FILLING FROM EXCEL")
    
    print("""
This mode fills multiple forms using data from Excel files:
1. Reads Excel file (.xlsx, .xls)
2. Supports multiple sheets
3. Each row becomes a form submission
4. Ideal for organized data with multiple sheets

Use cases:
  • Job applications with resume data
  • Educational applications
  • Medical form submissions
  • Insurance quotes
    """)
    
    print("\nExample command:")
    print("  results = filler.batch_fill_from_excel('applications.xlsx', 'https://example.com/apply', sheet_name='Sheet1', submit=True)")


def demo_custom_template_creation(filler):
    """Demo: Creating custom templates"""
    print_header("CUSTOM TEMPLATE CREATION")
    
    print("""
Create your own custom templates for specific forms:

1. Create new template:
   data = {
       'company_name': 'My Company',
       'contact_person': 'John Doe',
       'email': 'john@mycompany.com',
       'industry': 'Technology',
       'employees': '50-100'
   }
   filler.create_custom_template('my_b2b_form', data)

2. Update existing template:
   filler.update_template('job_application', {
       'salary_expectation': '$120,000',
       'years_experience': '8'
   })

3. Export template to CSV for batch editing:
   filler.export_template_to_csv('job_application', 'template.csv')
   # Edit in Excel, then import back for batch filling
    """)


def demo_template_categories():
    """Demo: Show template categories"""
    print_header("TEMPLATE CATEGORIES")
    
    categories = {
        "Professional": [
            "job_application - Complete job application with resume details",
            "contact_form - Business contact/inquiry forms",
            "subscription_form - Newsletter and service subscriptions"
        ],
        "Personal": [
            "registration_form - User registration with account details",
            "survey_form - Surveys and feedback forms",
            "event_registration - Event tickets and registrations",
            "volunteer_form - Volunteer applications"
        ],
        "Financial": [
            "banking_form - Bank account applications",
            "billing_info - Payment and billing information",
            "insurance_quote - Insurance quote requests"
        ],
        "E-commerce": [
            "shipping_address - Delivery address forms",
            "billing_info - Payment information"
        ],
        "Healthcare": [
            "medical_form - Medical intake and patient forms"
        ],
        "Real Estate": [
            "rental_application - Rental/lease applications"
        ],
        "Education": [
            "educational_application - College/university applications"
        ],
        "Feedback": [
            "feedback_form - Product/service feedback",
            "newsletter_signup - Email newsletter signups"
        ]
    }
    
    for category, templates in categories.items():
        print(f"\n📁 {category}")
        for template in templates:
            print(f"   • {template}")


def interactive_demo():
    """Interactive demo menu"""
    filler = demo_list_templates()
    
    while True:
        print("\n" + "=" * 70)
        print("  BATCH FORM FILLER - INTERACTIVE DEMO")
        print("=" * 70)
        print("\n1. List all templates")
        print("2. View template details")
        print("3. Show template categories")
        print("4. Desktop form filling info")
        print("5. Clipboard filling info")
        print("6. Web form filling info")
        print("7. Batch CSV filling info")
        print("8. Batch Excel filling info")
        print("9. Custom template info")
        print("0. Exit")
        
        choice = input("\nSelect option (0-9): ").strip()
        
        if choice == '0':
            print("\n✅ Demo completed!")
            break
        elif choice == '1':
            filler = demo_list_templates()
        elif choice == '2':
            template_name = input("Enter template name: ").strip()
            demo_view_template(filler, template_name)
        elif choice == '3':
            demo_template_categories()
        elif choice == '4':
            demo_desktop_form_filling(filler)
        elif choice == '5':
            demo_clipboard_filling(filler)
        elif choice == '6':
            demo_web_form_selenium(filler)
        elif choice == '7':
            demo_batch_csv_filling(filler)
        elif choice == '8':
            demo_batch_excel_filling(filler)
        elif choice == '9':
            demo_custom_template_creation(filler)
        else:
            print("❌ Invalid option!")


def quick_reference():
    """Print quick reference guide"""
    print_header("QUICK REFERENCE GUIDE")
    
    print("""
INITIALIZATION:
  from modules.automation.batch_form_filler import BatchFormFiller
  filler = BatchFormFiller()

BASIC OPERATIONS:
  # List templates
  templates = filler.list_templates()
  
  # Get template
  data = filler.get_template('job_application')
  
  # Fill web form
  result = filler.fill_web_form_selenium(url, 'contact_form', submit=False)
  
  # Fill desktop form
  result = filler.fill_desktop_form_pyautogui('registration_form', delay=0.5)
  
  # Clipboard mode
  result = filler.fill_form_clipboard('medical_form')

BATCH OPERATIONS:
  # From CSV
  results = filler.batch_fill_from_csv('data.csv', url, submit=True)
  
  # From Excel
  results = filler.batch_fill_from_excel('data.xlsx', url, sheet_name=0)

TEMPLATE MANAGEMENT:
  # Create template
  filler.create_custom_template('my_form', {'field1': 'value1'})
  
  # Update template
  filler.update_template('job_application', {'company': 'New Corp'})
  
  # Export to CSV
  filler.export_template_to_csv('job_application', 'output.csv')
  
  # Delete template
  filler.delete_template('my_form')

CLEANUP:
  # Close browser
  filler.close_browser()
    """)


if __name__ == "__main__":
    print("\n🚀 BATCH FORM FILLER SYSTEM DEMO")
    print("=" * 70)
    
    # Check dependencies first
    from modules.automation.batch_form_filler import BatchFormFiller
    filler = BatchFormFiller()
    deps = filler.check_dependencies()
    
    print("\n📦 Checking Dependencies...")
    all_available = all(deps.values())
    
    if not all_available:
        print("\n⚠️  Some dependencies are missing:")
        for dep, available in deps.items():
            status = "✓" if available else "✗"
            print(f"  {status} {dep}")
        
        print("\n💡 Core templates work without dependencies!")
        print("   Web/batch features require Selenium + WebDriver setup.")
        print("   For Replit, clipboard mode is recommended.\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reference':
        quick_reference()
    else:
        interactive_demo()
