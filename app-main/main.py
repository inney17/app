import os

from flask import Flask, request, jsonify, render_template, redirect, url_for
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route : Liste des items avec jointure sur la table des catégories
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM prestataire
         """)
    prestataire = cur.fetchall()
    cur.close()
    return render_template('index.html', prestataire=prestataire)

# Route : Créer un nouvel item
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
        emploi = request.form.get('emploi')
        file = request.files['image']

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO prestataire (nom, prenom, téléphone,image_path, email, statut, commune,genre,langue, emploi) 
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, emploi))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('inscription.html')
@app.route('/prestataire/<int:id>')
def prestataire_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire WHERE ID_prestataire = %s", (id,))
    prestataire = cur.fetchone()
    cur.close()

    print("Prestataire récupéré :", prestataire)  # Debug: Vérifie les données récupérées

    return render_template('prestataire_detail.html', prestataire=prestataire)


app.run(debug=True)