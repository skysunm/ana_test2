from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# ✅ 좌표 저장
@app.route('/save_coords', methods=['POST'])
def save_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    address = data.get('address')

    conn = sqlite3.connect("coords.db")
    c = conn.cursor()
    c.execute("INSERT INTO coordinates (lat, lng, address) VALUES (?, ?, ?)", (lat, lng, address))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# ✅ 좌표 목록 조회
@app.route('/get_coords', methods=['GET'])
def get_coords():
    conn = sqlite3.connect("coords.db")
    c = conn.cursor()
    c.execute("SELECT lat, lng, address FROM coordinates")
    rows = c.fetchall()
    conn.close()

    result = [{'lat': r[0], 'lng': r[1], 'address': r[2]} for r in rows]
    return jsonify(result)

# ✅ 좌표 삭제
@app.route('/delete_coords', methods=['POST'])
def delete_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    conn = sqlite3.connect("coords.db")
    c = conn.cursor()
    c.execute("DELETE FROM coordinates WHERE lat=? AND lng=?", (lat, lng))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from flask import send_file

@app.route('/download_db', methods=['GET'])
def download_db():
    db_path = "coords.db"
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True)
    else:
        return "DB 파일이 존재하지 않습니다.", 404

@app.route('/admin/coords')
def admin_coords():
    conn = sqlite3.connect("coords.db")
    c = conn.cursor()
    c.execute("SELECT * FROM coordinates")
    rows = c.fetchall()
    conn.close()
    
    result = [
        {'id': r[0], 'lat': r[1], 'lng': r[2], 'address': r[3]}
        for r in rows
    ]
    return jsonify(result)
