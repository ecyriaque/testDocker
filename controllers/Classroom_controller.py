from flask import request, jsonify, Blueprint
from services.classroom import ClassroomService
from entities.DTO.materials import Material
import connect_pg
Classroom_bp = Blueprint('classrooms', __name__)


Classroom_service = ClassroomService()

@Classroom_bp.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    """
Récupérer toutes les salles de classe.

---
tags:
  - Salles de classe
parameters:
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "dto"
    enum: ["model", "dto"]
responses:
  200:
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        },
        {
            "id": 2,
            "name": "Salle2",
            "capacity": 40,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 8
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 12
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_classroom=None)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@Classroom_bp.route('/classrooms/<int:id_Classroom>', methods=['GET'])
def get_classroom(id_Classroom):
    """
Récupérer une salle de classe via son id
---
tags:
  - Salles de classe
parameters:
  - name: id_Classroom
    in: path
    description: L'identifiant unique de la salle de classe à laquelle ajouter les équipements.
    required: true
    type: integer
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "dto"
    enum: ["model", "dto"]
responses:
  200:
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_Classroom,)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

# Add a new route for searching classrooms with criteria
@Classroom_bp.route('/classrooms/search', methods=['GET'])
def search_classrooms():
    """
    Rechercher des salles de classe en fonction de critères spécifiés.
    ---
    tags:
      - Salles de classe
    parameters:
      - name: name
        in: query
        description: Le nom de la salle de classe à rechercher (optionnel).
        required: false
        type: string
      - name: capacity
        in: query
        description: La capacité de la salle de classe à rechercher (optionnel).
        required: false
        type: integer
      - name: equipment
        in: query
        description: Le matériel présent dans la salle de classe à rechercher (optionnel).
        required: false
        type: string
      - name: output_format
        in: query
        description: Le format de sortie des données (par défaut "model").
        required: false
        type: string
        default: "dto"
        enum: ["model", "dto"]
    responses:
      200:
        description: Liste des salles de classe récupérées depuis la base de données.
        examples:
          application/json: [
            {
                "id": 1,
                "name": "Salle1",
                "capacity": 30,
                "materials": [
                  {
                    "id": 1,
                    "equipment": "Ordinateur portable",
                    "quantity": 10
                  },
                  {
                    "id": 2,
                    "equipment": "Tableau blanc",
                    "quantity": 5
                  }
                ]
            },
            # ... (other classrooms)
          ]
      500:
        description: Erreur serveur en cas de problème lors de la recherche des salles de classe.
    """
    try:
        # Extract query parameters
        name = request.args.get('name', None)
        capacity = request.args.get('capacity', None)
        equipment = request.args.get('equipment', None)
        output_format = request.args.get('output_format', 'model')

        # Call the search function in your ClassroomService
        classrooms = Classroom_service.search_classrooms(name, capacity, equipment, output_format)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@Classroom_bp.route('/classrooms/<int:id_Classroom>/equipments', methods=['POST'])
def add_equipments_to_classroom(id_Classroom ):
    """
Ajouter des équipements à une salle de classe.

---
tags:
  - Salles de classe
parameters:
  - name: id_Classroom
    in: path
    description: L'identifiant unique de la salle de classe à laquelle ajouter les équipements.
    required: true
    type: integer
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        equipment_ids:
          type: array
          description: La liste des IDs des équipements à ajouter.
          items:
            type: integer
          example: [1, 2, 3]
responses:
  201:
    description: Les équipements ont été ajoutés avec succès à la salle de classe.
  400:
    description: Requête invalide ou données manquantes.
  404:
    description: La salle de classe spécifiée n'existe pas.
  500:
    description: Erreur serveur lors de l'ajout des équipements.

Example:
  Pour ajouter plusieurs équipements à une salle de classe avec l'ID 1, envoyez une requête POST avec les données JSON
  comme indiqué ci-dessus.
"""

    try:
        equipment_ids = request.json.get('equipment_ids', [])
        
        if not connect_pg.does_entry_exist("Classroom", id_Classroom):
            return jsonify({"message": "La salle de classe spécifiée n'existe pas."}), 404

        if not equipment_ids:
            return jsonify({"message": "Aucun équipement spécifié à ajouter."}), 400

        Classroom_service.add_equipments_to_classroom(id_Classroom, equipment_ids)

        return jsonify({"message": "Les équipements ont été ajoutés avec succès à la salle de classe"}), 201
    except Exception as e:
        return jsonify({"message": f"Erreur lors de l'ajout des équipements : {str(e)}"}), 500
