import psycopg2 as psy
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask('__name__')

app.config["SECRET_KEY"] = '5ad9334794e3df4af280c61e7399ad57'


@app.route("/modelListerFinal")
def modelListerFinal():
    return render_template('scolarite/modelListerFinal.html')

@app.route("/apprenant/listeApp")
def listApp():
    return render_template('scolarite/listeApprenant.html', apprenants=findAllApprenant())



@app.route("/")
def index():
    return render_template('index.html')

#Connexion à la base de données PostgreSQL
def connexionDB():
    serveur = "localhost"
    bd = "GestionApprenant"
    userBD = "majmoud"
    mdp = "diop"
    try:
        connexion = psy.connect(host=serveur, database=bd, user=userBD, password=mdp)
        return connexion
    except psy.OperationalError:
        print('Erreur lors de la connexion à la base de données!!!')

#Liste des promos
def listePromo():
    connexion = connexionDB()
    cur = connexion.cursor()
    requete = "SELECT idpromo, nompromo FROM promo"
    cur.execute(requete)
    donnees = cur.fetchall()
    connexion.close()
    cur.close()
    return donnees

#Liste Apprenant
def findAllApprenant():
    connexion = connexionDB()
    cur = connexion.cursor()
    requete = """SELECT idapp, nom, prenom, datelieunaissance, sexe, matricule, email, promo.nompromo,
    Apprenant.status FROM Apprenant, Promo where Apprenant.idpromo=promo.idpromo"""
    cur.execute(requete)
    donnees = cur.fetchall()
    connexion.close()
    cur.close()
    return donnees

def findApprenantByPromoEnCours():
    connexion = connexionDB()
    cur = connexion.cursor()
    requete = """SELECT idapp, nom, prenom, datelieunaissance, sexe, matricule, email, promo.nompromo,
    Apprenant.status FROM Apprenant, Promo where Apprenant.idpromo=promo.idpromo AND promo.status='{}'
    AND Apprenant.status='{}'""".format('En cours','inscrit')
    cur.execute(requete)
    donnees = cur.fetchall()
    connexion.close()
    cur.close()
    return donnees

def findInscriptionAnnuler():
    connexion = connexionDB()
    cur = connexion.cursor()
    requete = """SELECT idapp, nom, prenom, datelieunaissance, sexe, matricule, email, promo.nompromo,
    Apprenant.status FROM Apprenant, Promo where Apprenant.idpromo=promo.idpromo AND promo.status='{}'
    AND Apprenant.status='{}'""".format('En cours','annuler')
    cur.execute(requete)
    donnees = cur.fetchall()
    connexion.close()
    cur.close()
    return donnees

def findInscriptionSuspendu():
    connexion = connexionDB()
    cur = connexion.cursor()
    requete = """SELECT idapp, nom, prenom, datelieunaissance, sexe, matricule, email, promo.nompromo,
    Apprenant.status FROM Apprenant, Promo where Apprenant.idpromo=promo.idpromo AND promo.status='{}'
    AND Apprenant.status='{}'""".format('En cours','suspendu')
    cur.execute(requete)
    donnees = cur.fetchall()
    connexion.close()
    cur.close()
    return donnees

#Vérifier si un user fait parmi de la base de données
def voirApprenant(matricule):
    connexion = connexionDB()
    cur = connexion.cursor()
    sql = "SELECT * FROM Apprenant WHERE idpromo={}".format(matricule)
    cur.execute(sql)
    teste = cur.fetchall()
    cur.close()
    connexion.close()
    return teste

#Retrouver le nom d'une promo en fonction de son id se trouvant au niveau de la table Apprenant
def findNomPromo(idpromo):
    connexion = connexionDB()
    cur = connexion.cursor()
    sql = "SELECT nompromo FROM Promo WHERE idpromo={}".format(idpromo)
    cur.execute(sql)
    teste = cur.fetchall()
    cur.close()
    connexion.close()
    return teste

