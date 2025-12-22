# app.py
import base64
from pathlib import Path
from flask import Flask, request, make_response, render_template
from weasyprint import HTML
import traceback
from urllib.parse import quote
import json
app = Flask(__name__)

# === Preload static assets as base64 (at startup) ===
STATIC_DIR = Path(__file__).parent / "static"

# Load background and logo once


@app.route('/generate-badge-pdf', methods=['POST'])
def generate_badge_pdf():
    try:

        data = request.data
        data = json.loads(data)
        if not data:
            print("no json ")
            return "No JSON payload", 400

        # print(data)
        qr_b64 = data.get('qr_code', '')


        if qr_b64:
            base64.b64decode(qr_b64, validate=True)
        try:

            bg = {
            "ማቴዎስ": "mathewos",
            "ማርቆስ": "markos",
            "ሉቃስ": "lukas",
            "ዮሃንስ": "yohanes",
            "ጴጥሮስ": "petros",
            "ጳውሎስ": "pawlos"
            }

            with open(STATIC_DIR / f"{bg[data['stage']]}.png", "rb") as f:
                ID_FRONT_B64 = base64.b64encode(f.read()).decode('utf-8')

        except FileNotFoundError as e:
            print("❌ ERROR: Missing static asset:", e)
            ID_FRONT_B64 = ""
            LOGO_B64 = ""
        # Render template with ALL data as base64
        html_content = render_template(
            'index.html',
            avatar_b64=data.get('avatar_b64', ''),
            qr_base64=data.get('qr_code', ''),
            fullname=data['fullname'],
            age=data['age'],
            gender=data['gender'],
            parents_phone=data['parents_phone'],
            supervisor_phone=data['supervisor_phone'],
            badge_bg_b64=ID_FRONT_B64
        )

        # Generate PDF — no base_url needed!
        pdf = HTML(string=html_content).write_pdf()

        response = make_response(pdf)
        filename = f'badge_{data["id_number"]}.pdf'
        filename_utf8 = quote(filename)

        response.headers['Content-Disposition'] = (
            f"attachment; filename=badge.pdf; filename*=UTF-8''{filename_utf8}"
        )
        response.headers['Content-Type'] = 'application/pdf'
        return response

    except Exception as e:
        print("🔥 PDF Generation Error:")
        traceback.print_exc()
        return f"Server error: {str(e)}", 500

if __name__ == '__main__':


    app.run(host='0.0.0.0', port=5002, debug=True)