from flask import Blueprint, render_template, request
from datetime import datetime
from app.models import Resource, EventResourceAllocation, Event

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/utilization", methods=["GET", "POST"])
def utilization():
    report_data = []

    if request.method == "POST":
        start_date = datetime.fromisoformat(request.form["start_date"])
        end_date = datetime.fromisoformat(request.form["end_date"])

        resources = Resource.query.all()

        for r in resources:
            allocations = (
                EventResourceAllocation.query
                .join(Event)
                .filter(EventResourceAllocation.resource_id == r.resource_id)
                .filter(Event.start_time >= start_date)
                .filter(Event.end_time <= end_date)
                .all()
            )

            total_hours = sum(
                (a.event.end_time - a.event.start_time).total_seconds() / 3600
                for a in allocations
            )

            report_data.append({
                "name": r.resource_name,
                "type": r.resource_type,
                "hours": round(total_hours, 2),
                "count": len(allocations)
            })

    return render_template("reports/utilization.html", report_data=report_data)
