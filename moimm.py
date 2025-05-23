import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash



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

@app.route("/")
def index():
    from MySQLdb.cursors import DictCursor

    cur = mysql.connection.cursor(DictCursor)

    # 1) Récupération des filtres
    commune_filter   = request.args.get("commune")
    langue_filter    = request.args.get("langue")
    categorie_filter = request.args.get("categorie")
    prix_filter      = request.args.get("prix")    # ← nouveau

    # 2) Construction de la requête dynamique
    query = """
        SELECT
            p.id,
            p.nom,
            p.prenom,
            p.téléphone,
            p.image_path,
            p.email,
            p.statut,
            p.commune,
            p.genre,
            p.langue,
            p.prix,
            s.catégorie AS categorie
        FROM prestataire p
        LEFT JOIN service s ON p.service_id = s.id
        WHERE 1=1
    """
    params = []

    if commune_filter:
        query += " AND p.commune = %s"
        params.append(commune_filter)

    if langue_filter:
        query += " AND p.langue = %s"
        params.append(langue_filter)

    if categorie_filter:
        query += " AND s.catégorie = %s"
        params.append(categorie_filter)

    if prix_filter:
        # Intervalle "min-max" ou "100+"
        if prix_filter.endswith("+"):
            min_price = prix_filter.rstrip("+")
            query += " AND p.prix >= %s"
            params.append(min_price)
        else:
            min_price, max_price = prix_filter.split("-")
            query += " AND p.prix BETWEEN %s AND %s"
            params.extend([min_price, max_price])

    # Exécution
    cur.execute(query, tuple(params))
    prestataires = cur.fetchall()

    # 3) Valeurs pour les filtres
    cur.execute("SELECT DISTINCT commune FROM prestataire")
    communes = [r['commune'] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT langue FROM prestataire")
    langues = [r['langue'] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT catégorie FROM service")
    categories = [r['catégorie'] for r in cur.fetchall()]

    cur.close()

    # 4) Passage au template
    return render_template(
        "index.html",
        prestataires       = prestataires,
        communes           = communes,
        langues            = langues,
        categories         = categories,
        selected_commune   = commune_filter,
        selected_langue    = langue_filter,
        selected_categorie = categorie_filter,
        selected_prix      = prix_filter    # ← nouveau
    )


# Route : Connexion admin


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, catégorie FROM service")
    services = cur.fetchall()

    if request.method == 'POST':
        nom = request.form.get('Nom')
        prenom = request.form.get('prenom')
        téléphone = request.form.get('téléphone')
        email = request.form.get('email')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        prix = request.form.get('prix')
        password = generate_password_hash(request.form.get('password'))
        service_id = request.form.get('service_id')

        file = request.files['image']
        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"{UPLOAD_FOLDER}/{filename}"

        cur.execute("""
            INSERT INTO prestataire (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, prix , password, service_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, téléphone, image_path, email, statut, commune, genre, langue, prix , password, service_id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    cur.close()
    return render_template('inscription.html', services=services)

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

    # Récupérer des statistiques de base
    cur.execute("SELECT COUNT(*) FROM prestataire")
    total_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'active'")
    active_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestataire WHERE statut = 'inactive'")
    inactive_prestataire = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT catégorie) FROM prestataire")
    total_catégorie = cur.fetchone()[0]

    # Récupérer le total des paiements des prestataires actifs
    cur.execute("""
        SELECT SUM(montant) FROM paiement
        JOIN prestataire ON paiement.prestataire_id = prestataire.id
        WHERE prestataire.statut = 'active'
    """)
    total_paiement_actif = cur.fetchone()[0] or 0

    # Récupérer les données pour la courbe des paiements (30 derniers jours)
    cur.execute("""
        SELECT 
            DATE(date_paiement) AS date,
            SUM(montant) AS total
        FROM paiement
        WHERE date_paiement >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY date
        ORDER BY date
    """)
    paiements_data = cur.fetchall()

    cur.close()

    return render_template('statistics.html',
                         total_prestataire=total_prestataire,
                         active_prestataire=active_prestataire,
                         inactive_prestataire=inactive_prestataire,
                         total_catégorie=total_catégorie,
                         total_paiement_actif=total_paiement_actif
                        )

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
from werkzeug.security import check_password_hash


@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    # Admin login
    if username == 'admin' and password == 'admin123':
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))

    # Vérification prestataire
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM prestataire WHERE email = %s", (username,))
    result = cur.fetchone()
    cur.close()

    if result and check_password_hash(result[1], password):
        session['pending_prestataire_id'] = result[0]  # Pour désactivation
        session['show_disable_modal'] = True  # Pour afficher la modale dans index.html
        return redirect(url_for('index'))

    return "Identifiants incorrects", 400


@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()

    # Récupérer les prestataires
    cur.execute("SELECT * FROM prestataire")
    prestataire = cur.fetchall()
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
    conn = mysql.connection
    cursor = conn.cursor()

    # 🔁 Mise à jour automatique des statuts expirés
    cursor.execute("""
        UPDATE prestataire
        SET statut = 'inactive'
        WHERE id IN (
            SELECT p.prestataire_id
            FROM paiement p
            WHERE p.date_expiration < NOW()
        )
    """)
    conn.commit()

    # 🔎 Prestataires à payer
    cursor.execute("SELECT * FROM prestataire WHERE statut = 'inactive'")
    prestataires = cursor.fetchall()

    # 💳 Paiement reçu
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

    # 🧾 Historique des paiements
    cursor.execute("""
        SELECT paiement.id, prestataire.Nom, prestataire.Prenom, paiement.date_paiement,
               paiement.montant, paiement.date_expiration,
               CASE 
                   WHEN paiement.date_expiration < NOW() THEN 'inactive' 
                   ELSE 'active'
               END AS statut
        FROM paiement
        JOIN prestataire ON paiement.prestataire_id = prestataire.ID
    """)
    paiements = cursor.fetchall()

    cursor.close()
    return render_template('paiement.html', prestataires=prestataires, paiements=paiements)

@app.route('/disable_account', methods=['POST'])
def disable_account():
    prestataire_id = session.get('pending_prestataire_id')

    if prestataire_id:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE prestataire SET statut = 'inactive' WHERE id = %s", (prestataire_id,))
        mysql.connection.commit()
        cur.close()
        session.pop('pending_prestataire_id', None)
        return redirect(url_for('index'))
    else:
        return "Session expirée", 400

@app.route('/cancel_disable_modal', methods=['POST'])
def cancel_disable_modal():
    session.pop('show_disable_modal', None)
    session.pop('pending_prestataire_id', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)