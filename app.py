from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

from datos.achivos import excel
from datos.correo import nuevacontrasena, enviarmensaje
from forms.registerform import pacienteForm, hospitalForm, MedicoForm, ObsForm, ContrasenaForm, RecuperarContrasenaForm, \
    autentificarform
from usurarios import Usuarios
from datos.UsuarioDao import UsuarioDao
import json
from datos import  logger
################################################################################


#################################################################################
from database import  db
from usurarios.Usuarios import Paciente, Hospital, Medico, Observacion

app = Flask(__name__)

app.secret_key="qwerty"
#################################################################################
#configuracio db
datos_conexion=json.load(open("datos/conexion.json"))
full_url_db="postgresql://{}:{}@{}/{}".format(datos_conexion["user"],datos_conexion["password"],datos_conexion["host"],datos_conexion["database"])
app.config['SQLALCHEMY_DATABASE_URI']=full_url_db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
#INICIALIZACION DEL OBJETO DE DE SQLALCHEMY
db.init_app(app)

#configuracion flask-migrate
migrate=Migrate()
migrate.init_app(app,db)
#configuracion de flask-wtf
app.config['secret_key']="qwerty"
##############################################################################
#######################################################################

#######################################################################


##############################################################################
############################################################################
@app.route('/',methods=["GET","POST"])
def index():
    ocontrasena = RecuperarContrasenaForm()
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
        if ocontrasena.validate_on_submit():
            generarcontrasena(ocontrasena.id.data, ocontrasena.email.data, ocontrasena.tipo.data)
            return redirect(url_for("index"))

        elif UsuarioDao.autentificarUsuario(tipo=f["tipo"].lower(),id=f["userID"],password=f["password"]):
            session['userID'] = f["userID"]
            session['tipo']=f["tipo"].lower()
            # agregar el usuario a la sesión

            return redirect(url_for("index"))
        else:
            return "datos erroneos"
    else:


        return render_template("index.html",formC=ocontrasena)


@app.route("/logout")
def logout():
    session.pop("userID")
    session.pop("tipo")
    session.pop("datos")
    return redirect(url_for("index"))




@app.route("/Paciente")
def paciente():#falta autentificar con contraseña encriptada
    datos =json.loads(UsuarioDao.datosPacientes(id=session["userID"],tipo=session["tipo"]))["datos"]
    session["datos"]=datos
    if datos["verificacion"]!="True":
        return redirect(url_for("autentificar"))
    elif datos["cambio"]=="True":
        return redirect(url_for("contrasenapac"))
    else:


        return render_template("paciente.html",datos=datos)

@app.route("/paciente/observaciones")
def obsPaciente():
    #datos = json.loads(UsuarioDao.datosPacientes(id=session["userID"], tipo=session["tipo"]))["datos"]
    datos=session["datos"]
    registros=json.loads(UsuarioDao.obs(tipo="paciente",id=session["userID"]))
    if datos["verificacion"] != "True":
        return "falta validar"
    else:

        return render_template("obspaciente.html", datos=datos,registros=registros)



@app.route("/medico/observaciones")
def obsMedico():
    #datos = json.loads(UsuarioDao.datosPacientes(id=session["userID"], tipo=session["tipo"]))["datos"]
    datos=session["datos"]
    registros=json.loads(UsuarioDao.obs(tipo="medico",id=session["userID"]))
    if datos["verificacion"] != "True":
        return "falta validar"
    else:

        return render_template("obsmedico.html", datos=datos,registros=registros)




@app.route("/medico/cambiarcontrasena",methods=["GET","POST"])
def contrasenamed():
    datos = session["datos"]
    id=datos["id"]
    medico=Medico.query.get_or_404(id)
    contrasenaform=ContrasenaForm(obj=medico)
    if request.method == "POST":
        app.logger.debug("funciona hasta aqui {}".format(contrasenaform.validate_on_submit()))
        if contrasenaform.validate_on_submit():
            contrasenaform.populate_obj(medico)
            app.logger.debug("medico a cambiar contrasena {} ".format(medico.nombre))

            medico.verificaion = True
            medico.cambio=False
            db.session.commit()
            return  redirect(url_for("medico"))
        else:
            app.logger.debug(contrasenaform.errors)
    return render_template("contrasenamedico.html",form=contrasenaform,datos=datos)





