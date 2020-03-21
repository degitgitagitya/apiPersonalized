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

# Get Single Guru
@app.route('/guru/<id>', methods=['GET'])
def get_guru_by_id(id):
    guru = Guru.query.get(id)

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

    def __init__(self, id_guru, nama):
        self.id_guru = id_guru
        self.nama = nama

# Kelas Schema
class KelasSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_guru', 'nama')

# Init Kelas Schema
kelas_schema = KelasSchema()
kelases_schema = KelasSchema(many=True)

# Get All Kelas
@app.route('/kelases', methods=['GET'])
def get_kelases():
    all_kelas = Kelas.query.all()
    result = kelases_schema.dump(all_kelas)

    return jsonify(result)

# Get All Kelas by_id_guru
@app.route('/kelases/<id_guru>', methods=['GET'])
def get_kelases_by_guru(id_guru):
    all_kelas = Kelas.query.filter_by(id_guru=id_guru)
    result = kelases_schema.dump(all_kelas)

    return jsonify(result)

# Create a Kelas
@app.route('/kelas', methods=['POST'])
def add_kelas():
    id_guru = request.json['id_guru']
    nama = request.json['nama']

    new_kelas = Kelas(id_guru, nama)
    db.session.add(new_kelas)
    db.session.commit()

    return kelas_schema.jsonify(new_kelas)

# Delete a Kelas
@app.route('/kelas/<id>', methods=['DELETE'])
def delete_kelas(id):
    kelas = Kelas.query.get(id)
    db.session.delete(kelas)
    db.session.commit()

    return kelas_schema.jsonify(kelas)

# Edit Kelas
@app.route('/kelas/<id>', methods=['PUT'])
def update_kelas(id):
    kelas = Kelas.query.get(id)

    kelas.id_guru = request.json['id_guru']
    kelas.nama = request.json['nama']

    db.session.commit()

    return kelas_schema.jsonify(kelas)

# Siswa Model
class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_kelas = db.Column(db.String(100))
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    id_gaya_belajar = db.Column(db.Integer)
    password = db.Column(db.String(100))

    def __init__(self, id_kelas, nama, email, id_gaya_belajar, password):
        self.id_kelas = id_kelas
        self.nama = nama
        self.email = email
        self.id_gaya_belajar = id_gaya_belajar
        self.password = password

# Siswa Schema
class SiswaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_kelas', 'nama', 'email', 'id_gaya_belajar', 'password')

# Init Siswa Schema
siswa_schema = SiswaSchema()
siswas_schema = SiswaSchema(many=True)

# Get All Siswa
@app.route('/siswas', methods=['GET'])
def get_siswas():
    all_siswa = Siswa.query.all()
    result = siswas_schema.dump(all_siswa)

    return jsonify(result)

# Auth Siswa
@app.route('/auth/siswa', methods=['POST'])
def auth_siswa():
    email = request.json['email']
    password = request.json['password']

    siswa = Siswa.query.filter_by(email=email, password=password).first()

    return siswa_schema.jsonify(siswa)

# Get All Siswa by id_kelas
@app.route('/siswas/<id_kelas>', methods=['GET'])
def get_siswa_by_kelas(id_kelas):
    all_siswa = Siswa.query.filter_by(id_kelas=id_kelas)
    result = siswas_schema.dump(all_siswa)

    return jsonify(result)

# Create a Siswa
@app.route('/siswa', methods=['POST'])
def add_siswa():
    id_kelas = request.json['id_kelas']
    nama = request.json['nama']
    email = request.json['email']
    id_gaya_belajar = request.json['id_gaya_belajar']
    password = request.json['password']

    new_siswa = Siswa(id_kelas, nama, email, id_gaya_belajar, password)
    db.session.add(new_siswa)
    db.session.commit()

    return siswa_schema.jsonify(new_siswa)

# Delete a Siswa
@app.route('/siswa/<id>', methods=['DELETE'])
def delete_siswa(id):
    siswa = Siswa.query.get(id)
    db.session.delete(siswa)
    db.session.commit()

    return siswa_schema.jsonify(siswa)

# Edit Siswa
@app.route('/siswa/<id>', methods=['PUT'])
def update_siswa(id):
    siswa = Siswa.query.get(id)

    siswa.id_kelas = request.json['id_kelas']
    siswa.nama = request.json['nama']
    siswa.email = request.json['email']
    siswa.id_gaya_belajar = request.json['id_gaya_belajar']
    siswa.password = request.json['password']

    db.session.commit()

    return siswa_schema.jsonify(siswa)


# Materi Model
class Materi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100))
    keterangan = db.Column(db.String(100))
    indikator = db.Column(db.String(100))
    tujuan_belajar = db.Column(db.String(100))

    def __init__(self, judul, keterangan, indikator, tujuan_belajar):
        self.judul = judul
        self.keterangan = keterangan
        self.indikator = indikator
        self.tujuan_belajar = tujuan_belajar

