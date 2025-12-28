from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.ext import db
from app.models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.route("/")
def view_events():
    events = Event.query.order_by(Event.start_time).all()
    return render_template("events/view.html", events=events)


@events_bp.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        start_time = datetime.fromisoformat(request.form["start_time"])
        end_time = datetime.fromisoformat(request.form["end_time"])
        description = request.form.get("description")

        if start_time >= end_time:
            flash("Start time must be before end time", "danger")
            return redirect(url_for("events.add_event"))

        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description
        )

        db.session.add(event)
        db.session.commit()

        flash("Event created successfully", "success")
        return redirect(url_for("events.view_events"))

    return render_template("events/add.html")


@events_bp.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event.title = request.form["title"]
        event.start_time = datetime.fromisoformat(request.form["start_time"])
        event.end_time = datetime.fromisoformat(request.form["end_time"])
        event.description = request.form.get("description")

        if event.start_time >= event.end_time:
            flash("Invalid time range", "danger")
            return redirect(url_for("events.edit_event", event_id=event_id))

        db.session.commit()
        flash("Event updated", "success")
        return redirect(url_for("events.view_events"))

    # ✅ THIS LINE IS CRITICAL
    return render_template("events/edit.html", event=event)



@events_bp.route("/delete/<int:event_id>")
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted", "info")
    return redirect(url_for("events.view_events"))
