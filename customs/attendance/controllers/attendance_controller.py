from odoo import http
from odoo.http import request
from odoo import fields
import json
class AttendanceController(http.Controller):
    @http.route('/attendance/attendance', type='json',auth="user",methods=['POST'])
    def class_attendance(self,**kw):
        data = json.loads(request.httprequest.data)
        student = request.env['student.student'].search([('id_number', '=', data['id_number'])])

        attendance = request.env['class.attendance'].create({
            'student_id': student.id,
            'attendance_date': fields.Date.today(),
            'attendance_state': 'present',
            'stage_id': student.stage_id.id
        })

        return {
            'success': True,
            'message': 'Attendance recorded successfully',
            'attendance_id': attendance.id
        }
    

    @http.route('/attendance/feast', type='json',auth="user",methods=['POST'])
    def feast_attendance(self,**kw):
        data = json.loads(request.httprequest.data)
        student = request.env['student.student'].search([('id_number', '=', data['id_number'])])

        attendance = request.env['feast.attendance'].create({
            'student_id': student.id,
            'attendance_date': fields.Date.today(),
            'attendance_state': 'present',
            'stage_id': student.stage_id.id
        })

        return {
            'success': True,
            'message': 'Attendance recorded successfully',
            'attendance_id': attendance.id
        }