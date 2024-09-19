from . import db

class Section(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    image = db.Column(db.String(200))

class Recipe(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), db.ForeignKey('section.name'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    servings = db.Column(db.Integer, nullable=False)

    section_rel = db.relationship('Section', backref='recipes')