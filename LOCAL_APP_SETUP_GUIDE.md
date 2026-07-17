# 📦 Local App Setup Guide - APK/IPA Configuration

## 🎯 Two Types of App Installation

### Type 1: Pre-installed Apps
- App already installed on device
- You provide: **Package name** + **Activity name**
- Uses: `app_package` and `app_activity`

### Type 2: Local App Files (YOUR CASE ✅)
- App file on your local machine (APK/IPA)
- You provide: **Path to app file**
- Uses: `app_path`

---

## 📝 How to Enter Your Local App Path

### ✅ Method 1: Using `.env` File (EASIEST)

**Step 1: Find your app file location**

Example paths:
```
Windows:
C:\Users\NidhiChaure\apps\partner_app.apk
C:\Users\NidhiChaure\Downloads\partner_app.apk

Mac/Linux:
/Users/username/apps/partner_app.apk
~/apps/partner_app.apk
```

**Step 2: Open `.env` file and update:**

```env
# LOCAL APP FILE PATH
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk

# Leave these empty when using local app path
APPIUM_APP_PACKAGE=
APPIUM_APP_ACTIVITY=

# Device configuration
APPIUM_DEVICE_NAME=emulator-5554
APPIUM_PLATFORM=Android
APPIUM_SERVER_URL=http://localhost:4723
```

---

### ✅ Method 2: Direct Edit in `config/settings.py`

**File:** `config/settings.py` (Lines 25-40)

```python
class AppiumConfig(BaseSettings):
    """Appium configuration for mobile automation."""
    
    server_url: str = Field(default="http://localhost:4723")
    device_name: str = Field(default="emulator-5554")
    platform: Literal["Android", "iOS"] = Field(default="Android")
    
    # ⬇️ FOR LOCAL APP FILES, SET THIS:
    app_path: str = Field(default="C:\Users\NidhiChaure\apps\partner_app.apk")
    
    # Leave these empty when using local app
    app_package: str = Field(default="")
    app_activity: str = Field(default="")
```

---

## 🔍 Finding Your App File Location

### For Android (APK Files)

**Option 1: Already Downloaded**
```
Look in your Downloads folder
C:\Users\YourUsername\Downloads\app.apk
```

**Option 2: Build from Source**
```
If you have the source code:
C:\path\to\app\build\outputs\apk\release\app-release.apk
C:\path\to\app\build\outputs\apk\debug\app-debug.apk
```

**Option 3: Extract from Device**
```bash
# Get the app location
adb shell pm path com.partnerapp
# Output: package:/data/app/com.partnerapp-ABC123/base.apk

# Pull the app to your machine
adb pull /data/app/com.partnerapp-ABC123/base.apk ./partner_app.apk
```

### For iOS (IPA Files)

**Option 1: From Xcode Build**
```
~/Library/Developer/Xcode/DerivedData/YourApp-xyz/Build/Products/Debug-iphoneos/YourApp.app
```

**Option 2: From App Store**
```
Extract IPA from your iOS device or download from TestFlight
```

---

## 💾 Complete Configuration Examples

### Example 1: Android Local APK

**.env file:**
```env
# LOCAL APP PATH
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk

# DEVICE CONFIGURATION
APPIUM_DEVICE_NAME=emulator-5554
APPIUM_PLATFORM=Android
APPIUM_SERVER_URL=http://localhost:4723

# TIMING
APPIUM_TIMEOUT=30
APPIUM_IMPLICIT_WAIT=10
APPIUM_EXPLICIT_WAIT=20

# AUTOMATION
APPIUM_AUTOMATION_NAME=UiAutomator2

# Leave empty when using local app
APPIUM_APP_PACKAGE=
APPIUM_APP_ACTIVITY=
```

### Example 2: iOS Local IPA

**.env file:**
```env
# LOCAL APP PATH
APPIUM_APP_PATH=/Users/username/apps/partner_app.ipa

# DEVICE CONFIGURATION
APPIUM_DEVICE_NAME=iPhone 14
APPIUM_PLATFORM=iOS
APPIUM_SERVER_URL=http://localhost:4723

# AUTOMATION
APPIUM_AUTOMATION_NAME=XCUITest
APPIUM_UDID=00008020-000D4C3A2A5A002E

# Leave empty when using local app
APPIUM_APP_PACKAGE=
APPIUM_APP_ACTIVITY=
```

### Example 3: Physical Android Device with Local APK

**.env file:**
```env
# LOCAL APP PATH
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk

# PHYSICAL DEVICE
APPIUM_DEVICE_NAME=R38R70ABC01
APPIUM_PLATFORM=Android
APPIUM_UDID=R38R70ABC01

# APPIUM SERVER
APPIUM_SERVER_URL=http://localhost:4723
APPIUM_AUTOMATION_NAME=UiAutomator2
```

---

## ⚙️ Path Format Rules

### Windows Paths
```
✅ Correct: C:\Users\NidhiChaure\apps\partner_app.apk
❌ Wrong: C:/Users/NidhiChaure/apps/partner_app.apk (use backslash)
❌ Wrong: C:\\Users\\NidhiChaure\\apps\\partner_app.apk (don't escape)
```

### Mac/Linux Paths
```
✅ Correct: /Users/username/apps/partner_app.apk
✅ Correct: ~/apps/partner_app.apk
❌ Wrong: C:\Users\... (Windows path on Mac/Linux)
```

