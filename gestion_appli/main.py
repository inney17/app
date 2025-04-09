from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import os

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

if __name__ == "__main__":
    app.run(debug=True)
