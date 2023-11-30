"""
Enrique Martín <emartinm@ucm.es> 2023
Tests de unidad para comprobar el API REST sobre asignaturas.
ES IMPRESCINDIBLE QUE EL SERVIDOR FLASK ESTÉ EJECUTÁNDOSE ANTES DE LANZAR LOS TESTS

lanzar TODOS los tests desde el terminal:
$ python -m unittest tests.TestREST

Lanzar un test concreto desde el terminal
$ python -m unittest tests.TestREST.test_get_horario_inexistente
"""

import unittest
import requests
import copy

HOST = "http://127.0.0.1:5000"

ASIGS = [
    {"nombre": "GIW", "numero_alumnos": 10, "horario": [{"dia": "lunes", "hora_inicio": 9, "hora_final": 10}]},
    {"nombre": "KLO", "numero_alumnos": 30, "horario": [{"dia": "martes", "hora_inicio": 11, "hora_final": 12}]},
    {"nombre": "POL", "numero_alumnos": 60, "horario": [{"dia": "miercoles", "hora_inicio": 12, "hora_final": 14}]},
    {"nombre": "SGD", "numero_alumnos": 75, "horario": [{"dia": "jueves", "hora_inicio": 16, "hora_final": 17}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18, "hora_final": 20}]},
]

BAD_ASIGS = [
    dict(),
    {"nombre": "ABD"},
    {"numero_alumnos": 60},
    {"horario": [{"dia": "miercoles", "hora_inicio": 16, "hora_final": 17}]},
    {"nombre": "JUL", "numero_alumnos": 90, "horario": [{"dia": "miercoles", "hora_inicio": 16, "hora_final": 17}],
     "campo_adicional": 28},
    {"nombre": 3, "numero_alumnos": 20, "horario": [{"dia": "miercoles", "hora_inicio": 16, "hora_final": 17}]},
    {"nombre": "FAL", "numero_alumnos": "hola", "horario": [{"dia": "miercoles", "hora_inicio": 16, "hora_final": 17}]},
    # Horario mal formado
    {"nombre": "POL", "numero_alumnos": 12, "horario": 58},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": 5, "hora_inicio": 18, "hora_final": 20}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": "seis", "hora_final": 20}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18, "hora_final": "ocho"}]}, 
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": "", "hora_final": 20}]},  
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18, "hora_final": True}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18, "hora_final": False}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"day": "viernes", "hora_inicio": 18, "hora_final": 8}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"hora_inicio": 18, "hora_final": 8}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicial": 18, "hora_final": 20}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_final": 20}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18, "hora_finalizacion": 20}]},
    {"nombre": "OMG", "numero_alumnos": 90, "horario": [{"dia": "viernes", "hora_inicio": 18}]},        

]

PATCH = [
    {"nombre": "DAC"},
    {"numero_alumnos": 68},
    {"horario": [{"dia": "martes", "hora_inicio": 18, "hora_final": 21}]}
]

BAD_PATCH = [
    dict(),
    {"nombre": 67},
    {"numero_alumnos": "doscientos"},
    {"horario": 9.13},
    {"campo_incorrecto": "sí"},
    {"nombre": "pepe", "numero_alumnos": 20}
]


def rutas_asig_gte(list_asignturas, umbral):
    """Devuelve el conjunto de rutas de las asignaturas que tienen más o igual número de alumnos"""
    gte = filter(lambda x: x['numero_alumnos'] >= umbral, list_asignturas)
    return list(map(lambda x: f"/asignaturas/{x['id']}", gte))


def rutas_paginado(list_asignturas, per_page, page):
    """Devuelve el conjunto de rutas de las asignaturas considerando la paginación"""
    asigs = list_asignturas[(page - 1) * per_page:page * per_page]
    return list(map(lambda x: f"/asignaturas/{x['id']}", asigs))


