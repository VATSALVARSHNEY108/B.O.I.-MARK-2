# Fix Instructions for Local Machine

## Problem
The `virtual_language_model.py` file uses the old Google Gemini API which doesn't work with the new `google-genai` package.

## Solution: Update Your Local `virtual_language_model.py`

### Step 1: Update Imports (Lines 6-11)

**REPLACE:**
```python
import google.genai as genai
from gui_automation import GUIAutomation
```

**WITH:**
```python
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
from gui_automation import GUIAutomation
```

---

### Step 2: Update __init__ Method (Lines 21-30)

**REPLACE:**
```python
if not self.api_key:
    print("⚠️  Warning: GEMINI_API_KEY not found")
    self.client = None
else:
    genai.configure(api_key=self.api_key)
    self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
```

**WITH:**
```python
if not self.api_key:
    print("⚠️  Warning: GEMINI_API_KEY not found")
    self.client = None
    self.model = None
else:
    try:
        self.client = genai.Client(api_key=self.api_key)
        self.model = 'gemini-2.0-flash-exp'
    except Exception as e:
        print(f"⚠️  Warning: Failed to initialize Gemini client: {e}")
        self.client = None
        self.model = None
```

---

### Step 3: Update _analyze_screen_with_ai Method

**FIND** the section that uploads and analyzes the image (around line 130-170):

**REPLACE:**
```python
try:
    # Upload the image
    image_file = genai.upload_file(screenshot_path)
    
    # ... (prompt definition) ...
    
    response = self.client.generate_content([prompt, image_file])
```

**WITH:**
```python
try:
    # Read the image
    with open(screenshot_path, 'rb') as f:
        image_data = f.read()
    
    # ... (prompt definition stays the same) ...
    
    response = self.client.models.generate_content(
        model=self.model,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type="image/png",
                            data=image_data
                        )
                    )
                ]
            )
        ]
    )
```

---

### Step 4: Update decide_action Method

**FIND** (around line 290):
```python
response = self.client.generate_content(prompt)
```

**REPLACE WITH:**
```python
response = self.client.models.generate_content(
    model=self.model,
    contents=prompt
)
```

---

### Step 5: Update query_knowledge Method

**FIND** (around line 535):
```python
response = self.client.generate_content(prompt)
```

**REPLACE WITH:**
```python
response = self.client.models.generate_content(
    model=self.model,
    contents=prompt
)
```

---

## Alternative: Download Complete Fixed File

Or, download the complete fixed `virtual_language_model.py` file from this Replit and replace your local file entirely.

## After Making Changes

Save the file and run `python gui_app.py` again. The errors should be resolved!
