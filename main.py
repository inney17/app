import os

from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)
    lu = db.Column(db.Boolean, default=False)  # Pour savoir si le message a été lu

app = Flask(__name__)

app.secret_key = '07_17_53'
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
@app.route('/')
def index():

    cur = mysql.connection.cursor()

    # Requête SQL pour récupérer les prestataires et leurs catégories
    cur.execute('''
       SELECT prestataire.id, prestataire.nom, prestataire.prenom, prestataire.téléphone,
               prestataire.email, prestataire.statut, prestataire.commune, prestataire.genre,
               prestataire.langue, service.catégorie, prestataire.image_path
        FROM prestataire
        JOIN service ON prestataire.id_service = service.id_service
        WHERE prestataire.statut = 'active'
    ''')

    prestataire = cur.fetchall()

    # Fermer le curseur
    cur.close()

    # Passer les prestataires récupérés à la template
    return render_template('index.html', prestataire=prestataire)


# Route : Connexion admin

import os
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# Configuration du dossier d'upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        téléphone = request.form.get('téléphone')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        service_id = request.form.get('id_service')
        prix = request.form.get('prix')
        password = request.form.get('password')

        if not password:
            return render_template('inscription.html', error="Le mot de passe ne peut pas être vide")
        if len(password) < 6:
            return render_template('inscription.html', error="Le mot de passe doit contenir au moins 6 caractères")

        # Gérer les fichiers image
        def save_file(fieldname):
            f = request.files.get(fieldname)
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return f"{UPLOAD_FOLDER}/{filename}"
            return None

        image_path = save_file('image')
        carte_identite_path = save_file('carte_identité')
        casier_judiciaire_path = save_file('casier_judiciaire')
        papier_sejour_path = save_file('papier_séjour')

        # Hachage du mot de passe
        hashed_password = generate_password_hash(password)

        # Insertion dans la base de données
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO prestataire (
                nom, prenom, téléphone, image_path, email, statut, commune,
                genre, langue, id_service,prix, hashed_password,
                carte_identité, casier_judiciaire, papier_séjour
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nom, prenom, téléphone, image_path, email, statut, commune,
            genre, langue, service_id,prix, hashed_password,
            carte_identite_path, casier_judiciaire_path, papier_sejour_path
        ))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    # Récupérer les services
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_service, catégorie FROM service")
    service = cur.fetchall()
    cur.close()

    return render_template('inscription.html', service=service)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM prestataire WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Récupérer les services disponibles pour l'affichage dans le select
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM service")
    services = cur.fetchall()
    cur.close()

    # Récupérer les infos du prestataire à modifier
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT prestataire.*, service.catégorie 
        FROM prestataire 
        JOIN service ON prestataire.id_service = service.id_service
        WHERE prestataire.id = %s
    """, (id,))
    prestataire = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        téléphone = request.form.get('téléphone')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        service_id = request.form.get('id_service')
        password = request.form.get('password')  # Mot de passe optionnel
        image_path = prestataire[10]  # Chemin actuel de l’image

        # Fichiers supplémentaires (Carte d'identité, Casier judiciaire, Papier de séjour)
        carte_identite_path = prestataire[11]  # Carte d'identité actuelle
        casier_judiciaire_path = prestataire[12]  # Casier judiciaire actuel
        papier_séjour_path = prestataire[13]  # Papier de séjour actuel

        # Vérifier si une nouvelle image est envoyée
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        # Vérifier les fichiers de documents supplémentaires
        if 'carte_identité' in request.files:
            file = request.files['carte_identité']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                carte_identite_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        if 'casier_judiciaire' in request.files:
            file = request.files['casier_judiciaire']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                casier_judiciaire_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        if 'papier_séjour' in request.files:
            file = request.files['papier_séjour']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                papier_séjour_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        # Hash du mot de passe uniquement si un nouveau est fourni
        if password:
            hashed_password = generate_password_hash(password)
        else:
            hashed_password = prestataire[14]  # Mot de passe actuel

        # Mise à jour des données en base
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE prestataire 
            SET nom = %s, prenom = %s, email = %s, image_path = %s, téléphone = %s,
                statut = %s, commune = %s, genre = %s, langue = %s, id_service = %s, 
                carte_identité = %s, casier_judiciaire = %s, papier_séjour = %s, 
                hashed_password = %s
            WHERE id = %s
        """, (
            nom, prenom, email, image_path, téléphone, statut, commune, genre, langue, service_id,
            carte_identite_path, casier_judiciaire_path, papier_séjour_path, hashed_password, id
        ))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    return render_template('update.html', prestataire=prestataire, services=services)

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
    cur.execute("SELECT COUNT(*) FROM service")
    total_catégorie = cur.fetchone()[0]


    cur.close()

    # Retourner un template où on affiche ces stats
    return render_template('statistics.html',
                           total_prestataire=total_prestataire,
                           active_prestataire=active_prestataire,
                           inactive_prestataire=inactive_prestataire,
                           total_catégorie=total_catégorie)

