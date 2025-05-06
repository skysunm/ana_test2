from flask import Flask, render_template, request, jsonify
import pymysql
import os

app = Flask(__name__)

# ✅ MySQL 접속 설정
db_config = {
    'host': os.environ.get('MYSQL_HOST', 'metro.proxy.rlwy.net'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', '비밀번호'),
    'database': os.environ.get('MYSQL_DATABASE', 'railway'),
    'port': int(os.environ.get('MYSQL_PORT', 3306))
}

def get_db_connection():
    return pymysql.connect(
        cursorclass=pymysql.cursors.DictCursor,
        **db_config
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/table')
def table():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM coordinates ORDER BY id DESC")
        rows = cursor.fetchall()
    conn.close()
    return render_template("table.html", coordinates=rows)

@app.route('/save_coords', methods=['POST'])
def save_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    address = data.get('address')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO coordinates (lat, lng, address) VALUES (%s, %s, %s)", (lat, lng, address))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_coords')
def get_coords():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT lat, lng, address FROM coordinates")
        rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/delete_coords', methods=['POST'])
def delete_coords():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM coordinates WHERE lat=%s AND lng=%s", (lat, lng))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/admin/coords')
def admin_coords():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM coordinates")
        rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
