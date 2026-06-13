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

if __name__ == "__main__":
    aggregate_reports()
