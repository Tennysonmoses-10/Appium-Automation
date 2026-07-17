# ✅ Verify Local App Installation Guide

## 🎯 How to Verify Your Local App is Properly Installed

There are **5 verification steps** to ensure everything is working:

---

## ✅ Step 1: Verify APK File Exists

### Windows PowerShell:
```powershell
# Check if your APK file exists
Test-Path "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# If it shows "True" - file exists ✓
# If it shows "False" - file not found ❌
```

### Mac/Linux Terminal:
```bash
# Check if your APK file exists
ls -lh ~/Downloads/partner_app.apk

# If it shows file info - file exists ✓
# If it shows "No such file" - file not found ❌
```

### What to Check:
```
✓ File exists
✓ File size > 0 MB
✓ File ends with .apk or .ipa
✓ File is not corrupted
```

---

## ✅ Step 2: Verify APK is Valid

### Using ADB (Android):
```bash
# Install and verify in one command
adb install "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# Output should show:
# Success: ✓ APK is valid
# Error: ❌ APK is corrupted
```

### Verify APK Package:
```bash
# Get package name from APK without installing
aapt dump badging "C:\Users\NidhiChaure\Downloads\partner_app.apk" | grep package

# Output example:
# package: name='com.partnerapp' versionCode='1' versionName='1.0'
```

---

## ✅ Step 3: Verify Device Connection

### List Connected Devices:
```bash
adb devices

# Output should show:
# List of attached devices
# emulator-5554    device         ← Device is connected ✓
# R38R70ABC01      device         ← Physical device ✓

# If list is empty, device is not connected ❌
```

### Verify Device Status:
```bash
# Check if device is ready
adb shell getprop ro.build.version.release

# Output example:
# 14.0                              ← Device is ready ✓
```

---

## ✅ Step 4: Verify App Installation on Device

### Check if App is Installed:
```bash
# List all installed packages
adb shell pm list packages | grep partnerapp

# Output:
# package:com.partnerapp            ← App is installed ✓

# If no output - app not installed ❌
```

### Get Full App Info:
```bash
# Get detailed app info
adb shell pm dump com.partnerapp | grep -E "version|packages"

# Shows:
# versionName=1.0
# versionCode=1
# Package [com.partnerapp]
```

### Check App Location:
```bash
# Where the app is installed on device
adb shell pm path com.partnerapp

# Output:
# package:/data/app/com.partnerapp-ABC123/base.apk
```

---

## ✅ Step 5: Verify Configuration Files

### Check .env File:
```bash
# Display your .env file content
cat .env | grep APPIUM

# Should show:
# APPIUM_APP_PATH=C:\Users\NidhiChaure\Downloads\partner_app.apk
# APPIUM_DEVICE_NAME=emulator-5554
# APPIUM_PLATFORM=Android
```

### Verify Python Configuration:
```python
# In Python shell or test file
from config.settings import settings

print(f"App Path: {settings.appium.app_path}")
print(f"Device Name: {settings.appium.device_name}")
print(f"Platform: {settings.appium.platform}")
print(f"App Package: {settings.appium.app_package}")
print(f"Appium URL: {settings.appium.server_url}")

# Output should show your configuration values
```

---

## 🧪 Complete Verification Script

### Run This Python Script to Verify Everything:

**Create file: `verify_app_installation.py`**

```python
#!/usr/bin/env python3
"""
Verification script for local app installation.
Run this to verify your app is properly configured and installed.
"""

import os
import subprocess
import sys
from pathlib import Path
from config.settings import settings

print("\n" + "="*70)
print("APP INSTALLATION VERIFICATION")
print("="*70)

# Step 1: Verify APK File Exists
print("\n[STEP 1] Checking if APK file exists...")
app_path = settings.appium.app_path
if app_path:
    if os.path.exists(app_path):
        file_size = os.path.getsize(app_path) / (1024 * 1024)  # Convert to MB
        print(f"✓ APK file found: {app_path}")
        print(f"✓ File size: {file_size:.2f} MB")
    else:
        print(f"✗ APK file NOT found: {app_path}")
        sys.exit(1)
else:
    print("✗ APPIUM_APP_PATH not configured in .env")
    sys.exit(1)

# Step 2: Verify Device Connection
print("\n[STEP 2] Checking device connection...")
try:
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    output_lines = result.stdout.strip().split('\n')[1:]
    connected_devices = [line.split()[0] for line in output_lines if 'device' in line]
    
    if connected_devices:
        print(f"✓ Devices connected: {connected_devices}")
        print(f"✓ Device name: {settings.appium.device_name}")
    else:
        print("✗ No devices connected")
        print("  Run: adb devices")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error checking devices: {e}")
    sys.exit(1)

# Step 3: Verify App on Device
print("\n[STEP 3] Checking if app is installed on device...")
try:
    result = subprocess.run(
        ["adb", "shell", "pm", "list", "packages"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    installed_packages = result.stdout.split('\n')
    app_installed = any(settings.appium.app_package in pkg for pkg in installed_packages)
    
    if app_installed:
        print(f"✓ App installed: {settings.appium.app_package}")
    else:
        print(f"ℹ App not yet installed: {settings.appium.app_package}")
        print("  This is OK - Appium will install it automatically")
except Exception as e:
    print(f"✗ Error checking app: {e}")
    sys.exit(1)

# Step 4: Verify Configuration
print("\n[STEP 4] Checking configuration...")
print(f"✓ App Path: {settings.appium.app_path}")
print(f"✓ Device Name: {settings.appium.device_name}")
print(f"✓ Platform: {settings.appium.platform}")
print(f"✓ App Package: {settings.appium.app_package}")
print(f"✓ App Activity: {settings.appium.app_activity}")
print(f"✓ Appium Server: {settings.appium.server_url}")
print(f"✓ Timeout: {settings.appium.timeout}s")
print(f"✓ Implicit Wait: {settings.appium.implicit_wait}s")

# Step 5: Check Appium Server
print("\n[STEP 5] Checking Appium server...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 4723))
    sock.close()
    
    if result == 0:
        print("✓ Appium server is running on http://localhost:4723")
    else:
        print("✗ Appium server NOT running")
        print("  Start it with: appium")
except Exception as e:
    print(f"✗ Error checking Appium: {e}")

print("\n" + "="*70)
print("✅ VERIFICATION COMPLETE")
print("="*70)
print("\nYou can now run your tests:")
print("  pytest tests/mobile/ -v")
print("\n")
```

