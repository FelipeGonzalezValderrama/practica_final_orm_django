from django.test import TestCase
from django.urls import reverse
from .models import Laboratorio

#test modelos en postgresql
class LaboratorioModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Laboratorio.objects.create(
            nombre="Laboratorio de Prueba",
            ciudad="Ciudad de Prueba",
            pais="País de Prueba",
        )

    def test_datos_en_base_de_datos_simulada(self):
        laboratorio = Laboratorio.objects.get(nombre="Laboratorio de Prueba")
        self.assertEqual(laboratorio.ciudad, "Ciudad de Prueba")
        self.assertEqual(laboratorio.pais, "País de Prueba")

# test confirma respuesta HTTP 200 para laboratorio
class LaboratorioURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Laboratorio.objects.create(
            nombre="Laboratorio de Prueba",
            ciudad="Ciudad de Prueba",
            pais="País de Prueba",
        )

    def test_respuesta_http_200(self):
        laboratorio = Laboratorio.objects.get(nombre="Laboratorio de Prueba")
        url = reverse("lista_laboratorios") 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

#test uso reverse para obtener respuesta http 200
class LaboratorioPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Laboratorio.objects.create(
            nombre="Laboratorio de Prueba",
            ciudad="Ciudad de Prueba",
            pais="País de Prueba",
        )

    def test_pagina_laboratorio(self):
        laboratorio = Laboratorio.objects.get(nombre="Laboratorio de Prueba")
        url = reverse("lista_laboratorios")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "laboratorio/lista_laboratorios.html")  
        self.assertContains(response, "Laboratorio de Prueba")
        self.assertContains(response, "Ciudad de Prueba")
        self.assertContains(response, "País de Prueba")

