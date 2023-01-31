# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

import requests
from flask import Flask, render_template, request, redirect, url_for

from quiz_app import commands, public, user
from quiz_app.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)



def create_app(config_object="quiz_app.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


"""@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        # Handle form submissions
        theme = request.form["theme"]
        difficulty = request.form["difficulty"]
        # Get quiz questions from Open Trivia Database
        response = requests.get(f"https://opentdb.com/api.php?amount=10&category={theme}&difficulty={difficulty}&type=multiple")
        questions = response.json()["results"]
        score = 0
        # Evaluate the answers and keep track of the score
        for question in questions:
            answer = request.form[question["question"]]
            if answer == question["correct_answer"]:
                score += 1
        # Save the score to the database

        return redirect(url_for("index"))
    return render_template("quiz.html")"""