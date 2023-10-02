from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime
import mysql.connector
import os #Permite acceder a los directorios
import database as db
from flask_login import LoginManager,logout_user
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import make_response
from flask_paginate import Pagination, get_page_parameter

import re


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,"src", "templates")


app = Flask(__name__, template_folder = template_dir)
# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)