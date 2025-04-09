from datetime import datetime
from app import db
from flask_login import UserMixin

# Table des rôles
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

# Modèle pour les utilisateurs (étudiants, secrétaires, enseignants)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    # Relation avec le modèle Role
    role = db.relationship('Role', backref='users', lazy=True)
    
    def __repr__(self):
        return f"<User {self.username}>"


# Modèle pour les cours
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    course_type = db.Column(db.String(50), nullable=False)  # CM, TD, TP

    # Relation avec Enrollment (inscriptions)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.title}>'

# Modèle pour les inscriptions des étudiants
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date_enrolled = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation avec User (utilisateur)
    user = db.relationship('User', backref=db.backref('enrollments', lazy=True))

    def __repr__(self):
        return f'<Enrollment {self.user.username} in {self.course.title}>'

# Modèle pour les notes des étudiants
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # Examen final, Examen partiel
    description = db.Column(db.String(500))  # Commentaire du professeur

    # Relation avec User et Course
    user = db.relationship('User', backref=db.backref('grades', lazy=True))
    course = db.relationship('Course', backref=db.backref('grades', lazy=True))

    def __repr__(self):
        return f'<Grade {self.grade} for {self.user.username} in {self.course.title}>'
