# Letter Writing Feature

## Overview
The VATSAL AI Assistant now includes an intelligent letter writing feature that can generate various types of formal and informal letters based on natural language commands.

## Features

### 13 Letter Types Available

1. **Leave Application** - For requesting time off
2. **Complaint Letter** - For filing complaints
3. **Appreciation Letter** - For expressing gratitude
4. **Recommendation Letter** - For recommending someone
5. **Resignation Letter** - For resigning from a position
6. **Invitation Letter** - For inviting someone to an event
7. **Apology Letter** - For apologizing
8. **Job Application** - For applying to jobs
9. **Thank You Letter** - For thanking someone
10. **Permission Request** - For requesting permission
11. **Inquiry Letter** - For making inquiries
12. **Reference Request** - For requesting references
13. **General Formal Letter** - For any formal communication

## How to Use

### Voice Commands

Simply say any of these commands to your VATSAL assistant:

```
"Write a letter to principal for 2 days holiday"
"Write a complaint letter"
"Write a resignation letter"
"Write a thank you letter"
"Write an invitation letter"
"Write a job application letter"
```

### Natural Language Detection

The system automatically detects:
- **Letter type** from keywords (leave, complaint, invitation, etc.)
- **Recipient** from context (principal, manager, boss, teacher)
- **Duration** for leave requests (2 days, 3 days, etc.)
- **Reason** for leave (sick, family, personal, medical, wedding)

### Examples

#### Example 1: Simple Leave Letter
**Command:** "Write a letter to principal for 2 days leave"

**Result:** 
- Detects: Leave letter type
- Recipient: Principal
- Duration: 2 days
- Generates complete formal letter

#### Example 2: Sick Leave
**Command:** "Write a letter to manager for 3 days sick leave"

**Result:**
- Detects: Leave letter type
- Recipient: Manager
- Duration: 3 days
- Reason: Sick/health reasons
- Generates appropriate letter

#### Example 3: Custom Values (Advanced)
```python
custom_values = {
    "sender_name": "Vatsal Varshney",
    "recipient_name": "Mr. Sharma",
    "recipient_title": "Principal",
    "organization": "ABC School",
    "leave_days": "3",
    "leave_reason": "family wedding",
    "start_date": "November 5, 2025",
    "end_date": "November 7, 2025"
}

result = generate_letter("write a leave letter", custom_values=custom_values)
```

## Customizable Variables

Each letter type has specific variables that can be customized:

### Leave Letter Variables
- sender_name
- recipient_name
- recipient_title
- organization
- leave_days
- leave_reason
- start_date
- end_date

### Complaint Letter Variables
- sender_name
- sender_address
- recipient_name
- complaint_about
- issue_details
- expected_resolution

### Job Application Variables
- sender_name
- sender_address
- sender_phone
- sender_email
- position
- qualifications
- experience
- why_interested

(See letter_templates.py for complete list of variables for each letter type)

## Integration with VATSAL

The letter writing feature is fully integrated with:
- **Voice commands** - Say what you want
- **Code generator** - Automatically detects letter requests
- **Notepad integration** - Writes directly to Notepad
- **AI fallback** - Uses Gemini AI for complex requests

## Default Behavior

When you don't specify details, the system uses intelligent defaults:
- Current date is automatically filled
- Polite, professional language
- Standard formal letter format
- Placeholder text for missing information

## Output

Letters are generated in plain text format (.txt) and can be:
- Written directly to Notepad
- Saved to a file
- Copied to clipboard
- Used in further processing

## Benefits

✅ **Instant Generation** - No API calls needed for standard letters
✅ **Variety** - 13 different letter types
✅ **Customizable** - All variables can be changed
✅ **Natural Language** - Just speak what you need
✅ **Professional** - Proper formatting and language
✅ **Time-Saving** - No need to remember letter formats

## Technical Details

### Module Structure
```
modules/ai_features/
  ├── letter_templates.py    # Letter templates and generation
  └── code_generator.py      # Integration with code generation
```

### Key Functions
- `generate_letter(description, custom_values)` - Generate a letter
- `detect_letter_type(description)` - Detect letter type from description
- `list_letter_types()` - List all available letter types
- `get_letter_variables(letter_type)` - Get variables for a letter type

### Testing
Run the test suite:
```bash
python tests/test_letter_generator.py
```

## Future Enhancements

Potential improvements:
- More letter types
- Multi-language support
- Email integration
- PDF generation
- Letter history/templates
- Voice-to-variable extraction
