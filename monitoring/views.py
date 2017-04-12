# -*- coding: utf-8 -*-
"""monitoring"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from flaskapp.utils import flash_errors
from flaskapp.monitoring.automation.monitor import check


# from flaskapp.monitoring.automation import monitor


blueprint = Blueprint('monitoring', __name__, url_prefix='/monitoring', static_folder='../static', template_folder='templates')


@blueprint.route('/')
def test():
    """ external site monitors """
    # return "hi"
    status = check()
    return render_template('/monitoring/external.html',status=status)
