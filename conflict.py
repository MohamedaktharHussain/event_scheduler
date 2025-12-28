from app.models import EventResourceAllocation, Event
from app.ext import db

def has_conflict(resource_id, start_time, end_time, exclude_event_id=None):
    query = (
        db.session.query(Event)
        .join(EventResourceAllocation)
        .filter(EventResourceAllocation.resource_id == resource_id)
        .filter(Event.start_time < end_time)
        .filter(start_time < Event.end_time)
    )

    if exclude_event_id:
        query = query.filter(Event.event_id != exclude_event_id)

    return query.all()
