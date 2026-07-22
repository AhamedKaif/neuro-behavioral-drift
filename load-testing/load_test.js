import { SharedArray } from 'k6/data';
import http from 'k6/http';
import { check, group } from 'k6';
import { Trend, Counter } from 'k6/metrics';

// Load generated scenarios
const scenariosData = new SharedArray('scenarios', function () {
  return JSON.parse(open('./scenarios.json'));
});

// Custom metrics
const responseTimeMetric = new Trend('custom_response_time');
const passCounter = new Counter('custom_pass_count');
const failCounter = new Counter('custom_fail_count');

// Test configuration from environment
const testType = __ENV.TEST_TYPE || 'smoke';
const targetUrl = __ENV.TARGET_URL || 'http://localhost:5000';

export const options = {
  thresholds: {
    checks: ['rate==1.0'], // 100% of validation checks must pass
  },
};

// Define K6 stages based on test phase
if (testType === 'smoke') {
  options.scenarios = {
    smoke_test: {
      executor: 'per-vu-iterations',
      vus: 1,
      iterations: scenariosData.length,
      maxDuration: '1m',
    },
  };
} else if (testType === 'load') {
  options.stages = [
    { duration: '10s', target: 20 },
    { duration: '20s', target: 20 },
    { duration: '10s', target: 0 },
  ];
} else if (testType === 'stress') {
  options.stages = [
    { duration: '10s', target: 50 },
    { duration: '20s', target: 100 },
    { duration: '10s', target: 0 },
  ];
} else if (testType === 'spike') {
  options.stages = [
    { duration: '10s', target: 150 },
    { duration: '15s', target: 150 },
    { duration: '10s', target: 0 },
  ];
} else if (testType === 'soak') {
  options.stages = [
    { duration: '10s', target: 25 },
    { duration: '40s', target: 25 },
    { duration: '10s', target: 0 },
  ];
} else if (testType === 'breakpoint') {
  options.stages = [
    { duration: '45s', target: 200 },
  ];
}

// Setup runs once, registers/logins the test users to establish auth tokens
export function setup() {
  const registerUrl = `${targetUrl}/api/auth/register`;
  const loginUrl = `${targetUrl}/api/auth/login`;
  const headers = { 'Content-Type': 'application/json' };

  // 1. Setup a main user for requests that require auth
  const mainUsername = `main_test_user_${Math.floor(Math.random() * 100000)}`;
  const mainEmail = `${mainUsername}@test.com`;
  
  let mainPayload = JSON.stringify({
    full_name: 'Main Load User',
    username: mainUsername,
    email: mainEmail,
    password: 'ValidPassword123!',
    age: 30,
    gender: 'Female',
    occupation: 'Developer',
    stress_level: 5
  });

  let token = '';
  let regRes = http.post(registerUrl, mainPayload, { headers, timeout: '120s' });
  if (regRes.status === 201) {
    token = regRes.json().token;
  } else {
    let loginRes = http.post(loginUrl, JSON.stringify({ username: mainUsername, password: 'ValidPassword123!' }), { headers, timeout: '120s' });
    if (loginRes.status === 200) {
      token = loginRes.json().token;
    }
  }

  return { token: token };
}

export default function (data) {
  // Select scenario
  let index;
  if (testType === 'smoke') {
    index = __ITER;
  } else {
    // Random distribution for concurrency load
    index = Math.floor(Math.random() * scenariosData.length);
  }

  if (index >= scenariosData.length) return;
  const scenario = scenariosData[index];

  const url = `${targetUrl}${scenario.api}`;
  const method = scenario.method;
  
  // Setup headers
  let headers = { 'Content-Type': 'application/json' };
  let tokenToUse = data.token;

  if (scenario.api === '/api/profile/account' && method === 'DELETE' && scenario.requires_auth) {
    const tempUsername = `temp_del_${Math.floor(Math.random() * 10000000)}`;
    const tempPayload = JSON.stringify({
      full_name: 'Temp Delete User',
      username: tempUsername,
      email: `${tempUsername}@test.com`,
      password: 'ValidPassword123!',
      age: 25,
      gender: 'Male',
      occupation: 'Student',
      stress_level: 5
    });
    
    let regRes = http.post(`${targetUrl}/api/auth/register`, tempPayload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: '120s'
    });
    
    if (regRes.status === 201) {
      tokenToUse = regRes.json().token;
    } else {
      tokenToUse = "invalid_fallback_token_to_protect_main_user";
    }
  }
  
  if (scenario.requires_auth && tokenToUse) {
    headers['Authorization'] = `Bearer ${tokenToUse}`;
  }
  
  if (scenario.headers) {
    Object.assign(headers, scenario.headers);
  }

  let payload = null;
  if (scenario.payload) {
    let payloadObj = Object.assign({}, scenario.payload);
    if (scenario.api === '/api/auth/register' && payloadObj.username) {
      const rand = Math.floor(Math.random() * 1000000);
      payloadObj.username = `${payloadObj.username}_${rand}`;
      if (payloadObj.email) {
        payloadObj.email = payloadObj.email.replace('@', `_${rand}@`);
      }
    }
    payload = JSON.stringify(payloadObj);
  }

  // For GET requests, append query parameters if present
  let requestUrl = url;
  if (scenario.params) {
    const query = Object.keys(scenario.params)
      .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(scenario.params[k])}`)
      .join('&');
    requestUrl = `${url}?${query}`;
  }

  // Send request
  let res;
  const startTime = Date.now();
  
  if (method === 'GET') {
    res = http.get(requestUrl, { headers, timeout: '120s' });
  } else if (method === 'POST') {
    res = http.post(requestUrl, payload, { headers, timeout: '120s' });
  } else if (method === 'PUT') {
    res = http.put(requestUrl, payload, { headers, timeout: '120s' });
  } else if (method === 'DELETE') {
    res = http.del(requestUrl, payload, { headers, timeout: '120s' });
  }

  const duration = Date.now() - startTime;
  
  // Record metrics
  responseTimeMetric.add(duration);

  // Validate expectations
  const isStatusCorrect = res.status === scenario.expected_status;
  
  let isPassed = isStatusCorrect;
  let errMsg = '';
  
  if (!isStatusCorrect) {
    errMsg = `Expected status ${scenario.expected_status}, got ${res.status}`;
    // If the server returns 500 or crash, log details
    if (res.status >= 500) {
      errMsg += ` | Server Error: ${res.body ? res.body.substring(0, 100) : 'None'}`;
    }
  }

  if (isPassed) {
    passCounter.add(1);
  } else {
    failCounter.add(1);
  }

  // Log execution result line for post-processing
  const resultStr = isPassed ? 'PASS' : 'FAIL';
  console.log(`[RESULT] ${scenario.id} | ${res.status} | ${duration} | ${__VU} | ${resultStr} | ${errMsg} | ${Date.now()}`);

  // Also include K6 built-in assertion checks
  check(res, {
    'Status matches expectation': (r) => r.status === scenario.expected_status,
  });
}
