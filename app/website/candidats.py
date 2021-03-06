#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 00:11:41 2021

@author: loic
"""

from flask import  Blueprint, Flask, redirect , url_for , render_template, request, session, flash, jsonify
from flask_login import login_required, current_user
from .models import Candidat,User
from . import db
import json

candidats = Blueprint('candidats',__name__)

@candidats.route("/personnelle")
@login_required
def personnelle():
    if current_user.compte not in ["candidat","admin"]:
        flash("vous n'êtes pas un candidat !",'fail')
        return redirect(url_for("views.matching"))
    else:
        profil_image = url_for("static",filename=f"images/{current_user.profil_image}")
        return render_template("/candidat/personelle.html",profil_image = profil_image)


@candidats.route("/profil")
@login_required
def profil():
    if current_user.compte not in ["candidat","admin"]:
        flash("vous n'êtes pas un candidat !",'fail')
        return redirect(url_for("views.matching"))
    else:
        return render_template("/candidat/profil.html")


@candidats.route("/approfondir")
@login_required
def approfondir():
    if current_user.compte not in ["candidat","admin"]:
        flash("vous n'êtes pas un candidat !",'fail')
        return redirect(url_for("views.matching"))
    else:
        return render_template("/candidat/approfondir.html")
