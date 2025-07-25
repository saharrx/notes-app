from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Note, User
from app import db


notes = Blueprint('notes', __name__)

@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user_notes = Note.query.filter_by(user_id=user_id).all()

    notes_list = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "date_created": note.date_created.isoformat()
        }
        for note in user_notes
    ]

    return jsonify(notes_list), 200


@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400
    
    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created successfully"}), 201


@notes.route('/notes', methods=['PUT'])
@jwt_required
def update_note(note_id): #u should pass the note id in url
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"error":"Note not found"}), 404
    
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()

    return jsonify({"message": "Note updated"}), 200