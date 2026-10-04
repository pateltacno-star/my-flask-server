import os
from flask import Flask, request, abort, send_from_directory

app = Flask(__name__)

# જે ફોલ્ડર બતાવવું હોય તેનો પાથ અહીં લખો
FOLDER_PATH = r"I:\kevin's website\project OverDrive Studio"

# ફાયરવોલ પર્મીશન લિસ્ટ (તમારો IP ઉમેરેલો છે)
ALLOWED_IPS = ['127.0.0.1', '192.168.29.118', '192.168.29.60']

@app.before_request
def firewall():
    client_ip = request.remote_addr
    # જો IP માન્ય લિસ્ટમાં ન હોય તો access બંધ થશે (403 Forbidden Error)
    if client_ip not in ALLOWED_IPS:
        abort(403)

@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>')
def browse_folder(subpath):
    target_path = os.path.join(FOLDER_PATH, subpath)

   
import os
from flask import Flask, request, abort, send_from_directory

app = Flask(__name__)

# જે ફોલ્ડર સર્વર પર બતાવવું હોય તેનો મૂળ પાથ (Root Directory)
BASE_DIR = r"I:\study"

# તમારા ફોન અને PC નો IP (જેને એક્સેસ આપવો હોય તે અહીં લખો)
ALLOWED_IPS = ['127.0.0.1', '192.168.29.118', '192.168.29.60']

@app.before_request
def firewall():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        abort(403)

@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>')
def browse_folders(subpath):
    target_path = os.path.join(BASE_DIR, subpath)

    # જો પાથ અસ્તિત્વમાં ન હોય તો 404
    if not os.path.exists(target_path):
        return "<h3>૪૦૪ - ફાઇલ કે ફોલ્ડર મળ્યું નથી!</h3>", 404

    # જો ફાઇલ હોય તો તેને ડાઉનલોડ/ઓપન કરો
    if os.path.isfile(target_path):
        directory = os.path.dirname(target_path)
        filename = os.path.basename(target_path)
        return send_from_directory(directory, filename)

    # જો ફોલ્ડર હોય તો તેની અંદરની ફાઇલો અને ફોલ્ડરનું લિસ્ટ બતાવો
    items = os.listdir(target_path)
    
    html = f"<h2>Folder: /{subpath}</h2><hr><ul>"
    if subpath:
        # પાછા જવાનું બટન (Back Option)
        parent_path = os.path.dirname(subpath)
        html += f'<li><b><a href="/{parent_path}">⬅️ Back</a></b></li><br>'

    for item in items:
        item_path = os.path.join(subpath, item)
        full_item_path = os.path.join(BASE_DIR, item_path)
        
        # જો ફોલ્ડર હોય તો 📁 અને ફાઇલ હોય તો 📄 આઇકોન બતાવશે
        if os.path.isdir(full_item_path):
            html += f'<li>📁 <a href="/{item_path}">{item}/</a></li>'
        else:
            html += f'<li>📄 <a href="/{item_path}">{item}</a></li>'
            
    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)