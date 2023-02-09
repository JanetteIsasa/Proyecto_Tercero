from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,session
from flaskext.mysql import MySQL
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
import os


# Inicialización
app = Flask(__name__)

# Mysql Conección
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'proyecto_tercero'


mysql = MySQL(app)
mysql.init_app(app)
 
app.secret_key = "Secret Key"

#                                                                            #
#-------------------- RUTAS DEL ESCRITORIO (INDEX)---------------------------#
#  
# 
                                                                                  #
@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar "usuario" y "contraseña" un  POST request
    if request.method == 'POST':

        # Variables para el acceso
        nombreUsuario = request.form['nombreUsuario']
        contrasenaUsuario = request.form['contrasenaUsuario']
        # Verificar si existe en la bdb usando MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM usuario WHERE nombreUsuario="' +
                       nombreUsuario + '"')
       
        # Guarda un resultado
        cuenta = cursor.fetchone()
        # Cerrar conexion
        mysql.get_db().commit()
        # Si la cuenta existe en la tabla usuarios de la base de datos, devuelve al index
        if cuenta and check_password_hash(cuenta[2], contrasenaUsuario):
            # Crear inicio de sesion, para utilizar en las demas rutas, por posicionamiento en la tupla
            session['loggedin'] = True
            session['idUsuario'] = cuenta[0]
            session['nombreUsuario'] = cuenta[1]
            # Mensaje de inicio correcto
           # flash("correcto")
            # Direcciona al index
            return redirect(url_for('Index'))
        else:
            # Si no hay registro, redirecciona al login
            flash("Usuario o Contraseña inválida")
            return render_template('login.html')
    # Datos vacios, redireccion al login
    return render_template('login.html')


# Ruta de cierre de sesion
@app.route('/login/logout')
def logout():
    # Remueve los datos de sesion, asi cierra la sesion del usuario
    session.pop('loggedin', None)
    session.pop('idUsuario', None)
    session.pop('nombreUsuario', None)
    # Redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/index')
def Index():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
         #Extrae la cantidad de clientes que hay
        cur = mysql.get_db().cursor()
        cur.execute('SELECT COUNT(*) FROM cliente_personal')
        contador_cliente = cur.fetchone()[0]

        #Extrae los Clientes Deudores hasta la fecha 
        cur.execute("SELECT CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente),DATE_FORMAT( pagos.pagado_hasta, '%d-%m-%Y'), DATEDIFF(CURDATE(), pagos.pagado_hasta) FROM detalle_inscripcion, inscripcion, cliente_personal, pagos WHERE detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND pagos.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal AND inscripcion.estado_pago = 1 AND estado_eliminado_pago = 0 GROUP BY id_pago;")
        deudores = cur.fetchall()

        #Extrae la cantidad de pagos que hay
        cur.execute("SELECT REPLACE(FORMAT(SUM(monto),'#,#,,', 'es-ES'), ',', '.') FROM pagos WHERE pagos.estado_eliminado_pago = 0;")
        total_pagos = cur.fetchone()[0]
        cur.close()

        clientes_deudores = []
        for deudor in deudores:
            if deudores[2] > 0:
                clientes_deudores.append(deudor)      
        
        return render_template('index.html', contador_clientes = contador_cliente, clientes_deudores = clientes_deudores, total_pagos = total_pagos , user=user)

    

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


#                                                                                #
#------------------------------- RUTAS DE USUARIOS-------------------------------#
#                                                                                #

@app.route('/login/AgregarUsuario')
def AgregarUsuario():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('Usuarios/agregarUsuarios.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/getUsuarios', methods=['GET'])
def getUsuarios():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la modalidad
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'idUsuario' in request.args:
                id_usuario= request.args.get('id_usuario')
                cur.execute(
                    'SELECT * FROM usuario WHERE idUsuario = "' + id_usuario + '"')
            else:
                cur.execute(
                    'SELECT * FROM usuario ')
            usuarios = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for usuario in usuarios:
                # Se crea un diccionario para poder enviar como json
                usuario = {
                    "id_usuario": usuario[0],
                    "nombre_usuario": usuario[1],
                    "contrasena_usuario": usuario[2]
                   
                }
                respuesta.append(usuario)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/guardarUsuario', methods=['POST'])
def guardarUsuario():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        nombre_usuario = request.form['nombre_usuario']
        contraseña =  request.form['contraseña']
        hashedPassword = generate_password_hash(contraseña, method= 'sha256')
       
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO usuario (nombreUsuario,contrasenaUsuario) VALUES ('%s','%s')" % (nombre_usuario,hashedPassword))
        mysql.get_db().commit()
        flash('Modalidad agregado satisfactoriamente')

        return redirect(url_for('AgregarUsuario'))

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/actualizarUsuario', methods=['POST'])
def actualizarUsuario():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        id_usuario = request.form['id_usuario']
        nombre_usuario = request.form['nombre_usuario']
        contrasenaAnterior =  request.form['contrasenaAnterior']
        contrasenaActual =  request.form['contrasenaActual']

        cur = mysql.get_db().cursor()
        cur.execute('SELECT contrasenaUsuario FROM usuario WHERE idUsuario =' + id_usuario)
        conAnteriorBD = cur.fetchone()[0]
        cur.close()

        if check_password_hash(conAnteriorBD,contrasenaAnterior):
            hashedPassword = generate_password_hash(contrasenaActual, method= 'sha256')

            cur = mysql.get_db().cursor()
            cur.execute("UPDATE usuario SET  nombreUsuario= %s, contrasenaUsuario = %s WHERE idUsuario = %s",(nombre_usuario,hashedPassword, id_usuario))
            mysql.get_db().commit()
            flash('Datos del Usuario actualizado correctamente')
        else:
            flash('Contraseña anterior incorrecta')

        return redirect(url_for('AgregarUsuario'))

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/deleteUsuario', methods=['POST'])
def deleteUsuario():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        id_usuario = request.form['id_usuario']
        contrasenaAnterior =  request.form['contrasenaAnterior']

        cur = mysql.get_db().cursor()
        cur.execute('SELECT contrasenaUsuario FROM usuario WHERE idUsuario =' + id_usuario)
        conAnteriorBD = cur.fetchone()[0]
        cur.close()

        if check_password_hash(conAnteriorBD,contrasenaAnterior):    

            cur = mysql.get_db().cursor()
            cur.execute('DELETE FROM usuario WHERE idUsuario = %s ' % id_usuario)
            mysql.get_db().commit()

            flash('Datos del Usuario eliminado correctamente')
        else:
            flash('Contraseña anterior incorrecta')

        return redirect(url_for('AgregarUsuario'))

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

#                                                                                #
#------------------------------- RUTAS DE ENTRENADORES---------------------------#
#                                                                                #
@app.route('/login/Entrenador')
def Entrenador():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('Entrenadores/entrenador.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/getEntrenadores', methods=['GET'])
def getEntrenadores():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la modalidad
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'id_entrenador' in request.args:
                id_entrenador = request.args.get('id_entrenador')
                cur.execute(
                    'SELECT * FROM entrenador WHERE id__entrenador = "' + id_entrenador + '" and estado_entrenador = 1')
            else:
                cur.execute(
                    'SELECT * FROM entrenador WHERE estado_entrenador = 1')
            entrenadores = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for entrenador in entrenadores:
                # Se crea un diccionario para poder enviar como json
                entrenador = {
                    "id_entrenador": entrenador[0],
                    "nombre_entrenador": entrenador[1],
                    "cedula_entrenador": entrenador[2],
                    "edad_entrenador": entrenador[3],
                    "telefono_entrenador": entrenador[4],
                    "email_entrenador": entrenador[5],
                    "direccion_entrenador": entrenador[6] 
                }
                respuesta.append(entrenador)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))
  
#Funcion para saber si ya existe la modalidad
def existeEntrenador(id_entrenador):
    cur = mysql.get_db().cursor()
    codigo_entrenador = (id_entrenador)
    cur.execute('SELECT * FROM entrenador WHERE id_entrenador = "' + codigo_entrenador + '"')
    respuesta = cur.fetchone()
    cur.close()
    if respuesta:
        return True
    else:
        return False

