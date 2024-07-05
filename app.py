from flask import Flask, render_template, jsonify, request
from hh import extr_max_page, extr_hh_jobs, update_job_name_search
import sqlite3

app = Flask(__name__)
db_path = "jobs.db"

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
    experience_filter = request.args.get('experience', None)
    city_filter = request.args.get('city', None)
    company_filter = request.args.get('company', None)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if experience_filter == "Без опыта":
            query += " AND Experience = 'Без опыта'"
        
        if city_filter:
            query += " AND City = ?"
            params.append(city_filter)
        
        if company_filter:
            query += " AND Company LIKE ?" 
            params.append(f"%{company_filter}%")

        cursor.execute(query, params)
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)