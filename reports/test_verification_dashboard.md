# 🧪 HealthSense AI Unified Test Verification Dashboard

This dashboard presents a unified summary of E2E tests and security scans across all major components: Website, Mobile App, and Backend.

## 📊 Unified Summary Overview

| Component | Test Suite / Report | Total Tests | Passed / Fixed | Failed / Open | Pass/Fix Rate | Duration |
|-----------|--------------------|-------------|----------------|---------------|---------------|----------|
| **Website E2E** | Neuro Behavioral Drift Web App - Full E2E Workflow | 58 | ✅ 52 | ❌ 6 | 90% | 0.0s |
| **Mobile E2E** | HealthSense AI - Full Appium E2E Automation | 120 | ✅ 120 | ❌ 0 | 100.0% | 166.07 seconds |
| **Backend Security** | HealthSense AI — Security Vulnerability Report | 22 | ✅ 22 | 📄 0 | 100% | N/A |

## 🌐 Website E2E Test Verification Details

<details>
<summary>Click to view Website E2E Test Cases (58 tests)</summary>

| No. | Category | Test Name | Status | Error Details |
|-----|----------|-----------|--------|---------------|
| 1 | Navigation Page | `test_unauthenticated_navigation` | ✅ PASSED | None — test passed successfully. |
| 2 | Navigation Page | `test_navigation_links` | ✅ PASSED | None — test passed successfully. |
| 3 | Login Page | `test_valid_login` | ✅ PASSED | None — test passed successfully. |
| 4 | Login Page | `test_invalid_password` | ✅ PASSED | None — test passed successfully. |
| 5 | Login Page | `test_invalid_username` | ✅ PASSED | None — test passed successfully. |
| 6 | Login Page | `test_login_empty_fields` | ✅ PASSED | None — test passed successfully. |
| 7 | Login Page | `test_valid_login` | ✅ PASSED | None — test passed successfully. |
| 8 | Login Page | `test_invalid_password` | ✅ PASSED | None — test passed successfully. |
| 9 | Login Page | `test_invalid_username` | ✅ PASSED | None — test passed successfully. |
| 10 | Login Page | `test_login_empty_fields` | ✅ PASSED | None — test passed successfully. |
| 11 | Login Page | `test_provided_credentials` | ✅ PASSED | None — test passed successfully. |
| 12 | Logout Page | `test_logout` | ✅ PASSED | None — test passed successfully. |
| 13 | Settings Page | `test_model_telemetry_loads` | ✅ PASSED | None — test passed successfully. |
| 14 | E2E Page | `test_full_e2e_flow` | ✅ PASSED | None — test passed successfully. |
| 15 | Navigation Page | `test_unauthenticated_navigation` | ✅ PASSED | None — test passed successfully. |
| 16 | Navigation Page | `test_navigation_links` | ✅ PASSED | None — test passed successfully. |
| 17 | Settings Page | `test_model_telemetry_loads` | ✅ PASSED | None — test passed successfully. |
| 18 | Dashboard Page | `test_dashboard_loads` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@placeholder='Enter username']"}
  (Session info: chrome=149.0.7827.114); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#nosuchelementexception
