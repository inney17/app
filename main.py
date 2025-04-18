import os

from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)
    lu = db.Column(db.Boolean, default=False)  # Pour savoir si le message a été lu

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
@app.route('/')
def index():
    if 'admin' not in session:
        return redirect(url_for('login'))  # ou une autre route pour l'admin


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

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Récupérer les données du formulaire d'inscription
        nom = request.form.get('nom')

        prenom = request.form.get('prenom')
        email = request.form.get('email')
        téléphone = request.form.get('téléphone')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        service_id = request.form.get('id_service')
        password = request.form.get('password')
        if not password:
            # Retourner une erreur si le mot de passe est vide
            return render_template('inscription.html', error="Le mot de passe ne peut pas être vide")

            # Vérification de la complexité du mot de passe (si tu le souhaites)
        if len(password) < 6:
            return render_template('inscription.html', error="Le mot de passe doit contenir au moins 6 caractères")

        file = request.files['image']

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        # Insertion dans la base de données
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO prestataire (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, id_service, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, service_id, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))  # Rediriger après l'inscription

    # Récupérer toutes les catégories de service
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
    # Connexion à la base de données pour récupérer les informations de l'utilisateur
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire,service  WHERE id = %s", (id,))
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
        password = request.form.get('password')
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
                         commune = %s, genre = %s, langue = %s, catégorie = %s, password = %s, image_path = %s

                     WHERE id = %s
                 """, (nom, prenom, email, téléphone, statut, commune, genre, langue, catégorie, password, image_path, id))

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
               prestataire.langue, service.catégorie, prestataire.image_path
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
    return redirect(url_for('admin_logout'))

@app.route('/paiement', methods=['GET', 'POST'])
def paiement():
    conn = mysql.connection  # 🛠️ on va chercher la connexion
    cursor = conn.cursor()   # puis on ouvre le curseur

    # Après tu fais tes requêtes normalement...
    cursor.execute("SELECT * FROM prestataire WHERE statut = 'inactive'")
    prestataires = cursor.fetchall()

    if request.method == 'POST':
        prestataire_id = request.form['prestataire_id']
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



if __name__ == "__main__":
    app.run(debug=True)