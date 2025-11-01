"""
Letter Templates Module
Provides instant letter generation with customizable variables
"""

from datetime import datetime

LETTER_TEMPLATES = {
    "leave": {
        "name": "Leave Application Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "leave_days", "leave_reason", "start_date", "end_date"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Application for Leave

Respected {recipient_title},

I am writing to request leave from {start_date} to {end_date} ({leave_days} days) due to {leave_reason}.

I will ensure that all my pending work is completed before my leave, and I will be available for any urgent matters via phone or email if needed.

I kindly request you to grant me leave for the mentioned period. I will be grateful for your approval.

Thank you for your understanding and consideration.

Yours sincerely,
{sender_name}"""
    },
    
    "complaint": {
        "name": "Complaint Letter",
        "variables": ["sender_name", "sender_address", "recipient_name", "recipient_title", "organization", "complaint_about", "issue_details", "expected_resolution"],
        "template": """Date: {date}

{sender_name}
{sender_address}

{recipient_name}
{recipient_title}
{organization}

Subject: Complaint Regarding {complaint_about}

Dear {recipient_title},

I am writing to bring to your attention a matter that requires immediate resolution regarding {complaint_about}.

{issue_details}

I would appreciate it if you could look into this matter and {expected_resolution}. I believe that a prompt response will help resolve this issue amicably.

I look forward to hearing from you soon and hope for a satisfactory resolution to this problem.

Thank you for your attention to this matter.

Sincerely,
{sender_name}"""
    },
    
    "appreciation": {
        "name": "Appreciation Letter",
        "variables": ["sender_name", "recipient_name", "appreciation_for", "specific_achievements", "impact"],
        "template": """Date: {date}

Dear {recipient_name},

I am writing to express my sincere appreciation for {appreciation_for}.

{specific_achievements}

Your dedication and efforts have made a significant impact: {impact}

Thank you once again for your outstanding contribution. Your work is truly valued and appreciated.

With warm regards,
{sender_name}"""
    },
    
    "recommendation": {
        "name": "Recommendation Letter",
        "variables": ["sender_name", "sender_title", "sender_organization", "candidate_name", "position_applied", "relationship_duration", "key_skills", "achievements", "recommendation_statement"],
        "template": """Date: {date}

To Whom It May Concern,

I am writing to provide my highest recommendation for {candidate_name} for the position of {position_applied}.

I have known {candidate_name} for {relationship_duration} in my capacity as {sender_title} at {sender_organization}. During this time, I have been consistently impressed by their performance and character.

Key Skills and Qualities:
{key_skills}

Notable Achievements:
{achievements}

{recommendation_statement}

I am confident that {candidate_name} will be an excellent addition to your organization and will bring the same level of dedication and excellence that they have demonstrated while working with us.

Please feel free to contact me if you need any additional information.

Sincerely,
{sender_name}
{sender_title}
{sender_organization}"""
    },
    
    "resignation": {
        "name": "Resignation Letter",
        "variables": ["sender_name", "position", "recipient_name", "recipient_title", "organization", "last_working_day", "reason", "gratitude_message"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Resignation from the Position of {position}

Dear {recipient_title},

I am writing to formally notify you of my resignation from the position of {position} at {organization}. My last working day will be {last_working_day}.

{reason}

I want to express my sincere gratitude for the opportunities I have been given during my time here. {gratitude_message}

I am committed to ensuring a smooth transition and will do everything possible to complete my current projects and assist in training my replacement.

Thank you once again for the opportunity to be part of this organization.

Yours sincerely,
{sender_name}"""
    },
    
    "invitation": {
        "name": "Invitation Letter",
        "variables": ["sender_name", "event_name", "event_date", "event_time", "event_location", "event_purpose", "recipient_name", "rsvp_details"],
        "template": """Date: {date}

Dear {recipient_name},

It is my pleasure to invite you to {event_name}.

Event Details:
Date: {event_date}
Time: {event_time}
Location: {event_location}

Purpose: {event_purpose}

We would be honored by your presence at this event. Your attendance would mean a great deal to us.

{rsvp_details}

We look forward to seeing you there.

Warm regards,
{sender_name}"""
    },
    
    "apology": {
        "name": "Apology Letter",
        "variables": ["sender_name", "recipient_name", "what_happened", "impact", "corrective_actions", "commitment"],
        "template": """Date: {date}

Dear {recipient_name},

I am writing to sincerely apologize for {what_happened}.

I understand that this has {impact}, and I take full responsibility for my actions/oversight.

To rectify this situation, I have taken the following steps:
{corrective_actions}

{commitment}

I hope you can accept my sincere apology, and I am committed to ensuring that such incidents do not occur in the future.

Sincerely,
{sender_name}"""
    },
    
    "job_application": {
        "name": "Job Application Letter",
        "variables": ["sender_name", "sender_address", "sender_phone", "sender_email", "recipient_name", "recipient_title", "organization", "position", "qualifications", "experience", "why_interested"],
        "template": """Date: {date}

{sender_name}
{sender_address}
Phone: {sender_phone}
Email: {sender_email}

{recipient_name}
{recipient_title}
{organization}

Subject: Application for the Position of {position}

Dear {recipient_title},

I am writing to express my interest in the {position} position at {organization}. I believe my qualifications and experience make me an ideal candidate for this role.

Qualifications:
{qualifications}

Experience:
{experience}

Why I am interested:
{why_interested}

I have attached my resume for your review. I would welcome the opportunity to discuss how my skills and experiences align with your needs.

Thank you for considering my application. I look forward to the opportunity to speak with you.

Sincerely,
{sender_name}"""
    },
    
    "thank_you": {
        "name": "Thank You Letter",
        "variables": ["sender_name", "recipient_name", "occasion", "what_received", "how_it_helped", "closing_sentiment"],
        "template": """Date: {date}

Dear {recipient_name},

I wanted to take a moment to express my heartfelt thanks for {occasion}.

{what_received}

{how_it_helped}

{closing_sentiment}

Once again, thank you for your kindness and generosity.

With sincere gratitude,
{sender_name}"""
    },
    
    "permission": {
        "name": "Permission Request Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "permission_for", "reason", "duration", "benefits"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Request for Permission - {permission_for}

Respected {recipient_title},

I am writing to request your permission for {permission_for}.

Reason: {reason}

Duration: {duration}

Benefits: {benefits}

I assure you that I will adhere to all guidelines and regulations associated with this request. Your approval would be greatly appreciated.

Thank you for your time and consideration.

Respectfully,
{sender_name}"""
    },
    
    "inquiry": {
        "name": "Inquiry Letter",
        "variables": ["sender_name", "sender_organization", "recipient_name", "organization", "inquiry_about", "specific_questions", "purpose", "deadline"],
        "template": """Date: {date}

{sender_name}
{sender_organization}

{recipient_name}
{organization}

Subject: Inquiry Regarding {inquiry_about}

Dear {recipient_name},

I am writing on behalf of {sender_organization} to inquire about {inquiry_about}.

Purpose: {purpose}

Specific Questions:
{specific_questions}

{deadline}

I would greatly appreciate your response at your earliest convenience. Please feel free to contact me if you need any additional information.

Thank you for your assistance.

Best regards,
{sender_name}
{sender_organization}"""
    },
    
    "reference": {
        "name": "Reference Request Letter",
        "variables": ["sender_name", "recipient_name", "relationship", "position_applying", "deadline", "why_chosen", "contact_info"],
        "template": """Date: {date}

Dear {recipient_name},

I hope this letter finds you well. I am reaching out to ask if you would be willing to serve as a reference for me as I apply for {position_applying}.

{relationship}

{why_chosen}

The deadline for the reference is {deadline}. The potential employer may contact you at: {contact_info}

I would be happy to provide you with any additional information you might need. Thank you for considering my request.

Warm regards,
{sender_name}"""
    },
    
    "formal_general": {
        "name": "General Formal Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "subject", "opening", "main_content", "closing"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: {subject}

Dear {recipient_title},

{opening}

{main_content}

{closing}

Thank you for your attention to this matter.

Sincerely,
{sender_name}"""
    }
}

