# WhatsApp Batch Automation Guide

Complete guide to using the WhatsApp Batch Automation System for sending messages to multiple contacts.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Batch File Interface](#batch-file-interface)
- [Python CLI](#python-cli)
- [CSV File Format](#csv-file-format)
- [Message Templates](#message-templates)
- [Batch Operations](#batch-operations)
- [Logging & Tracking](#logging--tracking)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## Overview

The WhatsApp Batch Automation System allows you to send WhatsApp messages to multiple contacts from CSV files with support for:
- **Batch messaging** - Send to hundreds of contacts from a CSV file
- **Templated messages** - Personalize messages with dynamic placeholders
- **Batch image sending** - Send images to multiple contacts
- **Progress tracking** - Monitor sending progress in real-time
- **Logging** - Track all sent messages with timestamps and status
- **Error handling** - Continue on errors or stop on first failure

---

## Features

### ✅ Batch Messaging
- Send messages to multiple contacts from CSV files
- Support for hundreds of contacts per batch
- Automatic rate limiting (configurable delay between messages)

### 📝 Message Templates
- Use `{placeholders}` in messages that map to CSV columns
- Personalize each message automatically
- Support for unlimited custom fields

### 🖼️ Batch Image Sending
- Send same image to multiple contacts
- Support for personalized captions using templates
- JPG image format supported

### 📊 Progress Tracking
- Real-time progress display during batch operations
- Current contact counter (e.g., [5/100])
- Message preview for each contact

### 📋 Logging & History
- All sent messages logged with timestamps
- Success/failure tracking
- View recent batch logs
- JSON-based log storage in `data/whatsapp_batch_log.json`

### ⚙️ Configurable Settings
- Adjustable delay between messages (default: 20-25 seconds)
- Skip errors or stop on first failure
- Custom CSV templates for different use cases

---

## Getting Started

### Prerequisites
1. **WhatsApp Web** must be logged in on your default browser
2. **Python 3.x** installed
3. **pywhatkit** library installed (already included)

### Quick Start (3 Steps)

#### Step 1: Create a CSV Template
```batch
# Run the batch automation menu
batch_scripts\automation\whatsapp_batch_automation.bat

# Select option 4: Create CSV Template
# Choose template type (basic, personalized, or image)
# Save to data folder
```

#### Step 2: Edit Your CSV File
Open the created CSV file in Excel or any text editor and add:
- Phone numbers (with country code: +1234567890)
- Contact names
- Messages or custom fields

#### Step 3: Send Batch Messages
```batch
# Run the batch automation menu again
batch_scripts\automation\whatsapp_batch_automation.bat

# Select option 1 or 2
# Follow the prompts
```

---

## Batch File Interface

### Main Menu

Run: `batch_scripts\automation\whatsapp_batch_automation.bat`

```
================================================================
            📱 WHATSAPP BATCH AUTOMATION SYSTEM              
================================================================

  BATCH OPERATIONS:
  1. Send Batch Messages from CSV
  2. Send Batch Messages with Template
  3. Send Batch Images
  4. Create CSV Template

  MANAGEMENT:
  5. View Batch Logs
  6. View Available Templates
  7. Open Data Folder

  HELP:
  8. Quick Start Guide
  9. View Example Templates
  0. Exit
```

### Menu Options Explained

#### Option 1: Send Batch Messages from CSV
- **Use when**: Your CSV file has a "message" column with the full message text
- **CSV format**: `phone,name,message`
- **Example**: Each contact gets their specific message from the CSV

#### Option 2: Send Batch Messages with Template
- **Use when**: You want to personalize messages using a template
- **CSV format**: `phone,name,[custom columns]`
- **Example**: Template "Hi {name}, order {order_id} ready!" + CSV with name and order_id columns

#### Option 3: Send Batch Images
- **Use when**: You want to send the same image to multiple contacts
- **CSV format**: `phone,name,caption` (caption optional)
- **Supports**: JPG images with optional personalized captions

#### Option 4: Create CSV Template
- **Creates**: Sample CSV files with proper format
- **Types**: Basic, Personalized, or Image templates
- **Location**: Saves to `data/` folder

#### Option 5: View Batch Logs
- **Shows**: Recent batch messaging history
- **Details**: Timestamp, recipient, message, success/failure status
- **Limit**: Configurable number of logs to display

---

## Python CLI

For advanced users and automation scripts.

### Send Batch Messages

```bash
# Basic batch send
python scripts/whatsapp_batch.py send data/contacts.csv

# With template
python scripts/whatsapp_batch.py send data/contacts.csv --template "Hi {name}, order {order_id} ready!"

# With custom delay
python scripts/whatsapp_batch.py send data/contacts.csv --delay 30

# Stop on first error
python scripts/whatsapp_batch.py send data/contacts.csv --no-skip
```

### Send Batch Images

```bash
# Basic image send
python scripts/whatsapp_batch.py image data/contacts.csv path/to/image.jpg

# With caption template
python scripts/whatsapp_batch.py image data/contacts.csv image.jpg --caption "Hi {name}! Check this out!"

# With custom delay
python scripts/whatsapp_batch.py image data/contacts.csv image.jpg --delay 30
```

### Create CSV Template

```bash
# Create basic template
python scripts/whatsapp_batch.py create-template data/my_contacts.csv

# Create personalized template
python scripts/whatsapp_batch.py create-template data/customers.csv --type personalized

# Create image template
python scripts/whatsapp_batch.py create-template data/image_list.csv --type image
```

### View Logs

```bash
# View last 20 logs
python scripts/whatsapp_batch.py logs

# View last 50 logs
python scripts/whatsapp_batch.py logs --limit 50
```

---

## CSV File Format

### Basic Format (With Messages)
```csv
phone,name,message
+1234567890,John Doe,Hello John! How are you?
+0987654321,Jane Smith,Hi Jane! Thanks for your order.
```

### Personalized Format (Template-Based)
```csv
phone,name,order_id,amount,delivery_date
+1234567890,John Doe,ORD-1001,$50,2025-11-25
+0987654321,Jane Smith,ORD-1002,$75,2025-11-26
```

Use with template: `Hi {name}, order #{order_id} for {amount} will arrive on {delivery_date}!`

### Image Format
```csv
phone,name,caption
+1234567890,John Doe,Hi John! Exclusive offer for you!
+0987654321,Jane Smith,Hi Jane! Thought you'd love this.
```

### Important Rules
1. **Phone numbers MUST include country code** (e.g., +1234567890)
2. **First row is headers** (column names)
3. **No spaces in column names** (use underscores: order_id, not "order id")
4. **Use UTF-8 encoding** for special characters
5. **Quotes for commas**: If message contains commas, wrap in quotes

---

## Message Templates

Templates use `{placeholder}` syntax that matches CSV column names.

### Template Examples

#### Order Confirmation
**CSV Columns**: `phone, name, order_id, delivery_date`

**Template**: 
```
Hi {name}, your order #{order_id} has been confirmed! Expected delivery: {delivery_date}. Thank you!
```

**Result**:
```
Hi John Doe, your order #ORD-1001 has been confirmed! Expected delivery: 2025-11-25. Thank you!
```

#### Appointment Reminder
**CSV Columns**: `phone, name, date, time, location`

**Template**: 
```
Hello {name}, reminder for your appointment on {date} at {time}. Location: {location}. See you soon!
```

#### Payment Reminder
**CSV Columns**: `phone, name, amount, due_date, service`

**Template**: 
```
Dear {name}, your payment of {amount} for {service} is due on {due_date}. Please pay at your earliest convenience.
```

#### Discount Offer
**CSV Columns**: `phone, name, product, discount, code, expiry_date`

**Template**: 
```
Hi {name}! Exclusive offer: {discount}% off on {product}. Use code: {code}. Valid until {expiry_date}!
```

### Template Best Practices
1. **Keep it concise** - WhatsApp has message length limits
2. **Be clear** - Avoid ambiguous placeholders
3. **Test first** - Send to yourself before batch sending
4. **Match columns exactly** - Placeholder names must match CSV headers
5. **Use professional tone** - Represent your business well

---

## Batch Operations

### Sending Flow

1. **Preparation**
   - System loads CSV file
   - Validates phone numbers and data
   - Shows total contact count

2. **Sending Process**
   - Processes contacts one by one
   - Shows progress: [Current/Total]
   - Displays message preview
   - Applies configured delay between messages

3. **Progress Display**
   ```
   [5/100] Sending to John Doe (+1234567890)
   Message: Hi John, your order #1001 is ready!
   ✅ Sent successfully!
   ⏳ Waiting 20s before next message...
   ```

4. **Summary**
   ```
   ================================================================
   📊 BATCH SUMMARY
   ================================================================
   Total: 100
   ✅ Success: 95
   ❌ Failed: 3
   ⏭️  Skipped: 2
   ================================================================
   ```

### Error Handling

**Skip Errors Mode** (Default):
- Continues sending even if some fail
- Logs all failures
- Shows summary at the end

**Stop on Error Mode**:
- Stops at first failure
- Use `--no-skip` flag in CLI
- Useful for critical messages

### Rate Limiting

**Recommended Delays**:
- **Basic messages**: 20 seconds
- **Image messages**: 25 seconds
- **Large batches**: 25-30 seconds

**WhatsApp Limits**:
- **Daily limit**: ~250 messages recommended
- **Hourly limit**: ~100 messages recommended
- **Risk**: Sending too fast may trigger WhatsApp's spam detection

---

## Logging & Tracking

### Log File Location
- **JSON Log**: `data/whatsapp_batch_log.json`
- **Text Log**: `data/whatsapp_batch.log`

### Log Entry Format
```json
{
  "timestamp": "2025-11-19T10:30:45",
  "phone": "+1234567890",
  "name": "John Doe",
  "message": "Hi John, your order is ready!",
  "success": true,
  "response": "✅ WhatsApp message sent to +1234567890"
}
```

### Viewing Logs

**Batch File**:
1. Run `batch_scripts\automation\whatsapp_batch_automation.bat`
2. Select option 5: View Batch Logs

**Python CLI**:
```bash
python scripts/whatsapp_batch.py logs --limit 50
```

**Direct JSON**:
- Open `data/whatsapp_batch_log.json` in text editor
- Use JSON viewer for better formatting

---

## Best Practices

### ✅ Do's

1. **Test with yourself first**
   - Send a test batch to your own number
   - Verify template formatting
   - Check timing and delays

2. **Use appropriate delays**
   - Minimum 20 seconds between messages
   - 25-30 seconds for large batches
   - Never go below 15 seconds

3. **Verify phone numbers**
   - Always include country code (+1234567890)
   - Validate numbers before batch sending
   - Remove invalid/duplicate numbers

4. **Keep messages professional**
   - Use proper grammar and spelling
   - Avoid spam-like language
   - Provide value to recipients

5. **Monitor WhatsApp Web**
   - Keep WhatsApp Web logged in
   - Don't close the browser during batch send
   - Check for QR code re-scan prompts

6. **Backup your data**
   - Keep backup of CSV files
   - Save important logs
   - Export successful send lists

### ❌ Don'ts

1. **Don't spam**
   - Don't send unsolicited messages
   - Don't send too many messages per day
   - Don't send to people who opted out

2. **Don't rush**
   - Don't use delays less than 15 seconds
   - Don't send more than 250/day
   - Don't send during odd hours

3. **Don't ignore errors**
   - Review failed messages
   - Fix issues before retrying
   - Update CSV with correct data

4. **Don't share sensitive info**
   - Don't include passwords in messages
   - Don't share payment details
   - Don't send confidential data

---

## Troubleshooting

### Common Issues

#### ❌ "CSV file not found"
**Solution**: 
- Check file path is correct
- Use full path or relative to project root
- Ensure file is in `data/` folder

#### ❌ "Phone number format error"
**Solution**: 
- Add country code (+1234567890)
- Remove spaces and dashes
- Use international format

#### ❌ "WhatsApp Web not responding"
**Solution**: 
- Ensure WhatsApp Web is logged in
- Check internet connection
- Restart browser and re-login
- Scan QR code again if needed

#### ❌ "Template placeholder not found"
**Solution**: 
- Check placeholder names match CSV columns exactly
- Use correct case (case-sensitive)
- No spaces in column names

#### ❌ "Image not supported"
**Solution**: 
- Use JPG format (PNG not supported by pywhatkit)
- Convert PNG to JPG first
- Verify image file exists

#### ❌ "Too many messages failed"
**Solution**: 
- Increase delay between messages
- Check WhatsApp account status
- Verify phone numbers are valid
- Send in smaller batches

### Getting Help

1. **Check logs**: View batch logs for error details
2. **Test individually**: Send to one contact first
3. **Verify CSV**: Open in Excel to check format
4. **Review documentation**: Re-read relevant sections

---

## Examples

### Example 1: Simple Birthday Wishes

**CSV File** (`birthday_wishes.csv`):
```csv
phone,name
+1234567890,John Doe
+0987654321,Jane Smith
+1122334455,Bob Johnson
```

**Batch Command**:
```bash
python scripts/whatsapp_batch.py send birthday_wishes.csv --template "Happy Birthday {name}! 🎉 Wishing you an amazing year ahead!"
```

---

### Example 2: Order Confirmations

**CSV File** (`orders.csv`):
```csv
phone,name,order_id,amount,delivery_date
+1234567890,John Doe,ORD-1001,$50.00,Nov 25
+0987654321,Jane Smith,ORD-1002,$75.50,Nov 26
```

**Template**:
```
Hi {name}, your order #{order_id} for {amount} has been confirmed! Expected delivery: {delivery_date}. Thank you for shopping with us!
```

**Batch Command**:
```bash
python scripts/whatsapp_batch.py send orders.csv --template "Hi {name}, your order #{order_id} for {amount} has been confirmed! Expected delivery: {delivery_date}. Thank you!"
```

---

### Example 3: Appointment Reminders

**CSV File** (`appointments.csv`):
```csv
phone,name,date,time,location,service
+1234567890,John Doe,Nov 25,2:00 PM,Downtown Clinic,Dental Checkup
+0987654321,Jane Smith,Nov 26,10:30 AM,Main Office,Consultation
```

**Template**:
```
Hello {name}, reminder for your {service} appointment on {date} at {time}. Location: {location}. See you soon!
```

---

### Example 4: Batch Image Sending

**CSV File** (`promo_list.csv`):
```csv
phone,name,product
+1234567890,John Doe,Premium Plan
+0987654321,Jane Smith,Basic Plan
```

**Image**: `promo_image.jpg`

**Caption Template**:
```
Hi {name}! Exclusive offer on {product}. Limited time only!
```

**Batch Command**:
```bash
python scripts/whatsapp_batch.py image promo_list.csv promo_image.jpg --caption "Hi {name}! Exclusive offer on {product}. Limited time only!"
```

---

### Example 5: Payment Reminders

**CSV File** (`pending_payments.csv`):
```csv
phone,name,invoice_id,amount,due_date
+1234567890,John Doe,INV-2001,$150.00,Nov 30
+0987654321,Jane Smith,INV-2002,$200.00,Dec 05
```

**Template**:
```
Dear {name}, this is a reminder that payment for invoice {invoice_id} ({amount}) is due on {due_date}. Please pay at your earliest convenience. Thank you!
```

---

## Advanced Usage

### Scheduling Batch Sends

You can combine with Windows Task Scheduler:

1. Create batch send script
2. Schedule with Task Scheduler
3. Runs automatically at specified time

**Example Script** (`scheduled_send.bat`):
```batch
@echo off
python scripts/whatsapp_batch.py send data/daily_reminders.csv --template "Morning reminder for {name}: {task}"
```

### Integration with Other Systems

Export contacts from:
- **CRM systems** (Salesforce, HubSpot) → CSV
- **E-commerce** (Shopify, WooCommerce) → CSV
- **Databases** (MySQL, PostgreSQL) → CSV
- **Excel/Google Sheets** → CSV

Then use batch automation to send!

---

## Summary

The WhatsApp Batch Automation System provides:
- ✅ Easy batch messaging to multiple contacts
- ✅ Personalized messages with templates
- ✅ Progress tracking and logging
- ✅ User-friendly batch file interface
- ✅ Professional Python CLI
- ✅ Comprehensive error handling

**Get Started**: Run `batch_scripts\automation\whatsapp_batch_automation.bat`

**Need Help**: Check troubleshooting section or view logs

**Best Practice**: Test first, use appropriate delays, monitor WhatsApp Web

---

## Related Documentation

- [WhatsApp Messenger Guide](./WHATSAPP_MESSENGER_GUIDE.md) - Single message sending
- [Contact Calling Guide](./CONTACT_CALLING_GUIDE.md) - Voice calling features
- [Phone Link Notifications Guide](./PHONE_LINK_NOTIFICATIONS_GUIDE.md) - Notification monitoring

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0
