# 📱 Phone Link Dial Feature Guide

## Overview
Make phone calls using Windows Phone Link (Your Phone app) **without needing Twilio**! This feature automatically opens Phone Link and dials the number for you.

---

## ✅ Features

- ✅ **No Twilio required** - Works directly with Phone Link
- ✅ **Easy to use** - Just provide a phone number
- ✅ **Multiple formats** - Accepts any phone number format
- ✅ **Automatic dialing** - Opens Phone Link and starts the call
- ✅ **Uses tel: URI** - Standard protocol support

---

## 🎯 How to Use

### Method 1: Via Command Executor
```python
executor.execute_command({
    "action": "dial_phone_link",
    "parameters": {
        "phone": "+1234567890"
    }
})
```

### Method 2: Direct Phone Dialer
```python
from modules.communication.phone_dialer import create_phone_dialer

phone_dialer = create_phone_dialer()
result = phone_dialer.dial_with_phone_link("+1234567890")
print(result['message'])
```

### Method 3: Just Open Phone Link
```python
# Open Phone Link app without dialing
executor.execute_command({
    "action": "open_phone_link"
})

# OR
phone_dialer.open_phone_link()
```

---

## 📞 Available Commands

### 1. Dial with Phone Link
**Actions:** `dial_phone_link` or `phone_link_dial`

**Parameters:**
- `phone` or `number`: Phone number to dial (any format)

**Example:**
```python
{
    "action": "dial_phone_link",
    "parameters": {
        "phone": "+1 (123) 456-7890"
    }
}
```

### 2. Open Phone Link App
**Action:** `open_phone_link`

**Parameters:** None

**Example:**
```python
{
    "action": "open_phone_link"
}
```

---

## 💡 Phone Number Formats Supported

All these formats work:
- `+1234567890`
- `123-456-7890`
- `(123) 456-7890`
- `+91 98765 43210`
- `9876543210`

The system automatically cleans the number before dialing!

---

## 🔧 How It Works

1. **Windows:** Uses `tel:` URI protocol → Opens Phone Link
2. **Phone Link** receives the number and initiates the call
3. Your phone (connected to Phone Link) starts dialing

---

## 📋 Requirements

- ✅ **Windows 10/11** with Phone Link (Your Phone) installed
- ✅ **Phone connected** to Phone Link app
- ✅ **Phone Link setup** complete

---

## 🎨 Example Usage in GUI

When you use the VATSAL GUI, you can simply type:
```
Dial +1234567890 using phone link
```

Or use the command executor directly:
```python
result = self.executor.execute_command({
    "action": "dial_phone_link",
    "parameters": {
        "phone": "+1234567890"
    }
})
```

---

## 🆚 Phone Link vs Twilio

| Feature | Phone Link | Twilio |
|---------|-----------|--------|
| **Cost** | ✅ Free | 💰 Paid API |
| **Setup** | ✅ Easy | ⚙️ API keys needed |
| **Your Phone** | ✅ Uses your phone | ☁️ Cloud service |
| **Windows Only** | ⚠️ Yes | ✅ Cross-platform |

---

## 🐛 Troubleshooting

**Issue:** Phone Link doesn't open
- **Solution:** Make sure Phone Link is installed and your phone is connected

**Issue:** Number doesn't dial
- **Solution:** Check that Phone Link has permission to make calls

**Issue:** "Phone Link is only available on Windows"
- **Solution:** This feature requires Windows 10/11 with Phone Link

---

## 🎯 Quick Test

Run this test to verify it works:
```bash
python test_phone_link_simple.py
```

This will test:
1. Opening Phone Link
2. Dialing with various number formats
3. Showing how to use the feature

---

**Enjoy making calls without Twilio! 📱**
