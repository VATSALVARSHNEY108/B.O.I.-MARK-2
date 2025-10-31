## 📧 Email Sending Feature - Complete Guide

## 🎯 What You Can Do

Your project now has **powerful email sending** with these features:

✅ **Simple Text Emails** - Send plain text emails quickly  
✅ **HTML Emails** - Send beautiful formatted emails  
✅ **Email Templates** - Use pre-made professional templates  
✅ **Attachments** - Send files with your emails  
✅ **Multiple Recipients** - Send to multiple people at once  
✅ **CC & BCC** - Carbon copy and blind carbon copy support  
✅ **Contact Integration** - Send to saved contacts by name  

---

## 🚀 Quick Start

### **Super Fast Way:**
```bash
python quick_email.py
```

Enter:
1. Recipient email
2. Subject
3. Message (press Enter twice when done)
4. Optional attachment

Done! Email sent! 📤

---

## 📖 Detailed Usage

### **1. Simple Text Email**

```python
from email_sender import EmailSender

sender = EmailSender()

sender.send_simple_email(
    to="friend@example.com",
    subject="Hello!",
    message="This is a quick message!"
)
```

---

### **2. HTML Email (Pretty Formatting)**

```python
from email_sender import EmailSender

sender = EmailSender()

html_content = """
<html>
<body style="font-family: Arial;">
    <h1 style="color: blue;">Hello!</h1>
    <p>This is a <strong>formatted</strong> email.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>
"""

sender.send_html_email(
    to="friend@example.com",
    subject="Formatted Email",
    html_content=html_content
)
```

---

### **3. Email with Attachment**

```python
from email_sender import EmailSender

sender = EmailSender()

sender.send_email(
    to=["friend@example.com"],
    subject="Report Attached",
    body="Please find the report attached.",
    attachments=["report.pdf", "data.xlsx"]
)
```

---

### **4. Multiple Recipients with CC/BCC**

```python
from email_sender import EmailSender

sender = EmailSender()

sender.send_email(
    to=["person1@example.com", "person2@example.com"],
    subject="Team Update",
    body="Important team announcement!",
    cc=["manager@example.com"],
    bcc=["hr@example.com"]
)
```

---

### **5. Use Email Templates**

```python
from email_sender import EmailSender
from datetime import datetime

sender = EmailSender()

# Welcome email
sender.send_template_email(
    to="newuser@example.com",
    template="welcome",
    name="John",
    message="Thanks for signing up!"
)

# Notification email
sender.send_template_email(
    to="user@example.com",
    template="notification",
    title="Report Ready",
    message="Your monthly report is ready to download!",
    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

# Report email
sender.send_template_email(
    to="manager@example.com",
    template="report",
    title="Monthly Sales Report",
    summary="Sales increased by 25%",
    details="Detailed breakdown: ..."
)

# Invitation email
sender.send_template_email(
    to="guest@example.com",
    template="invitation",
    name="Sarah",
    event="Annual Company Dinner",
    date="December 25, 2025",
    time="7:00 PM",
    location="Grand Hotel",
    message="Dress code: Formal",
    rsvp_date="December 15"
)
```

---

## 🔧 Setup (First Time Only)

### **Step 1: Get Gmail App Password**

1. Go to your **Google Account settings**
2. Click **Security**
3. Enable **2-Step Verification** (if not already)
4. Go to **App passwords**
5. Generate a new app password for "Mail"
6. Copy the 16-character password

### **Step 2: Set Environment Variables**

**Windows (PowerShell):**
```powershell
$env:GMAIL_USER="your.email@gmail.com"
$env:GMAIL_APP_PASSWORD="your-app-password"
```

**Mac/Linux:**
```bash
export GMAIL_USER="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

**Or create a `.env` file:**
```
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

---

## 🎨 Available Templates

### **1. Welcome Template**
```python
sender.send_template_email(
    to="user@example.com",
    template="welcome",
    name="John Doe",
    message="Welcome to our service!"
)
```

