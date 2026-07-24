# Jenkins mobile pipeline

The pipeline in `jenkins/Jenkinsfile` runs the Android Behave suite on a
Windows Jenkins agent and publishes JUnit, Allure, logs, screenshots, and
screen recordings.

## One-time Jenkins configuration

1. Give the Windows agent access to Java, Node.js, Appium 2 with the
   UiAutomator2 driver, Android SDK platform tools, and an Android emulator.
2. Install the Jenkins Pipeline, Git, JUnit, and Allure plugins.
3. Configure the Allure command-line installation under **Manage Jenkins >
   Tools**.
4. Create a **Pipeline script from SCM** job:
   - SCM: Git
   - Branch: `*/main`
   - Script path: `jenkins/Jenkinsfile`
5. Ensure the account running the Jenkins Windows service can read:
   - the APK selected by `APK_PATH`
   - the AVD selected by `AVD_NAME`
   - the Android SDK and npm directories declared in the Jenkinsfile

The current workstation defaults are included as build parameters. Change
those defaults when the job moves to another Windows agent.

## Build parameters

- `TEST_TAGS`: Behave tag expression, such as `smoke` or `invalidotp`
- `DEVICE_TARGET`: `emulator` or `real`
- `APK_PATH`: absolute APK path on the agent
- `AVD_NAME`: AVD used for emulator builds
- `DEVICE_UDID`: adb serial, such as `emulator-5556`
- `APP_PACKAGE` and `APP_ACTIVITY`: Android launch component

Only one build runs at a time because Android and Appium use shared local
resources. The pipeline shuts down the Appium listener and any emulator it
started during cleanup.
