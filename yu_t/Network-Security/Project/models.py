from .extension import db

# Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String)

    # optional
    def __repr__(self):
        return "%d-%r>" % (self.id, self.task)