import gzip
import shutil

from flask import Flask, flash, redirect, render_template, request

from decoder import (encoded_text_to_binary, get_data_of_nfe,
                     get_encoded_nfe_gzip)

NAME_FILE_GZ = "arqxml.tar.gz"
NAME_FILE_XML = "arqxml.xml"
app = Flask(__name__)
app.secret_key = '1234'


@app.route("/")
def init():
    return render_template('index.html')


@app.route("/nfe/", methods=['POST', 'GET'])
def nfe():
    if request.method == 'POST':
        enc_nfe_zip = get_encoded_nfe_gzip(request.form['idnfe'])

        if not enc_nfe_zip:
            flash("NF-e correspondente à chave de acesso não localizado!")
            return redirect("/")

        encoded_text_to_binary(enc_nfe_zip[0], NAME_FILE_GZ)
        with gzip.open(NAME_FILE_GZ, 'r') as f_in, open(NAME_FILE_XML, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        nfe = get_data_of_nfe(NAME_FILE_XML)
        return render_template('guia_cega.html', produtos=nfe.produtos,
                               fornecedor=nfe.fornecedor, dados_nfe=nfe.dados_nfe)


if __name__ == '__main__':
    app.run(debug=True)