@app.route("/crudEntrenador", methods=['POST'])
def crudEntrenador():
    if request.method == 'POST':
        id = request.form['id_entrenador']
        nombre_entrenador = request.form['nombre_entrenador'].title()
        cedula_entrenador = request.form['cedula_entrenador']
        edad_entrenador = request.form['edad_entrenador']
        telefono_entrenador = request.form['telefono_entrenador']
        email_entrenador = request.form['email_entrenador']
        direccion_entrenador = request.form['direccion_entrenador'].title()
        estado = 1

        if (existeEntrenador(id)):
            cur = mysql.get_db().cursor()
            cur.execute("""
            UPDATE entrenador SET nombre_entrenador=%s,
                                cedula_entrenador=%s,
                                edad_entrenador=%s,
                                telefono_entrenador=%s,
                                email_entrenador=%s,
                                direccion_entrenador=%s, 
                                estado_entrenador=%s
                                WHERE id_entrenador=%s
            """, (nombre_entrenador, cedula_entrenador, edad_entrenador, telefono_entrenador, email_entrenador, direccion_entrenador,estado, id))
            mysql.get_db().commit()

            flash('Datos del Entrenador actualizado satisfactoriamente')         
        else:
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO entrenador (nombre_entrenador, cedula_entrenador, edad_entrenador, telefono_entrenador, email_entrenador, direccion_entrenador,estado_entrenador) VALUES ('%s','%s','%s','%s','%s','%s',%s)" % 
            (nombre_entrenador, cedula_entrenador, edad_entrenador, telefono_entrenador, email_entrenador, direccion_entrenador,estado))
            mysql.get_db().commit()

            flash('Datos del Entrenador agregado satisfactoriamente')

        return redirect(url_for('Entrenador'))

       

@app.route('/deleteEntrenador')
def deleteEntrenador():  
    id = request.args.get('idEntrenadorEliminar')

    cur = mysql.get_db().cursor()
    cur.execute(" UPDATE entrenador SET estado_entrenador = 0 WHERE id_entrenador = " + id)
    mysql.get_db().commit()
    flash('Datos del Entrenador eliminado correctamente')
    return redirect(url_for('Entrenador'))


#                                                                                #
#------------------------------- RUTAS DE MODALIDADES ---------------------------#
#                                                                                #
@app.route("/login/ModalidadInterfaz")
def ModalidadInterfaz():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('Modalidades/modalidad.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))
   

@app.route('/login/Modalidad', methods=['GET'])
def Modalidad():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la modalidad
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'id_modalidad' in request.args:
                id_modalidad = request.args.get('id_modalidad')
                cur.execute(
                    'SELECT * FROM modalidad WHERE id_modalidad = "' + id_modalidad + '" and estado_modalidad = 1')
            else:
                cur.execute(
                    'SELECT * FROM modalidad WHERE estado_modalidad = 1')
            modalidades = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for modalidad in modalidades:
                # Se crea un diccionario para poder enviar como json
                modalidad = {
                    'id_modalidad': modalidad[0],
                    "nombre_modalidad": modalidad[1]
                
                }
                respuesta.append(modalidad)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

#Funcion para saber si ya existe la modalidad
def existeModalidad(id_modalidad):
   
    cur = mysql.get_db().cursor()
    codigo_modalidad = (id_modalidad)
    cur.execute('SELECT * FROM modalidad WHERE id_modalidad = "' + codigo_modalidad + '"')
    respuesta = cur.fetchone()
    cur.close()
    if respuesta:
        return True
    else:
        return False

@app.route("/crudModalidad", methods=['POST'])
def crudModalidad():
    if request.method == 'POST':
        id = request.form['id_modalidad']
        nombre_modalidad = request.form['nombre_modalidad'].title()
        estado = 1

        if (existeModalidad(id)):
            cur = mysql.get_db().cursor()
            cur.execute("""
            UPDATE modalidad SET nombre_modalidad=%s, estado_modalidad=%s
            WHERE id_modalidad=%s
                """, (nombre_modalidad,estado, id))
            mysql.get_db().commit()

            flash('Datos de la Modalidad actualizado satisfactoriamente')    
        else:
            
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO modalidad (nombre_modalidad,estado_modalidad) VALUES ('%s',%s)" % (nombre_modalidad,estado))
            mysql.get_db().commit()
            flash('Modalidad agregado satisfactoriamente')

        return redirect(url_for('ModalidadInterfaz'))


@app.route('/deleteModalidad')
def deleteModalidad():
    id = request.args.get('idModalidadE')

    cur = mysql.get_db().cursor()
    cur.execute(" UPDATE modalidad SET estado_modalidad = 0 WHERE id_modalidad = " + id)
    mysql.get_db().commit()
    flash('Datos de la Modalidad eliminado correctamente')
    return redirect(url_for('ModalidadInterfaz'))

#                                                                                #
#--------------------- RUTAS DE CLIENTES CON DATOS PERSONALES--------------------#
#                                                                                #
#Funcion para saber si ya existe la modalidad
def existeCliente(id_cliente_personal):
    cur = mysql.get_db().cursor()
    codigo_cliente = (id_cliente_personal)
    cur.execute('SELECT id_cliente_personal FROM cliente_personal WHERE id_cliente_personal = "' + codigo_cliente + '"')
    respuesta = cur.fetchone()
    cur.close()
    if respuesta:
        return True
    else:
        return False

@app.route('/login/ClientePersonal')
def ClientePersonal():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()

        return render_template('Clientes/clientePersonal.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/getClientePersonal', methods=['GET'])
def getClientePersonal():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la modalidad
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'id_cliente_personal' in request.args:
                id_cliente_personal = request.args.get('id_cliente_personal')
                cur.execute(
                    "SELECT id_cliente_personal, nombre_cliente, apellido_cliente, DATE_FORMAT(fecha_nacimiento_cliente, '%d-%m-%Y'),fecha_nacimiento_cliente, cedula_cliente, telefono_cliente, email_cliente, direccion_cliente, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente, horario_traslado_cliente, enfermedades_cliente, pesaje_actual_seguimiento FROM cliente_personal WHERE id_cliente_personal = " + id_cliente_personal + " and estado_cliente = 1")
            else:
                cur.execute(
                    "SELECT id_cliente_personal, nombre_cliente, apellido_cliente, DATE_FORMAT(fecha_nacimiento_cliente, '%d-%m-%Y'), fecha_nacimiento_cliente,cedula_cliente, telefono_cliente, email_cliente, direccion_cliente, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente, horario_traslado_cliente, enfermedades_cliente, pesaje_actual_seguimiento FROM cliente_personal WHERE estado_cliente = 1")
            clientes = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for cliente in clientes:
                # Se crea un diccionario para poder enviar como json
                cliente = {
                    'id_cliente_personal': cliente[0],
                    "nombre_cliente": cliente[1],
                    "apellido_cliente": cliente[2],
                    "fecha_formateado": cliente[3],
                    "fecha_nacimiento": cliente[4],
                    "cedula": cliente[5],
                    "telefono": cliente[6],
                    "email": cliente[7],
                    "direccion": cliente[8],
                    "obra_social": cliente[9],
                    "contacto_urgencia": cliente[10],
                    "telefono_urgencia": cliente[11],
                    "grupo_sanguineo": cliente[12],
                    "carnet_cliente": cliente[13],
                    "lugar_traslado": cliente[14],
                    "horario_traslado": cliente[15],
                    "enfermedades": cliente[16],
                    "peso_actual": cliente[17]
                
                }
                respuesta.append(cliente)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


@app.route("/crudCliente", methods=['POST'])
def crudCliente():

    if request.method == 'POST':
        try:      
            id = request.form['id_cliente']
            nombre_cliente = request.form['nombre_cliente'].title()
            apellido_cliente = request.form['apellido_cliente'].title()
            fecha_nacimiento_cliente = request.form['fecha_nacimiento_cliente']
            cedula_cliente = request.form['cedula_cliente']
            telefono_cliente = request.form['telefono_cliente']
            email_cliente = request.form['email_cliente']
            direccion_cliente = request.form['direccion_cliente'].title()
            peso_actual_seguimiento = request.form['peso_actual_seguimiento']
            obra_social_cliente = request.form['obra_social_cliente']
            contacto_urgencia_cliente = request.form['contacto_urgencia_cliente'].title()
            telefono_urgencia_cliente = request.form['telefono_urgencia_cliente']
            grupo_sanguineo_cliente = request.form['grupo_sanguineo_cliente']
            carnet_cliente = request.form['carnet_cliente']
            lugar_traslado_cliente = request.form['lugar_traslado_cliente']
            horario_traslado_cliente = request.form['horario_traslado_cliente']
            enfermedades_cliente = request.form['enfermedades_cliente'].capitalize()
            estado=1

            if (existeCliente(id)):
                cur = mysql.get_db().cursor()
                cur.execute("""
                UPDATE cliente_personal SET nombre_cliente=%s, apellido_cliente=%s, fecha_nacimiento_cliente=%s, cedula_cliente=%s, telefono_cliente=%s, email_cliente=%s, direccion_cliente=%s, pesaje_actual_seguimiento=%s,  obra_social_cliente=%s, contacto_urgencia_cliente=%s, telefono_urgencia_cliente=%s, grupo_sanguineo_cliente=%s, carnet_cliente=%s, lugar_traslado_cliente=%s, horario_traslado_cliente=%s, enfermedades_cliente=%s
                WHERE id_cliente_personal=%s
                    """,  (nombre_cliente, apellido_cliente, fecha_nacimiento_cliente, cedula_cliente, telefono_cliente,email_cliente, direccion_cliente, peso_actual_seguimiento, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente,  horario_traslado_cliente , enfermedades_cliente, id))
                mysql.get_db().commit()
                flash('Datos del Cliente ha sido actualizado satisfactoriamente')
            else:

                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO cliente_personal (nombre_cliente, apellido_cliente, fecha_nacimiento_cliente, cedula_cliente, telefono_cliente, email_cliente, direccion_cliente,pesaje_actual_seguimiento, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente, horario_traslado_cliente, enfermedades_cliente, estado_cliente) VALUES ('%s','%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s)" %  
                (nombre_cliente, apellido_cliente, fecha_nacimiento_cliente, cedula_cliente, telefono_cliente,email_cliente, direccion_cliente, peso_actual_seguimiento, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente,  horario_traslado_cliente , enfermedades_cliente, estado))
                mysql.get_db().commit()

                flash('Datos del Cliente agregado satisfactoriamente')
        except:
                flash('No se puede eliminar porque el Cliente esta relacionado con otra tabla')


        return redirect(url_for('ClientePersonal'))

@app.route('/deleteClientePersonal')
def deleteClientePersonal():
    
    id = request.args.get('id_cliente_personal')
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('DELETE FROM cliente_personal WHERE id_cliente_personal = '+ id)
        mysql.get_db().commit()
        flash('Datos del Cliente eliminado satisfactoriamente')
    except:
          flash('No se puede eliminar este Cliente porque está vinculado con otras tablas! Pero ponerlo en estado inactivo si así lo desea')

    return redirect(url_for('ClientePersonal'))

   

#                                                                                #
#------------------------------- RUTAS DE ACIVIDADES-----------------------------#
#                                                                                #

#Ruta para estirar datos del cliente
@app.route('/getCliente', methods=['GET'])
def getCliente():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        if request.method == 'GET':
            cedula = request.args.get('cedulaCliente')
            cur = mysql.get_db().cursor()
            cur.execute('SELECT id_cliente_personal, nombre_cliente, apellido_cliente, pesaje_actual_seguimiento FROM cliente_personal WHERE cedula_cliente = "' + cedula + '"')
            data = cur.fetchone()
            cur.close()
            print (data)
            #Si hay datos, mandarlos por json
            if data: 
                #Se crea un diccionario para poder enviar como json
                cliente = {
                    "idCliente": data[0],
                    "nombreCliente": data[1],
                    "apellidoCliente": data[2],
                    "pesoAnterior": data[3]
                }
                return jsonify(cliente)

            else: 
                #Sino retorna un json vacío
                return jsonify({})
    
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))   


