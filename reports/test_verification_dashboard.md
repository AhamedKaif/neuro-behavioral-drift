# 🧪 HealthSense AI Unified Test Verification Dashboard

This dashboard presents a unified summary of E2E tests and security scans across all major components: Website, Mobile App, and Backend.

## 📊 Unified Summary Overview

| Component | Test Suite / Report | Total Tests | Passed / Fixed | Failed / Open | Pass/Fix Rate | Duration |
|-----------|--------------------|-------------|----------------|---------------|---------------|----------|
| **Website E2E** | Neuro Behavioral Drift Web App - Full E2E Workflow | 29 | ✅ 0 | ❌ 29 | 0% | 592.1s |
| **Mobile E2E** | HealthSense AI - Full Appium E2E Automation | 120 | ✅ 120 | ❌ 0 | 100.0% | 166.07 seconds |
| **Backend Security** | HealthSense AI — Security Vulnerability Report | 22 | ✅ 22 | 📄 0 | 100% | N/A |

## 🌐 Website E2E Test Verification Details

<details>
<summary>Click to view Website E2E Test Cases (29 tests)</summary>

| No. | Category | Test Name | Status | Error Details |
|-----|----------|-----------|--------|---------------|
| 1 | Dashboard Page | `test_dashboard_loads` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 2 | Dashboard Page | `test_user_profile_display` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 3 | Dashboard Page | `test_dashboard_stats_exist` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 4 | Dashboard Page | `test_analytics_charts_rendering` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 5 | Dashboard Page | `test_retrain_model_button` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 6 | E2E Page | `test_full_e2e_flow` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: 
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 7 | Login Page | `test_valid_login` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 8 | Login Page | `test_invalid_password` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 9 | Login Page | `test_invalid_username` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@placeholder='Enter username']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 10 | Login Page | `test_login_empty_fields` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//button[@type='submit']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 11 | Logout Page | `test_logout` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 12 | Navigation Page | `test_unauthenticated_navigation` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: |
| 13 | Navigation Page | `test_navigation_links` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 14 | Notifications Page | `test_notification_bell_presence` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 15 | Notifications Page | `test_medium_strain_notification_generation` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 16 | Notifications Page | `test_notifications_history_page` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 17 | Notifications Page | `test_delete_notification` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 18 | Prediction Page | `test_transmit_metrics_success` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 19 | Prediction Page | `test_cognitive_strain_prediction` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 20 | Prediction Page | `test_behavioral_drift_score` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 21 | Profile Page | `test_profile_loads` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 22 | Profile Page | `test_edit_profile` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 23 | Registration Page | `test_valid_registration` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 24 | Registration Page | `test_registration_existing_user` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 25 | Registration Page | `test_registration_empty_fields` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//button[@type='submit']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 26 | Responsive Page | `test_responsive_layout` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 27 | Routing Page | `test_protected_route_redirect` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: |
| 28 | Routing Page | `test_unknown_route_redirect` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |
| 29 | Settings Page | `test_model_telemetry_loads` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@name='full_name']"}
  (Session info: chrome=149.0.7827.103); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Stacktrace:
	chromedriver!GetHandleVerifier [0x7ff6b6823fa5+14925]
	chromedriver!GetHandleVerifier [0x7ff6b6824000+14980]
	chromedriver!(No symbol) [0x7ff6b636793d]
	chromedriver!(No symbol) [0x7ff6b63c1aad]
	chromedriver!(No symbol) [0x7ff6b63c1dac]
	chromedriver!(No symbol) [0x7ff6b64127d7]
	chromedriver!(No symbol) [0x7ff6b640f39b]
	chromedriver!(No symbol) [0x7ff6b63b401c]
	chromedriver!(No symbol) [0x7ff6b63b4f43]
	chromedriver!GetHandleVerifier [0x7ff6b6e07591+5f7f11]
	chromedriver!GetHandleVerifier [0x7ff6b6e01902+5f2282]
	chromedriver!GetHandleVerifier [0x7ff6b6e27115+617a95]
	chromedriver!GetHandleVerifier [0x7ff6b6841dce+3274e]
	chromedriver!GetHandleVerifier [0x7ff6b684a82c+3b1ac]
	chromedriver!GetHandleVerifier [0x7ff6b682d744+1e0c4]
	chromedriver!GetHandleVerifier [0x7ff6b682d8d4+1e254]
	chromedriver!GetHandleVerifier [0x7ff6b6811447+1dc7]
	KERNEL32!BaseThreadInitThunk [0x7ffaf51ee957+17]
	ntdll!RtlUserThreadStart [0x7ffaf68aad6c+2c] |

</details>

## 📱 Mobile App E2E Test Verification Details

<details>
<summary>Click to view Mobile E2E Test Cases (120 tests)</summary>

*(List truncated for brevity in Web summary)*

</details>

## 🛡️ Backend Security Scan Details

*(List truncated for brevity in Web summary)*
