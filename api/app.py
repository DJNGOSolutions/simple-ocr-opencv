from flask import Flask
from flask_cors import CORS
from api import db
from api import ocr_controller

app = Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER = './uploads'

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:root@localhost:5432/aca'

db.db.init_app(app)
app.app_context().push()
app.register_blueprint(ocr_controller.ocr_controller)


@app.route('/')
def hello_world():
    return 'Hello World!'


def init_db():
    with app.app_context():
        db.db.create_all()
        db.db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
