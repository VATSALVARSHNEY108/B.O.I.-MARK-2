# Quick Fix: Phone Link Not Clicking Call Button

## Problem
Phone Link opens and shows the number, but doesn't actually start the call.

## ✅ SOLUTION (2 Easy Steps)

### Step 1: Run Calibration Tool
This finds the EXACT position of the Call button on YOUR screen.

**Option A - Use batch file:**
```bash
batch_scripts\calibrate_call_button.bat
```

**Option B - Use Python:**
```bash
python scripts/calibrate_phone_link_button.py
```

### What the Calibration Does:
1. Opens Phone Link with a test number
2. Asks you to hover your mouse over the Call button
3. Records the exact position
4. Tests if it clicks correctly
5. Saves the position for future use

### Step 2: Test Auto-Call
After calibration, test that it works:

```bash
python tests/test_phone_link_fix.py
```

## How It Works Now

**Before Calibration:**
- Tries clicking at 4 different typical positions
- Uses keyboard shortcuts as backup
- May or may not hit the Call button

**After Calibration:**
- Clicks at the EXACT position you showed it
- Works every time! ✅

## Troubleshooting

### Calibration doesn't click correctly?
1. Make sure Phone Link window is fully open (not minimized)
2. Hover your mouse DIRECTLY over the green Call button
3. Keep your mouse VERY STILL during the 3-second capture
4. Run calibration again

### Auto-call still doesn't work?
1. Re-run calibration: `python scripts/calibrate_phone_link_button.py`
2. Make sure Phone Link is connected to your phone
3. Check that Phone Link window stays in focus (don't click away)
4. Try increasing wait time in `phone_dialer.py` (line 403) from 4 to 6 seconds

## Files Created
- `config/phone_link_button.json` - Stores your calibrated button position
- Position is specific to your screen resolution and Phone Link layout

## Need to Recalibrate?
Run the calibration tool anytime:
- After changing screen resolution
- After updating Phone Link
- If Phone Link layout changes
- If you move Phone Link window to a different monitor

That's it! After calibration, auto-calling will work perfectly every time. 🎉
