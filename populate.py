from database import get_db_config, db_connect, db_close
import json

# CONSTANTS
VERBOSE = True
CONFIG_FILE_PATH = 'config.json'
CONFIG = get_db_config(CONFIG_FILE_PATH)

bdd = db_connect(CONFIG, VERBOSE)

def add_row_materiels(bdd, nom, dimension, etat):
    """Fonction qui ajoute une ligne à la table 'materiel'."""
    try :
        cursor = bdd.cursor()
        query = f"""INSERT INTO materiels (nom, dimension, etat) VALUES ("{nom}", "{dimension}", "{etat}");"""
        print(f"""Query => {query}""")
        cursor.execute(query)
        bdd.commit()
    except Exception as e:
        print("Something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()

def add_row_employes(bdd, nom, prenom, age, poste):
    """Fonction qui ajoute une ligne à la table 'employes'."""
    try :
        cursor = bdd.cursor()
        query = f"""INSERT INTO employes (nom, prenom, age, poste) VALUES ("{nom}", "{prenom}", "{age}", "{poste}");"""
        print(f"""Query => {query}""")
        cursor.execute(query)
        bdd.commit()
    except Exception as e:
        print("Something went wrong.")
        print(e)
    finally:
        if bdd.is_connected():
            cursor.close()


def read_json(file_path):
    """Fonction qui lit un fichier JSON."""
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

data = read_json('data.json')

def populate_materiels(data):
    """Fonction qui remplit la table 'materiels' avec les données du fichier JSON."""
    for materiels in data["materiel"]:
        for materiel in materiels.values():
            materiel_nom = str(materiel[0]).strip()
            materiel_dimension = str(materiel[1]).strip()
            materiel_etat = str(materiel[2]).strip()
            add_row_materiels(bdd, materiel_nom, materiel_dimension, materiel_etat)

def populate_employes(data):
    """Fonction qui remplit la table 'employes' avec les données du fichier JSON."""
    for employes in data["employé.e informatique"]:
        for employe in employes.values():
            employe_nom = str(employe[0]).strip()
            employe_prenom = str(employe[1]).strip()
            employe_age = employe[2]
            employe_poste = str(employe[3]).strip()
            add_row_employes(bdd, employe_nom, employe_prenom, employe_age, employe_poste)  

# Populate table 'materiels'
populate_materiels(data)
# Populate table 'employes'
populate_employes(data)

db_close(bdd, VERBOSE)