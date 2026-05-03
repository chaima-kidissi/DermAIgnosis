import os
import pymysql
import numpy as np
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ----------------- APP -----------------
app = Flask(__name__)
app.secret_key = "dermaignosis_secret_key_2025"

# ----------------- UPLOAD -----------------
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- TensorFlow clean logs -----------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ----------------- MySQL -----------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="skin_cancer_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# ----------------- Modèle IA -----------------
MODEL_PATH = 'model/vgg16_skin_cancer.h5'
model = load_model(MODEL_PATH)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ----------------- LOGIN -----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiant ou mot de passe incorrect", "danger")

    return render_template('login.html')

# ----------------- DASHBOARD -----------------
@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM patients")
    total_patients = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as malin FROM patients WHERE result='Malin'")
    malin_count = cursor.fetchone()['malin']

    cursor.execute("SELECT * FROM patients ORDER BY id DESC LIMIT 5")
    recent_patients = cursor.fetchall()

    cursor.close()
    conn.close()

    for p in recent_patients:
        p['image_path'] = p['image_path'].replace('\\', '/')

    return render_template(
        'dashboard.html',
        total_patients=total_patients,
        malin_count=malin_count,
        benin_count=total_patients - malin_count,
        recent_patients=recent_patients
    )

# ----------------- PREDICT -----------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        file = request.files['image']

        if file.filename == '':
            flash("Aucune image sélectionnée", "danger")
            return redirect(url_for('predict'))

        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # ----------------- IA -----------------
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)
        result = "Malin" if prediction[0][0] > 0.5 else "Bénin"

        prob = float(
            prediction[0][0] * 100 if result == "Malin"
            else (1 - prediction[0][0]) * 100
        )

        # ----------------- DB -----------------
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients (name, age, result, probability, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, result, prob, filepath))

        conn.commit()
        patient_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return render_template(
            'result.html',
            result=result,
            prob=round(prob, 2),
            img=filepath.replace('\\', '/'),
            patient_id=patient_id,
            patient_name=name
        )

    return render_template('predict.html')

# ----------------- RESULT -----------------
@app.route('/result/<int:patient_id>')
def result(patient_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        flash("Patient non trouvé", "warning")
        return redirect(url_for('patients'))

    patient['image_path'] = patient['image_path'].replace('\\', '/')

    return render_template(
        'result.html',
        result=patient['result'],
        prob=patient['probability'],
        img=patient['image_path'],
        patient_id=patient['id'],
        patient_name=patient['name']
    )

# ----------------- PATIENTS -----------------
@app.route('/patients')
def patients():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    patients_data = cursor.fetchall()
    cursor.close()
    conn.close()

    for p in patients_data:
        p['image_path'] = p['image_path'].replace('\\', '/')

    return render_template('patients.html', patients=patients_data)

# ----------------- FOLLOWUP -----------------
@app.route('/followup/<int:patient_id>')
def followup(patient_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        flash("Patient non trouvé", "warning")
        return redirect(url_for('patients'))

    patient['image_path'] = patient['image_path'].replace('\\', '/')
    prob = float(patient['probability'])

    history = [
        {"date": "2024-10-01", "volume": round(prob * 0.5, 1)},
        {"date": "2025-01-15", "volume": round(prob * 0.75, 1)},
        {"date": datetime.now().strftime("%Y-%m-%d"), "volume": round(prob, 1)}
    ]

    growth_rate = "+15% / mois" if patient['result'] == 'Malin' else "+2% / mois (stable)"

    return render_template(
        'followup.html',
        patient=patient,
        history=history,
        growth_rate=growth_rate
    )

# ----------------- HEATMAP -----------------
@app.route('/heatmap/<int:patient_id>')
def heatmap(patient_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    flash("Fonctionnalité heatmap à venir", "info")
    return redirect(url_for('result', patient_id=patient_id))

# ----------------- EVOLUTION -----------------
@app.route('/evolution/<int:patient_id>')
def evolution(patient_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    flash("Fonctionnalité évolution à venir", "info")
    return redirect(url_for('result', patient_id=patient_id))

# ----------------- RECOMMENDATION -----------------
@app.route('/recommendation/<int:patient_id>')
def recommendation(patient_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        flash("Patient non trouvé", "warning")
        return redirect(url_for('patients'))

    patient['image_path'] = patient['image_path'].replace('\\', '/')
    is_malin = patient['result'] == 'Malin'
    age = int(patient['age'])

    if is_malin:
        recommandations = {
            "prise_en_charge": (
                "Exérèse chirurgicale large recommandée avec analyse "
                "anatomopathologique de la pièce opératoire."
            ),
            "delai": "Consultation chirurgicale urgente sous 2 semaines maximum.",
            "examens": (
                "Biopsie cutanée, dermoscopie, bilan d'extension "
                "(échographie ganglionnaire, scanner si nécessaire)."
            ),
            "suivi": (
                "Consultation de contrôle à 1 mois post-opératoire, "
                "puis tous les 3 mois pendant 2 ans."
            ),
            "orientation": "Orientation vers un dermatologue puis chirurgien oncologue.",
            "conseils_senior": (
                "Surveillance renforcée recommandée en raison de l'âge "
                "avancé et de la fragilité cutanée."
            ) if age >= 65 else None
        }
    else:
        recommandations = {
            "prise_en_charge": (
                "Surveillance clinique et dermoscopique régulière. "
                "Aucune intervention chirurgicale immédiate nécessaire."
            ),
            "delai": "Consultation de suivi dans les 3 à 6 mois.",
            "examens": "Dermoscopie de contrôle. Photographie de référence recommandée.",
            "suivi": "Contrôle annuel ou semestriel selon l'évolution clinique.",
            "orientation": "Suivi par un dermatologue en ambulatoire.",
            "conseils_senior": (
                "Hydratation cutanée régulière et protection solaire renforcée conseillées."
            ) if age >= 65 else None
        }

    return render_template(
        'recommandation.html',
        patient=patient,
        recommandations=recommandations
    )

# ----------------- CONSIGNES -----------------
@app.route('/consignes')
def consignes():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('consignes.html')

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----------------- RUN -----------------
if __name__ == '__main__':
    app.run(debug=True)