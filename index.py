from flask import Flask, render_template,request
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

web = Flask(__name__)
web.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.mszzaqinklhbntpvovzr:lYSZK6SwjVvGusWQ@aws-0-us-west-1.pooler.supabase.com:5432/postgres?client_encoding=utf8'
db.init_app(web)


class Libros(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(db.String(50))
    titulo: Mapped[str] = mapped_column(db.String(255))
    autor: Mapped[str] = mapped_column(db.String(255))
    genero: Mapped[str] = mapped_column(db.String(100))



class Usuarios(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(255))
    email: Mapped[str] = mapped_column(db.String(255))




class Prestamos(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_libro : Mapped[int] = mapped_column(db.Integer, db.ForeignKey('libros.id'))
    id_usuario : Mapped[int] = mapped_column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_prestamo = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_devolucion = mapped_column(DateTime)


    libro = db.relationship('Libros', backref='prestamos')
    usuario = db.relationship('Usuarios', backref='prestamos')


@web.route('/')
def principal():
    return render_template('index.html')

@web.route('/destroy/<int:id>')
def destroy(id):
      libro = Libros.query.get(id)
      if Libros:
        try:
            db.session.delete(libro)
            db.session.commit()
            return f'Libro con ID {id} eliminado correctamente.'
        except Exception as e:
            db.session.rollback()
            return f'Error al eliminar el libro: {str(e)}'
      
      

@web.route('/destroyUsuarios/<int:id>')
def destroyUsuarios(id):
      usuario = Usuarios.query.get(id)
      if Usuarios:
        try:
            db.session.delete(usuario)
            db.session.commit()
            return f'Usuario con ID {id} eliminado correctamente.'
        except Exception as e:
            db.session.rollback()
            return f'Error al eliminar el Usuario: {str(e)}'
      

@web.route('/Añadir_Libro')
def añadir_libro():
 return render_template('AñadirLibro.html')
  
  
@web.route('/storeLibros', methods=['post'])
def strorageLibros():
    id = request.form['txtID']
    isbn = request.form['txtISBN']
    titulo = request.form['txtTitulo']
    autor = request.form['txtAutor']
    genero= request.form['txtGenero']
    nuevo_libro = Libros(id=id, isbn=isbn, titulo=titulo, autor=autor,  genero=genero,)
    db.session.add(nuevo_libro)
    try:
        db.session.commit()
        return 'Libro agregado correctamente'
    except IntegrityError:
        db.session.rollback()
        return 'Error: El Libro ya existe en la biblioteca'
        

@web.route('/Registrar_nuevo_usuario')
def registrar_usuario():
    return render_template('RegistrarUsuario.html')

@web.route('/storeUsuarios', methods=['post'])
def strorageUsuarios():
    nombre = request.form['txtNombre']
    email = request.form['txtEmail']
    nuevo_usuario = Usuarios(nombre=nombre, email=email)
    db.session.add(nuevo_usuario)
    try:
        db.session.commit()
        return 'Usuario agregado correctamente'
    except IntegrityError:
        db.session.rollback()
        return 'Error: El email ya existe en la biblioteca'
  
@web.route('/Usuarios')
def usuario():
  usuarios = Usuarios.query.all()
  return render_template('Usuarios.html', usuarios=usuarios)


@web.route('/devolver_libro', methods=['GET', 'POST'])
def devolver_libro():
    if request.method == 'GET':
        prestamos = Prestamos.query.all()
        return render_template('devolverLibro.html', prestamos=prestamos)
    elif request.method == 'POST':
        prestamo_id = request.form['prestamo_id']
        prestamo = Prestamos.query.get(prestamo_id)
        if prestamo:
            db.session.delete(prestamo)
            db.session.commit()
            return f'El libro ha sido devuelto correctamente.'
        else:
            return 'No se encontró el préstamo.'


@web.route('/libros_con_retraso')
def libros_retraso():
    libros_con_retraso = []
    prestamos = Prestamos.query.all()
    fecha_actual = datetime.now(timezone.utc)  
    for prestamo in prestamos:
        if prestamo.fecha_devolucion.replace(tzinfo=timezone.utc) < fecha_actual:
            libros_con_retraso.append((prestamo.libro, prestamo.fecha_devolucion))  
    return render_template('LibrosRetraso.html', libros_con_retraso=libros_con_retraso)

@web.route('/Solicitar_prestamo')
def prestamo_libro():
    return render_template('PrestamoLibro.html')

@web.route('/prestamosulicitud', methods=['POST'])
def solicitar_prestamo():
    id_libro = request.form['id_libro']
    id_usuario = request.form['id_usuario']
    fecha_devolucion = datetime.strptime(request.form['fecha_devolucion'], '%Y-%m-%d')
    libro = Libros.query.get(id_libro)
    usuario = Usuarios.query.get(id_usuario)

    if libro and usuario:
        if len(libro.prestamos) == 0:  
            nuevo_prestamo = Prestamos(id_libro=id_libro, id_usuario=id_usuario, fecha_devolucion=fecha_devolucion)
            db.session.add(nuevo_prestamo)
            try:
                db.session.commit()
                return f'El usuario {usuario.nombre} ha tomado prestado el libro "{libro.titulo}" correctamente.'
            except Exception as e:
                db.session.rollback()
                return f'Error al solicitar préstamo: {str(e)}'
        else:
            return f'El libro "{libro.titulo}" no está disponible en este momento.'
    else:
        return 'Libro o usuario no encontrado.'

@web.route('/registros_de_biblioteca')
def registro():
   libros = Libros.query.all()  
   return render_template('Registro.html', libros=libros)

 
if __name__== '__main__':
  with web.app_context():
    db.create_all()
  web.run(debug=True)


    
