import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, getdate

from employee_attendance_leave_management.attendance_utils import (
	create_or_update_attendance,
)


class AttendanceCorrectionRequest(Document):
	def validate(self):
		self.validate_times()
		self.fetch_current_attendance()
		self.validate_duplicate()
		self.validate_approval_permission()

	def validate_approval_permission(self):
		"""Only System Manager and HR Manager can approve requests."""
		if self.status in ("Approved", "Rejected"):
			if self.is_new() or self.has_value_changed("status"):
				self.check_approval_permission()

	def check_approval_permission(self):
		"""Allow HR to manage all requests and managers to manage direct reports."""
		user = frappe.session.user
		roles = set(frappe.get_roles(user))

		if user == "Administrator" or "System Manager" in roles:
			return

		if {
			"HR Manager",
			"HR User",
		}.intersection(roles):
			return

		if "Manager" in roles:
			manager_employee = frappe.db.get_value(
				"Employee",
				{"user_id": user},
				"name",
			)

			employee_manager = frappe.db.get_value(
				"Employee",
				self.employee,
				"reports_to",
			)

			if manager_employee and employee_manager == manager_employee:
				return

		frappe.throw(
			_("Only HR or the employee's Manager can approve or reject Attendance Correction Requests.")
		)

	def validate_times(self):
		if getdate(self.attendance_date) > getdate():
			frappe.throw(_("Attendance Date cannot be in the future."))

		check_in = get_datetime(self.requested_check_in)
		check_out = get_datetime(self.requested_check_out)

		if check_out <= check_in:
			frappe.throw(_("Requested Check-out must be after Requested Check-in."))

		if getdate(check_in) != getdate(self.attendance_date):
			frappe.throw(_("Requested Check-in must fall on the Attendance Date."))

	@frappe.whitelist()
	def fetch_current_attendance(self):
		att = frappe.db.get_value(
			"Attendance",
			{
				"employee": self.employee,
				"attendance_date": self.attendance_date,
				"docstatus": ["<", 2],
			},
			["name", "in_time", "out_time"],
			as_dict=True,
		)

		self.attendance = att.name if att else None
		self.current_check_in = att.in_time if att else None
		self.current_check_out = att.out_time if att else None

		return {
			"attendance": self.attendance,
			"current_check_in": self.current_check_in,
			"current_check_out": self.current_check_out,
		}

	def validate_duplicate(self):
		dup = frappe.db.exists(
			"Attendance Correction Request",
			{
				"employee": self.employee,
				"attendance_date": self.attendance_date,
				"status": "Pending Approval",
				"name": ["!=", self.name],
			},
		)

		if dup:
			frappe.throw(_("A pending correction request already exists for this date: {0}").format(dup))

	def on_update(self):
		if self.status == "Approved" and self.has_value_changed("status"):
			self.apply_correction()

	def apply_correction(self):
		self.check_approval_permission()

		name = create_or_update_attendance(
			self.employee,
			self.attendance_date,
			get_datetime(self.requested_check_in),
			get_datetime(self.requested_check_out),
			force=True,
		)

		self.db_set("attendance", name)
		frappe.msgprint(
			_("Attendance {0} has been updated.").format(name),
			alert=True,
		)
