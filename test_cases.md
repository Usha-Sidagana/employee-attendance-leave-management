# Test Cases — Employee Attendance & Leave Management

| ID | Scenario | Expected Result | Actual Result |
|---|---|---|---|
| TC-01 | Employee creates a correction request | Request is saved | Record result |
| TC-02 | Employee views own requests | Own requests are visible | Record result |
| TC-03 | Employee accesses another employee's request | Access is denied | Record result |
| TC-04 | Manager views a direct report's request | Request is visible | Record result |
| TC-05 | Manager accesses an unrelated employee's request | Access is denied | Record result |
| TC-06 | Manager approves a valid request | Attendance record is updated | Record result |
| TC-07 | Manager rejects a request | Attendance record remains unchanged | Record result |
| TC-08 | Employee tries to approve own request | Operation is denied | Record result |
| TC-09 | HR User accesses requests | Authorized access works | Record result |
| TC-10 | HR Manager accesses requests | Authorized access works | Record result |
| TC-11 | System Manager accesses requests | Administrative access works | Record result |
| TC-12 | User has no linked Employee record | Access is restricted safely | Record result |
| TC-13 | Invalid correction data is submitted | Server-side validation prevents invalid changes | Record result |

## Test Environment

- Frappe: 16.35.0
- ERPNext: 16.35.0
- HRMS: 16.50.0

## Automated Test Results

Record the actual test command, pass count, failures, and errors after execution.
