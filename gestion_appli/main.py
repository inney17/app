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

from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, catégorie FROM service")
    services = cur.fetchall()

    if request.method == 'POST':
        # Récupérer les données du formulaire
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

        # Fichiers
        def save_file(file_obj):
            if file_obj and allowed_file(file_obj.filename):
                filename = secure_filename(file_obj.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_obj.save(file_path)
                return f"{UPLOAD_FOLDER}/{filename}"
            return None

        image_path = save_file(request.files.get('image'))
        carte_identite = save_file(request.files.get('carte_identite'))
        casier_judiciaire = save_file(request.files.get('casier_judiciaire'))
        papier_sejour = save_file(request.files.get('papier_sejour'))

        # Insertion dans la base
        cur.execute("""
            INSERT INTO prestataire (
                Nom, prenom, téléphone, email, statut, commune, genre, langue, prix, password, 
                service_id, image_path, carte_identite, casier_judiciaire, papier_sejour
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nom, prenom, téléphone, email, statut, commune, genre, langue, prix, password,
            service_id, image_path, carte_identite, casier_judiciaire, papier_sejour
        ))

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

    # ✅ Requête pour récupérer les prestataires
    cur.execute("""
        SELECT 
            p.id,            -- 0
            p.nom,           -- 1
            p.prenom,        -- 2
            p.téléphone,     -- 3
            p.email,         -- 4
            p.statut,        -- 5
            p.commune,       -- 6
            p.genre,         -- 7
            p.langue,        -- 8
            p.service_id,    -- 9
            p.image_path,    -- 10
            p.password,      -- 11
            p.prix,          -- 12 ← MANQUAIT !
            p.carte_identite,-- 13
            p.casier_judiciaire, -- 14
            p.papier_sejour,     -- 15
            s.catégorie       -- 
        FROM prestataire p
        JOIN service s ON p.service_id = s.id
    """)

    # ✅ Il te manquait cette ligne :
    prestataires = cur.fetchall()
    cur.close()

    # ✅ Et ici on passe bien la variable récupérée :
    return render_template('admin_dashboard.html', prestataires=prestataires)



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


from MySQLdb.cursors import DictCursor


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor(DictCursor)  # Utilisation de DictCursor

    # Récupérer les informations du prestataire à mettre à jour
    cur.execute("SELECT * FROM prestataire WHERE id = %s", (id,))
    prestataire = cur.fetchone()

    if not prestataire:
        return "Prestataire non trouvé", 404

    # Récupérer les services disponibles pour le formulaire
    cur.execute("SELECT id, catégorie FROM service")
    services = cur.fetchall()

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('Nom')
        prenom = request.form.get('prenom')
        téléphone = request.form.get('téléphone')
        email = request.form.get('email')
        statut = request.form.get('statut')
        commune = request.form.get('commune')
        genre = request.form.get('genre')
        langue = request.form.get('langue')
        prix = request.form.get('prix')
        service_id = request.form.get('service_id')

        # Gérer le fichier image
        def save_file(file_obj):
            if file_obj and allowed_file(file_obj.filename):
                filename = secure_filename(file_obj.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_obj.save(file_path)
                return f"{UPLOAD_FOLDER}/{filename}"
            return None

        image_path = save_file(request.files.get('image')) or prestataire['image_path']
        carte_identite = save_file(request.files.get('carte_identite')) or prestataire['carte_identite']
        casier_judiciaire = save_file(request.files.get('casier_judiciaire')) or prestataire['casier_judiciaire']
        papier_sejour = save_file(request.files.get('papier_sejour')) or prestataire['papier_sejour']

        # Mettre à jour les informations dans la base de données
        cur.execute("""
            UPDATE prestataire
            SET Nom = %s, prenom = %s, téléphone = %s, email = %s, statut = %s, commune = %s, 
                genre = %s, langue = %s, prix = %s, service_id = %s, image_path = %s, 
                carte_identite = %s, casier_judiciaire = %s, papier_sejour = %s
            WHERE id = %s
        """, (
            nom, prenom, téléphone, email, statut, commune, genre, langue, prix, service_id,
            image_path, carte_identite, casier_judiciaire, papier_sejour, id
        ))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))  # Rediriger vers la page d'accueil après la mise à jour

    cur.close()

    # Retourner le formulaire de mise à jour avec les données actuelles
    return render_template('update.html', prestataire=prestataire, services=services)


# routes.py ou dans ton app principale
@app.route("/dashboard_service")
def dashboard_service():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, catégorie FROM service")
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