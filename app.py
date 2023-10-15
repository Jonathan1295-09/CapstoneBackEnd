from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get("DATABASE_URL",None)
db = SQLAlchemy(app) 


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(25), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(500), nullable=False)
    supplies = db.Column(db.String(350), nullable=False)
    image = db.Column(db.String)

    def __init__(self, project_name, start_date, end_date, notes, supplies, image):
        self.project_name = project_name
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.supplies = supplies
        self.image = image

    def as_dict(self):
        """
        Convert the Project object to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "project_name": self.project_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes,
            "supplies": self.supplies,
            "image": self.image
        }
    
    @classmethod
    def projects_to_dicts(cls, projects):
        """
        Convert a list of Project objects to a list of dictionaries.
        """
        return [project.as_dict() for project in projects]
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def main_route():
    return "hello world"


@app.route('/project', methods=['POST'])
def add_project():
    project_name = request.json['project_name']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    notes = request.json['notes']
    supplies = request.json['supplies']
    image = request.json['image']

    new_project = Project(project_name, start_date, end_date, notes, supplies, image)
  
    db.session.add(new_project)
    db.session.commit()

    return jsonify(new_project.as_dict())

@app.route('/projects', methods=['GET'])
def get_projects():
    # Retrieve a list of Project objects from the database
    projects = Project.query.all()

    # Use the class method to convert Project objects to dictionaries
    project_dicts = Project.projects_to_dicts(projects)

    return jsonify(project_dicts), 200

@app.route('/project/<id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)

    if project is not None:
        project_dict = project.as_dict()
        return jsonify(project_dict), 200
    else:
        return jsonify({"error": "Project not found"}), 404
    
@app.route('/project/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)

    project_name = request.json['project_name']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    notes = request.json['notes']
    supplies = request.json['supplies']
    image = request.json['image']

    update_project = Project(project_name, start_date, end_date, notes, supplies, image)

    db.session.commit()

    return jsonify(update_project.as_dict())

@app.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)

    if project is not None:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    else:
        return jsonify({"error": "Project not found"}, 404)

if __name__ == '__main__':
     app.run(debug=True,port=os.environ.get("PORT", 4444))