from datetime import datetime

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (name, email, message, date) VALUES (%s, %s, %s, %s)",
                (name, email, message, datetime.now()))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))





# Route : Tableau de bord admin
@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Identifiants incorrects, veuillez réessayer", 400


@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()

    # Récupérer les prestataires avec la catégorie de service
    cur.execute('''
        SELECT prestataire.id, prestataire.nom, prestataire.prenom, prestataire.téléphone,
               prestataire.email, prestataire.statut, prestataire.commune, prestataire.genre,
               prestataire.langue, service.catégorie, prestataire.image_path,
               prestataire.carte_identité, prestataire.casier_judiciaire, prestataire.papier_séjour
        FROM prestataire
        JOIN service ON prestataire.id_service = service.id_service
    ''')
    prestataire = cur.fetchall()

    cur.close()

    return render_template(
        'admin_dashboard.html',
        prestataire=prestataire
    )

@app.route('/messages')
def messages():
    if 'admin' not in session:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE messages SET lu = TRUE WHERE lu = FALSE")
    mysql.connection.commit()

    cur.execute("SELECT * FROM messages ")
    messages = cur.fetchall()
    cur.close()

    return render_template('messages.html', messages=messages)

# Route : Déconnexion de l'admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)  # Supprimer la session de l'admin
    return redirect(url_for('index'))

@app.route('/paiement', methods=['GET', 'POST'])
def paiement():
    conn = mysql.connection  # 🛠️ on va chercher la connexion
    cursor = conn.cursor()   # puis on ouvre le curseur

    # Après tu fais tes requêtes normalement...
    cursor.execute("SELECT * FROM prestataire WHERE statut = 'inactive'")
    prestataires = cursor.fetchall()

    if request.method == 'POST':
        téléphone = request.form['téléphone']

        # Récupérer l'ID du prestataire à partir du téléphone
        cursor.execute("SELECT ID FROM prestataire WHERE téléphone = %s", (téléphone,))
        result = cursor.fetchone()
        if not result:
            flash("Téléphone non reconnu", "danger")
            return redirect(url_for('paiement'))
        prestataire_id = result[0]

        montant = request.form['montant']
        date_paiement = datetime.now().strftime('%Y-%m-%d')
        date_expiration = (datetime.now().replace(month=datetime.now().month + 1)).strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO paiement (prestataire_id, montant, date_paiement, date_expiration) 
            VALUES (%s, %s, %s, %s)
        """, (prestataire_id, montant, date_paiement, date_expiration))

        cursor.execute("""
            UPDATE prestataire 
            SET statut = 'active'
            WHERE id = %s
        """, (prestataire_id,))

        conn.commit()
        return redirect(url_for('paiement'))

    cursor.execute("""
        SELECT paiement.id, prestataire.Nom, prestataire.Prenom, paiement.date_paiement, 
        paiement.montant, paiement.date_expiration, 
        CASE 
            WHEN paiement.date_expiration < NOW() THEN 'Expiré' 
            ELSE 'active' 
        END AS statut
        FROM paiement 
        JOIN prestataire ON paiement.prestataire_id = prestataire.ID
    """)
    paiements = cursor.fetchall()

    cursor.close()

    return render_template('paiement.html', prestataires=prestataires, paiements=paiements)

# routes.py ou dans ton app principale
@app.route("/dashboard_service")
def dashboard_service():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_service, catégorie FROM service")
    services = cur.fetchall()
    cur.close()
    return render_template("dashboard_service.html", services=services)

@app.route("/ajouter_service", methods=["POST"])
def ajouter_service():
    if request.method == "POST":
        categorie = request.form["categorie"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO service (catégorie) VALUES (%s)", (categorie,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("dashboard_service"))



if __name__ == "__main__":
    app.run(debug=True)