# controllers/hr_badge.py
import logging
import requests
from odoo import http
from odoo.http import request, content_disposition
from odoo.exceptions import AccessError
from datetime import timedelta
_logger = logging.getLogger(__name__)

class HrBadgeController(http.Controller):

    @http.route('/hr/badge/pdf/<int:employee_id>', type='http', auth='user')
    def download_badge_pdf(self, employee_id, **kwargs):
        # Fetch employee
        emp = request.env['student.student'].sudo().browse(employee_id)
        if not emp.exists():
            return request.not_found()

        # Security: ensure user has access
        try:
            emp.check_access_rights('read')
            emp.check_access_rule('read')
        except AccessError:
            return request.not_found()


        qr_b64 = emp.qr_code.decode('utf-8') if emp.qr_code else ''

        # Build payload for Flask
        payload = {
            "fullname": emp.full_name,
            "age": emp.age,
            "gender": emp.gender,
            "parents_phone": emp.parents_phone,
            "supervisor_phone": emp.stage_id.supervisor.work_phone or '',
            "qr_code": emp.qr_code.decode(),
            "avatar_b64": emp.photo.decode() if emp.photo else "",
            "id_number": emp.id_number,
            "stage": emp.stage_id.name,
        }

        # Call Flask service
        try:
            _logger.info("Generating badge PDF: %s", payload)
            flask_url = 'http://flask_bg:5002/generate-badge-pdf'
            response = requests.post(flask_url, json=payload, timeout=20)
            response.raise_for_status()
            pdf_content = response.content
        except Exception as e:
            _logger.error("Failed to generate badge PDF: %s", e)
            return request.make_response(
                f"Error generating badge. Please check the Flask service. {str(e)}",
                [('Content-Type', 'text/plain')],
                status=500
            )

        # Return PDF as download
        filename = f'badge_{ emp.id_number}.pdf'
        return request.make_response(
            pdf_content,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', content_disposition(filename)),
            ]
        )