DEFAULT_VALUES = {
    "sender_name": "Your Name",
    "recipient_name": "Recipient Name",
    "recipient_title": "Sir/Madam",
    "organization": "Organization Name",
    "date": datetime.now().strftime("%B %d, %Y"),
    "leave_days": "2",
    "leave_reason": "personal reasons",
    "start_date": "specify start date",
    "end_date": "specify end date",
    "sender_address": "Your Address",
    "complaint_about": "the issue",
    "issue_details": "Please provide detailed information about the issue.",
    "expected_resolution": "take appropriate action",
    "appreciation_for": "your excellent work",
    "specific_achievements": "Your recent contributions have been outstanding.",
    "impact": "Your efforts have positively influenced our team and results.",
    "sender_title": "Your Title",
    "sender_organization": "Your Organization",
    "candidate_name": "Candidate Name",
    "position_applied": "Position Title",
    "relationship_duration": "duration of relationship",
    "key_skills": "- Skill 1\n- Skill 2\n- Skill 3",
    "achievements": "- Achievement 1\n- Achievement 2",
    "recommendation_statement": "I strongly recommend this candidate without reservation.",
    "position": "Your Position",
    "last_working_day": "specify last working day",
    "reason": "I have accepted a new opportunity that aligns with my career goals.",
    "gratitude_message": "I have learned and grown tremendously during my tenure here.",
    "event_name": "Event Name",
    "event_date": "Event Date",
    "event_time": "Event Time",
    "event_location": "Event Location",
    "event_purpose": "Purpose of the event",
    "rsvp_details": "Please RSVP by [date] to [contact].",
    "what_happened": "the situation that occurred",
    "corrective_actions": "- Action 1\n- Action 2",
    "commitment": "I am committed to preventing similar issues in the future.",
    "sender_phone": "Your Phone Number",
    "sender_email": "your.email@example.com",
    "qualifications": "Your relevant qualifications",
    "experience": "Your relevant experience",
    "why_interested": "Your interest in the position and company",
    "occasion": "your kindness",
    "what_received": "The gift/help you provided was wonderful.",
    "how_it_helped": "It has made a significant positive difference.",
    "closing_sentiment": "Your thoughtfulness is deeply appreciated.",
    "permission_for": "activity or event",
    "duration": "specify duration",
    "benefits": "This will benefit both parties involved.",
    "inquiry_about": "product/service/information",
    "specific_questions": "1. Question 1\n2. Question 2",
    "purpose": "The purpose of this inquiry",
    "deadline": "Please respond by [date] if possible.",
    "relationship": "I have known you through [context] for [duration].",
    "position_applying": "position title",
    "why_chosen": "I believe you would provide an excellent reference given your knowledge of my work.",
    "contact_info": "your contact information",
    "subject": "Subject of the Letter",
    "opening": "I am writing to discuss an important matter.",
    "main_content": "Main content of your letter goes here.",
    "closing": "I appreciate your time and consideration."
}