@app.route("/paciente/cambiarcontrasena",methods=["GET","POST"])
def contrasenapac():
    datos = session["datos"]
    id=datos["id"]
    paciente=Paciente.query.get_or_404(id)
    contrasenaform=ContrasenaForm(obj=paciente)
    if request.method == "POST":
        app.logger.debug("funciona hasta aqui {}".format(contrasenaform.validate_on_submit()))
        if contrasenaform.validate_on_submit():
            contrasenaform.populate_obj(paciente)
            app.logger.debug("medico a cambiar contrasena {} ".format(paciente.nombre))

            paciente.cambio=False
            db.session.commit()
            return  redirect(url_for("paciente"))
        else:
            app.logger.debug(contrasenaform.errors)
    return render_template("contrasenamedico.html",form=contrasenaform,datos=datos)



@app.route("/hospital/cambiarcontrasena",methods=["GET","POST"])
def contrasenahos():
    datos = session["datos"]
    id=datos["id"]
    hospital=Hospital.query.get_or_404(id)
    contrasenaform=ContrasenaForm(obj=hospital)
    if request.method == "POST":
        app.logger.debug("funciona hasta aqui {}".format(contrasenaform.validate_on_submit()))
        if contrasenaform.validate_on_submit():
            contrasenaform.populate_obj(hospital)
            app.logger.debug("medico a cambiar contrasena {} ".format(hospital.nombre))

            hospital.cambio=False
            db.session.commit()
            return  redirect(url_for("hospital"))
        else:
            app.logger.debug(contrasenaform.errors)
    return render_template("contrasenahospital.html",form=contrasenaform,datos=datos)




@app.route("/hospital/observaciones")
def obsHospital():
    #datos = json.loads(UsuarioDao.datosPacientes(id=session["userID"], tipo=session["tipo"]))["datos"]
    datos=session["datos"]
    registros=json.loads(UsuarioDao.obs(tipo="hospital",id=session["userID"]))
    if datos["verificacion"] != "True":
        return "falta validar"
    else:

        return render_template("obshospital.html", datos=datos,registros=registros)




@app.route("/hospital/addmedico",methods=["GET","POST"])
def addMedico():
    datos = session["datos"]
    medico=Medico()
    #medico.id_hospital=session["userID"]
    #modificar valores cuando se acticve la verificacio y el cambio de contraseña
    #medico.cambioContraseña=False
    #medico.verificaion=True
    medicoform=MedicoForm(obj=medico)
    if request.method == "POST":
        app.logger.debug("funciona hasta aqui {}".format(medicoform.validate_on_submit()))
        if medicoform.validate_on_submit():
            medicoform.populate_obj(medico)
            app.logger.debug("medico a insertar {}".format(medico.nombre))
            medico.id_hospital=session["userID"]

            medico.verificaion=True
            medico.cambio=True
            db.session.add(medico)
            db.session.commit()
            return  redirect(url_for("hospital"))
        else:
            app.logger.debug(medicoform.errors)
    return render_template("addmedico.html",form=medicoform,datos=datos)



@app.route("/medico/addobs",methods=["GET","POST"])
def addObs():
    datos = session["datos"]
    observacion=Observacion()
    obsform=ObsForm()
    if request.method == "POST":
        app.logger.debug("funciona hasta aqui {}".format(obsform.validate_on_submit()))
        if obsform.validate_on_submit():
            obsform.populate_obj(observacion)
            app.logger.debug("medico a insertar {}".format(observacion.especialidad))
            observacion.medico=session["userID"]
            db.session.add(observacion)
            db.session.commit()
            return  redirect(url_for("medico"))
        else:
            app.logger.debug(obsform.errors)
    return render_template("addobs.html",form=obsform,datos=datos)





@app.route("/hospital")
def hospital():#falta autentificar con contraseña encriptada

    datos =json.loads(UsuarioDao.datosHospital(id=session["userID"],tipo=session["tipo"]))["datos"]
    session["datos"] = datos
    if datos["verificacion"]!="True":
        return redirect(url_for("autentificar"))
    elif datos["cambio"]=="True":
        return redirect(url_for("contrasenahos"))
    else:

        return render_template("hospital.html",datos=datos)



@app.route("/medico")
def medico():#falta autentificar con contraseña encriptada
    datos =json.loads(UsuarioDao.datosMedico(id=session["userID"],tipo="medico"))["datos"]
    session["datos"] = datos
    if datos["cambio"] != "False":
        return(redirect(url_for("contrasenamed")))
    datos.pop("cambio")
    return render_template("medico.html",datos=datos)


