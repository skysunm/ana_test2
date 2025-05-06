from flask import Flask, render_template, request, jsonify
import pymysql
import os

app = Flask(__name__)

# ✅ MySQL DB 설정
db_config = {
    'host': os.environ.get('MYSQL_HOST', 'containers-us-west-179.railway.app'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', 'your_password'),
    'database': os.environ.get('MYSQL_DATABASE', 'railway'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'charset': 'utf8mb4'  # Unicode 오류 방지
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/save_coords', methods=['POST'])
def save_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    address = data.get('address')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO coordinates (lat, lng, address) VALUES (%s, %s, %s)", (lat, lng, address))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_coords', methods=['GET'])
def get_coords():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT lat, lng, address FROM coordinates")
    rows = c.fetchall()
    conn.close()
    result = [{'lat': r[0], 'lng': r[1], 'address': r[2]} for r in rows]
    return jsonify(result)

@app.route('/delete_coords', methods=['POST'])
def delete_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM coordinates WHERE lat=%s AND lng=%s", (lat, lng))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

# ✅ 저장된 좌표를 웹 테이블로 출력
@app.route('/table')
def coords_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, lat, lng, address FROM coordinates")
    rows = c.fetchall()
    conn.close()
    return render_template('table.html', coords=rows)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
