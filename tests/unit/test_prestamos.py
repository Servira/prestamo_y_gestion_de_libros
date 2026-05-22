import sys
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tests', 'unit'))

from base_test import BaseTest
import mysql.connector

class TestPrestamos(BaseTest):

    def setUp(self):
        super().setUp()
        self.cursor.execute(
            "INSERT INTO materias (nombre, departamento) VALUES (%s,%s)",
            ("Materia Test", "Depto Test")
        )
        self.cursor.execute("SELECT id FROM materias WHERE nombre = %s", ("Materia Test",))
        id_materia = self.cursor.fetchone()[0]
        self.cursor.execute(
            "INSERT INTO cursos (curso, nivel) VALUES (%s,%s)", ("TEST-A", "1º Test")
        )
        self.cursor.execute(
            "INSERT INTO libros (isbn, titulo, autor, numero_ejemplares, id_materia, id_curso) VALUES (%s,%s,%s,%s,%s,%s)",
            ("TEST-ISBN", "Libro Test", "Autor Test", 10, id_materia, "TEST-A")
        )
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-P01", "Juan", "García", "I", 1)
        )

    def test_asignar_libro(self):
        self.cursor.execute("SELECT * FROM alumnoscursoslibros WHERE nie = %s", ("TEST-P01",))
        self.assertIsNone(self.cursor.fetchone())

        self.cursor.execute(
            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-P01", "TEST-A", "TEST-ISBN", date.today(), "P")
        )

        self.cursor.execute("SELECT estado FROM alumnoscursoslibros WHERE nie = %s", ("TEST-P01",))
        self.assertEqual(self.cursor.fetchone()[0], "P")

    def test_asignar_libro_alumno_inexistente(self):
        self.cursor.execute("SELECT * FROM alumnos WHERE nie = %s", ("NOEXISTE",))
        self.assertIsNone(self.cursor.fetchone())

        with self.assertRaises(mysql.connector.Error):
            self.cursor.execute(
                "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s,%s,%s,%s,%s)",
                ("NOEXISTE", "TEST-A", "TEST-ISBN", date.today(), "P")
            )

    def test_registrar_devolucion(self):
        self.cursor.execute(
            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-P01", "TEST-A", "TEST-ISBN", date.today(), "P")
        )
        self.cursor.execute("SELECT estado FROM alumnoscursoslibros WHERE nie = %s", ("TEST-P01",))
        self.assertEqual(self.cursor.fetchone()[0], "P")

        self.cursor.execute(
            "UPDATE alumnoscursoslibros SET estado = 'D', fecha_devolucion = %s WHERE nie = %s",
            (date.today(), "TEST-P01")
        )

        self.cursor.execute("SELECT estado FROM alumnoscursoslibros WHERE nie = %s", ("TEST-P01",))
        self.assertEqual(self.cursor.fetchone()[0], "D")

    def test_cerrar_prestamo_con_pendientes(self):
        self.cursor.execute(
            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-P01", "TEST-A", "TEST-ISBN", date.today(), "P")
        )

        self.cursor.execute(
            "SELECT COUNT(*) FROM alumnoscursoslibros WHERE nie = %s AND estado = 'P'", ("TEST-P01",)
        )
        pendientes = self.cursor.fetchone()[0]

        self.assertGreater(pendientes, 0)

    def test_cerrar_prestamo_sin_pendientes(self):
        self.cursor.execute(
            "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, fecha_devolucion, estado) VALUES (%s,%s,%s,%s,%s,%s)",
            ("TEST-P01", "TEST-A", "TEST-ISBN", date.today(), date.today(), "D")
        )

        self.cursor.execute(
            "SELECT COUNT(*) FROM alumnoscursoslibros WHERE nie = %s AND estado = 'P'", ("TEST-P01",)
        )
        pendientes = self.cursor.fetchone()[0]

        self.assertEqual(pendientes, 0)

if __name__ == '__main__':
    import unittest

    unittest.main()