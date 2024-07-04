from flask import Flask, render_template, jsonify, request
from hh import extr_max_page, extr_hh_jobs, update_job_name_search
import sqlite3

app = Flask(__name__)
db_path = "/Users/malfurion/Desktop/Практика/Parser/jobs.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_jobs')
def update_jobs():
    job_name = request.args.get('job_name_search', '')
    try:
        update_job_name_search(job_name)
        last_page = extr_max_page()
        extr_hh_jobs(last_page) 
        return jsonify({'message': 'Jobs updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_jobs')
def get_jobs():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