@app.route('/login/Actividades')
def Actividades():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()

        #Estira los datos de modalidad para rellenar el select
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM modalidad WHERE estado_modalidad = 1')
        modalidad = cur.fetchall()
        cur.close()

        #Estira los datos de entrenador para rellenar el select
        cur = mysql.get_db().cursor()
        cur.execute('SELECT id_entrenador,nombre_entrenador FROM entrenador WHERE estado_entrenador = 1')
        entrenador = cur.fetchall()
        cur.close()
        
        return render_template('Actividades/actividades.html', modalidades = modalidad, entrenadores = entrenador, user= user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))  


#Funcion para saber si ya existe la modalidad
def existeActividad(id_actividades):
    cur = mysql.get_db().cursor()
    codigo_actividad = (id_actividades)
    cur.execute('SELECT * FROM actividades WHERE id_actividades = "' + codigo_actividad + '"')
    respuesta = cur.fetchone()
    cur.close()
    if respuesta:
        return True
    else:
        return False

@app.route('/login/getActividades/', methods=['GET'])
def getActividades():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la tabla actividades
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            query = 'SELECT id_actividades,modalidad.id_modalidad,modalidad.nombre_modalidad, entrenador.id_entrenador, entrenador.nombre_entrenador, dia_actividad, horario_actividad FROM actividades,entrenador, modalidad WHERE actividades.id_modalidad = modalidad.id_modalidad AND actividades.id_entrenador = entrenador.id_entrenador'
            if 'id_actividades' in request.args:
                id_actividades = request.args.get('id_actividades')
                cur.execute(
                   query + ' AND id_actividades = "' + id_actividades + '"')
            else:
                cur.execute(query)    
            actividades = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for actividad in actividades:
                # Se crea un diccionario para poder enviar como json
                actividad = {
                    'id_actividad': actividad[0],
                    "id_modalidad": actividad[1],
                    "nombre_modalidad": actividad[2],
                    "id_entrenador": actividad[3],
                    "nombre_entrenador": actividad[4],
                    "dia_actividad": actividad[5],
                    "horario_actividad": actividad[6]       
                
                }
                respuesta.append(actividad)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route("/crudActividades", methods=['POST'])
def crudActividades():

    if request.method == 'POST':
        id = request.form['id_actividades']
        tipo_modalidad = request.form['tipo_modalidad']
        nom_entrenador = request.form['nom_entrenador']
        dia_actividad = request.form['dia_actividad']
        horario_actividad = request.form['horario_actividad']

        if (existeActividad(id)):
            cur = mysql.get_db().cursor()
            cur.execute("""
            UPDATE actividades SET id_modalidad=%s, id_entrenador=%s, dia_actividad=%s, horario_actividad=%s
            WHERE id_actividades=%s
                """, (tipo_modalidad,nom_entrenador,dia_actividad, horario_actividad, id))
            mysql.get_db().commit()

            flash('La Actividad ha sido actualizada satisfactoriamente')
        else:
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO actividades (id_modalidad, id_entrenador, dia_actividad, horario_actividad) VALUES (%s,%s,'%s','%s')" % 
            (tipo_modalidad, nom_entrenador, dia_actividad, horario_actividad))
            mysql.get_db().commit()
            flash('Actividad agregado satisfactoriamente')

        return redirect(url_for('Actividades'))


@app.route('/deleteActividad')
def deleteActividad():
    id = request.args.get('id_actividades')
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('DELETE FROM actividades WHERE id_actividades = '+ id)
        mysql.get_db().commit()
        flash('Datos del Cliente eliminado satisfactoriamente')
    except:
          flash('No se puede eliminar esta Actividad porque aún está vinculado con otras tablas!')

    return redirect(url_for('Actividades'))

#                                                                                #
#------------------------ RUTAS DE REGISTRO DE PESOS ----------------------------#
#                                                                                #
@app.route('/login/RegistroPesos')
def RegistroPesos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:   
        user = session['nombreUsuario'].capitalize()
        return render_template('Seguimiento/registroPesos.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route('/login/getRegistroPesos', methods=['GET'])
def getRegistroPesos():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la modalidad
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'id_seguimiento' in request.args:
                id_seguimiento = request.args.get('id_seguimiento')
                cur.execute(
                    "SELECT id_seguimiento, cliente_personal.id_cliente_personal, cliente_personal.nombre_cliente, cliente_personal.apellido_cliente,  DATE_FORMAT(fecha_seguimiento, '%d-%m-%Y'), fecha_seguimiento, pesaje_seguimiento, diferencia_pesaje FROM cliente_personal, seguimiento WHERE cliente_personal.id_cliente_personal = seguimiento.id_cliente_personal AND id_seguimiento = " + id_seguimiento )
            else:
                cur.execute(
                    "SELECT id_seguimiento, cliente_personal.id_cliente_personal, cliente_personal.nombre_cliente, cliente_personal.apellido_cliente,  DATE_FORMAT(fecha_seguimiento, '%d-%m-%Y'),fecha_seguimiento, pesaje_seguimiento, diferencia_pesaje FROM cliente_personal, seguimiento WHERE cliente_personal.id_cliente_personal = seguimiento.id_cliente_personal")
            seguimientos = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for seguimiento in seguimientos:
                # Se crea un diccionario para poder enviar como json
                seguimiento = {
                    'id_seguimiento': seguimiento[0],
                    'id_cliente': seguimiento[1],
                    "nombre_cliente_seguimiento": seguimiento[2],
                    "apellido_cliente_seguimiento": seguimiento[3],
                    "fecha_formateado": seguimiento[4],
                    "fecha_seguimiento": seguimiento[5],
                    "pesaje_seguimiento": seguimiento[6],
                    "diferencia_pesaje": seguimiento[7]
                
                }
                respuesta.append(seguimiento)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))
  
