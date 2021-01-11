from flask import Flask, render_template, session, request, redirect, url_for
from datos.UsuarioDao import UsuarioDao
import json
from datos import  logger

app = Flask(__name__)

app.secret_key="qwerty"


@app.route('/',methods=["GET","POST"])
def index():
    if "userID" in session:
        if session["tipo"]=="paciente":
            return redirect(url_for("paciente"))
        elif session["tipo"]=="hospital":
            return redirect(url_for("hospital"))
        else :
            logger.logger.debug("reconoce medico")
            return redirect(url_for("medico"))
    elif request.method=="POST" :
        f=request.form
        if UsuarioDao.autentificarUsuario(tipo=f["tipo"].lower(),id=f["userID"],password=f["password"]):
            session['userID'] = f["userID"]
            session['tipo']=f["tipo"].lower()
            # agregar el usuario a la sesión

            return redirect(url_for("index"))
        else:
            return "datos erroneos"
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("userID")
    session.pop("tipo")
    return redirect(url_for("index"))


@app.route("/registro")
def registro():

    return render_template("registro.html")









@app.route("/session",methods=["Get","POST"])
def sesion():
    if "userID" in session:
        if session["tipo"]=="paciente":
            return redirect(url_for("paciente"))
        elif session["tipo"]=="hospital":
            return redirect(url_for("hospital"))
        else :
            logger.logger.debug("reconoce medico")
            return redirect(url_for("medico"))
    elif request.method=="POST" :
        f=request.form
        if UsuarioDao.autentificarUsuario(tipo=f["tipo"].lower(),id=f["userID"],password=f["password"]):
            session['userID'] = request.form['userID']
            session['tipo']=f["tipo"].lower()
            # agregar el usuario a la sesión

            return redirect(url_for("sesion"))
        else:
            return "datos erroneos"
    else:
        return render_template(("session.html"))









@app.route("/register")
def register():
    return "registrar usuario"


@app.route("/Paciente")
def paciente():#falta autentificar con contraseña encriptada
    datos =json.loads(UsuarioDao.datosPacientes(id=session["userID"],tipo=session["tipo"]))["datos"]

    return render_template("paciente.html",datos=datos)


@app.route("/hospital")
def hospital():#falta autentificar con contraseña encriptada
    datos =json.loads(UsuarioDao.datosHospital(id=session["userID"],tipo=session["tipo"]))["datos"]

    return render_template("hospital.html",datos=datos)


@app.route("/medico")
def medico():#falta autentificar con contraseña encriptada
    datos =json.loads(UsuarioDao.datosMedico(id=session["userID"],tipo=session["tipo"]))["datos"]

    return render_template("medico.html",datos=datos)


if __name__ == '__main__':
    app.run()
