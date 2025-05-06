from flask import Flask, render_template, request, jsonify, send_file
import pymysql
import os

app = Flask(__name__)

# ✅ MySQL DB 접속 설정
db_config = {
    'host': os.environ.get('MYSQL_HOST', 'mysql.railway.internal'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', 'PjHVnNakvTZvDCYwcurlJxuvoJOLohAC'),
    'database': os.environ.get('MYSQL_DATABASE', 'railway'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.Cursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

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

    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute("INSERT INTO coordinates (lat, lng, address) VALUES (%s, %s, %s)", (lat, lng, address))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# ✅ 좌표 목록 조회
@app.route('/get_coords', methods=['GET'])
def get_coords():
    conn = get_db_connection()
    with conn.cursor() as c:
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

    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute("DELETE FROM coordinates WHERE lat=%s AND lng=%s", (lat, lng))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

# ✅ DB 전체 목록 출력용 (관리자용)
@app.route('/admin/coords')
def admin_coords():
    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute("SELECT * FROM coordinates")
        rows = c.fetchall()
    conn.close()

    result = [{'id': r[0], 'lat': r[1], 'lng': r[2], 'address': r[3]} for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
