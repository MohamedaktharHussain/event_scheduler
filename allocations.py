from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.ext import db
from app.models import Event, Resource, EventResourceAllocation
from app.utils.conflict import has_conflict

allocations_bp = Blueprint("allocations", __name__, url_prefix="/allocations")

@allocations_bp.route("/", methods=["GET", "POST"])
def allocate():
    events = Event.query.all()
    resources = Resource.query.all()

    if request.method == "POST":
        event_id = int(request.form["event_id"])
        resource_ids = request.form.getlist("resource_ids")

        event = Event.query.get(event_id)

        for rid in resource_ids:
            conflicts = has_conflict(int(rid), event.start_time, event.end_time)
            if conflicts:
                flash("Resource conflict detected!", "danger")
                return redirect(url_for("allocations.allocate"))

            allocation = EventResourceAllocation(
                event_id=event_id,
                resource_id=int(rid)
            )
            db.session.add(allocation)

        db.session.commit()
        flash("Resources allocated successfully", "success")
        return redirect(url_for("allocations.allocate"))

    return render_template(
        "allocations/allocate.html",
        events=events,
        resources=resources
    )
