
from flask import Flask, render_template, request, make_response
import csv

# Think about LINQ C# syntax for python (From Mr. Parra)? Not enough time for this.

app = Flask(__name__)

fsReadFound = 0

importedlist = []
def fsWriteProtocol(n,p,t):
    fs = open('phn_database.csv', 'a')
    writer = csv.writer(fs, delimiter=";")
    writer.writerow((n,p,t))

def fsReadProtocol(n,p,t):
    importedlist = []
    scan1list = []
    scan2list = []
    returnlist = []
    idcode = 1
    global fsReadFound
    fsReadFound = 0
    fs = open('phn_database.csv', 'r')
    reader = csv.DictReader(fs, delimiter=';')
    for row in reader:
        importedlist.append({'name' : str(row['name']),
                              'firstname' :str(row['firstname']),
                              'phonenumber' :str(row['phonenumber'])})
    for phonerow in importedlist:
        if phonerow['name'] == n or phonerow['firstname'] == p or phonerow['phonenumber'] == t:
            scan1list.append({'name' : str(phonerow['name']),
                              'firstname' :str(phonerow['firstname']),
                              'phonenumber' :str(phonerow['phonenumber']),
                              'idcode' :str(idcode)})
            fsReadFound += 1
        idcode += 1
    returnlist = scan1list
    if (n == '' and p != '' and t != '') or (n != '' and p != '' and t == '') or (n != '' and p == '' and t != '') or (n != '' and p != '' and t != ''):
        print("[SERVEXEC]: Executing Second Scan...")
        fsReadFound = 0
        returnlist = []
        scan2list = []
        for scan2list in scan1list:
            if (scan2list['name'] != n and scan2list['firstname'] == p and scan2list['phonenumber'] == t) or (scan2list['name'] == n and scan2list['firstname'] == p and scan2list['phonenumber'] != t) or (scan2list['name'] == n and scan2list['firstname'] != p and scan2list['phonenumber'] == t) or (scan2list['name'] == n and scan2list['firstname'] == p and scan2list['phonenumber'] == t):
                returnlist.append({'name' : str(scan2list['name']),
                                      'firstname' :str(scan2list['firstname']),
                                      'phonenumber' :str(scan2list['phonenumber']),
                                      'idcode' :str(scan2list['idcode'])})
                fsReadFound += 1
        print("[SERVEXEC]: Second scan executed successfully.")
        return([returnlist])
    else:
        return([returnlist])

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/registerphone')
def registerphone():
    return render_template("registerphone.html")

@app.route('/searchphone')
def searchphone():
    return render_template("searchphone.html")

@app.route('/searchphoneresults', methods=['GET'])
def searchphoneresults():
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    telephone = request.args.get('telephone')
    print("[SERVEXEC]: Args fetched!")
    
    finalprocessing = fsReadProtocol(nom, prenom, telephone)
    print("[SERVEXEC]: Final Processing values fetched! " + str(finalprocessing))
    print("[SERVEXEC]: Found occurences: " + str(fsReadFound))
    
    result = finalprocessing[0]
    # Ce code génère une erreur 500, utilisée pour le test de l'activation de l'erreur 500
    #print(finalprocessing[7])
    
    if finalprocessing[0] == None or fsReadFound == 0:
        print("[SERVEXEC]: Reader hasn't found anything. Returning 'Not Found'")
        return render_template("searchphoneresults.html", returndata = [{'name': 'UNKNOWN', 'firstname': 'UNKNOWN', 'phonenumber': 'UNKNOWN', 'idcode': '#'}])
    print("[SERVEXEC]: Reader found occurence in database!")
    return render_template("searchphoneresults.html", returndata = result)

@app.route('/registrationresult', methods=['POST', 'GET'])
def registrationresult():
    nom = request.form['nom']
    prenom = request.form['prenom']
    telephone = request.form['telephone']
    if nom != '' and prenom != '' and telephone != '':
        fsWriteProtocol(nom, prenom, telephone)
        print("[SERVEXEC]: Starting database write")
        print("[SERVEXEC]: STATUS WRITEDATA")
        print("[SERVEXEC]: Writing new database row")
        
        return render_template("registrationresult.html", name=nom, firstname=prenom, telephone=telephone)
    print("[SERVEXEC]: Invalid Data. Returning 406")
    
    return render_template('406.html')

@app.errorhandler(404)
def notfounderror(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def notfounderror(e):
    return render_template('500.html'), 500

@app.route('/406')
def notacceptable():
    print("406")
    return render_template('406.html'), 406

if __name__ == '__main__': 
    app.run()
