import frappe
from frappe.utils import get_datetime, now_datetime


def process_employee_checkin(employee, checkin_time, log_type):
	"""
	Background job to create an Employee Checkin record.
	Revalidates the request before creating the record.
	"""

	checkin_time = get_datetime(checkin_time)
	log_type = str(log_type).strip().upper()

	# Validate employee
	employee_doc = frappe.db.get_value(
		"Employee",
		employee,
		["name", "status"],
		as_dict=True,
	)

	if not employee_doc:
		frappe.throw(f"Employee {employee} does not exist.")

	if employee_doc.status != "Active":
		frappe.throw("Check-in is allowed only for active employees.")

	# Validate log type and timestamp
	if log_type not in ("IN", "OUT"):
		frappe.throw("Log Type must be either IN or OUT.")

	if checkin_time > get_datetime(now_datetime()):
		frappe.throw("Check-in time cannot be in the future.")

	# Check for duplicates again inside the worker
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

	# Create the record in the background
	checkin = frappe.get_doc(
		{
			"doctype": "Employee Checkin",
			"employee": employee,
			"time": checkin_time,
			"log_type": log_type,
		}
	)

	checkin.insert(ignore_permissions=True)

	frappe.db.commit()

	frappe.logger("attendance_background_job").info(
		f"Created Employee Checkin {checkin.name} for employee {employee}"
	)

	return {
		"success": True,
		"checkin": checkin.name,
	}
