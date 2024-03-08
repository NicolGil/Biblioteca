from flask import Flask, render_template,request, redirect, url_for
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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

@web.route('/Devolver_libro')
def devolver_libro():
    return render_template('Devolverlibro.html')

@web.route('/libros_con_retraso')
def libros_retraso():
    return render_template('LibrosRetraso.html')

@web.route('/Solicitar_prestamo')
def prestamo_libro():
    return render_template('PrestamoLibro.html')

@web.route('/registros_de_biblioteca')
def registro():
   libros = Libros.query.all()  
   return render_template('Registro.html', libros=libros)

 
if __name__== '__main__':
  with web.app_context():
    db.create_all()
  web.run(debug=True)


    