---

## 🚀 Using Local App Path in Tests

### In Test Files

```python
from core.appium_manager import AppiumManager
from config.settings import settings

# Initialize with local app
appium_manager = AppiumManager()
driver = appium_manager.get_driver()

# The driver will automatically use app_path from .env
```

### In conftest.py

```python
@pytest.fixture(scope="function")
def mobile_driver():
    """Fixture for mobile testing with local app."""
    manager = AppiumManager()
    driver = manager.get_driver()
    
    yield driver
    
    driver.quit()
```

---

## 📋 Configuration Priority

Appium will use configuration in this order:

1. **Local App Path** (if `app_path` is set) ← USE THIS FOR LOCAL FILES
2. **Pre-installed App** (if `app_package` is set)
3. **Hybrid approach** (install then use)

**Current Setup:**
```env
APPIUM_APP_PATH=C:\Users\...\partner_app.apk    # ← This takes priority
APPIUM_APP_PACKAGE=com.partnerapp                # ← This is ignored if app_path exists
```

---

## ✅ Step-by-Step Setup Process

### Step 1: Get Your App File

```bash
# If building from source
gradle build
# Output: app/build/outputs/apk/debug/app-debug.apk

# Or copy to a known location
cp /path/to/partner_app.apk ~/apps/partner_app.apk
```

### Step 2: Get Full Path to App

```bash
# Windows (PowerShell)
Get-Item "C:\Users\NidhiChaure\apps\partner_app.apk" | Select-Object FullName

# Mac/Linux
realpath ~/apps/partner_app.apk
```

### Step 3: Copy .env.example to .env

```bash
cp .env.example .env
```

### Step 4: Update .env with App Path

```env
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk
```

### Step 5: Start Appium Server

```bash
appium
```

### Step 6: Run Tests

```bash
pytest tests/mobile/ -v
```

---

## 🔧 Advanced: Installing and Running Local App

### Option A: Auto-Install (Recommended)

Appium can automatically install the app before testing:

**.env configuration:**
```env
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk
APPIUM_AUTO_INSTALL=true      # Auto-install before test
APPIUM_AUTO_LAUNCH=true       # Auto-launch after install
```

### Option B: Manual Install

```bash
# Pre-install the app
adb install C:\Users\NidhiChaure\apps\partner_app.apk

# Then configure with package name
APPIUM_APP_PACKAGE=com.partnerapp
APPIUM_APP_ACTIVITY=.MainActivity
```

### Option C: Fresh Install Each Test

```env
APPIUM_APP_PATH=C:\Users\NidhiChaure\apps\partner_app.apk
APPIUM_NO_RESET=false         # Fresh install before each test
```

---

## 🆘 Troubleshooting

### "File not found" Error

```bash
# Verify file exists
dir C:\Users\NidhiChaure\apps\partner_app.apk

# Check file permissions
icacls C:\Users\NidhiChaure\apps\partner_app.apk

# Get full path
Get-Item "C:\Users\NidhiChaure\apps\partner_app.apk" | Select-Object FullName
```

### "Invalid APK" Error

```bash
# Verify APK is not corrupted
adb install C:\Users\NidhiChaure\apps\partner_app.apk

# If install fails, APK is corrupted - get a fresh copy
```

### App Not Launching

```env
# Ensure automation name matches platform
APPIUM_PLATFORM=Android
APPIUM_AUTOMATION_NAME=UiAutomator2
```

### Path Format Error

```
❌ DON'T use: C:/Users/NidhiChaure/apps/partner_app.apk
✅ DO use: C:\Users\NidhiChaure\apps\partner_app.apk
```

---

## 📊 Quick Reference

| Scenario | Configuration |
|----------|---------------|
| **Local APK** | `APPIUM_APP_PATH=C:\...\app.apk` |
| **Local IPA** | `APPIUM_APP_PATH=/..../app.ipa` |
| **Pre-installed** | `APPIUM_APP_PACKAGE=com.app` |
| **Physical Device** | `APPIUM_UDID=R38R70ABC01` |
| **Emulator** | `APPIUM_DEVICE_NAME=emulator-5554` |

---

## 📁 File Organization

Create organized folder for your apps:

```
C:\Users\NidhiChaure\
├── apps/                    ← Create this folder
│   ├── partner_app.apk      ← Put your APK here
│   ├── partner_app-v1.apk
│   └── partner_app-v2.apk
├── PyCharmMiscProject/
│   └── partner_app_qa/
│       ├── .env             ← Update this with path
│       ├── config/
│       └── tests/
```

---

## ✨ Next Steps

1. ✅ Locate your `partner_app.apk` file
2. ✅ Copy `.env.example` to `.env`
3. ✅ Add your app path to `.env`:
   ```env
   APPIUM_APP_PATH=C:\path\to\your\partner_app.apk
   ```
4. ✅ Start Appium: `appium`
5. ✅ Run tests: `pytest tests/mobile/ -v`

---

## 📖 Related Files

- **config/settings.py** - Configuration classes
- **.env.example** - Configuration template
- **DEVICE_CONFIGURATION_GUIDE.md** - Device setup
- **core/appium_manager.py** - Appium driver setup

---

**Happy testing with your local app! 📱✨**
