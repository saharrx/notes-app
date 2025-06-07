from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/')
def home():
    return "Notes Home Page"