class TestREST(unittest.TestCase):
    """Tests a ejecutar sobre el servidor con el API REST"""

    def borra_e_inserta(self, list_asignaturas):
        """Borra todas las asignaturas e inserta las asignaturas de 'list_asignaturas' una por una
        Devuelve una lista de asignaturas donde cada una ha sido extendida con el identificador"""
        requests.delete(f'{HOST}/asignaturas')
        ids = list()
        for asig in list_asignaturas:
            r = requests.post(f'{HOST}/asignaturas', json=asig)
            self.assertEqual(r.status_code, 201)
            self.assertEqual(len(r.json()), 1)
            self.assertTrue('id' in r.json())
            new_asig = copy.deepcopy(asig)
            new_asig['id'] = r.json()['id']
            ids.append(new_asig)
        return ids

    def test_delete_asignaturas(self):
        """Código de retorno de DELETE /asignaturas"""
        r = requests.delete(f'{HOST}/asignaturas')
        self.assertEqual(r.status_code, 204)

    def test_delete_get_asignaturas(self):
        """Después de borrar /asignaturas, el siguiente GET no devuelve ninguna"""
        requests.delete(f'{HOST}/asignaturas')
        r = requests.get(f'{HOST}/asignaturas')
        self.assertEqual(r.json()['asignaturas'], [])

    def test_post_get_asignaturas(self):
        """Añadir varias asignaturas después de borrarlas todas: el código de retorno es correcto, el JSON
        devuelto tiene únicamente la clave 'id' y el siguiente GET devuelve URL a todas las asignaturas"""
        added = self.borra_e_inserta(ASIGS)

        r = requests.get(f'{HOST}/asignaturas')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['asignaturas']), len(ASIGS))
        self.assertEqual(set(r.json()['asignaturas']), {f"/asignaturas/{asig['id']}" for asig in added})

    def test_post_get_filtro(self):
        """Añadir varias asignaturas después de borrarlas todas: el siguiente GET devuelve correctamente
        las asignaturas teniendo en cuenta el filtro"""
        added = self.borra_e_inserta(ASIGS)

        r = requests.get(f'{HOST}/asignaturas?alumnos_gte=5')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['asignaturas']), len(ASIGS))

        r = requests.get(f'{HOST}/asignaturas?alumnos_gte=1000')
        self.assertEqual(r.status_code, 206)
        self.assertEqual(len(r.json()['asignaturas']), 0)

        for umbral in range(10, 100, 10):
            # Genera peticiones con umbrales 10--100 de 10 en 10
            r = requests.get(f'{HOST}/asignaturas?alumnos_gte={umbral}')
            expected = rutas_asig_gte(added, umbral)
            expected_code = 200 if len(expected) == len(added) else 206
            self.assertEqual(r.status_code, expected_code)
            self.assertEqual(set(r.json()['asignaturas']), set(expected))

    def test_paginado(self):
        """Añadir varias asignaturas después de borrarlas y obtenerlas con paginación"""
        added = self.borra_e_inserta(ASIGS)

        for page in range(1, 10):
            for per_page in range(1, 10):
                r = requests.get(f'{HOST}/asignaturas?per_page={per_page}&page={page}')
                expected = set(rutas_paginado(added, per_page, page))
                expected_code = 200 if len(expected) == len(added) else 206
                self.assertEqual(r.status_code, expected_code)
                self.assertEqual(set(r.json()['asignaturas']), expected)

    def test_paginado_filtro(self):
        """Añadir varias asignaturas después de borrarlas y obtenerlas con paginación" y filtrado"""
        added = self.borra_e_inserta(ASIGS)

        for page in range(1, 10):
            for per_page in range(1, 10):
                for umbral in range(10, 150, 10):
                    r = requests.get(f'{HOST}/asignaturas?per_page={per_page}&page={page}&alumnos_gte={umbral}')
                    expected = set(rutas_paginado(
                        list(filter(lambda x: x['numero_alumnos'] >= umbral, added)), per_page, page))
                    expected_code = 200 if len(expected) == len(added) else 206
                    self.assertEqual(r.status_code, expected_code)
                    self.assertEqual(set(r.json()['asignaturas']), expected)

    def test_post_incorrecto(self):
        """Las peticiones POST con asignaturas mal formadas devuelven 400"""
        self.borra_e_inserta(ASIGS)
        for asig in BAD_ASIGS:
            r = requests.post(f'{HOST}/asignaturas', json=asig)
            self.assertEqual(r.status_code, 400)

    def test_post_get_asignatura(self):
        """Después de añadir las asignaturas, los GET individuales son correctos"""
        self.borra_e_inserta([])
        for ident in range(10):
            r = requests.get(f'{HOST}/asignaturas/{ident}')
            self.assertEqual(r.status_code, 404)

        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            r = requests.get(f'{HOST}/asignaturas/{asig["id"]}')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), asig)

    def test_delete_asignatura(self):
        """Borra asignaturas"""
        self.borra_e_inserta([])
        for ident in range(10):
            r = requests.delete(f'{HOST}/asignaturas/{ident}')
            self.assertEqual(r.status_code, 404)

        for i in range(len(ASIGS)):
            added = self.borra_e_inserta(ASIGS)
            ident = added[i]['id']
            r = requests.delete(f'{HOST}/asignaturas/{ident}')
            self.assertEqual(r.status_code, 204)
            r = requests.get(f'{HOST}/asignaturas')
            self.assertFalse(f'{HOST}/asignaturas/{ident}' in r.json()['asignaturas'])

    def test_put_asignatura_inexistente(self):
        """Reemplazar asignaturas inexistentes debe devolver 404"""
        self.borra_e_inserta([])

        data = {"nombre": "TEST",
                "numero_alumnos": 55,
                "horario": [{"dia": "martes", "hora_inicio": 18, "hora_final": 19}]}
        for ident in range(10):
            r = requests.put(f'{HOST}/asignaturas/{ident}', json=data)
            self.assertEqual(r.status_code, 404)

    def test_put_asignatura(self):
        """Obtener asignaturas reemplazadas obtiene los datos nuevos"""
        added = self.borra_e_inserta(ASIGS)

        data = {"nombre": "TEST",
                "numero_alumnos": 55,
                "horario": [{"dia": "martes", "hora_inicio": 18, "hora_final": 19}]}
        expected = copy.deepcopy(data)
        for asig in added:
            r = requests.put(f'{HOST}/asignaturas/{asig["id"]}', json=data)
            self.assertEqual(r.status_code, 200)
            r = requests.get(f'{HOST}/asignaturas/{asig["id"]}')
            self.assertEqual(r.status_code, 200)
            expected['id'] = asig['id']
            self.assertEqual(r.json(), expected)

    def test_put_asignatura_mal_formada(self):
        """Reemplazar una asignatura usando datos mal formados debe obtener 404 si no existe y 400 si existe"""
        self.borra_e_inserta([])
        for ident in range(10):
            for data in BAD_ASIGS:
                r = requests.put(f'{HOST}/asignaturas/{ident}', json=data)
                self.assertEqual(r.status_code, 404)

        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            for data in BAD_ASIGS:
                r = requests.put(f'{HOST}/asignaturas/{asig["id"]}', json=data)
                self.assertEqual(r.status_code, 400)

    def test_patch_asignatura_inexistente(self):
        """Actualizar un campo de una asignatura que no existe debe obtener 404"""
        self.borra_e_inserta([])

        data = {"nombre": "TEST"}
        for ident in range(10):
            r = requests.patch(f'{HOST}/asignaturas/{ident}', json=data)
            self.assertEqual(r.status_code, 404)

    def test_patch_asignatura(self):
        """Actualizar un campo de una asignatura que y luego obtenerla debe devolver los datos actualizados"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            for patch in PATCH:
                r = requests.get(f'{HOST}/asignaturas/{asig["id"]}')
                original = r.json()
                r = requests.patch(f'{HOST}/asignaturas/{asig["id"]}', json=patch)
                self.assertEqual(r.status_code, 200)
                r = requests.get(f'{HOST}/asignaturas/{asig["id"]}')
                self.assertEqual(r.status_code, 200)
                original.update(patch)
                self.assertEqual(r.json(), original)

    def test_patch_asignatura_mal_formada(self):
        """Actualizar un campo de una asignatura usando datos mal formados obtiene 404 si la asignatura
        no existe, y 400 si existe"""
        self.borra_e_inserta([])
        for ident in range(10):
            for data in BAD_PATCH:
                r = requests.patch(f'{HOST}/asignaturas/{ident}', json=data)
                self.assertEqual(r.status_code, 404)

        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            for data in BAD_PATCH:
                r = requests.put(f'{HOST}/asignaturas/{asig["id"]}', json=data)
                self.assertEqual(r.status_code, 400)

    def test_get_horario_inexistente(self):
        """Obtener el horario de una asignatura inexistente devuelve 404"""
        self.borra_e_inserta([])
        for ident in range(10):
            r = requests.get(f'{HOST}/asignaturas/{ident}/horario')
            self.assertEqual(r.status_code, 404)

    def test_get_horario(self):
        """Obtener el horario de una asignatura devuelve el valor esperado"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            r = requests.get(f'{HOST}/asignaturas/{asig["id"]}/horario')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.json()), 1)
            self.assertTrue('horario' in r.json())
            self.assertEqual(r.json()['horario'], asig['horario'])
