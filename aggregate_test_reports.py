import json
import glob
import os

def aggregate_reports():
    reports_dir = "reports"
    report_files = glob.glob(os.path.join(reports_dir, "report_*.json"))
    
    aggregated_data = {
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total_time": 0.0
        },
        "tests": []
    }
    
    for f in report_files:
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                
                # Aggregate summary
                summary = data.get("summary", {})
                aggregated_data["summary"]["total"] += summary.get("total", 0)
                aggregated_data["summary"]["passed"] += summary.get("passed", 0)
                aggregated_data["summary"]["failed"] += summary.get("failed", 0)
                aggregated_data["summary"]["skipped"] += summary.get("skipped", 0)
                aggregated_data["summary"]["total_time"] += summary.get("total_time", 0.0)
                
                # Aggregate tests
                tests = data.get("tests", [])
                aggregated_data["tests"].extend(tests)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    # Write aggregated data to report.json
    output_file = os.path.join(reports_dir, "report.json")
    with open(output_file, 'w') as out_file:
        json.dump(aggregated_data, out_file, indent=4)
        
    print(f"Successfully aggregated {len(report_files)} JSON reports into {output_file}")
    
    # Generate HTML Report
    generate_html_report(aggregated_data)

def generate_html_report(data):
    html_content = """<html>
<head>
<title>Selenium Test Report</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
table { border-collapse: collapse; width: 100%; margin-top: 20px; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
.passed { color: green; font-weight: bold; }
.failed { color: red; font-weight: bold; }
</style>
</head>
<body>
<h1>Selenium Test Execution Report</h1>
"""
    summary = data.get("summary", {})
    html_content += f"<p><strong>Total Tests:</strong> {summary.get('total', 0)}</p>"
    html_content += f"<p><strong>Passed:</strong> {summary.get('passed', 0)}</p>"
    html_content += f"<p><strong>Failed:</strong> {summary.get('failed', 0)}</p>"
    html_content += f"<p><strong>Total Time:</strong> {summary.get('total_time', 0):.2f}s</p>"
    
    html_content += """<table>
<tr><th>Test Name</th><th>Status</th><th>Duration (s)</th><th>Error</th></tr>
"""
    
    for test in data.get("tests", []):
        name = test.get("nodeid", "")
        status = test.get("outcome", "unknown").upper()
        duration = test.get("call", {}).get("duration", 0.0)
        
        error = ""
        if status == "FAILED":
            error = test.get("call", {}).get("crash", {}).get("message", "Test Failed")
            
        status_class = "passed" if status == "PASSED" else "failed"
        
        html_content += f"<tr><td>{name}</td><td class='{status_class}'>{status}</td><td>{duration:.2f}</td><td>{error}</td></tr>\n"
        
    html_content += """</table>
</body>
</html>"""

    with open(os.path.join("reports", "report.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Successfully generated reports/report.html")

if __name__ == "__main__":
    aggregate_reports()
