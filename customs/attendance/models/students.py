from odoo import models,fields,api,_


class Students(models.Model):
    _inherit = "student.student"

    class_attendance = fields.One2many("class.attendance",'student_id')
    holy_feasts_attendance = fields.One2many("feast.attendance","student_id")
    total_attendance = fields.Integer(string="Class Attendance",compute="_compute_total_attendance")
    feats_attendance = fields.Integer(string="Special Attendance",compute="_compute_total_feast_attendance")

    @api.depends("class_attendance")
    def _compute_total_attendance(self):
        for record in self:
            record.total_attendance = len(record.class_attendance)
    
    @api.depends("holy_feasts_attendance")
    def _compute_total_feast_attendance(self):
        for record in self:
            record.feats_attendance = len(record.holy_feasts_attendance)

    
    def action_class_attendance(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Class Attendance',
        'res_model': 'class.attendance',
        "view_id": self.env.ref("attendance.class_attendance_view_list").id,
        'view_mode': 'list',
        'domain': [('student_id', '=', self.id)],
        }
    
    def action_feast_attendance(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "feast.attendance",
            "name": "Feast Attendance",
            "view_mode": "list",
            "domain": [('student_id', '=', self.id)],
            "view_id": self.env.ref("attendance.feast_attendance_view_list").id,
        }

    
    def deactivate_student_attendances(self):
        for i in self.class_attendance:
            if i.stage_id != self.stage_id:
                i.active = False
        for i in self.holy_feasts_attendance:
            if i.stage_id != self.stage_id:
                i.active = False
           