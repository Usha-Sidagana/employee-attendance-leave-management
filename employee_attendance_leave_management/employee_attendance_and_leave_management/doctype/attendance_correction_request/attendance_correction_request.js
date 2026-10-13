// Copyright (c) 2026, Usha Sidagana and contributors
// For license information, please see license.txt


frappe.ui.form.on("Attendance Correction Request", {
    employee(frm) { frm.trigger("load_current"); },
    attendance_date(frm) { frm.trigger("load_current"); },

    load_current(frm) {
        if (!frm.doc.employee || !frm.doc.attendance_date) return;
        frm.call("fetch_current_attendance").then((r) => {
            if (r.message) {
                frm.set_value("attendance", r.message.attendance);
                frm.set_value("current_check_in", r.message.current_check_in);
                frm.set_value("current_check_out", r.message.current_check_out);
            }
        });
    },
});