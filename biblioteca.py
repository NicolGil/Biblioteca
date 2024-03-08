
from datetime import datetime, timedelta

class Libro:
    def __init__(self, titulo, autor, isbn, genero):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.genero = genero
        self.disponible = True
        self.fecha_devolucion = None

class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        self.libros_prestados = []

class Biblioteca:
    def __init__(self):
        self.libros: Libro  = []  
        self.usuarios = [] 
    
    def agregar_libro(self, libro): 
        self.libros.append(libro) 
        print(f"El libro '{libro.titulo}' fue añadido a la biblioteca.")

    def eliminar_libro(self, titulo):
        for libro in self.libros: 
            if libro.titulo == titulo:
               self.libros.remove(libro)  
               print(f" El libro'{titulo}' fue eliminado de la biblioteca.")
               return
        print(f" El libro'{titulo}' fue eliminado de la biblioteca.")

    def registrar_usuario(self, nombre, email):
        usuario = Usuario(nombre, email)
        self.usuarios.append(usuario)  
        print(f"Usuario '{nombre}' registrado exitosamente.")

    def prestar_libro(self, titulo_libro, nombre_usuario, fecha_devolucion):
        libro_prestamo = None
        usuario_prestamo = None
    
        for libro in self.libros:
            if libro.titulo == titulo_libro:
                libro_prestamo = libro
                break

        for usuario in self.usuarios:  
            if usuario.nombre == nombre_usuario:
                usuario_prestamo = usuario
                break

        if libro_prestamo and usuario_prestamo:
            if libro_prestamo.disponible:
                libro_prestamo.disponible = False
                libro_prestamo.fecha_devolucion = fecha_devolucion
                usuario_prestamo.libros_prestados.append(libro_prestamo)
                print(f"El libro '{libro_prestamo.titulo}' ha sido prestado a {usuario_prestamo.nombre}.")
            else:
                print(f"El libro '{libro_prestamo.titulo}' no esta disponible.")
        else:
            print("Libro o usuario no encontrado.")
        
    
    def devolver_libro(self, titulo_libro, nombre_usuario):
        libro_devolucion = None
        usuario_devolucion = None

        for libro in self.libros:  
            if libro.titulo == titulo_libro:
                libro_devolucion = libro
                break

        for usuario in self.usuarios: 
            if usuario.nombre == nombre_usuario:
                usuario_devolucion = usuario
                break

        if libro_devolucion and usuario_devolucion:
            if libro_devolucion in usuario_devolucion.libros_prestados:
                libro_devolucion.disponible = True
                libro_devolucion.fecha_devolucion = None
                usuario_devolucion.libros_prestados.remove(libro_devolucion)
                print(f"El libro '{libro_devolucion.titulo}' ha sido devuelto por {usuario_devolucion.nombre}.")
            else:
                print(f"El libro '{libro_devolucion.titulo}' no fue prestado a {usuario_devolucion.nombre}.")
        else:
            print("Libro o usuario no encontrado.")

    def verificar_retraso(self):
        today = datetime.now()
        for usuario in self.usuarios: 
            for libro in usuario.libros_prestados:
                if libro.fecha_devolucion < today:
                    print(f"¡Atencion! El libro '{libro.titulo}' prestado por {usuario.nombre} esta retrasado.")

    def mostrar_usuarios(self):
     print("--- Usuarios Registrados ---")
     for usuario in self.usuarios:
        print(f"Nombre: {usuario.nombre}, Email: {usuario.email}")
        if usuario.libros_prestados:
            print("Libros Prestados:")
            for libro in usuario.libros_prestados:
                fecha_devolucion = libro.fecha_devolucion.strftime("%d/%m/%Y") if libro.fecha_devolucion else "N/A"
                print(f"  - {libro.titulo}, Fecha de Devolucion: {fecha_devolucion}")
        else:

            print("Libros Prestados: Ninguno")

    def mostrar_registro(self):
        for libro in self.libros:
          print (f"Libro: {libro.titulo}, Genero:{libro.genero}, ISBN:{libro.isbn}, Autor: {libro.autor}")
                

   
def main():
    biblioteca = Biblioteca()

    while True:
        print("\n--- Menu Principal ---")
        print("1. Añadir libro a la biblioteca")
        print("2. Eliminar libro de la biblioteca")
        print("3. Registrar nuevo usuario")
        print("4. Solicitar prestamo de libro")
        print("5. Devolver libro")
        print("6. Mostrar Usuarios")
        print("7. Verificar libros con retraso")
        print("8. Mostrar registros de la biblioteca")
        print("9. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            titulo = input("Ingrese el titulo del libro: ")
            autor = input("Ingrese el autor del libro: ")
            isbn = input("Ingrese el ISBN del libro: ") 
            genero = input("Ingrese el genero del libro: ")
            libro = Libro(titulo, autor, isbn, genero)
            biblioteca.agregar_libro(libro)
        elif opcion == "2":
            titulo = input("Ingrese el titulo del libro que desea eliminar: ")
            biblioteca.eliminar_libro(titulo)
        elif opcion == "3":
            nombre = input("Ingrese el nombre del nuevo usuario: ")
            email = input("Ingrese el correo electronico del nuevo usuario: ")
            biblioteca.registrar_usuario(nombre, email)
        elif opcion == "4":
            titulo_libro = input("Ingrese el titulo del libro que desea solicitar: ")
            nombre_usuario = input("Ingrese el nombre del usuario que solicita el prestamo: ")
            fecha_devolucion_str = input("Ingrese la fecha de devolucion (formato: dd/mm/aaaa): ")
            fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%d/%m/%Y")
            biblioteca.prestar_libro(titulo_libro, nombre_usuario, fecha_devolucion)
        elif opcion == "5":
            titulo_libro = input("Ingrese el titulo del libro que desea devolver: ")
            nombre_usuario = input("Ingrese el nombre del usuario que devuelve el libro: ")
            biblioteca.devolver_libro(titulo_libro, nombre_usuario)
        elif opcion == "6":
            biblioteca.mostrar_usuarios()
        elif opcion == "7":
            biblioteca.verificar_retraso()
        elif opcion == "8":
            biblioteca.mostrar_registro()
        elif opcion == "9":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

# if __name__ == "__main__":
#     main()
