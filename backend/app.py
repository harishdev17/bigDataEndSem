from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://harishrealmepadx_db_user:Rx5sOV0DsNGGwxlf@cluster0.dedti3w.mongodb.net/traffic_db"
                    ,serverSelectionTimeoutMS=5000  # 5 seconds)
db = client["traffic_db"]

@app.route("/")
def index():
    # -------------------------
    # Traffic Flow
    # -------------------------
    flow_data = list(db.traffic_flow.find())
    flow = {}
    for doc in flow_data:
        hour = doc["hour"]
        flow[hour] = flow.get(hour, 0) + int(doc["total_vehicle_count"])

    flow_hours = sorted(flow.keys())
    flow_values = [flow[h] for h in flow_hours]

    # -------------------------
    # Speed Analysis
    # -------------------------
    speed_data = list(db.speed_analysis.find())
    speed = {}
    for doc in speed_data:
        hour = doc["hour"]
        speed[hour] = float(doc["avg_speed"])

    speed_hours = sorted(speed.keys())
    speed_values = [speed[h] for h in speed_hours]

    # -------------------------
    # Vehicle Count by Location
    # -------------------------
    vehicle_data = list(db.vehicle_count_location.find())
    locations = [d["location"] for d in vehicle_data]
    vehicle_counts = [int(d["total_vehicle_count"]) for d in vehicle_data]

    # -------------------------
    # Congestion Distribution
    # -------------------------
    cong_data = list(db.congestion_distribution.find())
    cong_labels = [d["congestion_level"] for d in cong_data]
    cong_values = [int(d["count"]) for d in cong_data]

    # -------------------------
    # Summary
    # -------------------------
    total_records = sum(cong_values)
    avg_speed = round(sum(speed_values) / len(speed_values), 2) if speed_values else 0
    avg_vehicles = int(sum(vehicle_counts) / len(vehicle_counts)) if vehicle_counts else 0
    active_locations = len(locations)

    return render_template("index.html",
                           flow_hours=flow_hours,
                           flow_values=flow_values,
                           speed_hours=speed_hours,
                           speed_values=speed_values,
                           locations=locations,
                           vehicle_counts=vehicle_counts,
                           cong_labels=cong_labels,
                           cong_values=cong_values,
                           total_records=total_records,
                           avg_speed=avg_speed,
                           avg_vehicles=avg_vehicles,
                           active_locations=active_locations)

if __name__ == "__main__":
    app.run(debug=True)
