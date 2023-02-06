
from flask import Flask, render_template, request, make_response
import csv

# Think about LINQ C# syntax for python?

app = Flask(__name__)

fsReadFound = 0

importedlist = []
def fsWriteProtocol(n,p,t):
    fs = open('phn_database.csv', 'a')
    writer = csv.writer(fs, delimiter=";")
    #header = ['name', 'firstname', 'phonenumber']
    #writer.writerow(header)
    writer.writerow((n,p,t))

def fsReadProtocol(n,p,t):
    importedlist = []
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
    #print(str(importedlist))
    for phonerow in importedlist:
        if phonerow['name'] == n or phonerow['firstname'] == p or phonerow['phonenumber'] == t:
            returnlist.append({'name' : str(phonerow['name']),
                              'firstname' :str(phonerow['firstname']),
                              'phonenumber' :str(phonerow['phonenumber']),
                              'idcode' :str(idcode)})
            #returnlist.append([str(phonerow['name']),str(phonerow['firstname']),str(phonerow['phonenumber']),str(idcode)])
            fsReadFound += 1
            #return([phonerow['name'], phonerow['firstname'], phonerow['phonenumber'], idcode])
        idcode += 1
    return([returnlist])

# Scrap Delete Protocol for now, I'll work on it later            
def fsDeleteProtocol(n,p,t):
    imported_delete_list = []
    fs = open('phn_database.csv', 'r')
    print('A')
    reader = csv.DictReader(fs, delimiter=';')
    for row in reader:
        imported_delete_list.append({'name' : str(row['name']),
                              'firstname' :str(row['firstname']),
                              'phonenumber' :str(row['phonenumber'])})
        print(imported_delete_list)
    fsWriteProtocol('name', 'firstname', 'phonenumber')
    print("Init A")
    fsReplacementProtocol(n,p,t,imported_delete_list)
    
def fsReplacementProtocol(n,p,t,implist):
    fs = open('phn_database.csv', 'a')
    writer = csv.writer(fs, delimiter=";")
    for phonerow in implist:
        print("Init B")
        if phonerow['name'] != n and phonerow['firstname'] != p and phonerow['phonenumber'] != t:
            #return([phonerow['name'], phonerow['firstname'], phonerow['phonenumber']])
            print(phonerow['name'],phonerow['firstname'],phonerow['phonenumber'])
            writer.writerow((phonerow['name'],phonerow['firstname'],phonerow['phonenumber']))
    
    #fs = open('phn_database.csv', 'w')
    #writer = csv.writer(fs)
    #writer.writerows(importedlist)
    
    

#registrationlist = {"0611651627": "Liam COLLE"}
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
    # Ce code génère une erreur 500
    #print(finalprocessing[7])
    
    if finalprocessing[0] == None or fsReadFound == 0:
        print("[SERVEXEC]: Reader hasn't found anything. Returning 'Not Found'")
        return render_template("searchphoneresults.html", returndata = [{'name': 'UNKNOWN', 'firstname': 'UNKNOWN', 'phonenumber': 'UNKNOWN', 'idcode': '#'}])
    #print("[SERVEXEC]: Reader found occurence in database! Name:",finalprocessing[0] + " Firstname: " + finalprocessing[1] + " Phonenumber: " + finalprocessing[2])
    print("[SERVEXEC]: Reader found occurence in database!")
    #data2processing = finalprocessing[0]
    #print(finalprocessing[0])
    #for dataone in data2processing:
    #    print(str(dataone))
    #    securelist = [str(dataone['name']),str(dataone['firstname']),str(dataone['phonenumber']),str(dataone['idcode'])]
    #    print(str(securelist))
    #result = finalprocessing[0] + ' ' + finalprocessing[1]
    #return render_template("searchphoneresults.html", name = finalprocessing[0], firstname = finalprocessing[1], number = finalprocessing[2], idcode = finalprocessing[3])
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
    
    #♣notacceptable(406)
    #return "Record not found", HTTP_406_NOT_ACCEPTABLE
    return render_template('406.html')

@app.route('/admin')
def adminmode():
    return render_template("adminmode.html")

@app.route('/admincompleted', methods=['POST', 'GET'])
def adminmodefinished():
    nom = request.form['nom']
    prenom = request.form['prenom']
    telephone = request.form['telephone']
    
    fsDeleteProtocol(nom, prenom, telephone)
    print("[SERVEXEC]: Starting database write")
    print("[SERVEXEC]: STATUS WRITEDATA")
    print("[SERVEXEC]: Writing new database row")
    
    return render_template("registrationresult.html", name=nom, firstname=prenom, telephone=telephone)

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
