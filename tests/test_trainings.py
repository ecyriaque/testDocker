import unittest
import requests

class AddTrainingTestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5050'

    def test_add_training_missing_datas_key(self):
         # Envoie une requête POST avec un corps JSON qui ne comprend pas la clé 'datas'
        response = requests.post(
            f'{self.BASE_URL}/trainings/add',
            json={},  # An empty dict does not have the 'datas' key
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request status code")
        response_json = response.json()
        self.assertIn('message', response_json, "JSON response does not contain 'message' key")
        self.assertEqual(response_json['message'], "Données manquantes", "Expected error message 'Données manquantes' not found in the response")
   
    def test_add_training_empty_name(self):
        # Envoie une requête POST avec 'name' comme chaîne vide
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': '', 'id_Degree': 1}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "Le nom du parcours est requis")

    def test_add_training_missing_name(self):
        # Envoie une requête POST sans la clé 'name' dans le corps JSON
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'id_Degree': 1}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'),"Le champ 'name' est requis")

    def test_add_training_invalid_id_degree_type(self):
         # Envoie une requête POST sans la clé 'name' dans le corps JSON
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': 'Training Name', 'id_Degree': 'invalid'}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "L'identifiant du diplôme doit être un entier")

    def test_add_training_nonexistent_id_degree(self):
       # Envoie une requête POST avec un 'id_Degree' qui n'existe pas
       # Vous devez simuler ou vous assurer que la fonction does_entry_exist renverra False pour le 'id_Degree' utilisé ici
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': 'Training Name', 'id_Degree': 9999999999}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'),"La formation spécifiée n'existe pas."),

class GetTrainingTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5050/trainings"  # Mettez à jour avec l'URL de base de votre API

    def test_get_training_success(self):
        # Teste le cas où le parcours existe
        response = requests.get(f"{self.BASE_URL}/get/3")  # Assurez-vous que le parcours avec l'ID 1 existe dans la base de données pour ce test
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json())



class TestUpdateTraining(unittest.TestCase):
    BASE_URL = "http://localhost:5050/trainings/update"

    def test_update_training_success(self):
        """ Test de la mise à jour réussie d'un parcours avec des données valides """
        valid_training_id = 3
        valid_degree_id = 1   
        new_name = "Parcours Mis à Jour"
        response = requests.put(f"{self.BASE_URL}/{valid_training_id}", json={"datas": {"name": new_name, "id_Degree": valid_degree_id}})
        self.assertEqual(response.status_code, 200)
        self.assertIn(new_name.lower(), response.json().get("message").lower())

    def test_update_training_not_found(self):
        """ Test de la mise à jour d'un parcours qui n'existe pas """
        invalid_training_id = 99999 
        new_name = "Nom de Parcours Test"
        response = requests.put(f"{self.BASE_URL}/{invalid_training_id}", json={"datas": {"name": new_name, "id_Degree": 1}})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Le parcours spécifié n'existe pas.", response.json().get("message"))

    def test_update_training_invalid_degree(self):
        """ Test de la mise à jour d'un parcours avec un identifiant de diplôme invalide """
        valid_training_id = 1 
        invalid_degree_id = 22222
        update_data = {
            "datas": {
                "name": "Nom de Parcours Mis à Jour",
                "id_Degree": invalid_degree_id
            }
        }
        response = requests.put(f"{self.BASE_URL}/{valid_training_id}", json=update_data)
        self.assertEqual(response.status_code, 404)  # Attendre un 404 si le diplôme n'existe pas
        self.assertIn("La formation spécifiée n'existe pas.", response.json().get("message"))

    def test_update_training_missing_parameters(self):
        """ Test de la mise à jour d'un parcours avec des paramètres manquants """
        valid_training_id = 1
        response = requests.put(f"{self.BASE_URL}/{valid_training_id}", json={"datas": {}})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Le nom du parcours est requis", response.json().get("message"))

import unittest
import requests

class DeleteTrainingTestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5050/trainings'

    def setUp(self):
        # Ajout d'un parcours pour le supprimer plus tard
        add_response = requests.post(
            f'{self.BASE_URL}/add',
            json={'datas': {'name': 'Temporary Training', 'id_Degree': 1}},
            headers={"Content-Type": "application/json"}
        )
        if add_response.status_code == 201:
            self.training_id = add_response.json().get('id')
        else:
            self.training_id = None

    def test_delete_training_success(self):
        # Vérifier si la configuration a été réussie
        if self.training_id is None:
            self.skipTest('Training creation failed in setup, skipping deletion test.')

        # Test de suppression d'un parcours existant
        response = requests.delete(f'{self.BASE_URL}/{self.training_id}')
        self.assertEqual(response.status_code, 200, "Expected 200 OK status code for successful deletion")

    def test_delete_training_not_found(self):
        # Test de suppression d'un parcours qui n'existe pas
        response = requests.delete(f'{self.BASE_URL}/99999999')  # ID très probablement inexistant
        self.assertEqual(response.status_code, 404, "Expected 404 Not Found status code for a non-existent training")

    def tearDown(self):
        # Supprimer le parcours si jamais il n'a pas été supprimé pendant le test
        if self.training_id is not None:
            requests.delete(f'{self.BASE_URL}/{self.training_id}')


if __name__ == "__main__":
    unittest.main()
