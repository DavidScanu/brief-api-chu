from database import get_db_config, db_connect, db_close
from flask import Flask, request, jsonify, Response, render_template
import json
from config_flask import Config

app = Flask(__name__)
app.config["DEBUG"] = True
# Auto-refresh
app.jinja_env.auto_reload = True
app.config.from_object(Config)

# CONSTANTS
VERBOSE = True
CONFIG_FILE_PATH = 'config.json'
CONFIG = get_db_config(CONFIG_FILE_PATH)

# API DOCUMENTATION
@app.route('/', methods=['GET'])
def documentation():
    return render_template('index.html')

# READ
@app.route('/materiels', methods=['GET'])
def api_get_materiels():
    """Route qui retourne tous les materiels dans un objet JSON."""
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""SELECT id, nom, dimension, etat FROM materiels"""
        cursor.execute(query)
        materiels = cursor.fetchall()
        materiels_list = []
        for materiel in materiels :
            materiel_dict = {}
            materiel_dict['id'] = materiel[0]
            materiel_dict['nom'] = materiel[1]
            materiel_dict['dimension'] = materiel[2]
            materiel_dict['etat'] = materiel[3]
            materiels_list.append(materiel_dict)
        return jsonify(materiels_list)
    except Exception as e:
        print("Get materiels : something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)


# READ
@app.route('/materiel/<int:materiel_id>', methods=['GET'])
def api_get_materiel(materiel_id):
    """Route qui retourne un materiel en focntion de son ID."""
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""SELECT id, nom, dimension, etat FROM materiels WHERE id={materiel_id};"""
        cursor.execute(query)
        materiel = cursor.fetchone()
        return jsonify({"id":materiel[0], "nom":materiel[1], "dimension":materiel[2], "etat":materiel[3]})
    except Exception as e:
        print("Get materiel : something went wrong.")
        print(e)
        # return jsonify({"error": e})
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)

# CREATE
# Add an animal
@app.route('/add_materiel', methods=['POST'])
def api_add_materiel():
    try :
        data = request.get_json()
        materiel_nom = data["nom"]
        materiel_dimension = data["dimension"]
        materiel_etat = data["etat"]
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""INSERT INTO materiels (nom, dimension, etat) VALUES ("{materiel_nom}", "{materiel_dimension}", "{materiel_etat}");"""
        cursor.execute(query)
        bdd.commit()
        return jsonify({"message" : "Materiel ajouté avec succès !"})
    except Exception as e:
        print("Add materiel : something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)

# UPDATE
@app.route('/update_materiel/<int:materiel_id>', methods=['PUT'])
def api_update_materiel(materiel_id):
    try :
        data = request.get_json()
        materiel_nom = data["nom"]
        materiel_dimension = data["dimension"]
        materiel_etat = data["etat"]
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""UPDATE materiels SET nom="{materiel_nom}", dimension="{materiel_dimension}", etat="{materiel_etat}" WHERE id = {materiel_id};"""
        cursor.execute(query)
        bdd.commit()
        return jsonify({"message" : "Materiel mis à jour avec succès !"})
    except Exception as e:
        print("Update animal : something went wrong.")
        print(e)
        return jsonify({"message" : "Update materiel : something went wrong."})
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)

#DELETE
@app.route('/delete_materiel/<int:materiel_id>', methods=['DELETE'])
def api_delete_materiel(materiel_id):
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""DELETE FROM materiels WHERE id={materiel_id};"""
        cursor.execute(query)
        bdd.commit()
        return jsonify({"message" : "Materiel supprimé avec succès !"})
    except Exception as e:
        print("Delete materiel : something went wrong.")
        print(e)
        return jsonify({"message" : "Delete materiel : something went wrong."})
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)




# READ
@app.route('/employes', methods=['GET'])
def api_get_employes():
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""SELECT id, nom, prenom, age, poste FROM employes"""
        cursor.execute(query)
        employes = cursor.fetchall()
        employes_list = []
        for employe in employes :
            employe_dict = {}
            employe_dict['id'] = employe[0]
            employe_dict['nom'] = employe[1]
            employe_dict['prenom'] = employe[2]
            employe_dict['age'] = employe[3]
            employe_dict['poste'] = employe[4]
            employes_list.append(employe_dict)
        return jsonify(employes_list)
    except Exception as e:
        print("Get employes : something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)

# READ
@app.route('/employe/<int:employe_id>', methods=['GET'])
def api_get_employe(employe_id):
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""SELECT id, nom, prenom, age, poste FROM employes WHERE id={employe_id};"""
        cursor.execute(query)
        employe = cursor.fetchone()
        return jsonify({"id":employe[0], "nom":employe[1], "prenom":employe[2], "age":employe[3], "poste":employe[4]})
    except Exception as e:
        print("Get employe : something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)


# CREATE
@app.route('/add_employe', methods=['POST'])
def api_add_employe():
    try :
        data = request.get_json()
        nom = data["nom"]
        prenom = data["prenom"]
        age = data["age"]
        poste = data["poste"]
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""INSERT INTO employes (nom, prenom, age, poste) VALUES ("{nom}", "{prenom}", "{age}", "{poste}");"""
        cursor.execute(query)
        bdd.commit()
        return jsonify({"message" : "Employé ajouté avec succès !"})
    except Exception as e:
        print("Add employe : something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)

#DELETE
@app.route('/delete_employe/<int:employe_id>', methods=['DELETE'])
def api_delete_employe(employe_id):
    try :
        bdd = db_connect(CONFIG, VERBOSE)
        cursor = bdd.cursor()
        query = f"""DELETE FROM employes WHERE id={employe_id};"""
        cursor.execute(query)
        bdd.commit()
        return jsonify({"message" : "Employé supprimé avec succès !"})
    except Exception as e:
        print("Delete employe : something went wrong.")
        print(e)
        return jsonify({"message" : "Delete employe : something went wrong."})
    finally:
        if bdd.is_connected():
            cursor.close()
            db_close(bdd, VERBOSE)


if __name__ == "__main__":
    app.run()
