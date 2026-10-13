from datetime import timedelta

import frappe
from frappe.utils import get_datetime, getdate, time_diff_in_hours

# Fallbacks when the employee has no default shift
DEFAULT_START = timedelta(hours=9, minutes=30)
DEFAULT_END = timedelta(hours=18, minutes=30)
DEFAULT_LATE_GRACE = 0
DEFAULT_EARLY_GRACE = 0
HALF_DAY_HOURS = 4


def get_shift_timings(employee, attendance_date):
	"""Return (shift_start, shift_end, late_grace_min, early_grace_min)."""
	day = get_datetime(attendance_date)  # midnight of that date
	start_td, end_td = DEFAULT_START, DEFAULT_END
	late_grace, early_grace = DEFAULT_LATE_GRACE, DEFAULT_EARLY_GRACE

	shift = frappe.db.get_value("Employee", employee, "default_shift")
	if shift:
		st = frappe.db.get_value(
			"Shift Type",
			shift,
			["start_time", "end_time", "late_entry_grace_period", "early_exit_grace_period"],
			as_dict=True,
		)
		if st:
			start_td, end_td = st.start_time, st.end_time
			late_grace = st.late_entry_grace_period or 0
			early_grace = st.early_exit_grace_period or 0

	start = day + start_td
	end = day + end_td
	if end <= start:  # night shift crossing midnight
		end += timedelta(days=1)
	return start, end, late_grace, early_grace


def calculate_metrics(employee, attendance_date, in_time, out_time):
	start, end, late_grace, early_grace = get_shift_timings(employee, attendance_date)

	late_minutes = early_minutes = 0
	working_hours = 0.0

	if in_time:
		diff = (in_time - start).total_seconds() / 60
		if diff > late_grace:
			late_minutes = int(diff)

	if out_time:
		diff = (end - out_time).total_seconds() / 60
		if diff > early_grace:
			early_minutes = int(diff)

	if in_time and out_time and out_time > in_time:
		working_hours = round(time_diff_in_hours(out_time, in_time), 2)

	status = "Present"
	if out_time and working_hours < HALF_DAY_HOURS:
		status = "Half Day"

	return frappe._dict(
		late_minutes=late_minutes,
		early_minutes=early_minutes,
		working_hours=working_hours,
		status=status,
	)


def create_or_update_attendance(employee, attendance_date, in_time, out_time, checkins=None, force=False):
	"""Create or update the Attendance for an employee/date. Returns its name."""
	attendance_date = getdate(attendance_date)
	m = calculate_metrics(employee, attendance_date, in_time, out_time)

	values = {
		"in_time": in_time,
		"out_time": out_time,
		"working_hours": m.working_hours,
		"late_entry": 1 if m.late_minutes else 0,
		"early_exit": 1 if m.early_minutes else 0,
		"custom_late_minutes": m.late_minutes,
		"custom_early_leaving_minutes": m.early_minutes,
		"status": m.status,
	}
	if m.status == "Half Day":
		values["half_day_status"] = "Present"  # ignored if your HRMS version lacks it

	existing = frappe.db.get_value(
		"Attendance",
		{"employee": employee, "attendance_date": attendance_date, "docstatus": ["<", 2]},
		["name", "status"],
		as_dict=True,
	)

	if existing:
		if existing.status == "On Leave" and not force:
			return existing.name  # never override approved leave from a punch
		frappe.db.set_value("Attendance", existing.name, values)
		name = existing.name
	else:
		att = frappe.new_doc("Attendance")
		att.employee = employee
		att.attendance_date = attendance_date
		att.company = frappe.db.get_value("Employee", employee, "company")
		att.update(values)
		att.flags.ignore_permissions = True
		att.insert()
		att.submit()
		name = att.name

	for c in checkins or []:
		frappe.db.set_value("Employee Checkin", c, "attendance", name)
	return name


def process_attendance(employee, attendance_date):
	"""Build the day's attendance from Employee Checkin logs."""
	day_start = get_datetime(attendance_date)
	day_end = day_start + timedelta(days=1) - timedelta(seconds=1)

	logs = frappe.get_all(
		"Employee Checkin",
		filters={"employee": employee, "time": ["between", [day_start, day_end]]},
		fields=["name", "log_type", "time"],
		order_by="time asc",
	)
	ins = [l for l in logs if l.log_type == "IN"]
	outs = [l for l in logs if l.log_type == "OUT"]
	if not ins:
		return

	in_time = get_datetime(ins[0].time)  # first IN
	out_time = get_datetime(outs[-1].time) if outs else None  # last OUT
	if out_time and out_time <= in_time:
		out_time = None

	create_or_update_attendance(employee, attendance_date, in_time, out_time, checkins=[l.name for l in logs])


def on_checkin_save(doc, method=None):
	"""doc_events hook for Employee Checkin."""
	process_attendance(doc.employee, getdate(doc.time))
