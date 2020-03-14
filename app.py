from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Init cors
CORS(app)

# Kuesioner Model
class Kuesioner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_gaya_belajar = db.Column(db.Integer)
    pertanyaan = db.Column(db.String(100))

    def __init__(self, id_gaya_belajar, pertanyaan):
        self.id_gaya_belajar = id_gaya_belajar
        self.pertanyaan = pertanyaan

# Kuesioner Schema
class KuesionerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_gaya_belajar', 'pertanyaan')

# Init Kuensioner Schema
kuesioner_schema = KuesionerSchema()
kuesioners_schema = KuesionerSchema(many=True)

# Get All Kuesioner
@app.route('/kuesioners', methods=['GET'])
def get_kuesioners():
    all_kuesioner = Kuesioner.query.all()
    result = kuesioners_schema.dump(all_kuesioner)

    return jsonify(result)

# Create a Kuesioner
@app.route('/kuesioner', methods=['POST'])
def add_kuesioner():
    id_gaya_belajar = request.json['id_gaya_belajar']
    pertanyaan = request.json['pertanyaan']
    new_kuesioner = Kuesioner(id_gaya_belajar, pertanyaan)
    db.session.add(new_kuesioner)
    db.session.commit()

    return kuesioner_schema.jsonify(new_kuesioner)

# Delete a Kuesioner
@app.route('/kuesioner/<id>', methods=['DELETE'])
def delete_kuesioner(id):
    kuesioner = Kuesioner.query.get(id)
    db.session.delete(kuesioner)
    db.session.commit()

    return kuesioner_schema.jsonify(kuesioner)

# Edit Kuesioner
@app.route('/kuesioner/<id>', methods=['PUT'])
def update_kuesioner(id):
    kuesioner = Kuesioner.query.get(id)

    kuesioner.id_gaya_belajar = request.json['id_gaya_belajar']
    kuesioner.pertanyaan = request.json['pertanyaan']

    db.session.commit()

    return kuesioner_schema.jsonify(kuesioner)

# Guru Model
class Guru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    mata_pelajaran = db.Column(db.String(100))

    def __init__(self, nama, email, password, mata_pelajaran):
        self.nama = nama
        self.email = email
        self.password = password
        self.mata_pelajaran = mata_pelajaran

# Guru Schema
class GuruSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama', 'email', 'password', 'mata_pelajaran')

# Init Guru Schema
guru_schema = GuruSchema()
gurus_schema = GuruSchema(many=True)

# Get All Guru
@app.route('/gurus', methods=['GET'])
def get_gurus():
    all_guru = Guru.query.all()
    result = gurus_schema.dump(all_guru)

    return jsonify(result)

# Auth Guru
@app.route('/auth/guru', methods=['POST'])
def auth_guru():
    email = request.json['email']
    password = request.json['password']

    guru = Guru.query.filter_by(email=email, password=password).first()

    return guru_schema.jsonify(guru)

# Create a Guru
@app.route('/guru', methods=['POST'])
def add_guru():
    nama = request.json['nama']
    email = request.json['email']
    password = request.json['password']
    mata_pelajaran = request.json['mata_pelajaran']

    new_guru = Guru(nama, email, password, mata_pelajaran)
    db.session.add(new_guru)
    db.session.commit()
    
    return guru_schema.jsonify(new_guru)

# Delete a Guru
@app.route('/guru/<id>', methods=['DELETE'])
def delete_guru(id):
    guru = Guru.query.get(id)
    db.session.delete(guru)
    db.session.commit()

    return guru_schema.jsonify(guru)

# Edit Guru
@app.route('/guru/<id>', methods=['PUT'])
def update_guru(id):
    guru = Guru.query.get(id)

    guru.nama = request.json['nama']
    guru.email = request.json['email']
    guru.password = request.json['password']
    guru.mata_pelajaran = request.json['mata_pelajaran']

    db.session.commit()

    return guru_schema.jsonify(guru)

# Kelas Model
class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_guru = db.Column(db.Integer)
    nama = db.Column(db.String(100))
    jumlah = db.Column(db.Integer)

    def __init__(self, id_guru, nama, jumlah):
        self.id_guru = id_guru
        self.nama = nama
        self.jumlah = id_guru

# Kelas Schema
class KelasSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_guru', 'nama', 'jumlah')

# Init Kelas Schema
kelas_schema = KelasSchema()
kelases_schema = KelasSchema(many=True)

# Get All Kelas
@app.route('/kelases', methods=['GET'])
def get_kelases():
    all_kelas = Kelas.query.all()
    result = kelas_schema.dump(all_kelas)

    return jsonify(result)

# Create a Kelas
# @app.route('/kelas', methods=['POST'])



# Run Server
if __name__ == '__main__':
    app.run(debug=True)