Stacktrace:
#0 0x5624da87380a <unknown>
#1 0x5624da256289 <unknown>
#2 0x5624da2aa9b4 <unknown>
#3 0x5624da2aac01 <unknown>
#4 0x5624da2f5874 <unknown>
#5 0x5624da2f2a4c <unknown>
#6 0x5624da29df7f <unknown>
#7 0x5624da29ed61 <unknown>
#8 0x5624da83a0f7 <unknown>
#9 0x5624da8388bd <unknown>
#10 0x5624da8235a6 <unknown>
#11 0x5624da83949a <unknown>
#12 0x5624da80b560 <unknown>
#13 0x5624da860288 <unknown>
#14 0x5624da860425 <unknown>
#15 0x5624da87238e <unknown>
#16 0x7f419d69caa4 <unknown>
#17 0x7f419d729c6c <unknown> |
| 19 | Dashboard Page | `test_user_profile_display` | ✅ PASSED | None — test passed successfully. |
| 20 | Dashboard Page | `test_dashboard_stats_exist` | ✅ PASSED | None — test passed successfully. |
| 21 | Dashboard Page | `test_retrain_model_button` | ✅ PASSED | None — test passed successfully. |
| 22 | Dashboard Page | `test_dashboard_loads` | ✅ PASSED | None — test passed successfully. |
| 23 | Dashboard Page | `test_user_profile_display` | ✅ PASSED | None — test passed successfully. |
| 24 | Dashboard Page | `test_dashboard_stats_exist` | ✅ PASSED | None — test passed successfully. |
| 25 | Dashboard Page | `test_analytics_charts_rendering` | ✅ PASSED | None — test passed successfully. |
| 26 | Dashboard Page | `test_retrain_model_button` | ✅ PASSED | None — test passed successfully. |
| 27 | Profile Page | `test_profile_loads` | ✅ PASSED | None — test passed successfully. |
| 28 | Profile Page | `test_edit_profile` | ✅ PASSED | None — test passed successfully. |
| 29 | Profile Page | `test_profile_loads` | ❌ FAILED | assert 'Profile Management' in '<html lang="en"><head>     <script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>      <script type="module" src="/@vite/client"></script>      <meta charset="UTF-8">     <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,&lt;svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22 width=%22100%22 height=%22100%22&gt;&lt;text y=%220.9em%22 font-size=%2290%22&gt;🧠&lt;/text&gt;&lt;/svg&gt;">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>Neuro-Behavioral Drift   Cognitive Strain Monitor</title>     <!-- Google Fonts -->     <link rel="preconnect" href="https://fonts.googleapis.com">     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">     <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet">   <style type="text/css" data-vite-dev-id="/home/runner/work/neuro-behavioral-drift/neuro-behavioral-drift/frontend/src/index.css">*, ::before, ::after { ..." class="lucide lucide-bell h-5 w-5"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path></svg></a><a class="flex items-center gap-2 bg-slate-900 border border-slate-800/80 rounded-xl px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white hover:border-slate-700 transition-colors" href="/profile"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user h-3.5 w-3.5 text-accentBlue"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span>Test User</span></a></div></div></header><main class="flex-grow w-full"><div class="flex justify-center items-center h-64 text-slate-400">Loading Profile...</div></main><footer class="border-t border-slate-900 bg-slate-950/20 py-4 text-center text-xs text-slate-600"><div class="container mx-auto">© 2026 Neuro-Behavioral Drift Modeling Platform. Local secure processing sandbox active.</div></footer></div></div>     <script type="module" src="/src/main.jsx"></script>     </body></html>'
 +  where '<html lang="en"><head>     <script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>      <script type="module" src="/@vite/client"></script>      <meta charset="UTF-8">     <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,&lt;svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22 width=%22100%22 height=%22100%22&gt;&lt;text y=%220.9em%22 font-size=%2290%22&gt;🧠&lt;/text&gt;&lt;/svg&gt;">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>Neuro-Behavioral Drift   Cognitive Strain Monitor</title>     <!-- Google Fonts -->     <link rel="preconnect" href="https://fonts.googleapis.com">     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">     <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet">   <style type="text/css" data-vite-dev-id="/home/runner/work/neuro-behavioral-drift/neuro-behavioral-drift/frontend/src/index.css">*, ::before, ::after { ..." class="lucide lucide-bell h-5 w-5"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path></svg></a><a class="flex items-center gap-2 bg-slate-900 border border-slate-800/80 rounded-xl px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white hover:border-slate-700 transition-colors" href="/profile"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user h-3.5 w-3.5 text-accentBlue"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span>Test User</span></a></div></div></header><main class="flex-grow w-full"><div class="flex justify-center items-center h-64 text-slate-400">Loading Profile...</div></main><footer class="border-t border-slate-900 bg-slate-950/20 py-4 text-center text-xs text-slate-600"><div class="container mx-auto">© 2026 Neuro-Behavioral Drift Modeling Platform. Local secure processing sandbox active.</div></footer></div></div>     <script type="module" src="/src/main.jsx"></script>     </body></html>' = <selenium.webdriver.chrome.webdriver.WebDriver (session="89473804dc02ff02337d94e78dd4fb18")>.page_source |
