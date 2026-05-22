import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP_DIR = os.path.join(BASE_DIR, 'app')
UNIT_DIR = os.path.join(BASE_DIR, 'tests', 'unit')

sys.path.insert(0, APP_DIR)
sys.path.insert(0, UNIT_DIR)

from base_test import BaseTest
from db import conectar, cerrar

class TestDb(BaseTest):

    def test_conexion_exitosa(self):
        conexion = None
        self.assertIsNone(conexion)

        conexion = conectar()

        self.assertIsNotNone(conexion)
        self.assertTrue(conexion.is_connected())
        conexion.close()

    def test_cerrar_conexion(self):
        conexion = conectar()
        cursor = conexion.cursor()
        self.assertTrue(conexion.is_connected())

        cerrar(conexion, cursor)

        self.assertFalse(conexion.is_connected())

    def test_tabla_alumnos_existe(self):
        self.cursor.execute("SHOW TABLES LIKE 'alumnos'")
        antes = self.cursor.fetchone()
        self.assertIsNotNone(antes)

        self.cursor.execute("SELECT COUNT(*) FROM alumnos")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

    def test_tabla_cursos_existe(self):
        self.cursor.execute("SHOW TABLES LIKE 'cursos'")
        antes = self.cursor.fetchone()
        self.assertIsNotNone(antes)

        self.cursor.execute("SELECT COUNT(*) FROM cursos")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

    def test_tabla_libros_existe(self):
        self.cursor.execute("SHOW TABLES LIKE 'libros'")
        antes = self.cursor.fetchone()
        self.assertIsNotNone(antes)

        self.cursor.execute("SELECT COUNT(*) FROM libros")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

    def test_tabla_materias_existe(self):
        self.cursor.execute("SHOW TABLES LIKE 'materias'")
        antes = self.cursor.fetchone()
        self.assertIsNotNone(antes)

        self.cursor.execute("SELECT COUNT(*) FROM materias")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

    def test_tabla_alumnoscursoslibros_existe(self):
        self.cursor.execute("SHOW TABLES LIKE 'alumnoscursoslibros'")
        antes = self.cursor.fetchone()
        self.assertIsNotNone(antes)

        self.cursor.execute("SELECT COUNT(*) FROM alumnoscursoslibros")
        resultado = self.cursor.fetchone()

        self.assertIsNotNone(resultado)

if __name__ == '__main__':
    import unittest
    unittest.main()