### **2. Notification Template**
```python
sender.send_template_email(
    to="user@example.com",
    template="notification",
    title="System Alert",
    message="Your backup is complete!",
    time="2025-10-23 15:30:00"
)
```

### **3. Report Template**
```python
sender.send_template_email(
    to="manager@example.com",
    template="report",
    title="Weekly Analytics",
    summary="All metrics improved this week",
    details="Traffic: +15%, Sales: +20%, Users: +10%"
)
```

### **4. Invitation Template**
```python
sender.send_template_email(
    to="guest@example.com",
    template="invitation",
    name="Alice",
    event="Product Launch Party",
    date="Nov 15, 2025",
    time="6:00 PM",
    location="Tech Hub",
    message="Join us for food and networking!",
    rsvp_date="Nov 10"
)
```

---

## 🤖 Use with AI Assistant

Your AI assistant already knows how to send emails! Just say:

```
"Send email to john@example.com about the meeting"
"Email my boss the report"
"Send this file to sarah@example.com"
```

The AI will automatically use your email system!

---

## 📂 Integration with Contacts

Already have contacts saved? Use them!

```python
from email_sender import EmailSender
from contact_manager import ContactManager

contacts = ContactManager()
sender = EmailSender()

# Add a contact
contacts.add_contact("Mom", email="mom@example.com")

# Send to contact by name (using existing messaging service)
from messaging_service import MessagingService
msg = MessagingService(contacts)

msg.send_email(
    contact_name="Mom",
    subject="Hi Mom!",
    body="Just checking in!"
)
```

---

## 🎯 Use Cases

### **For Business:**
- Send reports to managers
- Send invoices to clients
- Send notifications to team
- Send welcome emails to new users

### **For Personal:**
- Send party invitations
- Share files with friends
- Send updates to family
- Send reminders to yourself

### **For Automation:**
- Automated daily reports
- Error notifications
- Backup completion alerts
- System health reports

---

## ⚡ Quick Commands

### Run the interactive emailer:
```bash
python email_sender.py
```

### Send a quick email:
```bash
python quick_email.py
```

### Use in your code:
```python
from email_sender import create_email_sender

sender = create_email_sender()
sender.send_simple_email("to@example.com", "Subject", "Message")
```

---

## 🐛 Troubleshooting

### **"Demo Mode" appears?**
- You haven't set Gmail credentials
- Set `GMAIL_USER` and `GMAIL_APP_PASSWORD` environment variables

### **"Authentication failed"?**
- Make sure you're using an **App Password**, not your regular Gmail password
- Enable 2-Step Verification in your Google Account first

### **Email not received?**
- Check spam folder
- Verify email address is correct
- Make sure Gmail account is active

### **Attachment not sending?**
- Check file path is correct
- Make sure file exists
- File must be accessible

---

## 📊 Features Summary

| Feature | Simple Email | HTML Email | Template | Full Email |
|---------|--------------|------------|----------|------------|
| Plain Text | ✅ | ✅ | ✅ | ✅ |
| HTML Format | ❌ | ✅ | ✅ | ✅ |
| Attachments | ❌ | ❌ | ❌ | ✅ |
| CC/BCC | ❌ | ❌ | ❌ | ✅ |
| Multiple Recipients | ❌ | ❌ | ❌ | ✅ |
| Templates | ❌ | ❌ | ✅ | ❌ |

---

## 🔐 Security Notes

- Never commit your Gmail password to git
- Use environment variables or .env file
- Use App Passwords, not your main password
- Add `.env` to your `.gitignore`

---

## 🚀 Ready to Send!

**Quick test:**
```bash
python quick_email.py
```

**With code:**
```python
from email_sender import create_email_sender

sender = create_email_sender()
result = sender.send_simple_email(
    "friend@example.com",
    "Test Email",
    "This is my first automated email!"
)
print(result['message'])
```

Happy emailing! 📧
