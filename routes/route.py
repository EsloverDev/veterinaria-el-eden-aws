from controller.controller import *
from server import app

@app.route("/")
def home():
    return func_home_page()

@app.route("/register_page")
def register_page():
    return func_register_page()
    
@app.route("/consult_page")
def consult_page():
    return func_consult_page()
    
@app.route("/register_user", methods=["post"])
def register_user():
    return func_register_user()

@app.route("/consult_pet", methods=["post"])
def consult_pet():
    return func_consult_pet()