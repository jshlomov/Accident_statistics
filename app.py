from database.connect import crashes
from repository.csv_repository import init_db
from repository.repository import get_all_crashes, get_all_daily_crashes, get_all_weekly_crashes, \
    get_all_monthly_crashes, get_all_crash_causes, get_all_areas, get_all_injuries_by_area

from flask import Flask, jsonify
import json
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))

app = Flask(__name__)

@app.route('/init', methods=['GET'])
def init_database():
    try:
        init_db()
        return jsonify("Success"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/crashes', methods=['GET'])
def get_crashes():
    try:
        result = get_all_crashes()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/daily_crashes', methods=['GET'])
def daily_crashes():
    try:
        result = get_all_daily_crashes()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/weekly_crashes', methods=['GET'])
def weekly_crashes():
    try:
        result = get_all_weekly_crashes()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/monthly_crashes', methods=['GET'])
def monthly_crashes():
    try:
        result = get_all_monthly_crashes()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/areas', methods=['GET'])
def areas():
    try:
        result = get_all_areas()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/crashes_cause', methods=['GET'])
def crashes_by_cause():
    try:
        result = get_all_crash_causes()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/injuries', methods=['GET'])
def injuries_by_area():
    try:
        result = get_all_injuries_by_area()
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/daily_crashes/<date>', methods=['GET'])
def get_daily_crashes_by_date(date):
    try:
        result = get_daily_crashes_by_date(date)
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/weekly_crashes/<date>', methods=['GET'])
def get_weekly_crashes_by_date(date):
    try:
        result = get_weekly_crashes_by_date(date)
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/monthly_crashes/<date>', methods=['GET'])
def get_monthly_crashes_by_date(date):
    try:
        result = get_monthly_crashes_by_date(date)
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/injuries/<area>', methods=['GET'])
def get_injuries_by_area(area):
    try:
        result = get_injuries_by_area(area)
        return jsonify(parse_json(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
