# 📱 Device & App Configuration Guide

## 🎯 Where to Enter Your Device Details

You have **TWO ways** to configure your device and app details:

---

## Method 1: Using `.env` File (RECOMMENDED ✅)

### Step 1: Create `.env` File

Copy the `.env.example` file to create your `.env` file:

```bash
cp .env.example .env
```

### Step 2: Edit `.env` File with Your Device Details

Open `.env` in your editor and update with your actual device information:

```env
# APPIUM CONFIGURATION - FOR PHYSICAL DEVICES

# Your Appium server URL
APPIUM_SERVER_URL=http://localhost:4723

# Physical device name (from 'adb devices' list)
APPIUM_DEVICE_NAME=emulator-5554

# Platform: Android or iOS
APPIUM_PLATFORM=Android

# Your app package name
APPIUM_APP_PACKAGE=com.partnerapp

# Your app main activity
APPIUM_APP_ACTIVITY=.MainActivity

# Appium timeouts
APPIUM_TIMEOUT=30
APPIUM_IMPLICIT_WAIT=10
APPIUM_EXPLICIT_WAIT=20
```

---

## Method 2: Direct Configuration in `config/settings.py`

If you prefer, edit the `AppiumConfig` class directly in `config/settings.py`:

```python
class AppiumConfig(BaseSettings):
    """Appium configuration for mobile automation."""
    
    server_url: str = Field(default="http://localhost:4723")
    timeout: int = Field(default=30)
    implicit_wait: int = Field(default=10)
    explicit_wait: int = Field(default=20)
    
    # ⬇️ UPDATE THESE WITH YOUR DEVICE DETAILS:
    device_name: str = Field(default="YOUR_DEVICE_NAME")  # From 'adb devices'
    platform: Literal["Android", "iOS"] = Field(default="Android")  # Android or iOS
    app_package: str = Field(default="com.your.app.package")  # Your app package
    app_activity: str = Field(default=".MainActivity")  # Your app main activity
```

---

## 📋 Finding Your Device Details

### For Android Devices:

#### 1. Find Device Name (via ADB):
```bash
# List connected devices
adb devices

# Output example:
# List of attached devices
# emulator-5554             device
# R38R70ABC01               device
```

**Use the device ID** (e.g., `emulator-5554` or `R38R70ABC01`)

#### 2. Find App Package Name:
```bash
# List all installed packages
adb shell pm list packages

# Or search for your app
adb shell pm list packages | grep partnerapp

# Output example:
# package:com.partnerapp
# package:com.partnerapp.beta
```

**Use the full package name** (e.g., `com.partnerapp`)

#### 3. Find App Main Activity:
```bash
# Get app activities
adb shell cmd package resolve-activity --brief com.partnerapp

# Or use aapt (if apk available)
aapt dump badging /path/to/app.apk | grep activity

# Output example:
# com.partnerapp/.MainActivity
# com.partnerapp/.SplashActivity
```

**Use the main activity** (e.g., `.MainActivity`)

---

### For iOS Devices:

#### 1. Find Device UUID:
```bash
# Connect device via USB
# In Xcode: Window > Devices and Simulators

# Or via CLI:
xcrun xctrace list devices 2>&1 | grep -oE "([0-9A-F]{8}-([0-9A-F]{4}-){3}[0-9A-F]{12})"
```

#### 2. Find App Bundle ID:
```bash
# List installed apps on iOS device
ios-deploy --list_bundle_id

# Or from your Xcode project: com.company.appname
```

#### 3. Find App Activity:
```bash
# For iOS, use bundle identifier and activity name
# Usually the same as bundle ID
```

---

## 🔧 Complete Configuration Examples

### Example 1: Android Physical Device with Partner App

**.env file:**
```env
# Android Physical Device
APPIUM_DEVICE_NAME=R38R70ABC01
APPIUM_PLATFORM=Android
APPIUM_APP_PACKAGE=com.partnerapp
APPIUM_APP_ACTIVITY=.MainActivity
APPIUM_SERVER_URL=http://localhost:4723
APPIUM_TIMEOUT=30
APPIUM_IMPLICIT_WAIT=10
APPIUM_EXPLICIT_WAIT=20
```

### Example 2: Android Emulator

**.env file:**
```env
# Android Emulator
APPIUM_DEVICE_NAME=emulator-5554
APPIUM_PLATFORM=Android
APPIUM_APP_PACKAGE=com.partnerapp
APPIUM_APP_ACTIVITY=.MainActivity
APPIUM_SERVER_URL=http://localhost:4723
APPIUM_TIMEOUT=30
APPIUM_IMPLICIT_WAIT=10
APPIUM_EXPLICIT_WAIT=20
```

