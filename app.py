import gzip
import shutil
import os

from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from decoder import (encoded_text_to_binary, get_data_of_nfe,
                     get_encoded_nfe_gzip)

NAME_FILE_GZ = "arqxml.tar.gz"
NAME_FILE_XML = "arqxml.xml"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'
app.secret_key = '1234'
db = SQLAlchemy(app)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, nullable=False)
    # porta = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Config(id={self.id},ip={self.ip})"


if not os.path.exists("config.db"):
    db.create_all()


@app.route("/")
def init():
    return render_template('index.html')


@app.route("/nfe/", methods=['POST', 'GET'])
def nfe():
    if request.method == 'POST':
        enc_nfe_zip = get_encoded_nfe_gzip(
            request.form['idnfe'], Config.query.filter_by(id=1).first())

        if not enc_nfe_zip:
            flash("NF-e correspondente à chave de acesso não localizado!")
            return redirect("/")

        encoded_text_to_binary(enc_nfe_zip[0], NAME_FILE_GZ)
        with gzip.open(NAME_FILE_GZ, 'r') as f_in, open(NAME_FILE_XML, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        nfe = get_data_of_nfe(NAME_FILE_XML)
        return render_template('guia_cega.html', produtos=nfe.produtos,
                               fornecedor=nfe.fornecedor, dados_nfe=nfe.dados_nfe)


@app.route("/config/", methods=["POST", "GET"])
def config():
    if request.method == 'POST':
        new_config = Config.query.filter_by(id=1).first()
        new_config.ip = request.form["ip"]

        db.session.add(new_config)
        db.session.commit()

        flash("Configuração salva no banco de dados!")
        return redirect("/config/")

    data = Config.query.filter_by(id=1).first()
    return render_template("config.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
