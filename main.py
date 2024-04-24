import json
import os
import pymongo
from dotenv import load_dotenv
import mysql.connector


class Alumno:
    def __init__(self, idalumno, nomalumno, diralumno, telalumno, fechanacalumno, sexo):
        self.id = idalumno
        self.nombre = nomalumno
        self.direccion = diralumno
        self.telefono = telalumno
        self.fecnac = fechanacalumno
        self.sexo = sexo

    def __str__(self):
        return f"Alumno(id:{self.id}, nombre:{self.nombre}, dirección:{self.direccion}, telefono:{self.telefono}, fecnac:{self.fecnac}, sexo:{self.sexo})"

    def a_dict(self):
        return {
            "idalumno": self.id,
            "nomalumno": self.nombre,
            "diralumno": self.direccion,
            "telalumno": self.telefono,
            "fechanacalumno": self.fecnac,
            "sexo": self.sexo
        }


class GestionAlumnos:

    def insertar_alumno(self):
        print("\n\t\t\t Opción: Insertar alumno\n")
        idalumno = input("Id del alumno: ")
        nomalumno = input("Nombre del alumno: ")
        diralumno = input("Dirección del alumno: ")
        telalumno = input("Teléfono del alumno: ")
        fechanacalumno = input("Fecha de nacimiento del alumno (dd/mm/aaaa): ")
        sexo = input("Sexo del alumno: ")
        alumno = Alumno(idalumno, nomalumno, diralumno, telalumno, fechanacalumno, sexo)

        try:
            with open('alumnos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(alumno.a_dict())

        with open('alumnos.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)
        print("\n1 alumno insertado en el fichero.")

    def eliminar_alumno(self):
        print("\n\t\t\t Opción: Eliminar alumno\n")
        id_eliminar = input("Id del alumno: ")

        try:
            with open('alumnos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Eliminar el alumno con el ID especificado
        data_actualizado = []
        for alumno in data:
            if alumno["idalumno"] != id_eliminar:
                data_actualizado.append(alumno)
        data = data_actualizado

        with open('alumnos.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)
        print("\n1 alumno eliminado del fichero.")

    def consultar_alumno(self):
        print("\n\t\t\t Opción: Consultar alumno\n")
        id_consultar = input("Id del alumno: ")

        try:
            with open('alumnos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for alumno in data:
                    if alumno["idalumno"] == id_consultar:
                        alumno_consultado = Alumno(alumno["idalumno"],
                                                   alumno["nomalumno"],
                                                   alumno["diralumno"],
                                                   alumno["telalumno"],
                                                   alumno["fechanacalumno"],
                                                   alumno["sexo"])
                        print("\nDatos del alumno consultado:")
                        print(alumno_consultado)
                        return
                print("No se encontró ningún alumno con ese ID.")
        except FileNotFoundError:
            print("No se encontró el archivo 'alumnos.json'.")

    def consultar_todos_alumnos(self):
        print("\n\t\t\t Opción: Consultar todos los alumnos\n")

        try:
            with open('alumnos.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not data:
                    print("No se encontró ningún alumno en el archivo 'alumnos.json'.")
                    return
                lista_alumnos = []
                for alumno_data in data:
                    alumno = Alumno(
                        alumno_data["idalumno"],
                        alumno_data["nomalumno"],
                        alumno_data["diralumno"],
                        alumno_data["telalumno"],
                        alumno_data["fechanacalumno"],
                        alumno_data["sexo"]
                    )
                    # lista_alumnos.append(str(alumno))
                    lista_alumnos.append(alumno)

                # Imprimir la lista de objetos alumno
                print("Datos de alumnos: ")
                for alumno in lista_alumnos:
                    print(alumno)
                if len(lista_alumnos) == 1:
                    print(f"\nHay un total de {len(lista_alumnos)} alumno en el fichero.")
                elif len(lista_alumnos) > 1:
                    print(f"\nHay un total de {len(lista_alumnos)} alumnos en el fichero.")



        except FileNotFoundError:
            print("No se encontró el archivo 'alumnos.json'.")

    def menu_alumnos(self):
        while True:
            print("""
            PROGRAMA GESTIÓN INSTITUTO

            \tGestión de alumnos
            \t=================

            1) Insertar alumno
            2) Eliminar alumno
            3) Consultar alumno
            4) Consultar todos los alumnos
            5) Volver
            """)
            opcion = input("\t\t\t\tOpción: ")
            if opcion == "1":
                self.insertar_alumno()
            elif opcion == "2":
                self.eliminar_alumno()
            elif opcion == "3":
                self.consultar_alumno()
            elif opcion == "4":
                self.consultar_todos_alumnos()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")


class Modulo:
    def __init__(self, idmodulo, nommodulo, nomprofesor, curso, creditos):
        self.idmodulo = idmodulo
        self.nommodulo = nommodulo
        self.nomprofesor = nomprofesor
        self.curso = curso
        self.creditos = creditos

    def __str__(self):
        return f"Modulo(id:{self.idmodulo}, nom_modulo:{self.nommodulo}, nom_profesor:{self.nomprofesor}, curso:{self.curso}, creditos:{self.creditos})"

    def a_tupla(self):
        return (self.idmodulo, self.nommodulo, self.nomprofesor, self.curso, self.creditos)


class GestionModulos:
    def __init__(self):
        load_dotenv()
        rootpassword = os.getenv("CONTRASEÑA")
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password=rootpassword,
            database="General"
        )
        self.cursor = self.db.cursor()

    def insertar_modulo(self):
        print("\n\t\t\t Opción: Insertar módulo\n")

        idmodulo = input("Id del módulo: ")
        nommodulo = input("Nombre del módulo: ")
        nomprofesor = input("Nombre del profesor: ")
        curso = input("Curso: ")
        creditos = input("Créditos: ")

        modulo = Modulo(idmodulo, nommodulo, nomprofesor, curso, creditos)

        sql_insert = """
        INSERT INTO Modulos (idmodulo, nommodulo, nomprofesor, curso, creditos)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = modulo.a_tupla()
        self.cursor.execute(sql_insert, values)
        self.db.commit()
        print(f"\n{str(self.cursor.rowcount)} módulo insertado en el fichero.")

    def eliminar_modulo(self):
        print("\n\t\t\t Opción: Eliminar módulo\n")
        id_eliminar = input("Id del módulo: ")

        try:
            sql_delete = "DELETE FROM Modulos WHERE idmodulo = %s"
            self.cursor.execute(sql_delete, (id_eliminar,))
            self.db.commit()
            print(f"\n{str(self.cursor.rowcount)} módulo eliminado del fichero.")
        except mysql.connector.Error as err:
            print("Error al eliminar el módulo:", err)

    def consultar_modulo(self):
        print("\n\t\t\t Opción: Consultar módulo\n")
        id_consultar = input("Id del módulo: ")

        try:
            sql_select = "SELECT * FROM Modulos WHERE idmodulo = %s"
            self.cursor.execute(sql_select, (id_consultar,))
            row = self.cursor.fetchone()
            if not row:
                print("No se encontró ningún módulo con ese ID.")
                return

            modulo = Modulo(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )
            print("\nDatos del módulo consultado:")
            print(modulo)

        except mysql.connector.Error as err:
            print("Error al consultar el módulo:", err)

    def consultar_todos_modulos(self):
        print("\n\t\t\t Opción: Consultar todos los módulos\n")

        try:
            sql_select = "SELECT * FROM Modulos"
            self.cursor.execute(sql_select)
            rows = self.cursor.fetchall()
            if not rows:
                print("No se encontró ningún módulo en la tabla 'Modulos'.")
                return

            lista_modulos = []
            for row in rows:
                modulo = Modulo(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
                lista_modulos.append(modulo)

            print("Datos de los módulos: ")
            for modulo in lista_modulos:
                print(modulo)
            # print(lista_modulos)
            if len(lista_modulos) == 1:
                print(f"\nHay un total de {len(lista_modulos)} modulo en el fichero.")
            elif len(lista_modulos) > 1:
                print(f"\nHay un total de {len(lista_modulos)} modulos en el fichero.")

        except mysql.connector.Error as err:
            print("Error al consultar los módulos:", err)

    def menu_modulos(self):
        while True:
            print("""
            PROGRAMA GESTIÓN INSTITUTO

            \tGestión de modulos
            \t=================

            1) Insertar modulo
            2) Eliminar modulo
            3) Consultar modulo
            4) Consultar todos los modulos
            5) Volver
            """)
            opcion = input("\t\t\t\tOpción: ")
            if opcion == "1":
                self.insertar_modulo()
            elif opcion == "2":
                self.eliminar_modulo()
            elif opcion == "3":
                self.consultar_modulo()
            elif opcion == "4":
                self.consultar_todos_modulos()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")


class Trabajo:
    def __init__(self, idalumno, idmodulo, trimestre, trabajo, nota):
        self.idalumno = idalumno
        self.idmodulo = idmodulo
        self.trimestre = trimestre
        self.trabajo = trabajo
        self.nota = nota

    def __str__(self):
        return f"Trabajo(idalumno: {self.idalumno}, idmodulo: {self.idmodulo}, trimestre: {self.trimestre}, trabajo: {self.trabajo}, nota: {self.nota})"

class GestionTrabajo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["General"]
        self.collection = self.db["Trabajos"]

    def insertar_trabajo(self):
        print("\n\t\t\t Opción: Insertar trabajo\n")
        idalumno = input("Id del alumno: ")
        idmodulo = input("Id del módulo: ")
        trimestre = input("Trimestre: ")
        trabajo = input("Descripción del trabajo: ")
        nota = input("Nota: ")

        trabajo_doc = {
            "idalumno": idalumno,
            "idmodulo": idmodulo,
            "trimestre": trimestre,
            "trabajo": trabajo,
            "nota": nota
        }

        self.collection.insert_one(trabajo_doc)
        print("\n1 trabajo insertado en la base de datos.")

    def eliminar_trabajo(self):
        print("\n\t\t\t Opción: Eliminar trabajo\n")
        id_eliminar = input("Id del trabajo: ")

        result = self.collection.delete_one({"_id": id_eliminar})
        if result.deleted_count == 1:
            print("\n1 trabajo eliminado de la base de datos.")
        else:
            print("No se encontró ningún trabajo con ese ID.")

    def consultar_trabajo(self):
        print("\n\t\t\t Opción: Consultar trabajo\n")
        # idalumno = input("ID del alumno: ")
        # idcurso = input("ID del curso: ")
        # trimestre = input("Trimestre: ")
        idtrabajo = input("Id del trabajo: ")

        trabajos = self.collection.find({"_id": idtrabajo})
        for trabajo in trabajos:
            print(trabajo)

        trabajos_list = list(trabajos)  # Convertir el cursor en una lista de resultados

        if not trabajos_list:
            print("No se encontraron trabajos con esos criterios.")
            return []

        print("\nTrabajos encontrados: ")
        trabajos_obj_list = []
        for trabajo in trabajos_list:
            trabajo_obj = Trabajo(
                trabajo["idalumno"],
                trabajo["idmodulo"],
                trabajo["trimestre"],
                trabajo["trabajo"],
                trabajo["nota"]
            )
            trabajos_obj_list.append(trabajo_obj)
        for trabajo in trabajos_obj_list:
            print(trabajo)
        # return trabajos_list

    def consultar_todos_trabajos(self):
        print("\n\t\t\t Opción: Consultar todos los trabajos\n")

        trabajos = self.collection.find()
        if trabajos.count() == 0:
            print("No se encontró ningún trabajo en la base de datos.")
            return

        print("Datos de todos los trabajos: ")
        for trabajo in trabajos:
            print(trabajo)
        print(f"\nTotal de trabajos: {trabajos.count()}")

    def menu_trabajos(self):
        while True:
            print("""
            PROGRAMA GESTIÓN INSTITUTO

            \tGestión de trabajos
            \t=================

            1) Insertar trabajo
            2) Eliminar trabajo
            3) Consultar trabajo
            4) Consultar todos los trabajos
            5) Volver
            """)
            opcion = input("\t\t\t\tOpción: ")
            if opcion == "1":
                self.insertar_trabajo()
            elif opcion == "2":
                self.eliminar_trabajo()
            elif opcion == "3":
                self.consultar_trabajo()
            elif opcion == "4":
                self.consultar_todos_trabajos()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")


class GestionInstituto:
    def __init__(self):
        self.gestion_alumnos = GestionAlumnos()
        self.gestion_modulos = GestionModulos()
        self.gestion_trabajos = GestionTrabajo()

    def menu_principal(self):
        while True:
            print("""
            PROGRAMA GESTIÓN INSTITUTO

            \tMenú de Opciones
            \t=================

            1) Gestión de alumnos
            2) Gestión de módulos
            3) Gestión de trabajos
            4) Situación actual de un alumno
            5) Salir
            """)
            opcion = input("\t\t\t\tOpción: ")
            if opcion == "1":
                self.gestion_alumnos.menu_alumnos()
            elif opcion == "2":
                self.gestion_modulos.menu_modulos()
            elif opcion == "3":
                self.gestion_trabajos.menu_trabajos()
            # elif opcion == "4":
            #     self.consultar_todos_modulos()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")


if __name__ == '__main__':
    gestion_instituto = GestionInstituto()  # Crear una instancia de la clase GestionAlumnos
    gestion_instituto.menu_principal()