def detect_letter_type(description: str) -> str:
    """Detect letter type from user description"""
    description_lower = description.lower()
    
    letter_keywords = {
        "leave": ["leave", "holiday", "vacation", "absent", "time off"],
        "complaint": ["complaint", "complain", "issue", "problem"],
        "appreciation": ["appreciation", "thank", "appreciate", "gratitude"],
        "recommendation": ["recommendation", "recommend", "reference letter"],
        "resignation": ["resignation", "resign", "quit", "leaving job"],
        "invitation": ["invitation", "invite", "event"],
        "apology": ["apology", "apologize", "sorry", "regret"],
        "job_application": ["job application", "apply", "applying for"],
        "thank_you": ["thank you", "thanks"],
        "permission": ["permission", "request permission", "allow"],
        "inquiry": ["inquiry", "inquire", "ask about", "question about"],
        "reference": ["reference request", "asking for reference"],
        "formal_general": ["formal letter", "general letter"]
    }
    
    for letter_type, keywords in letter_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            return letter_type
    
    return "formal_general"


def extract_custom_values(description: str) -> dict:
    """Extract custom values from user's natural language description"""
    custom_values = {}
    description_lower = description.lower()
    
    # Extract recipient title
    if "principal" in description_lower:
        custom_values["recipient_title"] = "Principal"
        custom_values["recipient_name"] = "Principal"
    elif "manager" in description_lower:
        custom_values["recipient_title"] = "Manager"
        custom_values["recipient_name"] = "Manager"
    elif "boss" in description_lower:
        custom_values["recipient_title"] = "Sir/Madam"
        custom_values["recipient_name"] = "Boss"
    elif "teacher" in description_lower:
        custom_values["recipient_title"] = "Teacher"
        custom_values["recipient_name"] = "Teacher"
    
    # Extract duration for leave
    import re
    days_match = re.search(r'(\d+)\s*days?', description_lower)
    if days_match:
        custom_values["leave_days"] = days_match.group(1)
    
    # Extract reason for leave
    if "sick" in description_lower:
        custom_values["leave_reason"] = "health reasons / sickness"
    elif "family" in description_lower:
        custom_values["leave_reason"] = "family emergency"
    elif "personal" in description_lower:
        custom_values["leave_reason"] = "personal reasons"
    elif "wedding" in description_lower:
        custom_values["leave_reason"] = "attending a wedding"
    elif "medical" in description_lower:
        custom_values["leave_reason"] = "medical appointment"
    
    return custom_values


