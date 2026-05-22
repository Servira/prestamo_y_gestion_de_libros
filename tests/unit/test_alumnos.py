import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tests', 'unit'))

from base_test import BaseTest
import mysql.connector

class TestAlumnos(BaseTest):


    def test_insertar_alumno(self):
        self.cursor.execute("SELECT * FROM alumnos WHERE nie = %s", ("TEST-A01",))
        self.assertIsNone(self.cursor.fetchone())

        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-A01", "Juan", "García", "I", 1)
        )

        self.cursor.execute("SELECT nie, nombre, tramo FROM alumnos WHERE nie = %s", ("TEST-A01",))
        alumno = self.cursor.fetchone()
        self.assertEqual(alumno, ("TEST-A01", "Juan", "I"))

    def test_insertar_nie_duplicado(self):
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-A02", "Ana", "Pérez", "0", 1)
        )

        with self.assertRaises(mysql.connector.Error):
            self.cursor.execute(
                "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
                ("TEST-A02", "Otro", "Alumno", "0", 1)
            )


    def test_buscar_por_nie_existente(self):
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-A03", "María", "López", "I", 0)
        )

        self.cursor.execute("SELECT nie FROM alumnos WHERE nie = %s", ("TEST-A03",))
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

    def test_buscar_por_nie_inexistente(self):
        self.cursor.execute("SELECT * FROM alumnos WHERE nie = %s", ("NOEXISTE",))
        self.assertIsNone(self.cursor.fetchone())

        self.cursor.execute("SELECT * FROM alumnos WHERE nie = %s", ("NOEXISTE",))

        self.assertIsNone(self.cursor.fetchone())


    def test_modificar_nombre(self):
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-A04", "Pedro", "Sánchez", "0", 1)
        )
        self.cursor.execute("SELECT nombre FROM alumnos WHERE nie = %s", ("TEST-A04",))
        self.assertEqual(self.cursor.fetchone()[0], "Pedro")

        self.cursor.execute("UPDATE alumnos SET nombre = %s WHERE nie = %s", ("Pablo", "TEST-A04"))

        self.cursor.execute("SELECT nombre FROM alumnos WHERE nie = %s", ("TEST-A04",))
        self.assertEqual(self.cursor.fetchone()[0], "Pablo")

    def test_modificar_tramo(self):
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("TEST-A05", "Sofía", "Torres", "0", 1)
        )
        self.cursor.execute("SELECT tramo FROM alumnos WHERE nie = %s", ("TEST-A05",))
        self.assertEqual(self.cursor.fetchone()[0], "0")

        self.cursor.execute("UPDATE alumnos SET tramo = %s WHERE nie = %s", ("II", "TEST-A05"))

        self.cursor.execute("SELECT tramo FROM alumnos WHERE nie = %s", ("TEST-A05",))
        self.assertEqual(self.cursor.fetchone()[0], "II")

if __name__ == '__main__':
    import unittest
    unittest.main()