### Example 3: iOS Simulator

**.env file:**
```env
# iOS Simulator
APPIUM_DEVICE_NAME=iPhone 14
APPIUM_PLATFORM=iOS
APPIUM_APP_PACKAGE=com.partnerapp
APPIUM_APP_ACTIVITY=com.partnerapp
APPIUM_SERVER_URL=http://localhost:4723
APPIUM_TIMEOUT=30
APPIUM_IMPLICIT_WAIT=10
APPIUM_EXPLICIT_WAIT=20
```

---

## ✅ Step-by-Step Setup Process

### Step 1: Enable Developer Mode (Android)

```
Settings > About Phone > Build Number (tap 7 times)
Settings > Developer Options > USB Debugging (Enable)
Settings > Developer Options > Install via USB (Enable)
```

### Step 2: Connect Device

```bash
# Connect via USB
# Verify connection:
adb devices

# Output should show your device as "device"
```

### Step 3: Get Device Details

```bash
# Get device name
adb devices
# Note: emulator-5554 or R38R70ABC01

# Get app package
adb shell pm list packages | grep partnerapp
# Note: com.partnerapp

# Get app activity
adb shell dumpsys window | grep mCurrentFocus
# Note: com.partnerapp/.MainActivity
```

### Step 4: Update .env File

```env
APPIUM_DEVICE_NAME=emulator-5554
APPIUM_APP_PACKAGE=com.partnerapp
APPIUM_APP_ACTIVITY=.MainActivity
```

### Step 5: Start Appium Server

```bash
appium
# Server runs on http://localhost:4723
```

### Step 6: Run Tests

```bash
pytest tests/mobile/
```

---

## 🚀 Quick Reference

| Configuration | Where to Find | Example |
|---------------|---------------|---------|
| **Device Name** | `adb devices` | `emulator-5554` |
| **App Package** | `adb shell pm list packages` | `com.partnerapp` |
| **App Activity** | `adb shell dumpsys window` | `.MainActivity` |
| **Appium URL** | Default (localhost) | `http://localhost:4723` |
| **Platform** | Your OS | `Android` or `iOS` |

---

## 📁 Configuration File Locations

```
partner_app_qa/
├── .env                      ← Your device config (EDIT THIS!)
├── .env.example              ← Template (reference only)
├── config/
│   └── settings.py           ← Alternative config file
└── ...
```

---

## ⚙️ How Configuration is Loaded

```python
# Pydantic loads configuration in this order:
# 1. .env file (highest priority)
# 2. config/settings.py defaults
# 3. Environment variables

# Your .env settings override everything
```

---

## 🔐 Best Practices

✅ **DO:**
- Keep `.env` file in project root
- Use `.env` for all configurations (easiest)
- Add `.env` to `.gitignore` (don't commit)
- Keep sensitive data in `.env` only

❌ **DON'T:**
- Hardcode device names in tests
- Commit `.env` to GitHub
- Share `.env` with credentials
- Modify `settings.py` directly (use `.env` instead)

---

## 🔍 Verification

After configuration, verify your setup:

```python
# In test or Python shell:
from config.settings import settings

print(settings.appium.device_name)      # Should show your device
print(settings.appium.app_package)      # Should show your app
print(settings.appium.app_activity)     # Should show your activity
print(settings.appium.server_url)       # Should show Appium URL
```

---

## 🆘 Troubleshooting

### Device Not Found
```bash
# Verify connection
adb devices

# If empty, try:
adb kill-server
adb start-server
adb devices
```

### App Package Not Found
```bash
# Make sure app is installed
adb shell pm list packages | grep partnerapp

# If not found, install it
adb install app.apk
```

### Appium Connection Failed
```bash
# Start Appium server
appium

# Check URL is correct
APPIUM_SERVER_URL=http://localhost:4723
```

---

## 📖 Related Files

- **config/settings.py** - Configuration classes (reference)
- **.env.example** - Configuration template
- **fixtures/conftest.py** - Uses configuration in fixtures
- **core/appium_manager.py** - Uses configuration in driver setup

---

## ✨ Your Next Steps

1. ✅ Connect your physical device via USB
2. ✅ Run `adb devices` to get device name
3. ✅ Find your app package and activity
4. ✅ Copy `.env.example` to `.env`
5. ✅ Update `.env` with your device details
6. ✅ Start Appium server
7. ✅ Run your first mobile test!

```bash
pytest tests/mobile/ -v
```

**Happy mobile testing! 📱**
