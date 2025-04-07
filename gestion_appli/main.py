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
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire")  # Récupérer tous les prestataires
    prestataire = cur.fetchall()  # Cela retourne toutes les lignes
    cur.close()

    return render_template('index.html', prestataire=prestataire)


@app.route("/index2/<int:id>")
def index2(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire WHERE id = %s", (id,))  # Recherche par ID
    prestataire = cur.fetchone()  # Cela retourne une seule ligne correspondant à l'ID
    cur.close()

    if prestataire:
        return render_template('index2.html', prestataire=prestataire)  # Passer les données à la page index2.html
    else:
        return "Prestataire non trouvé", 404  # Si aucun prestataire n'est trouvé


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
        catégorie = request.form.get('catégorie')
        password = request.form.get('password')
        file = request.files['image']

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO prestataire (nom, prenom, téléphone,image_path, email, statut, commune,genre,langue, catégorie,password) 
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone,image_path , email, statut, commune, genre, langue, catégorie,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('inscription.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connexion à la base de données pour vérifier l'email et le mot de passe
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM prestataire WHERE email = %s AND password = %s", (email, password))
        prestataire = cur.fetchone()  # Si un prestataire avec cet email et mot de passe existe
        cur.close()

        if prestataire:  # Si un utilisateur est trouvé
            return redirect(url_for('update', id=prestataire[0]))  # Redirige vers la page de mise à jour
        else:
            return "Identifiants incorrects, veuillez réessayer", 400  # Si les identifiants sont incorrects

    return render_template('login.html')  # Affiche le formulaire de connexion


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
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Vérifier si le fichier a une extension valide
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        # Connexion à la base de données pour mettre à jour les informations
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE prestataire 
                    SET nom = %s, prenom = %s, email = %s, téléphone = %s, statut = %s, 
                        commune = %s, genre = %s, langue = %s, catégorie = %s, image_path = %s

                    WHERE id = %s
                """, (nom, prenom, email, téléphone, statut, commune, genre, langue, catégorie,image_path, id))

        mysql.connection.commit()
        cur.close()
        # Rediriger l'utilisateur vers la page d'accueil ou vers un message de succès
        return redirect(url_for('index'))  # Vous pouvez rediriger vers la page de votre choix

        # Si la méthode est GET, on affiche le formulaire avec les informations actuelles de l'utilisateur
    return render_template('update.html', prestataire=prestataire)


app.run(debug=True)