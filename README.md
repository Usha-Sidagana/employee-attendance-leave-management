# Employee Attendance & Leave Management

## 1. Overview

A custom Frappe application implementing an Attendance Correction Request
workflow with role-based access control and linked Attendance record updates
after approval.

## 2. Technology Stack

- Frappe Framework v16
- ERPNext v16
- HRMS v16
- Python
- JavaScript
- Frappe DocTypes and JSON definitions

## 3. Architecture

- `api.py`: Application-level API methods.
- `attendance_utils.py`: Attendance-related utility functions.
- `attendance_jobs.py`: Attendance-related background jobs.
- `permissions.py`: Custom document access restrictions.
- `hooks.py`: Permission hooks and application configuration.
- `employee_attendance_and_leave_management/doctype/attendance_correction_request/attendance_correction_request.py`: Server-side controller and workflow logic.
- `attendance_correction_request.js`: Client-side form behavior.
- `attendance_correction_request.json`: DocType definition.
- `test_attendance_correction_request.py`: Automated tests.

## 4. Role-Based Access

- Employee: Access their own correction requests.
- Manager: Access their own requests and requests from direct reports.
- HR User / HR Manager: Access requests across employees.
- System Manager: Administrative access.

The application combines standard DocType permissions with custom
permission hooks and server-side authorization checks.

## 5. Prerequisites

- A compatible Frappe v16 bench.
- ERPNext and HRMS installed if required by the application.
- Employee records linked to user accounts.
- Correct manager reporting relationships.

## 6. Installation

From the bench directory, obtain the application source code and run:

    bench get-app <repository-url>
    bench --site <site-name> install-app employee_attendance_leave_management
    bench --site <site-name> migrate
    bench --site <site-name> clear-cache

Restart the bench after installation when required:

    bench restart

If the app is already present in the bench, skip `bench get-app`.

## 7. Configuration

1. Verify that the Attendance Correction Request DocType exists.
2. Configure the required role permissions.
3. Link each Employee record to the correct user account.
4. Configure reporting relationships through Employee `reports_to`.
5. Verify permission hooks in `hooks.py`.
6. Assign appropriate roles to test users.

## 8. API Usage

The app contains whitelisted methods in `api.py` and the Attendance
Correction Request controller.

Refer to the actual method definitions in these files for method paths,
parameters, HTTP methods, and authorization requirements. Only document
and use methods confirmed in the source code.

## 9. Important Design Decisions

- Access control is enforced server-side.
- Employees cannot approve their own requests.
- Managers are restricted to their direct reports.
- HR roles can access requests across employees.
- Approval updates the linked Attendance record.
- Rejection should not update the linked Attendance record.
- Employee mappings and manager reporting relationships must be configured.

## 10. Testing

Run automated tests using:

    bench --site <site-name> run-tests --app employee_attendance_leave_management

See `test_cases.md` for functional and permission test scenarios.
Record actual test results before submission.

## 11. Compatibility

Developed in a Frappe v16 environment. Verify dependencies and configuration
before installing the app on another site.
