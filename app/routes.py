import os
from flask import Blueprint, request, jsonify, url_for
from werkzeug.utils import secure_filename
from .models import Recipe, Section
from . import db

main = Blueprint('main', __name__)

@main.route('/sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    return jsonify([{'name': section.name, 'image': url_for('static', filename=f'images/{section.image}')} for section in sections])

@main.route('/recipes', methods=['GET'])
def get_recipes_by_section():
    section = request.args.get('section')
    recipes = Recipe.query.filter_by(section=section).all()
    return jsonify([{'name': recipe.name, 'description': recipe.description, 'image': url_for('static', filename=f'images/{recipe.image}')} for recipe in recipes])

@main.route('/recipe/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({
        'name': recipe.name,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'steps': recipe.steps,
        'servings': recipe.servings,
        'image': url_for('static', filename=f'images/{recipe.image}')
    })

@main.route('/recipe', methods=['POST'])
def add_recipe():
    data = request.form
    file = request.files['image']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(request.app.config['UPLOAD_FOLDER'], filename))

    new_recipe = Recipe(
        section=data['section'],
        name=data['name'],
        description=data['description'],
        ingredients=data['ingredients'],
        steps=data['steps'],
        servings=data['servings'],
        image=filename
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe created successfully!'})