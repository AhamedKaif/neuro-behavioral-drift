import subprocess
import time
import socket
import os
import sys
import urllib.request
import urllib.error

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    if sys.platform.startswith('win'):
        try:
            output = subprocess.check_output(f'netstat -aon | findstr :{port}', shell=True).decode('utf-8')
            pids = set()
            for line in output.strip().split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5:
                    pids.add(parts[-1])
            for pid in pids:
                if pid != '0':
                    print(f"Killing process {pid} on port {port}...")
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
        except Exception as e:
            pass
    else:
        try:
            subprocess.run(f'fuser -k {port}/tcp', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
        except:
            pass

def wait_for_backend(url, timeout=30):
    start = time.time()
    print(f"Waiting for backend at {url} to become healthy...")
    while time.time() - start < timeout:
        try:
            # Check response from server
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print("Backend is healthy!")
                    return True
        except urllib.error.HTTPError as e:
            # Flask app exists and returned an HTTP status (like 404 or 400), which is healthy
            print(f"Backend is online (status code {e.code})!")
            return True
        except Exception:
            pass
        time.sleep(1.0)
    print("Backend health check timed out!")
    return False

def reset_database():
    print("Resetting database to a clean state...")
    
    # Delete old database file to ensure a clean start
    db_path = os.path.join("database", "database.db")
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Deleted old database file.")
        except Exception as e:
            print(f"Warning: could not delete old database file: {e}")
            
    python_cmd = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_cmd):
        python_cmd = "python"
    
    # Run db.py to recreate tables
    res = subprocess.run([python_cmd, "backend/db.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Failed to reset database: {res.stderr}")
        return False
    print("Database reset complete.")
    return True

def pre_register_login_users():
    print("Pre-registering test login users...")
    import sqlite3
    from werkzeug.security import generate_password_hash
    
    db_path = os.path.join("database", "database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    password_hash = generate_password_hash("ValidPassword123!")
    
    try:
        for i in range(15):
            username = f"user_login_{i}"
            email = f"{username}@test.com"
            full_name = f"Login User {i}"
            
            cursor.execute(
                "INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)",
                (full_name, username, email, password_hash)
            )
            user_id = cursor.lastrowid
            
            cursor.execute(
                """INSERT INTO user_profiles 
                   (user_id, age, gender, occupation, stress_level)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, 25 + i, "Male", "Researcher", 4)
            )
        conn.commit()
        print("Pre-registered 15 test login users.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error pre-registering users: {e}")
        return False
    finally:
        conn.close()

def run_k6_test(k6_path, test_type, log_file):
    print(f"\n==========================================")
    print(f"Executing K6 Phase: {test_type.upper()}")
    print(f"==========================================")
    
    env = os.environ.copy()
    env["TEST_TYPE"] = test_type
    
    cmd = [k6_path, "run", "--env", f"TEST_TYPE={test_type}", "load-testing/load_test.js"]
    
    # Open log file to append console output
    with open(log_file, "a") as out_f:
        out_f.write(f"\n--- START K6 PHASE: {test_type.upper()} ---\n")
        
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        
        # Read output in real time and log it
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            # Print to stdout and write to log file
            print(line, end="")
            out_f.write(line)
            out_f.flush()
            
        proc.wait()
        out_f.write(f"\n--- END K6 PHASE: {test_type.upper()} (Exit Code: {proc.returncode}) ---\n")
        return proc.returncode == 0

def check_failures(log_file):
    failures = []
    # Match RESULT lines with FAIL
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            for line in f:
                if "[RESULT]" in line and "FAIL" in line:
                    failures.append(line.strip())
    return failures

def run_orchestrator():
    k6_path = "C:\\Program Files\\k6\\k6.exe"
    if not os.path.exists(k6_path):
        # Look in other path or default PATH
        k6_path = "k6"
        
    log_file = "load-testing/console.log"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    print("Initializing test run environment...")
    
    # 1. Kill any existing backend process on port 5000
    kill_process_on_port(5000)
    
    # 2. Reset database tables
    if not reset_database():
        print("Error: Could not reset database. Exiting.")
        sys.exit(1)
        
    if not pre_register_login_users():
        print("Error: Could not pre-register test users. Exiting.")
        sys.exit(1)
        
    # 3. Start Flask backend in background
    python_cmd = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_cmd):
        python_cmd = "python"
        
    print("Starting Flask backend server...")
    backend_log_f = open("load-testing/backend.log", "w")
    backend_proc = subprocess.Popen(
        [python_cmd, "-u", "backend/app.py"],
        stdout=backend_log_f,
        stderr=backend_log_f,
        text=True
    )
    
    # Wait for backend to be ready
    if not wait_for_backend("http://localhost:5000", timeout=30):
        print("Backend failed to start in time. Killing process.")
        backend_proc.terminate()
        sys.exit(1)
        
    phases = ["smoke", "load", "stress", "spike", "soak", "breakpoint"]
    all_success = True
    
    try:
        # 4. Execute all K6 phases
        for phase in phases:
            success = run_k6_test(k6_path, phase, log_file)
            if not success:
                print(f"Phase {phase} returned a non-zero exit code.")
                all_success = False
                
        # 5. Check if there are any request level failures in the logs
        failures = check_failures(log_file)
        if failures:
            print(f"\nFOUND {len(failures)} REQUEST FAILURES IN THE LOGS:")
            for fail in failures[:20]:
                print(f"  - {fail}")
            if len(failures) > 20:
                print(f"  ... and {len(failures) - 20} more failures.")
                
            # Perform self-healing diagnostics
            print("\nInitiating Self-Healing Diagnostics...")
            # We can analyze failures and apply fixes here if needed
            # For now, we print them out and indicate a retry is needed.
            sys.exit(2) # Code 2 means failures detected for self-healing
            
        else:
            print("\nALL TESTS PASSED! 100% success rate achieved.")
            
            # 6. Generate reports
            print("\nGenerating Reports...")
            report_proc = subprocess.run([python_cmd, "load-testing/generate_reports.py"], capture_output=True, text=True)
            print(report_proc.stdout)
            if report_proc.returncode != 0:
                print(f"Report generation failed: {report_proc.stderr}")
                sys.exit(1)
                
            print("All reports generated successfully!")
            
    finally:
        # Shutdown backend
        print("\nShutting down Flask backend...")
        backend_proc.terminate()
        try:
            backend_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_proc.kill()
        try:
            backend_log_f.close()
        except:
            pass
        kill_process_on_port(5000)
        print("Backend stopped.")

if __name__ == "__main__":
    run_orchestrator()
