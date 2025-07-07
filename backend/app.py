from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["recipe_db"]
recipes = db["recipes"]


def recipe_serializer(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "instructions": recipe["instructions"]
    }


@app.route("/recipes", methods=["GET"])
def get_recipes():
    all_recipes = list(recipes.find())
    return jsonify([recipe_serializer(r) for r in all_recipes])


@app.route("/recipes/<id>", methods=["GET"])
def get_recipe(id):
    recipe = recipes.find_one({"_id": ObjectId(id)})
    if recipe:
        return jsonify(recipe_serializer(recipe))
    return jsonify({"error": "Recipe not found"}), 404


@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.json
    new_recipe = {
        "title": data.get("title"),
        "ingredients": data.get("ingredients", []),
        "instructions": data.get("instructions", "")
    }
    result = recipes.insert_one(new_recipe)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route("/recipes/<id>", methods=["PUT"])
def update_recipe(id):
    data = request.json
    update_data = {
        "title": data.get("title"),
        "ingredients": data.get("ingredients", []),
        "instructions": data.get("instructions", "")
    }
    result = recipes.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count:
        return jsonify({"message": "Recipe updated"})
    return jsonify({"error": "Recipe not found"}), 404


@app.route("/recipes/<id>", methods=["DELETE"])
def delete_recipe(id):
    result = recipes.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Recipe deleted"})
    return jsonify({"error": "Recipe not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
