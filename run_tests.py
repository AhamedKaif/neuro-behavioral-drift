import subprocess
import os
import sys

# Add root folder to path so we can import the scripts
sys.path.append(os.path.abspath('.'))

from aggregate_test_reports import aggregate_reports
from generate_selenium_report import generate_report

test_files = [
    "tests/test_comprehensive.py"
]

def run_tests():
    print("Starting E2E Selenium Automation Testing...")
    os.makedirs("reports/logs", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    
    any_failed = False
    
    for tf in test_files:
        name = os.path.basename(tf).replace(".py", "")
        json_report = f"reports/report_{name}.json"
        html_report = f"reports/report_{name}.html"
        xml_report = f"reports/junit_{name}.xml"
        log_file = f"reports/logs/{name}.log"
        
        cmd = [
            "pytest",
            tf,
            "-v",
            f"--html={html_report}",
            "--self-contained-html",
            f"--junitxml={xml_report}",
            "--json-report",
            f"--json-report-file={json_report}"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        with open(log_file, "w") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
            print(f"Finished {tf} with exit code {result.returncode}")
            if result.returncode != 0:
                any_failed = True

    print("Aggregating reports...")
    try:
        aggregate_reports()
    except Exception as e:
        print(f"Failed to aggregate reports: {e}")
        any_failed = True
    
    print("Generating Excel sheet final report...")
    try:
        generate_report()
    except Exception as e:
        print(f"Failed to generate final Excel report: {e}")
        any_failed = True
    
    if any_failed:
        print("Some tests failed!")
        sys.exit(1)
    else:
        print("All tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
