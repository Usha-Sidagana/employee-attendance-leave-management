import frappe
from frappe.utils import get_datetime, now_datetime


@frappe.whitelist(methods=["POST"])
def employee_checkin(employee=None, time=None, log_type=None):
	"""Validate an attendance request and enqueue background processing."""

	# 1. Authentication
	user = frappe.session.user

	if user == "Guest":
		frappe.throw(
			"Authentication is required.",
			frappe.AuthenticationError,
		)

	# 2. Required fields
	if not employee or not str(employee).strip():
		frappe.throw("Employee is required.")

	if not time:
		frappe.throw("Check-in time is required.")

	if not log_type:
		frappe.throw("Log Type is required.")

	employee = str(employee).strip()
	log_type = str(log_type).strip().upper()

	# 3. Validate log type
	if log_type not in ("IN", "OUT"):
		frappe.throw("Log Type must be either IN or OUT.")

	# 4. Validate timestamp
	try:
		checkin_time = get_datetime(time)
	except TypeError, ValueError, OverflowError:
		frappe.throw("Invalid timestamp. Use YYYY-MM-DD HH:MM:SS format.")

	if not checkin_time:
		frappe.throw("A valid check-in timestamp is required.")

	if checkin_time > get_datetime(now_datetime()):
		frappe.throw("Check-in time cannot be in the future.")

	# 5. Validate employee
	employee_doc = frappe.db.get_value(
		"Employee",
		employee,
		["name", "status", "user_id"],
		as_dict=True,
	)

	if not employee_doc:
		frappe.throw(f"Employee {employee} does not exist.")

	if employee_doc.status != "Active":
		frappe.throw("Check-in is allowed only for active employees.")

	# 6. Authorization
	privileged_roles = {
		"System Manager",
		"HR Manager",
		"HR User",
	}

	roles = set(frappe.get_roles(user))
	is_privileged = bool(roles.intersection(privileged_roles))
	is_own_employee = employee_doc.user_id == user

	if not is_privileged and not is_own_employee:
		frappe.throw(
			"You are not authorized to submit check-ins for this employee.",
			frappe.PermissionError,
		)

	# 7. Check for an existing duplicate
	duplicate = frappe.db.exists(
		"Employee Checkin",
		{
			"employee": employee,
			"time": checkin_time,
			"log_type": log_type,
		},
	)

	if duplicate:
		frappe.throw(f"Duplicate check-in detected. Existing record: {duplicate}")

	# 8. Enqueue the background job
	job_id = frappe.generate_hash(length=12)

	frappe.enqueue(
		"employee_attendance_leave_management.attendance_jobs.process_employee_checkin",
		queue="short",
		job_id=job_id,
		enqueue_after_commit=True,
		employee=employee,
		checkin_time=str(checkin_time),
		log_type=log_type,
	)

	# 9. Return the queued job information
	return {
		"success": True,
		"message": "Employee check-in request queued successfully.",
		"status": "Queued",
		"job_id": job_id,
		"data": {
			"employee": employee,
			"time": str(checkin_time),
			"log_type": log_type,
		},
	}
