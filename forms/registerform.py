from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
import wtforms as w
from wtforms.validators import DataRequired
from wtforms import validators as v
#from wtforms.fields.html5 import DateField


class pacienteForm(FlaskForm):
    id =StringField("Identificacion",validators=[DataRequired()],render_kw={"placeholder": "IDENTIFICACION"})
    contrasena = PasswordField("CONTRASEÑA",render_kw={"placeholder": "CONTRASEÑA"})
    telefono =w.StringField("Telefono",validators=[DataRequired()],render_kw={"placeholder": "TELEFONO"})
    email = w.StringField("correo electronico",validators=[DataRequired(),v.email()],render_kw={"placeholder": "CORREO ELECTRONICO"})
    fecha_nacimieto = StringField("Fecha nacimiento",validators=[DataRequired()],render_kw={"placeholder": "FECHA NACIMIENTO"})
    nombre = StringField("nombre completo",validators=[DataRequired()],render_kw={"placeholder": "NOMBRE COMPLETO"})
    direccion = StringField("Direcion",validators=[DataRequired()],render_kw={"placeholder": "DIRECCION"})
    registrarse=w.SubmitField("registrarse",render_kw={"style": "background: #43a047"})


class hospitalForm(FlaskForm):
    id = StringField("Identificacion", validators=[DataRequired()], render_kw={"placeholder": "IDENTIFICACION"})
    contrasena = PasswordField("CONTRASEÑA", render_kw={"placeholder": "CONTRASEÑA"})
    telefono = w.StringField("Telefono", validators=[DataRequired()], render_kw={"placeholder": "TELEFONO"})
    email = w.StringField("correo electronico", validators=[DataRequired(),v.email()],render_kw={"placeholder": "CORREO ELECTRONICO"})
    servicios=StringField("servicios prestados",validators=[DataRequired()],render_kw={"placeholder": "SERVICIOS QUE PRESTA"})
    nombre = StringField("nombre completo", validators=[DataRequired()], render_kw={"placeholder": "NOMBRE COMPLETO"})
    direccion = StringField("Direcion", validators=[DataRequired()], render_kw={"placeholder": "DIRECCION"})
    registrarse = w.SubmitField("registrarse",render_kw={"style": "background: #43a047"})


class MedicoForm(FlaskForm):
    id = StringField("Identificacion", validators=[DataRequired()], render_kw={"placeholder": "IDENTIFICACION"})
    contrasena = PasswordField("CONTRASEÑA", render_kw={"placeholder": "CONTRASEÑA"})
    telefono = w.StringField("Telefono", validators=[DataRequired()], render_kw={"placeholder": "TELEFONO"})
    email = w.StringField("correo electronico", validators=[DataRequired(),v.email()],
                          render_kw={"placeholder": "CORREO ELECTRONICO"})
    verificaion = w.BooleanField(default=True)
    cambioContraseña = w.BooleanField(default=True)
    #id_hospital = StringField("id_hospital",render_kw={"placeholder": "ID HOSPITAL"})
    nombre = StringField("nombre completo", validators=[DataRequired()], render_kw={"placeholder": "NOMBRE COMPLETO"})
    agregar = w.SubmitField("agregar medico",render_kw={"style": "background: #43a047"})




class ObsForm(FlaskForm):

    obserbacion = StringField("Descripcion", validators=[DataRequired()], render_kw={"placeholder": "Descripcion"})
    paciente = StringField("Identificacion paciente", validators=[DataRequired()], render_kw={"placeholder": "ID paciente"})

    especialidad =StringField("especialidad", validators=[DataRequired()], render_kw={"placeholder": "especialidad"})
    agregar = w.SubmitField("agregar observacion",render_kw={"style": "background: #43a047"})

class ContrasenaForm(FlaskForm):
    contrasena=w.PasswordField("contraseña",validators=[DataRequired()], render_kw={"placeholder": "nueva contraseña"})
    enviar=w.SubmitField("enviar",render_kw={"style": "background: #43a047"})

class RecuperarContrasenaForm(FlaskForm):
    id=StringField("Identificacion",render_kw={"placeholder": "Identificacion"})
    email=StringField(validators=[DataRequired(),v.email()],render_kw={"placeholder": "email"})
    tipo=w.SelectField(validators=[DataRequired()],choices=[("paciente","paciente"),("hospital","hospital"),("medico","medico")],render_kw={"placeholder": "tipo de usuario ","class":'select-css'})
    enviar=w.SubmitField("ENVIAR",render_kw={"style": "background: #43a047"})

class login():
    id = StringField("Identificacion", render_kw={"placeholder": "Identificacion"})

class   autentificarform(FlaskForm):
    clave=w.PasswordField(validators=[DataRequired()],render_kw={"placeholder": "clave"})
    validar=w.SubmitField("validar",render_kw={"style": "background: #43a047"})
