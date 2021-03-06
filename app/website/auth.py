from flask import  Blueprint, redirect , url_for , render_template, request, flash
from .models import Candidat,Entreprise,User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
 
auth = Blueprint('auth',__name__)

#definir les admin du site
liste_admin = ["loic"]
admin = False

@auth.route("/login", methods = ['POST',"GET"])
def login():
    if request.method =="POST":
        username = request.form.get("utilisateur")
        user_password =  request.form.get("mdp")
        
        found_user = Candidat.query.filter_by(username = username).first() or Entreprise.query.filter_by(username = username).first()
        if found_user : 
            if check_password_hash(found_user.password,user_password) :
                login_user(found_user)
                
                
                if (username in liste_admin) and (found_user.compte != "admin"):
                    found_user.compte = "admin"
                    db.session.commit()

                flash(f"vous êtes bien connecté {username}", category="success")
                return redirect(url_for("views.matching"))
            else:
                flash("erreur de mot de passe!", category="fail")
        else:
            flash("ce compte n'existe pas", category="fail")
    else:
       if current_user.is_authenticated :
           flash(f"vous êtes deja connecté {current_user.username}", "fail")
           return redirect(url_for("views.matching"))
        
    return render_template("/authentification/login.html")
        
@auth.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated :
        logout_user()
        flash("vous êtes bien deconnete !",'succes')
    else:
        flash("authentifié vous d'abord",'fail')
    return redirect(url_for("auth.login"))
    

@auth.route("/signup", methods = ["POST","GET"])
def signup():       
    if request.method =="POST":
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")
        email = request.form.get("email")
        username = request.form.get("utilisateur")
        user_password =  request.form.get("mdp")
        verif_password =  request.form.get("mdp_check")
        naissance  = request.form.get("naissance")
        sexe = request.form.get("sexe")
        compte = "candidat"

        #verification du username dans la base de données
        found_user = Candidat.query.filter_by(username = username).first() #TODO: y'a que le username qui est unique ici
         
        #verification des informations valides
        longueur_key = False
        for key in [first_name,last_name,email,username,user_password]:
            if len(key) > 19 :
                longueur_key = True
                break
            else :
                longueur_key = False
                
        if user_password != verif_password :
            flash("mots de passe differents", category ='fail')
        elif longueur_key :
            flash("20 charactères maximum !", category ="fail")        
        elif found_user : 
            flash(f"le username {username} est deja prit !", category ='fail')         
        else: 
            new_user= Candidat(first_name=first_name,last_name=last_name,username=username,
                               naissance=naissance,sexe=sexe,compte=compte,email=email,
                               password =generate_password_hash(user_password, method="sha256"))
            
                
                        
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            
            flash(f"vous avez bien creer un compte candidat {username}",category ='success')
            return redirect(url_for("views.matching"))
    else:
         if current_user.is_authenticated :
             flash(f"deconnectez-vous d'abord {current_user.username}",'fail')
             return redirect(url_for("views.matching"))
    return render_template("/authentification/signup.html")


@auth.route("/entreprise_signup", methods = ["POST","GET"])
def entreprise_signup():       
    if request.method =="POST":
        entreprise = request.form.get("entreprise")
        username = request.form.get("utilisateur")
        siret = request.form.get("siret")
        email = request.form.get("email")
        user_password =  request.form.get("mdp")
        verif_password =  request.form.get("mdp_check")
        compte = "entreprise"

        #verification du username dans la base de données
        found_user = Entreprise.query.filter_by(nom = entreprise).first() #TODO: y'a que le username qui est unique ici
         
        #verification des informations valides
        longueur_key = False
        for key in [entreprise,username,email,siret,user_password]:
            if len(key) > 19 :
                longueur_key = True
                break
            else :
                longueur_key = False
                
        if user_password != verif_password :
            flash("mots de passe differents", category ='fail')
        elif longueur_key :
            flash("20 charactères maximum !", category ="fail")        
        elif found_user : 
            flash(f"le username {entreprise} est deja prit !", category ='fail')         
        else: 
            new_user= Entreprise(nom=entreprise,username=username,
                                 compte=compte,email=email,siret=siret,
                                 password =generate_password_hash(user_password, method="sha256"))
               
                                        
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            
            flash(f"vous avez bien creer un compte entreprise {username}",category ='success')
            return redirect(url_for("views.matching"))
    else:
         if current_user.is_authenticated :
             flash(f"deconnectez-vous d'abord {current_user.username}",'fail')
             return redirect(url_for("views.matching"))
    return render_template("/authentification/entreprise_signup.html")
