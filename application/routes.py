from flask import render_template, url_for, request, redirect
from application.forms.register_form import RegisterForm
from application.table import members
from application.data_access import add_member, get_member
from application import app