#Funcion para saber si ya existe el registro de Peso
def existeRegistro(id_registro):
    cur = mysql.get_db().cursor()
    codigo_registro = (id_registro)
    cur.execute('SELECT * FROM seguimiento WHERE id_seguimiento = "' + codigo_registro + '"')
    respuesta = cur.fetchone()
    cur.close()
    if respuesta:
        return True
    else:
        return False

@app.route("/guardarRegistroDePeso", methods=['POST'])
def guardarRegistroDePeso():
    if request.method == 'POST':
        id = request.form['id_seguimiento']
        cliente_registro_peso = request.form['idCliente']
        fecha_seguimiento = request.form['fecha_seguimiento']
        pesaje_seguimiento = request.form['pesaje_seguimiento']
       
        #Extrae el peso anterior para poder hacer la diferencia actual
        cur = mysql.get_db().cursor()
        cur.execute("SELECT pesaje_actual_seguimiento FROM cliente_personal WHERE id_cliente_personal = " + cliente_registro_peso)
        peso_anterior = cur.fetchone()[0]
        cur.close()
        #Calcula la diferencia 
        calculo_diferencia = peso_anterior - float(pesaje_seguimiento)

        if calculo_diferencia <  float(pesaje_seguimiento):
            calculo_diferencia = calculo_diferencia * -1

        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO seguimiento (id_cliente_personal, fecha_seguimiento, peso_anterior_seguimiento, pesaje_seguimiento, diferencia_pesaje) VALUES (%s,'%s',%s,%s,%s)" % 
                                                (cliente_registro_peso, fecha_seguimiento,peso_anterior, pesaje_seguimiento, str(calculo_diferencia)))
        mysql.get_db().commit()

        cur = mysql.get_db().cursor()
        cur.execute("""UPDATE cliente_personal SET pesaje_actual_seguimiento=%s WHERE id_cliente_personal=%s""", (pesaje_seguimiento, cliente_registro_peso))
        mysql.get_db().commit()

        flash('El registro ha sido agregado satisfactoriamente')

    return redirect(url_for('RegistroPesos'))
    

@app.route("/actualizarRegistroDePeso", methods=['POST'])
def actualizarRegistroDePeso():
    id = request.form['id_seguimiento']
    cliente_registro_peso = request.form['idCliente']
    fecha_seguimiento = request.form['fecha_seguimiento']
    pesaje_seguimiento = request.form['pesaje_seguimiento']
    
    if request.method == 'POST':
        #Extrae el peso anterior para poder hacer la diferencia actual
            cur = mysql.get_db().cursor()
            cur.execute("SELECT pesaje_actual_seguimiento FROM cliente_personal WHERE id_cliente_personal = " + cliente_registro_peso)
            peso_anterior = cur.fetchone()[0]
            cur.close()

            if(peso_anterior != pesaje_seguimiento):
                cur = mysql.get_db().cursor()
                cur.execute("SELECT peso_anterior_seguimiento FROM seguimiento WHERE id_seguimiento = " + id)
                peso_anterior = cur.fetchone()[0]
                cur.close()


            calculo_diferencia = peso_anterior - int(pesaje_seguimiento)

            if calculo_diferencia < int(pesaje_seguimiento):
                calculo_diferencia = calculo_diferencia * -1

            cur = mysql.get_db().cursor()
            cur.execute("""
                        UPDATE seguimiento SET fecha_seguimiento=%s, pesaje_seguimiento=%s, diferencia_pesaje=%s
                        WHERE id_seguimiento=%s""", (fecha_seguimiento,pesaje_seguimiento,calculo_diferencia, id))
            mysql.get_db().commit()

            cur = mysql.get_db().cursor()
            cur.execute("""UPDATE cliente_personal SET pesaje_actual_seguimiento=%s
                        WHERE id_cliente_personal=%s""", (pesaje_seguimiento, cliente_registro_peso))
            mysql.get_db().commit()

            flash('Datos del Registro actualizado satisfactoriamente') 

    return redirect(url_for('RegistroPesos'))

        
   
#                                                                                  #
#------------------------ RUTAS DE REGISTRO DE ENTRADA ----------------------------#
#                                                                                  #
@app.route('/login/RegistroEntrada')
def RegistroEntrada():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira los datos de modalidad para rellenar el select
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM modalidad')
        modalidad = cur.fetchall()
        cur.close()

        return render_template('EntradaGym/registroEntrada.html', modalidades = modalidad, user = user)
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))  


@app.route('/login/getRegistroDeEntrada', methods=['GET'])
def getREgistroDeEntrada():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la tabla actividades
        if request.method == 'GET':
            cur = mysql.get_db().cursor()
            query = 'SELECT registro_entrada.id_registro_entrada, cliente_personal.nombre_cliente, cliente_personal.apellido_cliente, modalidad.id_modalidad, modalidad.nombre_modalidad, fecha_entrada, horario_entrada, horario_salida FROM cliente_personal, modalidad, registro_entrada WHERE registro_entrada.id_cliente_personal = cliente_personal.id_cliente_personal AND registro_entrada.id_modalidad = modalidad.id_modalidad'
            if 'id_registro_entrada' in request.args:
                id_registro_entrada = request.args.get('id_registro_entrada')
                cur.execute(
                    query + 'AND id_registro_entrada' + id_registro_entrada)
            else:
                cur.execute(query)    
            registros = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for registro in registros:
                # Se crea un diccionario para poder enviar como json
                registro = {
                    'id_registro': registro[0],
                    "registro_nombre_cliente": registro[1],
                    "registro_apellido_cliente": registro[2], 
                    "registro_id_modalidad": registro[3] , 
                    "registro_nombre_modalidad": registro[4] , 
                    "registro_fecha_entrada": registro[5],
                    "registro_horario_entrada": registro[6], 
                    "registro_horario_salida": registro[7]        
                
                }
                respuesta.append(registro)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route("/guardarRegistroEntrada", methods=['POST'])
def guardarRegistroEntrada():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        tipo_modalidad = request.form['tipo_modalidad']
        fecha_entrada = request.form['fecha_entrada']
        horario_entrada = request.form['horario_entrada']
        horario_salida = "--:-- ---"
    
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO registro_entrada (id_cliente_personal, id_modalidad, fecha_entrada, horario_entrada, horario_salida) VALUES (%s,%s,'%s','%s','%s')" % (id_cliente, tipo_modalidad, fecha_entrada, horario_entrada, horario_salida))
        mysql.get_db().commit()
        flash('Registro de Entrada agregado satisfactoriamente')

        return redirect(url_for('RegistroEntrada'))

@app.route("/actualizarRegistroEntrada", methods=['POST'])
def actualizarRegistroEntrada():
        id_entrada = request.form['id_registro_entrada']
        tipo_modalidad = request.form['tipo_modalidad']
        fecha_entrada = request.form['fecha_entrada'] 
        horario_salida = request.form['horario_salida'] 

        cur = mysql.get_db().cursor()
        cur.execute("""UPDATE registro_entrada SET id_modalidad=%s, fecha_entrada=%s, horario_salida=%s WHERE id_registro_entrada=%s""", (tipo_modalidad, fecha_entrada, horario_salida, id_entrada))
        mysql.get_db().commit()

        flash('El registro ha sido actualizado satisfactoriamente')

        return redirect(url_for('RegistroEntrada'))  


@app.route('/deleteRegistroEntrada')
def deleteRegistroEntrada():
    id = request.args.get('RegistroEntradaEliminar')

    #Elimina de la BD el registro
    cur = mysql.get_db().cursor()
    cur.execute(" DELETE FROM registro_entrada WHERE id_registro_entrada = " + id)
    mysql.get_db().commit()
    flash('El registro ha sido eliminado correctamente')
    return redirect(url_for('RegistroEntrada'))

#                                                                                  #
#------------------------ RUTAS DE ESTADO DE CLIENTES  ----------------------------#
#                                                                                  #

@app.route('/login/EstadoClientes',methods=['GET','POST'])
def EstadoClientes():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:     
        user = session['nombreUsuario'].capitalize()

        if request.method == 'GET':
            cur = mysql.get_db().cursor()
            cur.execute('SELECT * FROM cliente_personal WHERE estado_cliente=1')
            cliente = cur.fetchall()
            cur.close()
            tipo = "Activo"
        
        if request.method == 'POST':
            tipo_estado = request.form['tipo_estado']

            cur = mysql.get_db().cursor()
            cur.execute('SELECT * FROM cliente_personal WHERE estado_cliente='+ tipo_estado)
            cliente = cur.fetchall()
            cur.close()
            tipo = "Inactivo"
            
        return render_template('Estados/estadoCliente.html', clientesActivos = cliente, user = user, tipo = tipo)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route('/cambioEstado', methods = ['POST'])
