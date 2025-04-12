import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'
app.secret_key = 'supersecretkey'

mysql = MySQL(app)

# Configuration pour le téléchargement des fichiers
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour vérifier si le fichier a une extension autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route : Page d'accueil
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire")
    prestataire = cur.fetchall()
    cur.close()
    return render_template('index.html', prestataire=prestataire)

# Route : Connexion admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin@' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Identifiants incorrects, veuillez réessayer.', 'danger')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

# Route : Tableau de bord admin
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire")
    prestataire = cur.fetchall()
    cur.close()

    return render_template('admin_dashboard.html', prestataire=prestataire)

# Route : Déconnexion de l'admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# Route : Inscription d'un prestataire
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('Nom')
        prenom = request.form.get('prenom')
        téléphone = request.form.get('téléphone')
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
            INSERT INTO prestataire (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, catégorie, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, catégorie, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('inscription.html')

# Route : Supprimer un prestataire
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM prestataire WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin_dashboard'))

# Route : Modifier un prestataire
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestataire WHERE id = %s", (id,))
    prestataire = cur.fetchone()
    cur.close()

    if request.method == 'POST':
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

        image_path = prestataire[4]  # Colonne 4 pour image_path

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE prestataire 
            SET nom = %s, prenom = %s, email = %s, téléphone = %s, statut = %s, 
                commune = %s, genre = %s, langue = %s, catégorie = %s, image_path = %s
            WHERE id = %s
        """, (nom, prenom, email, téléphone, statut, commune, genre, langue, catégorie, image_path, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin_dashboard'))

    return render_template('update.html', prestataire=prestataire)

# Route : Statistiques
@app.route('/statistics')
def statistics():
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM prestataire")
    total_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'active'")
    active_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'inactive'")
    inactive_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT catégorie) FROM prestataire")
    total_catégorie = cur.fetchone()[0]

    cur.close()

    return render_template('statistics.html',
                           total_prestataire=total_prestataire,
                           active_prestataire=active_prestataire,
                           inactive_prestataire=inactive_prestataire,
                           total_catégorie=total_catégorie)



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
        date_expiration = (datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d')

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
