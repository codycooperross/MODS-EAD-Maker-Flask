from flask import Flask, make_response, request, render_template, redirect, g, url_for

import EADMaker
from EADMaker import processExceltoEAD
from EADMaker import getSheetNames
from MODSMaker import processExceltoMODS
import sys
import uuid
import os
import urllib

app = Flask(__name__)
app.config["DEBUG"] = True

CACHEDIR = os.path.join(os.path.dirname(__file__), 'cache/')
HOMEDIR = os.path.dirname(__file__) + '/'

def redirectToSelectSheet(redirectToMethod, request):
        id = str(uuid.uuid4())
        input_file = request.files["input_file"]
        filename = request.files["input_file"].filename

        if ".xlsx" in filename:
            filename = urllib.parse.quote(filename)
            input_file.save(CACHEDIR + id + ".xlsx")
            return redirect(url_for(redirectToMethod, filename=filename, id=id))
        else:
            return render_template('error.html', error="Uploaded file must be a .XLSX Excel file.")

def returnSheetSelection(sheetSelectionPage, request):
        id = request.args.get('id')
        filename = urllib.parse.unquote(request.args.get('filename'))
        sheetnames = getSheetNames(CACHEDIR + id + ".xlsx")
        return render_template(sheetSelectionPage, sheets=sheetnames, publicfilename=filename, id=id, filename=filename)

def returnDownload(request, ead, mods):
        id = request.args.get('id')
        select = request.form.get('sheetlist')
        outputData = ""
        returnDict = {}
        if ead:
            outputData, returnDict = processExceltoEAD(CACHEDIR + id + ".xlsx", select, id)
        if mods:
            outputData, returnDict = processExceltoMODS(CACHEDIR + id + ".xlsx", select, id)
        response = make_response(outputData)
        response.headers["Content-Disposition"] = "attachment; filename=" + returnDict["filename"]
        return response

@app.route("/", methods=["GET", "POST"])
def redirectToEADMaker():
    return redirect(url_for('eadMakerHome'))

@app.route("/eadmaker", methods=["GET", "POST"])
def eadMakerHome():
    if request.method == "POST":
        return redirectToSelectSheet('eadMakerSelectSheet', request)
    else:
        return render_template('home.html')

@app.route("/eadmaker/renderead", methods=["GET", "POST"])
def eadMakerSelectSheet():
    if request.method == "POST":
        return returnDownload(request,True,False)
    else:
        return returnSheetSelection('resultspage.html', request)

#------MODS------

@app.route("/modsmaker", methods=["GET", "POST"])
def modsMakerHome():
    if request.method == "POST":
        return redirectToSelectSheet('modsMakerSelectSheet', request)
    else:
        return render_template('homeMODS.html')

@app.route("/modsmaker/rendermods", methods=["GET", "POST"])
def modsMakerSelectSheet():
    if request.method == "POST":
        return returnDownload(request,False,True)
    else:
        return returnSheetSelection('resultspageMODS.html', request)
