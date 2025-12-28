from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.ext import db
from app.models import Resource

resources_bp = Blueprint("resources", __name__, url_prefix="/resources")

@resources_bp.route("/")
def view_resources():
    resources = Resource.query.all()
    return render_template("resources/view.html", resources=resources)


@resources_bp.route("/add", methods=["POST"])
def add_resource():
    name = request.form["resource_name"]
    rtype = request.form["resource_type"]

    resource = Resource(resource_name=name, resource_type=rtype)
    db.session.add(resource)
    db.session.commit()

    flash("Resource added", "success")
    return redirect(url_for("resources.view_resources"))


@resources_bp.route("/edit/<int:resource_id>", methods=["GET", "POST"])
def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)

    if request.method == "POST":
        resource.resource_name = request.form["resource_name"]
        resource.resource_type = request.form["resource_type"]
        db.session.commit()

        flash("Resource updated", "success")
        return redirect(url_for("resources.view_resources"))

    return render_template("resources/edit.html", resource=resource)

@resources_bp.route("/delete/<int:resource_id>", methods=["POST"])
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash("Resource removed successfully", "warning")
    return redirect(url_for("resources.view_resources"))