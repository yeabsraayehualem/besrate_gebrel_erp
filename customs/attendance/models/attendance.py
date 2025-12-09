from odoo import models,fields,api,_


class ClassAttendance(models.Model):
    _name="class.attendance"
    _description="Class Attendance"

    student_id = fields.Many2one("student.student",string="Student")
    attendance_date = fields.Date(string="Attendance Date")
    attendance_state = fields.Selection([
        ('present','Present'),
        ('absent','Absent'),
        ('late','Late')
    ],string="Attendance State")
    stage_id = fields.Many2one("class.stage",string="Stage",related='student_id.stage_id')

    active = fields.Boolean(string="Active",default=True)

class FeastAttendance(models.Model):
    _name="feast.attendance"
    _description="Feast Attendance"

    student_id = fields.Many2one("student.student",string="Student")
    attendance_date = fields.Date(string="Attendance Date")
    attendance_state = fields.Selection([
        ('present','Present'),
        ('absent','Absent'),
        ('late','Late')
    ],string="Attendance State")
    stage_id = fields.Many2one("class.stage",string="Stage",related='student_id.stage_id')

    active = fields.Boolean(string="Active",default=True)
