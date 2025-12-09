from odoo import http
from odoo.http import request
import json

class Authenticate(http.Controller):

    @http.route('/attendance/authenticate', 
                type='json', auth='none', csrf=False, methods=['POST'])
    def authenticate(self, **kwargs):
        
        data = json.loads(request.httprequest.data)

        login = data.get('email')
        password = data.get('password')
        db = data.get('db')

        if not (db and login and password):
            return {
                "success": False,
                "message": "Missing credentials"
            }
        
        credential = {'login':login,'password':password,'type':'password'}
        uid = request.session.authenticate(db, credential)

        if uid:
            return {
                "success": True,
                "uid": uid,
                "session_id": request.session.sid,
                "message": "Authenticated"
            }

        return {
            "success": False,
            "message": "Invalid login"
        }