def cambioEstado():
    id_estado = request.form['id_estado']
    estado = request.form['cambio_estado']

    cur = mysql.get_db().cursor()
    cur.execute("UPDATE cliente_personal SET estado_cliente=%s WHERE id_cliente_personal =%s",(estado,id_estado))
    mysql.get_db().commit()
    flash('Estado del Cliente ha sido actualizado satisfactoriamente')
    return redirect(url_for('EstadoClientes'))
   

    

@app.route('/login/getTodosLosClientes', methods=['GET'])
def getTodosLosClientes():
    # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Extrae todos los datos de la tabla actividades
        if request.method == 'GET':
            cur = mysql.get_db().cursor()

            if 'id_cliente_personal' in request.args:
                id_cliente_personal = request.args.get('id_cliente_personal')
                cur.execute(
                    'SELECT id_cliente_personal, nombre_cliente, apellido_cliente FROM cliente_personal WHERE id_cliente_personal = ' + id_cliente_personal)
            else:
                cur.execute(
                    'SELECT id_cliente_personal, nombre_cliente, apellido_cliente FROM cliente_personal ')    
            clientes = cur.fetchall()

            respuesta = []
            # Si hay datos, mandarlos por json
            for cliente in clientes:
                # Se crea un diccionario para poder enviar como json
                cliente = {
                    'id_cliente_personal': cliente[0],
                    "nombre_cliente": cliente[1],
                    "apellido_cliente": cliente[2]      
                
                }
                respuesta.append(cliente)
                mysql.get_db().commit()
                cur.close()
            return jsonify({"data": respuesta})
  
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

#                                                                                #
#--------------------- RUTAS DE CONSULTA DE AVANCES -----------------------------#
#                                                                                #

@app.route('/login/ConsultaDeAvances')
def ConsultaDeAvances():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('Seguimiento/consultasDeAvances.html',user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/BuscarAvanceCliente', methods=['POST'])
def BuscarAvanceCliente():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:

        id_cliente = request.form['id_cliente']

        cur = mysql.get_db().cursor()
        cur.execute("SELECT cliente_personal.nombre_cliente, cliente_personal.apellido_cliente, DATE_FORMAT(seguimiento.fecha_seguimiento, '%d-%m-%Y'), seguimiento.peso_anterior_seguimiento, seguimiento.pesaje_seguimiento, seguimiento.diferencia_pesaje FROM cliente_personal, seguimiento WHERE cliente_personal.id_cliente_personal ="+id_cliente+" AND cliente_personal.id_cliente_personal = seguimiento.id_cliente_personal")
        avances = cur.fetchall()
       
        cur.close()

        return render_template('Seguimiento/consultasDeAvances.html', datos = avances)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


#                                                                                #
#--------------------- RUTAS DE CLIENTES POR ACTIVIDADES -----------------------#
#                                                                                #

@app.route('/login/ClientesPorActividad')
def ClientesPorActividad():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira las actividades para poner en la tabla1
        cur = mysql.get_db().cursor()
        cur.execute('SELECT id_actividades,modalidad.nombre_modalidad, entrenador.nombre_entrenador, dia_actividad, horario_actividad FROM actividades,entrenador, modalidad WHERE actividades.id_modalidad = modalidad.id_modalidad AND actividades.id_entrenador = entrenador.id_entrenador AND modalidad.estado_modalidad = 1 AND entrenador.estado_entrenador = 1')
        data = cur.fetchall()
        cur.close()

        return render_template('Inscripciones/clientesPorActividad.html', actividades = data, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))



@app.route("/crudClienteAdministrativo", methods=['POST'])
def crudClienteAdministrativo():
    if request.method == 'POST':
        id_inscripcion = uuid.uuid4()
        datos = request.get_json()
        fecha_pago =  datos[0]['Fecha De Pago']
        fecha_vencimiento =  datos[0]['Fecha Vencimiento']
        monto = datos[0]['Monto Total']
        monto2 = monto.replace(".", "")
        estado_pago = 1

        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO inscripcion (id_inscripcion, fecha_de_pago, fecha_de_vencimiento, fecha_vencimiento_actual, fecha_pago_anterior_actual, total_a_pagar, estado_pago) VALUES ('%s','%s','%s','%s','%s','%s',%s)" % (id_inscripcion, fecha_pago, fecha_vencimiento, fecha_vencimiento, fecha_pago, monto2, estado_pago))
           
        cliente = datos[0]['Cliente']   
        for dato in datos[1]:
            cur.execute("INSERT INTO detalle_inscripcion (id_inscripcion, id_cliente_personal, id_actividades) VALUES ('%s','%s','%s')" % (id_inscripcion, cliente, dato['Codigo']))
          
        mysql.get_db().commit()
       
        return redirect(url_for('ClientesPorActividad'))



@app.route('/login/getInscripcion')
def getInscripcion():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Estira las actividades para poner en la tabla1
        cur = mysql.get_db().cursor()
        cur.execute("SELECT DISTINCT inscripcion.id_inscripcion, CONCAT(cliente_personal.nombre_cliente,' ', cliente_personal.apellido_cliente), DATE_FORMAT(fecha_de_pago, '%d-%m-%Y'), fecha_de_pago, DATE_FORMAT(fecha_de_vencimiento, '%d-%m-%Y') ,fecha_de_vencimiento, REPLACE(FORMAT(total_a_pagar,'#,#,,', 'es-ES'), ',', '.') FROM inscripcion, cliente_personal, detalle_inscripcion WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion")
        registros_inscripciones = cur.fetchall()
        cur.close()

        respuesta = []
        # Si hay datos, mandarlos por json
        for registro in registros_inscripciones:
          # Se crea un diccionario para poder enviar como json
            registro = {
                    'id_inscripcion': registro[0],
                    "cliente_inscripcion": registro[1],
                    "fecha_formateado1": registro[2],
                    "fecha_de_pago_inscripcion": registro[3], 
                    "fecha_formateado2": registro[4],    
                    "fecha_de_vencimiento_inscripcion": registro[5],     
                    "total_pagar_inscripcion": registro[6]     
            }
            respuesta.append(registro)
            mysql.get_db().commit()
            cur.close()
        return jsonify({"data": respuesta})

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/ListadoInscripciones')
def ListadoInscripciones():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:   
        user = session['nombreUsuario'].capitalize() 
        return render_template('Inscripciones/listadoInscripciones.html', user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route('/actualizarRegistro', methods=['POST'])
def actualizarRegistro():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session: 
        #Usuario
        user = session['nombreUsuario'].capitalize() 
        #Datos para actualizar
        id_incripcion = request.form['id_inscripcion']
        fecha_pago =  request.form['fecha_de_pago']
        fecha_vencimiento = request.form['fecha_vencimiento']
        monto = request.form['total_a_pagar']
        monto1 = monto.replace(".", "")

        cur = mysql.get_db().cursor()
        cur.execute("SELECT DISTINCT inscripcion.id_inscripcion, CONCAT(cliente_personal.nombre_cliente,' ', cliente_personal.apellido_cliente),  fecha_de_pago, fecha_de_vencimiento, total_a_pagar FROM inscripcion, cliente_personal, detalle_inscripcion WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion AND inscripcion.id_inscripcion = '%s'"% (id_incripcion))
        registros_inscripciones = cur.fetchall()
        cur.close()

        #Fecha y hora actual
        fecha_hora = datetime.now()
        tipo_accion = "Editado"
        

        for registro in registros_inscripciones:
            
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO auditoria_inscripciones (id_inscripcion, usuario, fecha_hora, tipo_accion, cliente, fecha_pago, fecha_pago_auditoria, fecha_vencimiento, fecha_vencimiento_auditoria, monto, monto_auditoria) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_incripcion,user,fecha_hora, tipo_accion, registro[1], registro[2], fecha_pago, registro[3], fecha_vencimiento, registro[4], monto1))
            mysql.get_db().commit()

        cur = mysql.get_db().cursor()
        cur.execute("UPDATE inscripcion SET fecha_de_pago = %s, fecha_de_vencimiento = %s, fecha_vencimiento_actual = %s, fecha_pago_anterior_actual = %s, total_a_pagar = %s WHERE id_inscripcion = %s",(fecha_pago,fecha_vencimiento,fecha_vencimiento,fecha_pago, monto1, id_incripcion))
        mysql.get_db().commit()

        cur = mysql.get_db().cursor()
        cur.execute("UPDATE pagos SET monto = %s WHERE id_inscripcion = %s",(monto1, id_incripcion))
        mysql.get_db().commit()
        flash('La Inscripcion ha sido actualizado satisfactoriamente')

        return render_template('Inscripciones/listadoInscripciones.html')

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 

