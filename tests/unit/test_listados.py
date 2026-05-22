import sys
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tests', 'unit'))

from base_test import BaseTest

class TestListados(BaseTest):

    def setUp(self):
        super().setUp()
        self.cursor.execute(
            "INSERT INTO materias (nombre, departamento) VALUES (%s,%s)",
            ("Materia Lista", "Depto Lista")
        )
        self.cursor.execute("SELECT id FROM materias WHERE nombre = %s", ("Materia Lista",))
        id_materia = self.cursor.fetchone()[0]
        self.cursor.execute(
            "INSERT INTO cursos (curso, nivel) VALUES (%s,%s)", ("LIST-A", "1º Lista")
        )
        self.cursor.execute(
            "INSERT INTO libros (isbn, titulo, autor, numero_ejemplares, id_materia, id_curso) VALUES (%s,%s,%s,%s,%s,%s)",
            ("LIST-ISBN", "Libro Lista", "Autor Lista", 5, id_materia, "LIST-A")
        )
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("LIST-01", "Ana", "García", "I", 1)
        )
        self.cursor.execute(
            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s,%s,%s,%s,%s)",
            ("LIST-01", "LIST-A", "LIST-ISBN", date.today(), "P")
        )

    def test_listado_alumnos(self):
        self.cursor.execute("SELECT * FROM alumnos WHERE nie = %s", ("LIST-01",))
        alumnos = self.cursor.fetchall()

        self.assertGreater(len(alumnos), 0)


    def test_listado_libros(self):
        self.cursor.execute("SELECT * FROM libros WHERE isbn = %s", ("LIST-ISBN",))
        libros = self.cursor.fetchall()

        self.assertGreater(len(libros), 0)

    def test_listado_prestamos_activos(self):
        self.cursor.execute(
            "SELECT * FROM alumnoscursoslibros WHERE nie = %s AND estado = 'P'", ("LIST-01",)
        )
        prestamos = self.cursor.fetchall()

        self.assertGreater(len(prestamos), 0)
        self.assertEqual(prestamos[0][5], "P")

    def test_listado_por_curso(self):
        self.cursor.execute(
            "SELECT nie FROM alumnoscursoslibros WHERE curso = %s", ("LIST-A",)
        )
        nies = [f[0] for f in self.cursor.fetchall()]

        self.assertIn("LIST-01", nies)

    def test_listado_por_materia(self):
        self.cursor.execute(
            "SELECT l.isbn FROM libros l JOIN materias m ON l.id_materia = m.id WHERE m.nombre LIKE %s",
            ("%Materia Lista%",)
        )
        isbns = [f[0] for f in self.cursor.fetchall()]

        self.assertIn("LIST-ISBN", isbns)

if __name__ == '__main__':
    import unittest

    unittest.main()