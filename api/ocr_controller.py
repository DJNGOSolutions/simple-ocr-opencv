import os

from flask import request, jsonify, Blueprint, current_app
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

from .textract import extract

from .Document import Document
from .db import db
from .dui import Dui

ocr_controller = Blueprint('ocr_controller', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# helper to store docs
def saveDoc(lines):
    with current_app.app_context():
        doc = Document(
            value=lines,
        )
        db.session.add(doc)
        db.session.commit()


@ocr_controller.route('/duis/<docId>', methods=['PUT', 'OPTIONS'])
def update_document(docId):
    with current_app.app_context():
        doc = Document.query.filter_by(id=docId).first()
        req_data = request.get_json()
        doc.value = req_data['value']
        db.session.commit()
    return 'updated'


@ocr_controller.route('/duis', methods=['GET', 'OPTIONS'])
def show_documents():
    result = []
    with current_app.app_context():
        docs = Document.query.all()
        for doc in docs:
            result.append({
                'id': doc.id,
                'value': doc.value
            })

    return jsonify(result)


# since app is not going to be large and its gonna have a few end-points
# token validations is done without middleware
@ocr_controller.route('/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({
            'status': 400,
            'message': 'No file'
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'status': 400,
            'message': 'No selected file'
        }), 400

    if file and not allowed_file(file.filename):
        return jsonify({
            'status': 400,
            'message': 'Invalid File type'
        })

    filename = secure_filename(file.filename)
    filePath = os.path.join(current_app.root_path, 'uploads', filename)
    file.save(filePath)

    joined, lines, confidence, response = extract(filePath)

    dui = Dui(fs_string=joined)
    saveDoc(joined)
    # response = jsonify({
    #    'status': 200,
    #    'message': 'Success',
    #   'data': dui.front_side,
    #   'confidence': confidence
    # })
    response = jsonify({
        'status': 200,
        'data': joined
    })

    return response if response is not None else {}
