import gzip
import shutil
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from decoder import (encoded_text_to_binary, get_data_of_nfe,
                     get_encoded_nfe_gzip)

NAME_FILE_GZ = "arqxml.tar.gz"
NAME_FILE_XML = "arqxml.xml"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.secret_key = '1234'
db = SQLAlchemy(app)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, nullable=False)
    porta = db.Column(db.Integer, nullable=False)
    database = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Config(id={self.id},ip={self.ip},database={self.database})"


@app.route("/", methods=["GET"])
def init():
    # if not os.path.exists("config.db"):
    #     flash("Arquivo de configuração não localizado")
    #     db.create_all()
    #     return redirect(url_for("config"))
    if not Config.query.filter_by(id=1).first():
        flash("Não foram localizados nenhum registro de configuração")
        return redirect(url_for("config"))
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500


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
    data = Config.query.filter_by(id=1).first()

    if request.method == 'POST':
        new_config = data or Config()
        new_config.id = 1
        new_config.ip = request.form["ip"]
        new_config.porta = request.form["porta"]
        new_config.database = request.form["database"]
        new_config.user = request.form["user"]
        new_config.password = request.form["password"]

        db.session.add(new_config)
        db.session.commit()

        flash("Configuração salva no banco de dados!")
        return redirect("/config/")

    return render_template("config.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
