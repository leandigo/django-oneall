# -*- coding: utf-8 -*-
from django.test import TestCase

from pyoneall import OneAll


class TestOneAll(TestCase):
    def setUp(self):
        self._oa = OneAll('py3tests', 'bf3a6a88-5300-4880-8982-acabe89f9cd1', '35fc1a5e-fa81-4297-a0e6-723bcca838ee')
