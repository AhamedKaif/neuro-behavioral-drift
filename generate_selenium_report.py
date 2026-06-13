import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

REPORT_FILE = "reports/report.json"
EXCEL_FILE = "reports/selenium_test_report.xlsx"

def generate_report():
    if not os.path.exists(REPORT_FILE):
        print(f"JSON report file not found at {REPORT_FILE}. Skipping Excel generation.")
        return

    with open(REPORT_FILE, 'r') as f:
        data = json.load(f)

    # Initialize Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Selenium Test Results"

    # Define Styles
    bold_font = Font(bold=True)
    green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Headers
    headers = ["Test Case ID", "Test Case Name", "Module", "Status", "Execution Time (s)", "Remarks"]
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=8, column=col_num, value=header)
        cell.font = bold_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center")

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    row_num = 9
    for i, test in enumerate(data.get("tests", [])):
        nodeid = test.get("nodeid", "")
        # Expecting tests/test_login.py::test_valid_login
        parts = nodeid.split("::")
        if len(parts) != 2:
            continue
            
        file_path, test_method = parts
        module_name = file_path.split("/")[-1].replace(".py", "")
        
        # Test Case ID
        test_id = f"TC_{module_name.upper().replace('TEST_', '')}_{i+1:03d}"
        
        # Test Case Name
        test_name = test_method.replace("test_", "").replace("_", " ").title()
        
        # Status
        outcome = test.get("outcome", "unknown").upper()
        if outcome == "PASSED":
            passed_tests += 1
            remarks = "Executed Successfully"
        else:
            failed_tests += 1
            try:
                remarks = test.get("call", {}).get("crash", {}).get("message", "Test Failed")
            except:
                remarks = "Test Failed"
        total_tests += 1
        
        # Execution Time
        exec_time = 0.0
        if "call" in test:
            exec_time = test["call"].get("duration", 0.0)
            
        # Write Row
        ws.cell(row=row_num, column=1, value=test_id).border = thin_border
        ws.cell(row=row_num, column=2, value=test_name).border = thin_border
        ws.cell(row=row_num, column=3, value=module_name.title()).border = thin_border
        
        status_cell = ws.cell(row=row_num, column=4, value=outcome)
        status_cell.border = thin_border
        status_cell.alignment = Alignment(horizontal="center")
        if outcome == "PASSED":
            status_cell.fill = green_fill
        elif outcome == "FAILED":
            status_cell.fill = red_fill
            
        ws.cell(row=row_num, column=5, value=round(exec_time, 2)).border = thin_border
        ws.cell(row=row_num, column=6, value=remarks).border = thin_border
        
        row_num += 1

    # Write Summary at top
    pass_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    ws["A1"] = "Project: Neuro Behavioral Drift"
    ws["A2"] = "Test Framework: Selenium"
    ws["A3"] = f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws["A4"] = f"Total Tests: {total_tests}"
    ws["A5"] = f"Passed: {passed_tests}"
    ws["A6"] = f"Failed: {failed_tests}"
    ws["A7"] = f"Pass Percentage: {pass_percentage:.2f}%"

    for i in range(1, 8):
        ws[f"A{i}"].font = bold_font

    # Auto-fit columns
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    os.makedirs("reports", exist_ok=True)
    wb.save(EXCEL_FILE)
    print(f"Successfully generated {EXCEL_FILE}")

if __name__ == "__main__":
    generate_report()