| 30 | Profile Page | `test_edit_profile` | ✅ PASSED | None — test passed successfully. |
| 31 | Prediction Page | `test_transmit_metrics_success` | ✅ PASSED | None — test passed successfully. |
| 32 | Prediction Page | `test_cognitive_strain_prediction` | ✅ PASSED | None — test passed successfully. |
| 33 | Prediction Page | `test_behavioral_drift_score` | ✅ PASSED | None — test passed successfully. |
| 34 | Notifications Page | `test_notification_bell_presence` | ✅ PASSED | None — test passed successfully. |
| 35 | Notifications Page | `test_medium_strain_notification_generation` | ✅ PASSED | None — test passed successfully. |
| 36 | Notifications Page | `test_notifications_history_page` | ✅ PASSED | None — test passed successfully. |
| 37 | Notifications Page | `test_delete_notification` | ✅ PASSED | None — test passed successfully. |
| 38 | Registration Page | `test_valid_registration` | ✅ PASSED | None — test passed successfully. |
| 39 | Registration Page | `test_registration_existing_user` | ✅ PASSED | None — test passed successfully. |
| 40 | Registration Page | `test_registration_empty_fields` | ✅ PASSED | None — test passed successfully. |
| 41 | Responsive Page | `test_responsive_layout` | ✅ PASSED | None — test passed successfully. |
| 42 | Routing Page | `test_protected_route_redirect` | ✅ PASSED | None — test passed successfully. |
| 43 | Routing Page | `test_unknown_route_redirect` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: |
| 44 | Notifications Page | `test_notification_bell_presence` | ✅ PASSED | None — test passed successfully. |
| 45 | Notifications Page | `test_medium_strain_notification_generation` | ✅ PASSED | None — test passed successfully. |
| 46 | Notifications Page | `test_notifications_history_page` | ✅ PASSED | None — test passed successfully. |
| 47 | Notifications Page | `test_delete_notification` | ✅ PASSED | None — test passed successfully. |
| 48 | Prediction Page | `test_transmit_metrics_success` | ✅ PASSED | None — test passed successfully. |
| 49 | Prediction Page | `test_cognitive_strain_prediction` | ✅ PASSED | None — test passed successfully. |
| 50 | Prediction Page | `test_behavioral_drift_score` | ✅ PASSED | None — test passed successfully. |
| 51 | E2E Page | `test_full_e2e_flow` | ❌ FAILED | selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="fullName"]"}
  (Session info: chrome=149.0.7827.114); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#nosuchelementexception
Stacktrace:
#0 0x55b2bc18480a <unknown>
#1 0x55b2bbb67289 <unknown>
#2 0x55b2bbbbb9b4 <unknown>
#3 0x55b2bbbbbc01 <unknown>
#4 0x55b2bbc06874 <unknown>
#5 0x55b2bbc03a4c <unknown>
#6 0x55b2bbbaef7f <unknown>
#7 0x55b2bbbafd61 <unknown>
#8 0x55b2bc14b0f7 <unknown>
#9 0x55b2bc1498bd <unknown>
#10 0x55b2bc1345a6 <unknown>
#11 0x55b2bc14a49a <unknown>
#12 0x55b2bc11c560 <unknown>
#13 0x55b2bc171288 <unknown>
#14 0x55b2bc171425 <unknown>
#15 0x55b2bc18338e <unknown>
#16 0x7f4c8a69caa4 <unknown>
#17 0x7f4c8a729c6c <unknown> |
| 52 | Registration Page | `test_valid_registration` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: |
| 53 | Registration Page | `test_registration_existing_user` | ❌ FAILED | selenium.common.exceptions.TimeoutException: Message: |
| 54 | Registration Page | `test_registration_empty_fields` | ✅ PASSED | None — test passed successfully. |
| 55 | Logout Page | `test_logout` | ✅ PASSED | None — test passed successfully. |
| 56 | Routing Page | `test_protected_route_redirect` | ✅ PASSED | None — test passed successfully. |
| 57 | Routing Page | `test_unknown_route_redirect` | ✅ PASSED | None — test passed successfully. |
| 58 | Responsive Page | `test_responsive_layout` | ✅ PASSED | None — test passed successfully. |

</details>

## 📱 Mobile App E2E Test Verification Details

<details>
<summary>Click to view Mobile E2E Test Cases (120 tests)</summary>

*(List truncated for brevity in Web summary)*

</details>

## 🛡️ Backend Security Scan Details

*(List truncated for brevity in Web summary)*