@app.route('/deleteInscripcion')
def deleteInscripcion():
    user = session['nombreUsuario'].capitalize()
    id = request.args.get('idInscripcionE')
    #Elimina primero las actividades de esa inscripcion en la tabla detalle_inscripcion
    try:
        
        cur = mysql.get_db().cursor()

        cur.execute("SELECT pagos.id_inscripcion FROM pagos")
        datos = cur.fetchall()
        cur.close()
        print(datos)
        print(id)

        for dato in datos:

            if dato[0] == id:
                print("iguales")

            if dato[0] != id:
               
                cur = mysql.get_db().cursor()
                cur.execute("SELECT DISTINCT inscripcion.id_inscripcion, CONCAT(cliente_personal.nombre_cliente,' ', cliente_personal.apellido_cliente),  fecha_de_pago, fecha_de_vencimiento, total_a_pagar FROM inscripcion, cliente_personal, detalle_inscripcion WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion AND inscripcion.id_inscripcion = '%s'"% (id))
                registros_inscripciones = cur.fetchall()
                cur.close()
                #Fecha y hora actual
                fecha_hora = datetime.now()
                tipo_accion = "Eliminado"

                for registro in registros_inscripciones:
                    
                    cur = mysql.get_db().cursor()
                    cur.execute("INSERT INTO auditoria_inscripciones (id_inscripcion, usuario, fecha_hora, tipo_accion, cliente, fecha_pago, fecha_pago_auditoria, fecha_vencimiento, fecha_vencimiento_auditoria, monto, monto_auditoria) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id,user,fecha_hora, tipo_accion, registro[1], registro[2], registro[2], registro[3], registro[3], registro[4], registro[4]))
                    mysql.get_db().commit()

                cur = mysql.get_db().cursor()
                cur.execute(" DELETE FROM detalle_inscripcion WHERE detalle_inscripcion.id_inscripcion = '%s'" % id)
                mysql.get_db().commit()

                #Luego elimina la inscripcion en la tabla de inscripcion
                cur = mysql.get_db().cursor()
                cur.execute(" DELETE FROM inscripcion WHERE id_inscripcion = '%s'" % id)
                mysql.get_db().commit()
                flash('La Inscripcion ha sido eliminado correctamente')
            else:
                flash('La Inscripcion no se puede eliminar ya que está relacionada con otra tabla')  
        
    except:
         flash('La Inscripcion no se puede eliminar ya que está relacionada con otra tabla')
    return redirect(url_for('ListadoInscripciones'))

@app.route('/login/DetallesInscripciones', methods=['POST'])
def DetallesInscripciones():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session: 
        user = session['nombreUsuario'].capitalize()  
        codigo_inscripcion = request.form['id_inscripcion']
        str(codigo_inscripcion)
       
        #Estira las actividades en la que esta inscripto/a
        cur = mysql.get_db().cursor()
        cur.execute("SELECT COUNT(id_actividades), CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente)  FROM detalle_inscripcion, cliente_personal WHERE detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal AND detalle_inscripcion.id_inscripcion = '%s' "% codigo_inscripcion )
        contador_y_nombre = cur.fetchall()
        cur.close()

        #Estira las actividades en la que esta inscripto/a
        cur = mysql.get_db().cursor()
        cur.execute("SELECT inscripcion.id_inscripcion, CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente), detalle_inscripcion.id_detalle_inscripcion, CONCAT(modalidad.nombre_modalidad , '-' , entrenador.nombre_entrenador, '-' , actividades.dia_actividad, '-' , actividades.horario_actividad) FROM cliente_personal, actividades, detalle_inscripcion, modalidad, inscripcion, entrenador WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND detalle_inscripcion.id_actividades = actividades.id_actividades AND modalidad.id_modalidad = actividades.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion AND inscripcion.id_inscripcion = '%s'" % codigo_inscripcion)
        actividades_inscriptas = cur.fetchall()
        cur.close()

        return render_template('Incripciones/detallesInscripciones.html' , actividades = actividades_inscriptas,  cantidad_y_cliente = contador_y_nombre, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 



@app.route('/login/Reportes')
def Reportes():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira todos los datos del cliente personal
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM cliente_personal")
        cliente_personal = cur.fetchall()
        cur.close()

        return render_template('Reportes/reportes.html', cliente_personal = cliente_personal, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

    
@app.route('/login/reporteCliente')
def reporteCliente():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira todos los datos personales del cliente personal
        cur = mysql.get_db().cursor()
        cur.execute("SELECT nombre_cliente, apellido_cliente, DATE_FORMAT(fecha_nacimiento_cliente, '%d-%m-%Y'), cedula_cliente, telefono_cliente, email_cliente, direccion_cliente, pesaje_actual_seguimiento FROM cliente_personal")
        cliente_personal = cur.fetchall()
        cur.close()

        return render_template('Reportes/reporteCliente.html', cliente_personal = cliente_personal, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

   
@app.route('/login/reporteClienteFichaMedica')
def reporteClienteFichaMedica():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira todos los datos del cliente personal
        cur = mysql.get_db().cursor()
        cur.execute("SELECT nombre_cliente, apellido_cliente,DATE_FORMAT(fecha_nacimiento_cliente, '%d-%m-%Y'), cedula_cliente, telefono_cliente,  pesaje_actual_seguimiento, enfermedades_cliente, obra_social_cliente, contacto_urgencia_cliente, telefono_urgencia_cliente, grupo_sanguineo_cliente, carnet_cliente, lugar_traslado_cliente, horario_traslado_cliente FROM cliente_personal")
        cliente = cur.fetchall()
        cur.close()

        return render_template('Reportes/reporteClienteFichaMedica.html', cliente_personal = cliente, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

  
@app.route('/login/reporteRegistroDePesos')
def reporteRegistroDePesos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Estira todos los datos de la tabla seguimiento
        cur = mysql.get_db().cursor()
        cur.execute("SELECT cliente_personal.nombre_cliente, cliente_personal.apellido_cliente, DATE_FORMAT(seguimiento.fecha_seguimiento, '%d-%m-%Y'), seguimiento.peso_anterior_seguimiento, seguimiento.pesaje_seguimiento, seguimiento.diferencia_pesaje FROM cliente_personal, seguimiento WHERE cliente_personal.id_cliente_personal = seguimiento.id_cliente_personal")
        registros = cur.fetchall()
        cur.close()

        return render_template('Reportes/reporteRegistroDePesos.html', registrosPesos = registros)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))
 
@app.route('/login/reportesClientesActividades', methods=['GET','POST'])
def reportesClientesActividades():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        #Estira todos los datos de las actividades
        cur = mysql.get_db().cursor()
        cur.execute('SELECT id_actividades, modalidad.nombre_modalidad, entrenador.nombre_entrenador, dia_actividad, horario_actividad FROM actividades, modalidad, entrenador WHERE modalidad.id_modalidad = actividades.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador')
        actividades = cur.fetchall()
        cur.close()

        if request.method == 'GET':
            #Estira todos los datos de la actividad
            cur = mysql.get_db().cursor()
            cur.execute('SELECT cliente_personal.nombre_cliente , cliente_personal.apellido_cliente, modalidad.nombre_modalidad , entrenador.nombre_entrenador, actividades.dia_actividad, actividades.horario_actividad FROM cliente_personal, actividades, detalle_inscripcion, modalidad, inscripcion, entrenador WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND detalle_inscripcion.id_actividades = actividades.id_actividades AND modalidad.id_modalidad = actividades.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion')
            datos = cur.fetchall()
            cur.close()
           
            
        if request.method == 'POST':
            id_actividad =  request.form['id_actividad']
            #Estira todos los datos de la actividad de acuerdo al filtro aceptado
            cur = mysql.get_db().cursor()
            cur.execute("SELECT cliente_personal.nombre_cliente, cliente_personal.apellido_cliente, modalidad.nombre_modalidad, entrenador.nombre_entrenador, actividades.dia_actividad, actividades.horario_actividad FROM cliente_personal, actividades, detalle_inscripcion, inscripcion, modalidad, entrenador WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND actividades.id_modalidad = modalidad.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND actividades.id_actividades = detalle_inscripcion.id_actividades AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND actividades.id_actividades ='%s'" % id_actividad)
            datos = cur.fetchall()
            cur.close()

        return render_template('Reportes/reporteClientes-Actividades.html', datos = datos, actividades = actividades, user = user) 
    
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/reportePagos', methods=['GET','POST'])
def reportePagos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        if request.method == 'GET':
           #Estira las actividades para poner en la tabla1
            cur = mysql.get_db().cursor()
            cur.execute("SELECT pagos.id_pago, CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente), DATE_FORMAT(pagos.fecha_de_pago, '%d-%m-%Y'),  DATE_FORMAT( pagos.pagado_desde, '%d-%m-%Y'), DATE_FORMAT( pagos.pagado_hasta, '%d-%m-%Y'), REPLACE(FORMAT(inscripcion.total_a_pagar,'#,#,,', 'es-ES'), ',', '.'), GROUP_CONCAT(CONCAT(entrenador.nombre_entrenador,' ' , modalidad.nombre_modalidad, ' ', actividades.dia_actividad, ' ', actividades.horario_actividad) SEPARATOR ' - '), inscripcion.id_inscripcion FROM detalle_inscripcion, inscripcion, actividades, modalidad, entrenador , cliente_personal, pagos WHERE detalle_inscripcion.id_actividades = actividades.id_actividades AND actividades.id_modalidad = modalidad.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND pagos.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal AND inscripcion.estado_pago = 1 AND estado_eliminado_pago = 0 GROUP BY id_pago")
            pagos = cur.fetchall()
        
            cur.execute("SELECT REPLACE(FORMAT(SUM(monto),'#,#,,', 'es-ES'), ',', '.') FROM pagos WHERE pagos.estado_eliminado_pago = 0")
            suma = cur.fetchone()[0]
            cur.close()
               
        if request.method == 'POST':
            fecha_filtro1 =  request.form['fecha_filtro1']
            fecha_filtro2 =  request.form['fecha_filtro2']
           
            #Estira las actividades para poner en la tabla1
            cur = mysql.get_db().cursor()
            #Suma el total de acuerdo al filtro
            cur.execute('SELECT REPLACE(FORMAT(SUM(monto),"#,#,,", "es-ES"), ",", ".") FROM pagos WHERE pagos.estado_eliminado_pago = 0  AND fecha_de_pago BETWEEN "'+fecha_filtro1+'" AND "'+fecha_filtro2+'"')
            suma = cur.fetchone()[0]
           
            cur.execute('SELECT pagos.id_pago, CONCAT(cliente_personal.nombre_cliente," " , cliente_personal.apellido_cliente), DATE_FORMAT(pagos.fecha_de_pago, "%d-%m-%Y"),  DATE_FORMAT( pagos.pagado_desde, "%d-%m-%Y"), DATE_FORMAT( pagos.pagado_hasta, "%d-%m-%Y"), REPLACE(FORMAT(inscripcion.total_a_pagar,"#,#,,", "es-ES"), ",", "."), GROUP_CONCAT(CONCAT(entrenador.nombre_entrenador," " , modalidad.nombre_modalidad, " ", actividades.dia_actividad, " ", actividades.horario_actividad) SEPARATOR " - "), inscripcion.id_inscripcion FROM detalle_inscripcion, inscripcion, actividades, modalidad, entrenador , cliente_personal, pagos WHERE detalle_inscripcion.id_actividades = actividades.id_actividades AND actividades.id_modalidad = modalidad.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND pagos.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal AND inscripcion.estado_pago = 1 AND estado_eliminado_pago = 0  AND pagos.fecha_de_pago BETWEEN "'+fecha_filtro1+'" AND "'+fecha_filtro2+'" GROUP BY id_pago')
            pagos = cur.fetchall()
            cur.close()

        return render_template('Reportes/reportePagos.html', pagos = pagos, suma = suma, user = user) 
    
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/Pagos')
def Pagos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('Pagos/Pagos.html', user=user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


@app.route('/login/pagarCuotas', methods=['POST'])
def pagarCuotas():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        id_cliente = request.form['idCliente']
        
        if request.method == 'POST':
            cur = mysql.get_db().cursor()
            cur.execute("SELECT id_inscripcion, fecha_vencimiento_actual FROM inscripcion")
            datos = cur.fetchall()

            fecha_actual = date.today()

            for dato in datos:
                if dato[1] <= fecha_actual:
                    id = dato[0]
                    
                    cur = mysql.get_db().cursor()
                    cur.execute("UPDATE inscripcion SET estado_pago = 0 WHERE inscripcion.id_inscripcion =%s",(id))
                    mysql.get_db().commit()
                     
            #Estira todos los datos de la actividad de acuerdo al filtro aceptado
            cur = mysql.get_db().cursor()
            cur.execute("SELECT detalle_inscripcion.id_inscripcion, DATE_FORMAT(inscripcion.fecha_de_pago, '%d-%m-%Y'), DATE_FORMAT(inscripcion.fecha_de_vencimiento, '%d-%m-%Y'),  DATE_FORMAT(inscripcion.fecha_pago_anterior_actual, '%d-%m-%Y') , DATE_FORMAT( inscripcion.fecha_vencimiento_actual, '%d-%m-%Y'), REPLACE(FORMAT(inscripcion.total_a_pagar,'#,#,,', 'es-ES'), ',', '.'), GROUP_CONCAT(CONCAT(entrenador.nombre_entrenador,' , ' , modalidad.nombre_modalidad, ' , ', actividades.dia_actividad, ' , ', actividades.horario_actividad) SEPARATOR ' - ') FROM detalle_inscripcion, inscripcion, actividades, modalidad, entrenador WHERE detalle_inscripcion.id_actividades = actividades.id_actividades AND actividades.id_modalidad = modalidad.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = " + id_cliente + " GROUP BY detalle_inscripcion.id_inscripcion" )
            datos = cur.fetchall()
 
            cur.execute("SELECT CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente) FROM cliente_personal WHERE cliente_personal.id_cliente_personal  ='%s'" % id_cliente)
            nombre = cur.fetchone()[0]
 
            cur.close()
     
        return render_template('Pagos/pagarCuotas.html', user=user, datos = datos, nombre = nombre, idCliente = id_cliente)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/guardarPago', methods=['POST'])
def guardarPago():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        if request.method == 'POST':
            id_inscripcion = request.form.get('id_inscripcion')
            fecha_de_pago = request.form['fecha_de_pago']
            pagar_desde = request.form['pagar_desde']
            pagar_hasta = request.form['pagar_hasta']
            estado_pago = 1

            cur = mysql.get_db().cursor()
            cur.execute("SELECT inscripcion.total_a_pagar FROM inscripcion WHERE inscripcion.id_inscripcion= '%s'" %(id_inscripcion) )
            monto_inscripcion = cur.fetchone()[0]
            cur.close()

            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO pagos (fecha_de_pago, pagado_desde, pagado_hasta, id_inscripcion, monto) VALUES ('%s','%s','%s','%s','%s')" % (fecha_de_pago, pagar_desde, pagar_hasta, id_inscripcion, monto_inscripcion))
            mysql.get_db().commit()

            cur = mysql.get_db().cursor()
            cur.execute("UPDATE inscripcion SET fecha_pago_anterior_actual =%s, fecha_vencimiento_actual=%s, estado_pago=%s WHERE id_inscripcion =%s",(pagar_desde,pagar_hasta, estado_pago, id_inscripcion))
            mysql.get_db().commit()
            
            flash('Pago registrado satisfactoriament')

        return render_template('Pagos/Pagos.html')

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/getListadoPagos' ,methods=['GET'])
def getListadoPagos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        #Estira las actividades para poner en la tabla1
        cur = mysql.get_db().cursor()
        cur.execute("SELECT pagos.id_pago, CONCAT(cliente_personal.nombre_cliente,' ' , cliente_personal.apellido_cliente), DATE_FORMAT(pagos.fecha_de_pago, '%d-%m-%Y'),  DATE_FORMAT( pagos.pagado_desde, '%d-%m-%Y'), DATE_FORMAT( pagos.pagado_hasta, '%d-%m-%Y'), REPLACE(FORMAT(inscripcion.total_a_pagar,'#,#,,', 'es-ES'), ',', '.'), GROUP_CONCAT(CONCAT(entrenador.nombre_entrenador,' ' , modalidad.nombre_modalidad, ' ', actividades.dia_actividad, ' ', actividades.horario_actividad) SEPARATOR ' - '), inscripcion.id_inscripcion FROM detalle_inscripcion, inscripcion, actividades, modalidad, entrenador , cliente_personal, pagos WHERE detalle_inscripcion.id_actividades = actividades.id_actividades AND actividades.id_modalidad = modalidad.id_modalidad AND entrenador.id_entrenador = actividades.id_entrenador AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND pagos.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal AND inscripcion.estado_pago = 1 AND estado_eliminado_pago = 0 GROUP BY id_pago")
        listado_pagos = cur.fetchall()
        cur.close()

        respuesta = []
        # Si hay datos, mandarlos por json
        for lista in listado_pagos:
          # Se crea un diccionario para poder enviar como json
            lista = {
                    'id_pago': lista[0],
                    "cliente": lista[1],
                    "fecha_de_pago": lista[2],     
                    "desde": lista[3],     
                    "hasta": lista[4],    
                    "total": lista[5],    
                    "actividades": lista[6] ,    
                    "id_inscripcion": lista[7]     
            }
            respuesta.append(lista)
            mysql.get_db().commit()
            cur.close()
        return jsonify({"data": respuesta})

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


@app.route('/login/deletePago')
def deletePago():
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        id = request.args.get('id_pago')
        id_inscripcion = request.args.get('id_inscripcion')
        #Este es para el estado de pago de la inscripcion
        estado_pago = 0
        #Este para eliminar logicamente el registro de pago
        estado_eliminado_pago = 1

        cur = mysql.get_db().cursor()
        cur.execute("SELECT fecha_vencimiento_actual FROM inscripcion WHERE id_inscripcion = '%s'" % id_inscripcion)
        fecha_vencimiento_anterior = cur.fetchone()[0]

        cur = mysql.get_db().cursor()
        cur.execute("SELECT pagado_hasta FROM pagos WHERE id_pago = '%s'" % id)
        pagado_hasta = cur.fetchone()[0]

        if fecha_vencimiento_anterior == pagado_hasta:
          
            cur = mysql.get_db().cursor()
            cur.execute("UPDATE inscripcion SET estado_pago=%s WHERE id_inscripcion = %s ",(estado_pago, id_inscripcion))
            mysql.get_db().commit()

            cur = mysql.get_db().cursor()
            cur.execute("UPDATE pagos SET estado_eliminado_pago =%s WHERE id_pago =%s",(estado_eliminado_pago, id))
            mysql.get_db().commit()

            cur = mysql.get_db().cursor()
            cur.execute("SELECT DISTINCT pagado_desde FROM pagos WHERE id_inscripcion = '"+id_inscripcion +"' AND estado_eliminado_pago = 0 ORDER BY pagado_desde DESC")
            fecha_pago_inscripcion = cur.fetchone()[0]

            cur = mysql.get_db().cursor()
            cur.execute("SELECT DISTINCT pagado_hasta FROM pagos WHERE id_inscripcion = '"+id_inscripcion +"' AND estado_eliminado_pago = 0 ORDER BY pagado_desde DESC")
            fecha_vencimiento_inscripcion = cur.fetchone()[0]
            cur.close()

            cur = mysql.get_db().cursor()
            cur.execute("UPDATE inscripcion SET estado_pago=%s, fecha_vencimiento_actual=%s, fecha_pago_anterior_actual=%s WHERE id_inscripcion = %s ",(estado_pago, fecha_vencimiento_inscripcion, fecha_pago_inscripcion, id_inscripcion))
            mysql.get_db().commit()

            fecha_actual = date.today()
            if(fecha_actual < fecha_vencimiento_inscripcion ):
                cur = mysql.get_db().cursor()
                cur.execute("UPDATE inscripcion SET estado_pago=1 WHERE id_inscripcion = %s ",(id_inscripcion))
                mysql.get_db().commit()
      
        cur = mysql.get_db().cursor()
        cur.execute("UPDATE pagos SET estado_eliminado_pago =%s WHERE id_pago =%s",(estado_eliminado_pago, id))
        mysql.get_db().commit()

        #Fecha y hora actual
        fecha_hora = datetime.now()
        tipo_accion = "Eliminado" 
        estado_pago_anterior = 1   
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO auditoria_pago (id_pago, usuario, fecha_hora, tipo_accion, esta_pago_anterior, estado_actual) VALUES (%s,'%s','%s','%s', %s, %s)" % (id,user,fecha_hora, tipo_accion, estado_pago_anterior, estado_pago))
        mysql.get_db().commit() 

        flash('El registro ha sido eliminado correctamente')
        return redirect(url_for('Pagos'))

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))


@app.route('/login/EstadoPago',methods=['GET','POST'])
def EstadoPago():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:     
        user = session['nombreUsuario'].capitalize()

        if request.method == 'GET':
            cur = mysql.get_db().cursor()
            cur.execute("SELECT id_inscripcion, fecha_vencimiento_actual FROM inscripcion")
            dato = cur.fetchall()
            cur.close()

            print(dato)

            fecha_actual = date.today()

            for dat in dato:
                if dat[1] < fecha_actual:
                
                    id = dat[0]
                        
                    cur = mysql.get_db().cursor()
                    cur.execute("UPDATE inscripcion SET estado_pago = 0 WHERE inscripcion.id_inscripcion =%s",(id))
                    mysql.get_db().commit()

            datos = [()]
   
        if request.method == 'POST':

            tipo_estado = request.form['tipo_estado']
            
            cur = mysql.get_db().cursor()
            cur.execute("SELECT cliente_personal.nombre_cliente, cliente_personal.apellido_cliente, DATE_FORMAT(inscripcion.fecha_vencimiento_actual, '%d-%m-%Y'), inscripcion.total_a_pagar FROM inscripcion, cliente_personal, detalle_inscripcion WHERE inscripcion.estado_pago = '"+tipo_estado+"' AND detalle_inscripcion.id_inscripcion = inscripcion.id_inscripcion AND detalle_inscripcion.id_cliente_personal = cliente_personal.id_cliente_personal GROUP BY inscripcion.id_inscripcion")
            datos = cur.fetchall()
            cur.close()
 
        return render_template('Estados/estadoPago.html', datos = datos, user = user)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login')) 
   

@app.route('/login/AuditoriaPagos')
def AuditoriaPagos():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
       
        cur = mysql.get_db().cursor()
        cur.execute("SELECT DISTINCT auditoria_pago.usuario, DATE_FORMAT(auditoria_pago.fecha_hora, '%d-%m-%Y' ' ' '%H:%i:%s'), auditoria_pago.tipo_accion , CONCAT(cliente_personal.nombre_cliente,' ', cliente_personal.apellido_cliente), DATE_FORMAT(inscripcion.fecha_de_pago, '%d-%m-%Y'), inscripcion.fecha_de_pago, DATE_FORMAT(inscripcion.fecha_de_vencimiento, '%d-%m-%Y') , inscripcion.fecha_de_vencimiento, REPLACE(FORMAT(inscripcion.total_a_pagar,'#,#,,', 'es-ES'), ',', '.') FROM inscripcion, cliente_personal, detalle_inscripcion, auditoria_pago, pagos WHERE cliente_personal.id_cliente_personal = detalle_inscripcion.id_cliente_personal AND inscripcion.id_inscripcion = detalle_inscripcion.id_inscripcion AND auditoria_pago.id_pago = pagos.id_pago")
        auditoriaPagos = cur.fetchall()
        cur.close()
        return render_template('Auditorias/auditoria_pago.html', user=user, auditoriaPagos = auditoriaPagos)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

@app.route('/login/AuditoriaInscripciones')
def AuditoriaInscripciones():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
       
        cur = mysql.get_db().cursor()
        cur.execute("SELECT usuario, DATE_FORMAT(fecha_hora, '%d-%m-%Y' ' ' '%H:%i:%s'),tipo_accion , cliente ,DATE_FORMAT(fecha_pago, '%d-%m-%Y'), DATE_FORMAT(fecha_pago_auditoria, '%d-%m-%Y'), DATE_FORMAT(fecha_vencimiento, '%d-%m-%Y') , DATE_FORMAT(fecha_vencimiento_auditoria, '%d-%m-%Y'), REPLACE(FORMAT(monto,'#,#,,', 'es-ES'), ',', '.'), REPLACE(FORMAT(monto_auditoria,'#,#,,', 'es-ES'), ',', '.') FROM auditoria_inscripciones")
        auditoriaInscripciones = cur.fetchall()
        cur.close()
        return render_template('Auditorias/auditoria_inscripciones.html', user=user, auditoriaInscripciones = auditoriaInscripciones)

    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))
    
@app.route('/login/NuevoMenu')
def NuevoMenu():
     # Checkea si hay un inicio de sesion
    if 'loggedin' in session:
        user = session['nombreUsuario'].capitalize()
        return render_template('nuevomenu.html', user=user)
    # Si no hay sesion iniciada se redirecciona al login
    return redirect(url_for('login'))

# starting the app (debub=True es para que cualquier cambio que hagamos reinicie el servidor de nuevo)
if __name__ == "__main__":
    app.run(port=5050, debug=True)