def generate_letter(description: str, custom_values: dict = None) -> dict:
    """
    Generate a letter based on description
    
    Args:
        description: Natural language description of the letter needed
        custom_values: Dictionary of custom values to override defaults
    
    Returns:
        dict with letter content and metadata
    """
    letter_type = detect_letter_type(description)
    
    if letter_type not in LETTER_TEMPLATES:
        return {
            "success": False,
            "error": f"Letter type '{letter_type}' not found"
        }
    
    template_info = LETTER_TEMPLATES[letter_type]
    
    # Start with default values
    values = DEFAULT_VALUES.copy()
    
    # Extract values from description
    extracted_values = extract_custom_values(description)
    values.update(extracted_values)
    
    # Apply custom values if provided
    if custom_values:
        values.update(custom_values)
    
    # Generate the letter
    try:
        letter_content = template_info["template"].format(**values)
        
        return {
            "success": True,
            "letter": letter_content,
            "letter_type": letter_type,
            "letter_name": template_info["name"],
            "variables_used": template_info["variables"],
            "values": values,
            "description": description
        }
    except KeyError as e:
        return {
            "success": False,
            "error": f"Missing variable: {str(e)}"
        }


def list_letter_types():
    """List all available letter types"""
    return {
        letter_type: info["name"] 
        for letter_type, info in LETTER_TEMPLATES.items()
    }


def get_letter_variables(letter_type: str) -> list:
    """Get required variables for a specific letter type"""
    if letter_type in LETTER_TEMPLATES:
        return LETTER_TEMPLATES[letter_type]["variables"]
    return []


def show_letter_preview(letter_type: str) -> str:
    """Show a preview of a letter type with default values"""
    if letter_type not in LETTER_TEMPLATES:
        return f"Letter type '{letter_type}' not found"
    
    template_info = LETTER_TEMPLATES[letter_type]
    preview = template_info["template"].format(**DEFAULT_VALUES)
    
    return f"=== {template_info['name']} Preview ===\n\n{preview}"


if __name__ == "__main__":
    # Test the letter generator
    print("Available Letter Types:")
    for lt, name in list_letter_types().items():
        print(f"  - {lt}: {name}")
    
    print("\n" + "="*60)
    print("Test: Generate a leave letter")
    print("="*60)
    
    result = generate_letter("write a letter to principal for 2 days leave")
    if result["success"]:
        print(result["letter"])
        print(f"\n✅ Letter type detected: {result['letter_type']}")
