from .db import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    # Fields
    value = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % str(self.__dict__)
