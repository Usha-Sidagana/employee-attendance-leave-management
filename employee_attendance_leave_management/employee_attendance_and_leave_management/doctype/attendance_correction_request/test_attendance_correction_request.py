import frappe
from frappe.tests.classes.unit_test_case import UnitTestCase
from frappe.utils import getdate


EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class TestAttendanceCorrectionRequest(UnitTestCase):

    def make_request(self, attendance_date, check_in, check_out):
        doc = frappe.new_doc("Attendance Correction Request")
        doc.employee = "HR-EMP-00002"
        doc.attendance_date = attendance_date
        doc.requested_check_in = check_in
        doc.requested_check_out = check_out
        doc.reason = "Unit test"
        return doc

    def test_future_attendance_date_is_rejected(self):
        future_date = getdate().replace(year=getdate().year + 1)
        doc = self.make_request(
            future_date,
            f"{future_date} 09:30:00",
            f"{future_date} 18:30:00",
        )

        with self.assertRaises(frappe.ValidationError):
            doc.validate_times()

    def test_checkout_before_checkin_is_rejected(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 18:00:00",
            "2026-10-12 09:00:00",
        )

        with self.assertRaises(frappe.ValidationError):
            doc.validate_times()

    def test_checkout_equal_to_checkin_is_rejected(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 09:30:00",
        )

        with self.assertRaises(frappe.ValidationError):
            doc.validate_times()

    def test_checkin_on_different_date_is_rejected(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-13 09:30:00",
            "2026-10-13 18:30:00",
        )

        with self.assertRaises(frappe.ValidationError):
            doc.validate_times()

    def test_valid_request_times_are_accepted(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        doc.validate_times()

    def test_duplicate_pending_request_is_rejected(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        doc.name = "TEST-ACR-002"

        from unittest.mock import patch
        with patch("frappe.db.exists", return_value="TEST-ACR-001"):
            with self.assertRaises(frappe.ValidationError):
                doc.validate_duplicate()

    def test_no_duplicate_pending_request_is_accepted(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        doc.name = "TEST-ACR-003"

        from unittest.mock import patch
        with patch("frappe.db.exists", return_value=None):
            doc.validate_duplicate()

    def test_fetch_current_attendance_when_record_exists(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        attendance = frappe._dict(
            name="HR-ATT-0001",
            in_time="2026-10-12 09:00:00",
            out_time="2026-10-12 18:00:00",
        )

        from unittest.mock import patch
        with patch("frappe.db.get_value", return_value=attendance):
            result = doc.fetch_current_attendance()

        self.assertEqual(result["attendance"], "HR-ATT-0001")
        self.assertEqual(result["current_check_in"], attendance.in_time)
        self.assertEqual(result["current_check_out"], attendance.out_time)

    def test_fetch_current_attendance_when_record_does_not_exist(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )

        from unittest.mock import patch
        with patch("frappe.db.get_value", return_value=None):
            result = doc.fetch_current_attendance()

        self.assertIsNone(result["attendance"])
        self.assertIsNone(result["current_check_in"])
        self.assertIsNone(result["current_check_out"])

    def test_approval_triggers_correction(self):
        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        doc.status = "Approved"

        from unittest.mock import patch
        with (
            patch.object(doc, "has_value_changed", return_value=True),
            patch.object(doc, "apply_correction") as apply_mock,
        ):
            doc.on_update()

        apply_mock.assert_called_once()


    def test_system_manager_can_approve(self):
        from unittest.mock import patch

        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        with patch("frappe.get_roles", return_value=["System Manager"]):
            doc.check_approval_permission()

    def test_hr_manager_can_approve(self):
        from unittest.mock import patch

        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        with patch("frappe.get_roles", return_value=["HR Manager"]):
            doc.check_approval_permission()

    def test_user_without_approval_role_is_rejected(self):
        from unittest.mock import patch

        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )
        with patch("frappe.get_roles", return_value=[]), patch.dict(
            frappe.session, {"user": "ordinary.employee@example.com"}
        ):
            with self.assertRaises(frappe.ValidationError):
                doc.check_approval_permission()

    def test_apply_correction_links_attendance(self):
        from unittest.mock import patch

        doc = self.make_request(
            "2026-10-12",
            "2026-10-12 09:30:00",
            "2026-10-12 18:30:00",
        )

        controller = (
            "employee_attendance_leave_management."
            "employee_attendance_and_leave_management.doctype."
            "attendance_correction_request.attendance_correction_request"
        )

        with (
            patch("frappe.get_roles", return_value=["System Manager"]),
            patch(f"{controller}.create_or_update_attendance",
                  return_value="HR-ATT-0002") as create_mock,
            patch.object(doc, "db_set") as db_set_mock,
            patch("frappe.msgprint"),
        ):
            doc.apply_correction()

        create_mock.assert_called_once()
        self.assertEqual(create_mock.call_args.args[0], doc.employee)
        self.assertTrue(create_mock.call_args.kwargs["force"])
        db_set_mock.assert_called_once_with("attendance", "HR-ATT-0002")