### Run the Script:
```bash
python verify_app_installation.py
```

### Expected Output:
```
======================================================================
APP INSTALLATION VERIFICATION
======================================================================

[STEP 1] Checking if APK file exists...
✓ APK file found: C:\Users\NidhiChaure\Downloads\partner_app.apk
✓ File size: 45.23 MB

[STEP 2] Checking device connection...
✓ Devices connected: ['emulator-5554']
✓ Device name: emulator-5554

[STEP 3] Checking if app is installed on device...
✓ App installed: com.partnerapp

[STEP 4] Checking configuration...
✓ App Path: C:\Users\NidhiChaure\Downloads\partner_app.apk
✓ Device Name: emulator-5554
✓ Platform: Android
✓ App Package: com.partnerapp
✓ App Activity: .MainActivity
✓ Appium Server: http://localhost:4723
✓ Timeout: 30s
✓ Implicit Wait: 10s

[STEP 5] Checking Appium server...
✓ Appium server is running on http://localhost:4723

======================================================================
✅ VERIFICATION COMPLETE
======================================================================

You can now run your tests:
  pytest tests/mobile/ -v
```

---

## 🔍 Manual Verification Commands

### Command Checklist:

```bash
# 1. Check if APK file exists
ls -l "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# 2. Verify APK is valid
adb install "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# 3. List connected devices
adb devices

# 4. Check if app is installed
adb shell pm list packages | grep partnerapp

# 5. Get app information
adb shell pm dump com.partnerapp | grep version

# 6. Launch the app manually (test)
adb shell am start -n com.partnerapp/.MainActivity

# 7. Check app is running
adb shell pidof com.partnerapp
```

---

## ✅ Verification Checklist

Before running tests, verify all these boxes:

| Check | Command | Expected Result |
|-------|---------|-----------------|
| **APK Exists** | `Test-Path "C:\...\app.apk"` | `True` ✓ |
| **APK Valid** | `adb install app.apk` | `Success` ✓ |
| **Device Connected** | `adb devices` | Device listed ✓ |
| **App Installed** | `adb shell pm list packages` | Package listed ✓ |
| **Config Valid** | `python -c "from config.settings import settings; print(settings.appium.app_path)"` | Path shown ✓ |
| **Appium Running** | `nc -zv localhost 4723` | Connection successful ✓ |

---

## 🆘 Troubleshooting

### Problem: APK file not found
```
Error: No such file or directory
Solution: Check full path to APK
Command: ls -l "C:\path\to\file.apk"
```

### Problem: App not installing
```
Error: Failed to install apk
Solution: APK might be corrupted
Action: Redownload or rebuild APK
```

### Problem: Device not detected
```
Error: No devices connected
Solution: Check USB connection
Commands:
  - adb kill-server
  - adb start-server
  - adb devices
```

### Problem: App not launching
```
Error: Unable to start activity
Solution: Wrong package or activity name
Action: Verify with: adb shell pm dump com.partnerapp
```

### Problem: Appium connection failed
```
Error: Connection refused
Solution: Appium server not running
Action: Start Appium: appium
```

---

## 📊 Verification Workflow

```
┌─────────────────────────────────┐
│  1. Check APK file exists       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  2. Verify APK is valid         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  3. Connect device via ADB      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  4. Install app on device       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  5. Verify configuration        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  6. Start Appium server         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  7. Run tests                   │
│     pytest tests/mobile/ -v     │
└─────────────────────────────────┘
```

---

## 🚀 Quick Verification (2 Minutes)

Run these commands in order:

```bash
# 1. Check APK file
ls -lh "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# 2. Check devices
adb devices

# 3. Install app
adb install "C:\Users\NidhiChaure\Downloads\partner_app.apk"

# 4. Check if installed
adb shell pm list packages | grep partnerapp

# 5. Run verification script
python verify_app_installation.py

# 6. Start Appium
appium

# 7. Run a test (in another terminal)
pytest tests/mobile/test_login.py::TestLoginFlow::test_successful_login -v
```

---

## 📖 Related Documentation

- **LOCAL_APP_SETUP_GUIDE.md** - How to configure app path
- **DEVICE_CONFIGURATION_GUIDE.md** - How to setup device
- **tests/mobile/** - Mobile test examples

---

## ✨ You're Ready!

Once all verification checks pass ✓, your app is ready for testing! 🎉

```bash
pytest tests/mobile/ -v
```
