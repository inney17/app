import os

from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'

mysql = MySQL(app)

# Configuration pour le téléchargement des fichiers
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'votre_clé_secrète'  # Clé secrète pour les sessions

# Fonction pour vérifier si le fichier a une extension autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route : Page d'accueil
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire")  # Récupérer tous les prestataires
    prestataire = cur.fetchall()  # Cela retourne toutes les lignes
    cur.close()

    return render_template('index.html', prestataire=prestataire)


# Route : Connexion admin
@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérification des identifiants (admin et mot de passe statiques)
        if username == 'admin' and password == 'admin123':
            session['admin'] = True  # Créer une session pour l'admin


            return redirect(url_for('admin_dashboard'))
        else:
            return "Identifiants incorrects, veuillez réessayer", 400



# Route : Tableau de bord admin
@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect(url_for('index'))  # Si l'admin n'est pas connecté, rediriger vers la page d'accueil

    # Récupérer les prestataires depuis la base de données
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire")  # Récupérer tous les prestataires
    prestataire = cur.fetchall()
    cur.close()

    return render_template('admin_dashboard.html', prestataire=prestataire)

# Route : Déconnexion de l'admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)  # Supprimer la session de l'admin
    return redirect(url_for('index'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # Récupérer toutes les données du prestataire  pour le formulaire


    if request.method == 'POST':
        nom = request.form.get('Nom')
        prenom = request.form.get('prenom')
        téléphone = request.form.get('téléphone')  # Valeur de la catégorie sélectionnée
        email = request.form.get('email')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        catégorie = request.form.get('catégorie')
        password = request.form.get('password')
        file = request.files['image']

        image_path = None
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO prestataire (nom, prenom, téléphone,image_path, email, statut, commune,genre,langue, catégorie,password) 
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, catégorie,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('inscription.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM prestataire WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Connexion à la base de données pour récupérer les informations de l'utilisateur
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire WHERE id = %s", (id,))
    prestataire = cur.fetchone()
    cur.close()

    # Si la méthode est POST, on met à jour les informations de l'utilisateur
    if request.method == 'POST':
        # Récupérer les nouvelles informations du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        téléphone = request.form.get('téléphone')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        catégorie = request.form.get('catégorie')
        file = request.files['image']

        image_path = prestataire[10]  # Garder l'ancienne image par défaut

        # Vérifier si un fichier d'image est téléchargé
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"  # Nouvelle image

        # Connexion à la base de données pour mettre à jour les informations
        cur = mysql.connection.cursor()
        cur.execute("""
                     UPDATE prestataire 
                     SET nom = %s, prenom = %s, email = %s, téléphone = %s, statut = %s, 
                         commune = %s, genre = %s, langue = %s, catégorie = %s, image_path = %s

                     WHERE id = %s
                 """, (nom, prenom, email, téléphone, statut, commune, genre, langue, catégorie, image_path, id))

        mysql.connection.commit()
        cur.close()
        # Rediriger l'utilisateur vers la page d'accueil ou vers un message de succès
        return redirect(url_for('index'))  # Vous pouvez rediriger vers la page de votre choix

        # Si la méthode est GET, on affiche le formulaire avec les informations actuelles de l'utilisateur
    return render_template('update.html', prestataire=prestataire)

@app.route('/statistics')
def statistics():
    cur = mysql.connection.cursor()

    # Récupérer des statistiques supplémentaires ou spécifiques
    cur.execute("SELECT COUNT(*) FROM prestataire")
    total_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'active'")
    active_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'inactive'")
    inactive_prestataire = cur.fetchone()[0]

    # Si tu veux ajouter d'autres statistiques ou graphiques
    cur.execute("SELECT COUNT(DISTINCT catégorie) FROM prestataire")
    total_catégorie = cur.fetchone()[0]


    cur.close()

    # Retourner un template où on affiche ces stats
    return render_template('statistics.html',
                           total_prestataire=total_prestataire,
                           active_prestataire=active_prestataire,
                           inactive_prestataire=inactive_prestataire,
                           total_catégorie=total_catégorie)



if __name__ == "__main__":
    app.run(debug=True)