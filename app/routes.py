from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from app.models import User, Course, Enrollment, Grade, Role  # Assure-toi d'importer le modèle 'Role'
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

# Route d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash("Connexion réussie !", "success")  # Message de succès
            return redirect(next_page or url_for('dashboard'))  # Redirige vers le dashboard
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")  # Message d'erreur
    return render_template('login.html', form=form)

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # Convertir l'ID du rôle en entier
        role_id = int(form.role.data)  # Convertir en entier

        # Récupérer le rôle avec l'ID
        role = Role.query.get(role_id)

        # Vérifier si le rôle existe
        if not role:
            flash("Le rôle sélectionné est invalide.", "danger")
            return redirect(url_for('register'))

        # Créer l'utilisateur avec l'ID du rôle
        user = User(username=form.username.data, password=hashed_password, role_id=role.id)
        db.session.add(user)
        db.session.commit()

        # Recharger l'utilisateur pour s'assurer que le rôle est bien chargé
        user = User.query.get(user.id)  # Rechercher à nouveau l'utilisateur dans la base pour récupérer son rôle

        # Connexion de l'utilisateur après l'inscription
        login_user(user, remember=True)  # Le paramètre `remember=True` peut être utilisé pour garder l'utilisateur connecté
        flash("Vous êtes maintenant inscrit et connecté !", "success")
        return redirect(url_for('dashboard'))  # Redirige vers le dashboard

    return render_template('register.html', form=form)


# Route du dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Vérifier le rôle de l'utilisateur
    if current_user.role.name == 'Etudiant':
        return render_template('dashboard_etudiant.html', notes=Grade.query.filter_by(user_id=current_user.id).all(), courses=Course.query.all())
    elif current_user.role.name == 'Enseignant':
        return render_template('dashboard_professeur.html', courses=Course.query.all(), grades=Grade.query.all())
    elif current_user.role.name == 'Secrétaire':
        return render_template('dashboard_secretaire.html', courses=Course.query.all(), grades=Grade.query.all(), users=User.query.all())
    else:
        flash("Rôle non reconnu", "danger")
        return redirect(url_for('home'))




# Mise à jour d'un cours (pour les secrétaires)
@app.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    if current_user.role.name != 'Secrétaire':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form['description']
        course.hours = int(request.form['hours'])
        course.course_type = request.form['course_type']

        db.session.commit()
        flash("Cours mis à jour avec succès", "success")
        return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard

    return render_template('update_course.html', course=course)

# Ajouter un cours (pour les secrétaires)
@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.role.name != 'Secrétaire':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        hours = int(request.form['hours'])
        course_type = request.form['course_type']
        
        new_course = Course(title=title, description=description, hours=hours, course_type=course_type)
        db.session.add(new_course)
        db.session.commit()
        flash("Cours ajouté avec succès", "success")
        return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard

    return render_template('add_course.html')

# Supprimer un cours (pour les secrétaires)
@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if current_user.role.name != 'Secrétaire':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Cours supprimé avec succès", "success")
    return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard



# Ajouter une inscription
@app.route('/add_enrollment', methods=['GET', 'POST'])
@login_required
def add_enrollment():
    if current_user.role.name != 'Secrétaire':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        course_id = request.form['course_id']

        # Vérifie si l'inscription existe déjà
        existing_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existing_enrollment:
            flash("L'étudiant est déjà inscrit à ce cours", "danger")
            return redirect(url_for('dashboard'))  # Redirige vers le dashboard

        # Créer une nouvelle inscription
        new_enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        flash("Inscription ajoutée avec succès", "success")
        return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard

    return redirect(url_for('dashboard'))  # Si ce n'est pas une requête POST, on redirige


# Supprimer une inscription
@app.route('/delete_enrollment/<int:enrollment_id>', methods=['POST'])
@login_required
def delete_enrollment(enrollment_id):
    if current_user.role.name != 'Secrétaire':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    flash("Inscription supprimée avec succès", "success")
    return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard




@app.route('/delete_grade/<int:grade_id>', methods=['POST'])
@login_required
def delete_grade(grade_id):
    # Vérification du rôle de l'utilisateur (par exemple, un professeur)
    if current_user.role.name != 'Professeur':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))
    
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    flash("Note supprimée avec succès", "success")
    return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard

# Mise à jour d'une note (pour les professeurs)
# Mise à jour d'une note (pour les professeurs)
@app.route('/update_grade/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def update_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)

    # Vérifie si l'utilisateur est un enseignant
    if current_user.role.name != 'Enseignant':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Récupère la note envoyée via le formulaire
        grade.grade = request.form['grade']
        db.session.commit()
        flash("Note mise à jour avec succès", "success")
        return redirect(url_for('dashboard'))  # Redirige vers la route générique du dashboard

    # Si la méthode est GET, on affiche le formulaire avec la note actuelle
    return render_template('update_grade.html', grade=grade)


@app.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():


    users = User.query.all()
    courses = Course.query.all()

    if request.method == 'POST':
        user_id = request.form['user_id']
        course_id = request.form['course_id']
        grade_value = float(request.form['grade'])
        exam_type = request.form['exam_type']

        new_grade = Grade(user_id=user_id, course_id=course_id, grade=grade_value, exam_type=exam_type)
        db.session.add(new_grade)
        db.session.commit()
        flash("Note ajoutée avec succès", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_grade.html', users=users, courses=courses)



# Mise à jour d'un utilisateur
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if current_user.role.name != 'Secrétaire':  # Assurez-vous que c'est un administrateur
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.role_id = request.form['role_id']
        db.session.commit()
        flash("Utilisateur mis à jour avec succès", "success")
        return redirect(url_for('dashboard'))

    # Liste des rôles possibles à afficher dans un select
    roles = Role.query.all()
    return render_template('update_user.html', user=user, roles=roles)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role.name != 'Secrétaire':  # Vérification du rôle
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé avec succès", "success")
    return redirect(url_for('dashboard'))





# Déconnexion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté avec succès.", "info")  # Message de déconnexion
    return redirect(url_for('home'))  # Redirige vers la page d'accueil
