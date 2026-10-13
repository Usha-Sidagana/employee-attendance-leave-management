import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

WORKFLOW = "Attendance Correction Approval"


def after_migrate():
	create_attendance_custom_fields()
	create_correction_workflow()


def create_attendance_custom_fields():
	create_custom_fields(
		{
			"Attendance": [
				{
					"fieldname": "custom_late_minutes",
					"label": "Late Minutes",
					"fieldtype": "Int",
					"insert_after": "late_entry",
					"read_only": 1,
					"default": "0",
				},
				{
					"fieldname": "custom_early_leaving_minutes",
					"label": "Early Leaving Minutes",
					"fieldtype": "Int",
					"insert_after": "early_exit",
					"read_only": 1,
					"default": "0",
				},
			]
		},
		update=True,
	)


def create_correction_workflow():
	if not frappe.db.exists("DocType", "Attendance Correction Request"):
		return
	if frappe.db.exists("Workflow", WORKFLOW):
		return

	for state, style in [
		("Draft", "Warning"),
		("Pending Approval", "Primary"),
		("Approved", "Success"),
		("Rejected", "Danger"),
	]:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc(
				{"doctype": "Workflow State", "workflow_state_name": state, "style": style}
			).insert()

	for action in ["Submit for Approval", "Approve", "Reject"]:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert()

	frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": WORKFLOW,
			"document_type": "Attendance Correction Request",
			"is_active": 1,
			"workflow_state_field": "status",
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": "Employee"},
				{"state": "Pending Approval", "doc_status": "0", "allow_edit": "Manager"},
				{"state": "Approved", "doc_status": "0", "allow_edit": "Manager"},
				{"state": "Rejected", "doc_status": "0", "allow_edit": "Manager"},
			],
			"transitions": [
				{
					"state": "Draft",
					"action": "Submit for Approval",
					"next_state": "Pending Approval",
					"allowed": "Employee",
				},
				{
					"state": "Pending Approval",
					"action": "Approve",
					"next_state": "Approved",
					"allowed": "Manager",
				},
				{
					"state": "Pending Approval",
					"action": "Reject",
					"next_state": "Rejected",
					"allowed": "Manager",
				},
			],
		}
	).insert(ignore_permissions=True)
