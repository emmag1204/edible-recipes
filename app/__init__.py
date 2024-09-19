from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/recetario.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')

    db.init_app(app)
    Migrate(app, db)

    from .routes import main
    app.register_blueprint(main)

    @app.cli.command('seed')
    def seed_db():
        from .models import Section, Recipe

        if not Section.query.first():
            sections = [
                Section(name='Drinks', image='drinks.jpg'),
                Section(name='Appetizer', image='appetizer.jpg'),
                Section(name='Entree', image='entree.jpg'),
                Section(name='Dessert', image='dessert.jpg'),
            ]
            db.session.bulk_save_objects(sections)
            db.session.commit()

        if not Recipe.query.first():
            recipes = [
                Recipe(section='Drinks', name='Margarita', description='A classic margarita recipe', ingredients='1 oz tequila, 1 oz lime juice, 1 oz triple sec, salt, ice', steps='Rub the rim of the glass with the lime slice to make the salt stick to it. Take care to moisten only the outer rim and sprinkle the salt on it. The salt should present to the lips of the imbiber and never mix into the cocktail. Shake the other ingredients with ice, then carefully pour into the glass.', servings=1, image='margarita.jpg'),
                Recipe(section='Appetizer', name='Guacamole', description='A classic guacamole recipe', ingredients='2 avocados, 1/2 onion, 1 clove garlic, 1 ripe tomato, 1 lime, salt, pepper, 1 tablespoon cilantro', steps='Peel and mash avocados in a medium serving bowl. Stir in onion, garlic, tomato, lime juice, salt and pepper. Season with remaining lime juice and cilantro. Chill for half an hour to blend flavors.', servings=4, image='guacamole.jpg'),
                Recipe(section='Entree', name='Spaghetti Carbonara', description='A classic spaghetti carbonara recipe', ingredients='1 lb spaghetti, 2 eggs, 1 lb bacon, 1/2 cup grated Parmesan cheese, 1/2 cup heavy cream, salt, pepper', steps='Bring a large pot of salted water to a boil. Meanwhile, in a large skillet, cook bacon until crisp. Drain and set aside. In a large bowl, beat together eggs, Parmesan, cream, salt, and pepper. Cook pasta in boiling water until al dente. Drain well. Quickly toss hot pasta with egg mixture, bacon, and parsley.', servings=4, image='spaghetti-carbonara.jpg'),
                Recipe(section='Dessert', name='Apple Pie', description='A classic apple pie recipe', ingredients='1 recipe pastry for a 9 inch double crust pie, 1/2 cup unsalted butter, 3 tablespoons all-purpose flour, 1/4 cup water, 1/2 cup white sugar, 1/2 cup packed brown sugar, 8 Granny Smith apples - peeled, cored and sliced', steps='Preheat oven to 425 degrees F (220 degrees C). Melt the butter in a saucepan. Stir in flour to form a paste. Add water, white sugar and brown sugar, and bring to a boil. Reduce temperature and let simmer. Place the bottom crust in your pan. Fill with apples, mounded slightly. Cover with a lattice work crust. Gently pour the sugar and butter liquid over the crust. Pour slowly so that it does not run off.', servings=8, image='apple-pie.jpg'),
            ]   
            db.session.bulk_save_objects(recipes)
            db.session.commit()

        print('Database seeded!')

    return app