@app.route("/registro",methods=["GET","POST"])
def registro():
    usuarioP = Paciente()
    formularioP=pacienteForm(obj=usuarioP)
    usuarioH = Hospital()
    formularioH=hospitalForm(obj=usuarioH)
    if request.method =="POST":
        app.logger.debug("conexion  tipo POST {}{}".format(formularioP.validate_on_submit(),formularioP))
        if formularioP.validate_on_submit() :
            formularioP.populate_obj(usuarioP)
            app.logger.debug("paciente {} insertado".format(usuarioP))
            db.session.add(usuarioP)
            db.session.commit()
            return redirect(url_for("index"))
        elif formularioH.validate_on_submit():
            formularioH.populate_obj(usuarioH)
            app.logger.debug("paciente {} insertado".format(usuarioH))
            db.session.add(usuarioH)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            app.logger.debug(formularioP.errors)
            app.logger.debug(formularioH.errors)

    return render_template("registro.html",formP=formularioP,formH=formularioH)


if __name__ == '__main__':
    app.run()

#generar,actualizar y enviar nueva contraseña
def generarcontrasena(id,correo,tipo):
    app.logger.debug("funciona 1"+tipo)
    if tipo=="medico":
        app.logger.debug("funciona 2")
        try:
            med=Medico().query.get_or_404(id)
            if med.email==correo:
                med.cambio=True
                med.contrasena=nuevacontrasena()
                app.logger.debug("nueva contraseña generada {} ".format(med.nombre))
                db.session.commit()
                enviarmensaje("nueva contraseña generada {} ".format(med.contrasena),med.email,"nueva contrasena")
                return True
            else:
                app.logger.debug("datos erroneos")
                return False
        except:
            return False
    elif tipo=="paciente":
        app.logger.debug("funciona 2")
        try:
            app.logger.debug("funciona 3"+correo)
            pac=Paciente().query.get_or_404(id)
            if pac.email==correo:
                app.logger.debug("funciona 4")
                pac.cambio=True
                pac.contrasena=nuevacontrasena()
                app.logger.debug("nueva contraseña generada {} ".format(pac.nombre))
                db.session.commit()
                enviarmensaje("nueva contraseña generada {} ".format(pac.contrasena), pac.email, "nueva contrasena")
                return True
            else:
                return False
        except:
            return False
    elif tipo=="hospital":
        app.logger.debug("funciona 2")
        try:
            hos=Hospital().query.get_or_404(id)
            if hos.email==correo:
                hos.cambio=True
                hos.contrasena=nuevacontrasena()
                app.logger.debug("nueva contraseña generada {} ".format(hos.nombre))
                db.session.commit()
                enviarmensaje("nueva contraseña generada {} ".format(hos.contrasena), hos.email, "nueva contrasena")
                return True
            else:
                return False
        except:

            return False
    else:
        return False




@app.route("/autentificar",methods=["GET","POST"])
def autentificar():
    app.logger.debug("funciona ")

    validar=autentificarform()
    datos=session["datos"]

    app.logger.debug("funciona 1")
    if request.method=="POST":
        clave=session["clave"]
        app.logger.debug("funciona 2"+session["tipo"])
        if session["tipo"]=="paciente":
            app.logger.debug("funciona 3")
            pac = Paciente().query.get_or_404(datos["id"])
            app.logger.debug("funciona 4")
            if validar.clave.data==clave:
                app.logger.debug("funciona 5")
                pac.verificaion=True
                db.session.commit()
                app.logger.debug("funciona 6")
                return redirect(url_for("index"))
            else:
                return render_template("autentificar.html", form=validar)
        elif session["tipo"]=="medico":
            med = Medico().query.get_or_404(id)
            if validar.clave.data==clave:
                med.verificaion=True
                db.session.commit()
                return redirect(url_for("index"))
            else:
                return render_template("autentificar.html", form=validar)
        elif session["tipo"]=="hospital":
            hos = Hospital().query.get_or_404(datos["id"])
            if validar.clave.data==clave:
                hos.verificaion=True
                db.session.commit()
                return redirect(url_for("index"))
            else:
                return  render_template("autentificar.html",form=validar)
        else:

            return render_template("autentificar.html", form=validar)
    else:
        clave = nuevacontrasena()
        session["clave"]=clave
        enviarmensaje("su clave de validacion es {}".format(clave), datos["email"], "clave correo")
        return render_template("autentificar.html", form=validar)


@app.route("/descargar",methods=["GET"])
def descargar():
    excel(tipo=session["tipo"],id=session["userID"])
    return send_from_directory(directory="archivos", filename='observaciones_{}.xlsx'.format(session["userID"]), as_attachment=True)








"""
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
        return render_template(("session.html"))"""