# Materi Schema
class MateriSchema(ma.Schema):
    class Meta:
        fields = ('id', 'judul', 'keterangan', 'indikator', 'tujuan_belajar')

# Init Materi Schema
materi_schema = MateriSchema()
materis_schema = MateriSchema(many=True)

# Get All Materi
@app.route('/materi', methods=['GET'])
def get_all_materi():
    all_materi = Materi.query.all()
    result = materis_schema.dump(all_materi)

    return jsonify(result)

# Create a Materi
@app.route('/materi', methods=['POST'])
def add_materi():
    judul = request.json['judul']
    keterangan = request.json['keterangan']
    indikator = request.json['indikator']
    tujuan_belajar = request.json['tujuan_belajar']

    new_materi = Materi(judul, keterangan, indikator, tujuan_belajar)
    db.session.add(new_materi)
    db.session.commit()

    return materi_schema.jsonify(new_materi)

# Delete a Materi
@app.route('/materi/<id>', methods=['DELETE'])
def delete_materi(id):
    materi = Materi.query.get(id)
    db.session.delete(materi)
    db.session.commit()

    return materi_schema.jsonify(materi)

# Edit Materi
@app.route('/materi/<id>', methods=['PUT'])
def update_materi(id):
    materi = Materi.query.get(id)

    materi.judul = request.json['judul']
    materi.keterangan = request.json['keterangan']
    materi.indikator = request.json['indikator']
    materi.tujuan_belajar = request.json['tujuan_belajar']

    db.session.commit()

    return materi_schema.jsonify(materi)


# Sub Materi Model
class SubMateri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_gaya_belajar = db.Column(db.Integer)
    id_materi = db.Column(db.Integer)
    nama = db.Column(db.String(100))
    keterangan = db.Column(db.String(100))
    url = db.Column(db.String(100))

    def __init__(self, id_gaya_belajar, id_materi, nama, keterangan, url):
        self.id_gaya_belajar = id_gaya_belajar
        self.id_materi = id_materi
        self.nama = nama
        self.keterangan = keterangan
        self.url = url


# Sub Materi Schema
class SubMateriSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_gaya_belajar', 'id_materi', 'nama', 'keterangan', 'url')

sub_materi_schema = SubMateriSchema()
sub_materies_schema = SubMateriSchema(many=True)

# Get All Sub Materi
@app.route('/submateri', methods=['GET'])
def get_all_sub_materi():
    all_sub_materi = SubMateri.query.all()
    result = sub_materies_schema.dump(all_sub_materi)

    return jsonify(result)

# Get All Sub Materi by id_materi
@app.route('/submateri/<id_materi>', methods=['GET'])
def get_sub_materi_id_materi(id_materi):
    all_sub_materi = SubMateri.query.filter_by(id_materi=id_materi)
    result = sub_materies_schema.dump(all_sub_materi)

    return jsonify(result)

# Get All Sub Materi by id_materi & id_gaya_belajar
@app.route('/submateri/<id_materi>/<id_gaya_belajar>', methods=['GET'])
def get_sub_materi_id_materi_gaya(id_materi, id_gaya_belajar):
    all_sub_materi = SubMateri.query.filter_by(id_materi=id_materi, id_gaya_belajar=id_gaya_belajar)
    result = sub_materies_schema.dump(all_sub_materi)

    return jsonify(result)

# Create a Sub Materi
@app.route('/submateri', methods=['POST'])
def add_sub_materi():
    id_gaya_belajar = request.json['id_gaya_belajar'] 
    id_materi = request.json['id_materi'] 
    nama = request.json['nama'] 
    keterangan = request.json['keterangan'] 
    url = request.json['url'] 

    new_sub_materi = SubMateri(id_gaya_belajar, id_materi, nama, keterangan, url)
    db.session.add(new_sub_materi)
    db.session.commit()

    return sub_materi_schema.jsonify(new_sub_materi)

# Delete a Materi
@app.route('/submateri/<id>', methods=['DELETE'])
def delete_sub_materi(id):
    sub_materi = SubMateri.query.get(id)
    db.session.delete(sub_materi)
    db.session.commit()

    return sub_materi_schema.jsonify(sub_materi)

# Edit Materi
@app.route('/submateri/<id>', methods=['PUT'])
def edit_sub_materi(id):
    sub_materi = SubMateri.query.get(id)

    sub_materi.id_gaya_belajar = request.json['id_gaya_belajar']
    sub_materi.id_materi = request.json['id_materi']
    sub_materi.nama = request.json['nama']
    sub_materi.keterangan = request.json['keterangan']
    sub_materi.url = request.json['url']

    db.session.commit()

    return materi_schema.jsonify(sub_materi)



# Run Server
if __name__ == '__main__':
    app.run(debug=True)
