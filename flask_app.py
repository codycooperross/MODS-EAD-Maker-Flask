from flask import Flask, make_response, request, render_template, redirect, g, url_for

import EADMaker
from EADMaker import processExceltoEAD
from EADMaker import getSheetNames
from MODSMaker import processExceltoMODS
import sys
import uuid
import os

app = Flask(__name__)
app.config["DEBUG"] = True

#CACHEDIR = "/home/codyross/eadmaker/cache/"
CACHEDIR = os.getcwd() + "/cache"
#HOMEDIR = "/home/codyross/eadmaker/"
HOMEDIR = os.getcwd() + "/"

@app.route("/", methods=["GET", "POST"])
def redirectToEADMaker():
    return redirect(url_for('eadMakerHome'))

@app.route("/eadmaker", methods=["GET", "POST"])
def eadMakerHome():
    if request.method == "POST":
        id = str(uuid.uuid4())
        input_file = request.files["input_file"]
        filename = request.files["input_file"].filename

        if ".xlsx" in filename:
            filename = filename.replace("/", " ").replace("\\", " ")
            input_file.save(CACHEDIR + id + ".xlsx")
            return redirect("eadmaker/renderead/" + filename + "/" + id)
        else:
            return render_template('error.html', error="Uploaded file must be a .XLSX Excel file.")

    else:
        return render_template('home.html')

@app.route("/eadmaker/renderead/<string:filename>/<string:id>", methods=["GET", "POST"])
def eadMakerSelectSheet(filename, id):
    if request.method == "POST":
        select = request.form.get('sheetlist')
        output_data, returndict = processExceltoEAD(CACHEDIR + id + ".xlsx", select, id)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=" + returndict["filename"]
        return response
    else:
        sheetnames = getSheetNames(CACHEDIR + id + ".xlsx")
        return render_template('resultspage.html', sheets=sheetnames, publicfilename=filename, id=id, filename=filename)

@app.route("/eadmakerapi", methods=["GET", "POST"])
def eadMakerAPI():
    if request.method == "POST":
        id = str(uuid.uuid4())
        input_file = request.files['file']
        filename = request.files['file'].filename
        filename = filename.replace("/", " ").replace("\\", " ")
        if ".xlsx" in filename:
            input_file.save(CACHEDIR + id + ".xlsx")
            return "eadmaker/renderead/" + filename + "/" + id
        else:
            return render_template('error.html', error="Uploaded file must be a .XLSX Excel file.")

    else:
        return "ERROR"

#------MODS------

@app.route("/modsmaker", methods=["GET", "POST"])
def modsMakerHome():
    if request.method == "POST":
        id = str(uuid.uuid4())
        input_file = request.files["input_file"]
        filename = request.files["input_file"].filename
        filename = filename.replace("/", " ").replace("\\", " ")
        if ".xlsx" in filename:
            input_file.save(CACHEDIR + id + ".xlsx")
            return redirect("modsmaker/rendermods/" + filename + "/" + id)
        else:
            return render_template('error.html', error="Uploaded file must be a .XLSX Excel file.")

    else:
        return render_template('homeMODS.html')

@app.route("/modsmaker/rendermods/<string:filename>/<string:id>", methods=["GET", "POST"])
def modsMakerSelectSheet(filename, id):
    if request.method == "POST":
        select = request.form.get('sheetlist')
        output_data, returndict = processExceltoMODS(CACHEDIR + id + ".xlsx", select, id)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=" + returndict["filename"]
        return response
    else:
        sheetnames = getSheetNames(CACHEDIR + id + ".xlsx")
        return render_template('resultspageMODS.html', sheets=sheetnames, publicfilename=filename, id=id, filename=filename)

@app.route("/modsmakerapi", methods=["GET", "POST"])
def modsMakerAPI():
    if request.method == "POST":
        id = str(uuid.uuid4())
        input_file = request.files['file']
        filename = request.files['file'].filename
        filename = filename.replace("/", " ").replace("\\", " ")
        if ".xlsx" in filename:
            input_file.save(CACHEDIR + id + ".xlsx")
            return "modsmaker/rendermods/" + filename + "/" + id
        else:
            return render_template('error.html', error="Uploaded file must be a .XLSX Excel file.")

    else:
        return "ERROR"