@app.route('/traitementInscriptionApprenant', methods=["GET", "POST"])
def traitementInscriptionApprenant():
    #Récupération des données
    nom = request.form['nom']
    prenom = request.form['prenom']
    sexe = request.form['sexe']
    dateNaissance = request.form['dateNaissance']
    matricule = request.form['matricule']
    email = request.form['email']
    idpromo = int(request.form['promo'])
    try:
        connexion = connexionDB()
        cur = connexion.cursor()
        cur.execute("INSERT INTO Apprenant(idpromo, nom, prenom, sexe, datelieunaissance, matricule, email) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        ,(idpromo, nom, prenom, sexe, dateNaissance, matricule, email))
        connexion.commit()
        flash('Inscription réussie!!!')
        return redirect(url_for('inscription'))
    except ValueError:
        print("Erreur lors de l'insertion des données")
    


@app.route("/apprenant/inscriptionApprenant")
def inscription():
    return render_template('scolarite/inscriptionApprenant.html',promos=listePromo())

@app.route("/model")
def model():
    return render_template('model.html')

@app.route("/apprenant/annuler", methods=['POST', 'GET'])
def annuler_inscription():
    if request.method == 'POST':
        apprenant = request.form['apprenant']
        idapp = request.form['idApprenant']
        connexion = connexionDB()
        cur = connexion.cursor()
        requete = "UPDATE apprenant SET status=%s WHERE idapp=%s"
        cur.execute(requete,('annuler',idapp))
        connexion.commit()
        flash("L'annulation de l'inscription de {} est effectuée avec success!!!".format(apprenant))
        return render_template('scolarite/listeApprenantAnnuler.html')
    return render_template('scolarite/annulerInscription.html', apprenants=findApprenantByPromoEnCours())

@app.route('/apprenant/desactiverAnnulerInscription', methods=['POST'])
def desactiverAnnulerInscription():
    if request.method == 'POST':
        apprenant = request.form['apprenant']
        idapp = request.form['idApprenant']
        connexion = connexionDB()
        cur = connexion.cursor()
        requete = "UPDATE apprenant SET status=%s WHERE idapp=%s"
        cur.execute(requete,('inscrit',idapp))
        connexion.commit()
        flash("La desactivation de l'annulation de l'inscription de {} est effectuée avec success!!!".format(apprenant))
        return redirect(url_for('listApp'))

@app.route("/apprenant/listeInscriptionAnnuller")
def listeInscriptionAnnuller():
    return render_template('scolarite/listeApprenantAnnuler.html', apprenants=findInscriptionAnnuler())

@app.route("/apprenant/suspendre", methods=['POST', 'GET'])
def suspendre_inscription():
    if request.method == 'POST':
        apprenant = request.form['apprenant']
        idapp = request.form['idApprenant']
        connexion = connexionDB()
        cur = connexion.cursor()
        requete = "UPDATE apprenant SET status=%s WHERE idapp=%s"
        cur.execute(requete,('suspendu',idapp))
        connexion.commit()
        flash("La suspension de l'inscription de {} est effectuée avec success!!!".format(apprenant))
        return redirect(url_for('reactiverInscription'))
    return render_template('/scolarite/suspendreInscription.html', apprenants=findApprenantByPromoEnCours())

@app.route("/apprenant/reactiverInscription", methods=['POST', 'GET'])
def reactiverInscription():
    if request.method == 'POST':
        apprenant = request.form['apprenant']
        idapp = request.form['idApprenant']
        connexion = connexionDB()
        cur = connexion.cursor()
        requete = "UPDATE apprenant SET status=%s WHERE idapp=%s"
        cur.execute(requete,('inscrit',idapp))
        connexion.commit()
        flash("La réactivation de l'inscription de {} est effectuée avec success!!!".format(apprenant))
        return redirect(url_for('reactiverInscription'))
    return render_template('/scolarite/reactiverInscription.html', apprenants=findInscriptionSuspendu())


@app.route('/apprenant/modifier', methods=['POST', 'GET'])
def editer_inscription():
    if request.method == 'POST':
        idApprenant = request.form['idApprenant']
        nom = request.form['nom']
        prenom = request.form['prenom']
        datelieunaissance = request.form['datelieunaissance']
        sexe = request.form['sexe']
        matricule = request.form['matricule']
        promo = int(request.form['promo'])
        email = request.form['email']
        connexion = connexionDB()
        cur = connexion.cursor()
        requete = """UPDATE apprenant SET nom=%s, prenom=%s, datelieunaissance=%s, sexe=%s,
        matricule=%s, idpromo=%s, email=%s WHERE idapp=%s"""
        cur.execute(requete,(nom, prenom, datelieunaissance, sexe, matricule, promo, email, idApprenant))
        connexion.commit()
        flash('Modification effectuée avec succès!!!')
        return redirect(url_for('editer_inscription'))
    return render_template('scolarite/modifierApprenant.html', apprenants=findAllApprenant(), promo=listePromo())
        

if __name__ == '__main__':
	app.run(debug=True)
