import sys
import os
import json
import csv
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tests', 'unit'))

from base_test import BaseTest

class TestBackup(BaseTest):

    def setUp(self):
        super().setUp()
        self.cursor.execute(
            "INSERT INTO materias (nombre, departamento) VALUES (%s,%s)",
            ("Materia Backup", "Depto Backup")
        )

    def test_exportar_json(self):
        self.cursor.execute("SELECT * FROM materias WHERE nombre = %s", ("Materia Backup",))
        columnas = [d[0] for d in self.cursor.description]
        filas = self.cursor.fetchall()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump({"materias": [dict(zip(columnas, fila)) for fila in filas]}, f, default=str)
            nombre = f.name

        with open(nombre, encoding='utf-8') as f:
            datos = json.load(f)
        self.assertIn("materias", datos)
        self.assertGreater(len(datos["materias"]), 0)
        os.unlink(nombre)

    def test_exportar_csv(self):
        self.cursor.execute("SELECT * FROM materias WHERE nombre = %s", ("Materia Backup",))
        columnas = [d[0] for d in self.cursor.description]
        filas = self.cursor.fetchall()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(filas)
            nombre = f.name

        with open(nombre, encoding='utf-8') as f:
            filas_leidas = list(csv.reader(f))
        self.assertEqual(filas_leidas[0], columnas)
        self.assertGreater(len(filas_leidas), 1)
        os.unlink(nombre)

    def test_exportar_sql(self):
        self.cursor.execute("SELECT * FROM materias WHERE nombre = %s", ("Materia Backup",))
        filas = self.cursor.fetchall()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False, encoding='utf-8') as f:
            for fila in filas:
                valores = ", ".join(f"'{v}'" if v is not None else "NULL" for v in fila)
                f.write(f"INSERT INTO materias VALUES ({valores});\n")
            nombre = f.name

        with open(nombre, encoding='utf-8') as f:
            contenido = f.read()
        self.assertIn("INSERT INTO materias", contenido)
        self.assertIn("Materia Backup", contenido)
        os.unlink(nombre)

if __name__ == '__main__':
    import unittest

    unittest.main()