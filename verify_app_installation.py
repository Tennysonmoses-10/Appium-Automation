#!/usr/bin/env python3
"""
Verification script for local app installation.
Run this to verify your app is properly configured and installed.

Usage:
    python verify_app_installation.py
"""

import os
import subprocess
import sys
import socket
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)

def print_success(text):
    """Print success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print error message."""
    print(f"✗ {text}")

def print_info(text):
    """Print info message."""
    print(f"ℹ {text}")

def step_1_verify_apk_file():
    """Step 1: Verify APK file exists."""
    print("\n[STEP 1] Checking if APK file exists...")
    
    try:
        from config.settings import settings
        app_path = settings.appium.app_path
        
        if not app_path:
            print_error("APPIUM_APP_PATH not configured in .env")
            return False
        
        if os.path.exists(app_path):
            file_size = os.path.getsize(app_path) / (1024 * 1024)  # MB
            print_success(f"APK file found: {app_path}")
            print_success(f"File size: {file_size:.2f} MB")
            
            if file_size < 1:
                print_error("APK file is too small (< 1 MB) - might be corrupted")
                return False
            
            return True
        else:
            print_error(f"APK file NOT found: {app_path}")
            print_info("Please check the file path and ensure it exists")
            return False
    
    except Exception as e:
        print_error(f"Error checking APK: {e}")
        return False

def step_2_verify_device_connection():
    """Step 2: Verify device connection."""
    print("\n[STEP 2] Checking device connection...")
    
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output_lines = result.stdout.strip().split('\n')[1:]
        connected_devices = [line.split()[0] for line in output_lines if 'device' in line and 'attached' not in line]
        
        if connected_devices:
            print_success(f"Devices connected: {connected_devices}")
            return True
        else:
            print_error("No devices connected")
            print_info("Make sure device is connected via USB and USB debugging is enabled")
            print_info("Commands: adb kill-server && adb start-server && adb devices")
            return False
    
    except FileNotFoundError:
        print_error("ADB not found - please install Android SDK Platform Tools")
        return False
    except Exception as e:
        print_error(f"Error checking devices: {e}")
        return False

def step_3_verify_app_installation():
    """Step 3: Verify app is installed on device."""
    print("\n[STEP 3] Checking if app is installed on device...")
    
    try:
        from config.settings import settings
        
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        installed_packages = result.stdout.split('\n')
        app_package = settings.appium.app_package
        
        if app_package:
            app_installed = any(app_package in pkg for pkg in installed_packages)
            
            if app_installed:
                print_success(f"App installed: {app_package}")
                
                # Get app version
                try:
                    version_result = subprocess.run(
                        ["adb", "shell", "dumpsys", "package", app_package],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    for line in version_result.stdout.split('\n'):
                        if 'versionName=' in line or 'versionCode=' in line:
                            print_info(line.strip())
                except:
                    pass
                
                return True
            else:
                print_info(f"App not yet installed: {app_package}")
                print_info("This is OK - Appium will install it automatically")
                return True  # Not a failure
        else:
            print_error("App package not configured")
            return False
    
    except Exception as e:
        print_error(f"Error checking app: {e}")
        return False

def step_4_verify_configuration():
    """Step 4: Verify configuration."""
    print("\n[STEP 4] Checking configuration...")
    
    try:
        from config.settings import settings
        
        print_success(f"App Path: {settings.appium.app_path}")
        print_success(f"Device Name: {settings.appium.device_name}")
        print_success(f"Platform: {settings.appium.platform}")
        print_success(f"App Package: {settings.appium.app_package}")
        print_success(f"App Activity: {settings.appium.app_activity}")
        print_success(f"Appium Server: {settings.appium.server_url}")
        print_success(f"Timeout: {settings.appium.timeout}s")
        print_success(f"Implicit Wait: {settings.appium.implicit_wait}s")
        print_success(f"Explicit Wait: {settings.appium.explicit_wait}s")
        
        return True
    
    except Exception as e:
        print_error(f"Error checking configuration: {e}")
        return False

def step_5_check_appium_server():
    """Step 5: Check if Appium server is running."""
    print("\n[STEP 5] Checking Appium server...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 4723))
        sock.close()
        
        if result == 0:
            print_success("Appium server is running on http://localhost:4723")
            return True
        else:
            print_error("Appium server NOT running on port 4723")
            print_info("Start it with: appium")
            return False
    
    except Exception as e:
        print_error(f"Error checking Appium: {e}")
        return False

def main():
    """Main verification function."""
    print_header("APP INSTALLATION VERIFICATION")
    
    results = {
        "APK File": step_1_verify_apk_file(),
        "Device Connection": step_2_verify_device_connection(),
        "App Installation": step_3_verify_app_installation(),
        "Configuration": step_4_verify_configuration(),
        "Appium Server": step_5_check_appium_server(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = True
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check}: {status}")
        if not result and check != "Appium Server":  # Appium server is optional
            all_passed = False
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can now run your mobile tests:")
        print("  pytest tests/mobile/ -v")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running tests")
        print("\nTroubleshooting:")
        print("  1. Check APK file path in .env")
        print("  2. Connect device: adb devices")
        print("  3. Install app: adb install app.apk")
        print("  4. Start Appium: appium")
    
    print("="*70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
