import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 100,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<1500'], // 95% of requests must complete below 1.5s (1500ms)
  },
};

const BASE_URL = 'http://localhost:5000';

// Setup function runs once before tests begin to create a test user and obtain a JWT token.
export function setup() {
  const uniqueId = Math.floor(Math.random() * 1000000);
  const username = `loadtest_${uniqueId}`;
  const password = 'Password123!';
  const email = `loadtest_${uniqueId}@example.com`;

  const registerPayload = JSON.stringify({
    full_name: 'Load Test User',
    username: username,
    email: email,
    password: password,
    age: 25,
    gender: 'Other',
    occupation: 'Software Developer',
    institution: 'LoadTest Corp',
    department: 'QA',
    academic_year: 'N/A',
    working_hours: 8,
    avg_screen_time: 6,
    avg_sleep_hours: 7,
    preferred_work_time: 'Morning',
    stress_level: 5
  });

  const registerHeaders = { 'Content-Type': 'application/json' };
  const registerRes = http.post(`${BASE_URL}/api/auth/register`, registerPayload, { headers: registerHeaders });
  
  let token = '';
  if (registerRes.status === 201) {
    const body = JSON.parse(registerRes.body);
    token = body.token;
  } else {
    // If registration fails/user already exists, log in
    const loginPayload = JSON.stringify({ username, password });
    const loginRes = http.post(`${BASE_URL}/api/auth/login`, loginPayload, { headers: registerHeaders });
    if (loginRes.status === 200) {
      const body = JSON.parse(loginRes.body);
      token = body.token;
    }
  }

  return { token };
}

// The main loop that every Virtual User (VU) executes concurrently
export default function (data) {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${data.token}`
  };

  // 1. Get Dashboard Data
  const dashboardRes = http.get(`${BASE_URL}/api/dashboard`, { headers });
  check(dashboardRes, {
    'dashboard status is 200': (r) => r.status === 200,
  });

  // 2. Get User Profile
  const profileRes = http.get(`${BASE_URL}/api/profile`, { headers });
  check(profileRes, {
    'profile status is 200': (r) => r.status === 200,
  });

  // 3. Ingest Behavioral Metrics (simulating random metrics)
  const metricsPayload = JSON.stringify({
    screen_time: parseFloat((Math.random() * 8 + 1).toFixed(2)),
    typing_speed: parseFloat((Math.random() * 80 + 30).toFixed(2)),
    typing_error_rate: parseFloat((Math.random() * 0.1).toFixed(4)),
    session_duration: parseFloat((Math.random() * 120 + 10).toFixed(2)),
    click_frequency: parseFloat((Math.random() * 5 + 0.5).toFixed(2)),
    break_frequency: parseFloat((Math.random() * 3).toFixed(2)),
    mouse_speed: parseFloat((Math.random() * 300 + 50).toFixed(2))
  });

  const metricsRes = http.post(`${BASE_URL}/api/metrics`, metricsPayload, { headers });
  check(metricsRes, {
    'metrics ingestion status is 201': (r) => r.status === 201,
  });

  // Pacing: wait between 100ms and 500ms before sending the next set of requests
  sleep(Math.random() * 0.4 + 0.1);
}
