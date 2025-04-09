from app import db
from app.models import Role

# Créer les rôles
role_etudiant = Role(name="Etudiant")
role_secretaire = Role(name="Secretaire")
role_professeur = Role(name="Professeur")

# Ajouter à la base de données
db.session.add(role_etudiant)
db.session.add(role_secretaire)
db.session.add(role_professeur)
db.session.commit()

print("Rôles ajoutés avec succès.")
