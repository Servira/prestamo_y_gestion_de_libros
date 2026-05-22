import unittest
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP_DIR = os.path.join(BASE_DIR, 'app')
sys.path.insert(0, APP_DIR)

from db import conectar

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.conexion = conectar()
        self.assertIsNotNone(self.conexion, "No se pudo conectar a la base de datos")
        self.cursor = self.conexion.cursor()
        self.conexion.autocommit = False

    def tearDown(self):
        try:
            self.conexion.rollback()
        finally:
            self.cursor.close()
            self.conexion.close()