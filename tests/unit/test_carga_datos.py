import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tests', 'unit'))

from base_test import BaseTest

class TestCargaDatos(BaseTest):

    def test_insertar_materia(self):
        self.cursor.execute("SELECT * FROM materias WHERE nombre = %s", ("Materia Carga",))
        self.assertIsNone(self.cursor.fetchone())

        self.cursor.execute(
            "INSERT INTO materias (nombre, departamento) VALUES (%s,%s)",
            ("Materia Carga", "Depto Carga")
        )

        self.cursor.execute("SELECT nombre FROM materias WHERE nombre = %s", ("Materia Carga",))
        self.assertIsNotNone(self.cursor.fetchone())

    def test_insertar_curso(self):
        self.cursor.execute("SELECT * FROM cursos WHERE curso = %s", ("CARGA-A",))
        self.assertIsNone(self.cursor.fetchone())

        self.cursor.execute(
            "INSERT INTO cursos (curso, nivel) VALUES (%s,%s)", ("CARGA-A", "1º Carga")
        )

        self.cursor.execute("SELECT curso FROM cursos WHERE curso = %s", ("CARGA-A",))
        self.assertIsNotNone(self.cursor.fetchone())

    def test_parsear_linea_csv_correcta(self):
        linea = '"García López, Juan","12345678A","001","01/09/2024","","2024/2025","","","","","","","","","Favorable","","S","TramoI",""'

        campos = linea.strip().split(",")
        alumno_raw = campos[0].strip('"')
        nie = campos[1].strip('"')
        matriculado = campos[16].strip('"')
        tramo_raw = campos[17].strip('"')
        partes = alumno_raw.split(",")
        apellidos = partes[0].strip()
        nombre = partes[1].strip()
        tramo = "I" if tramo_raw == "TramoI" else ("II" if tramo_raw == "TramoII" else "0")

        self.assertEqual(nie, "12345678A")
        self.assertEqual(nombre, "Juan")
        self.assertEqual(apellidos, "García López")
        self.assertEqual(matriculado, "S")
        self.assertEqual(tramo, "I")

    def test_parsear_alumno_sin_beca(self):
        tramo_raw = ""

        tramo = "I" if tramo_raw == "TramoI" else ("II" if tramo_raw == "TramoII" else "0")

        self.assertEqual(tramo, "0")

    def test_parsear_alumno_no_matriculado(self):
        matriculado = "N"

        self.assertNotEqual(matriculado.upper(), "S")

    def test_vaciar_tabla_alumnos(self):
        self.cursor.execute(
            "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s,%s,%s,%s,%s)",
            ("CARGA-01", "Test", "Vaciar", "0", 1)
        )
        self.cursor.execute("SELECT COUNT(*) FROM alumnos WHERE nie = %s", ("CARGA-01",))
        self.assertEqual(self.cursor.fetchone()[0], 1)

        self.cursor.execute("DELETE FROM alumnos WHERE nie = %s", ("CARGA-01",))

        self.cursor.execute("SELECT COUNT(*) FROM alumnos WHERE nie = %s", ("CARGA-01",))
        self.assertEqual(self.cursor.fetchone()[0], 0)

if __name__ == '__main__':
    import unittest

    unittest.main()