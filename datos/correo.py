import smtplib
from email.mime.text import MIMEText
from random import choice



def enviarmensaje(mensaje,email,asunto):
    username = 'appaplicacion24@gmail.com'
    password = 'jyfnzpczpxmazdsr'
    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    # Construimos el mensaje
    mensaje = MIMEText(mensaje)
    mensaje['From'] = username
    mensaje['To'] = email
    mensaje['Subject'] = asunto
    # Envio del mensaje
    mailServer.sendmail(username,
                        email,
                        mensaje.as_string())

def nuevacontrasena():
    longitud = 10
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    p = ""
    p = p.join([choice(valores) for i in range(longitud)])
    return p


#enviarmensaje("hola","johan.cano0524@gmail.com","asunto")

