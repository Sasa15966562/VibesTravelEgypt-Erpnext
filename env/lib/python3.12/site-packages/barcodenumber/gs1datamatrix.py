# -*- encoding:utf-8 -*-
# This file is part of barcodenumber. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


__all__ = ['ProductCode', 'ExpirationDate', 'Lot', 'SerialNumber']

SEPARATOR = '\x1d'
HUMAN_SEPARATOR = '\xc7'


class Element(object):
    _ai = None
    _type = None
    _lenght = None

    @classmethod
    def extract(cls, item):

        def reverse_replace(s, old, new, count):
            return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]

        # if 'ai' isn't at the beginning of the word then return
        if item.find(cls._ai):
            return
        _, remainder = item.split(cls._ai, 1)
        element = remainder[:cls._lenght]
        if cls._type == 'variable':
            if HUMAN_SEPARATOR in element and SEPARATOR not in element:
                if not (element[-1] == HUMAN_SEPARATOR
                        and element.count(HUMAN_SEPARATOR) == 1):
                    element = reverse_replace(element, HUMAN_SEPARATOR,
                        SEPARATOR, 1)
            if SEPARATOR in element:
                element, _ = element.split(SEPARATOR, 1)
        return element


class ProductCode(Element):
    _ai = '01'
    _type = 'fixed'
    _lenght = 14


class ExpirationDate(Element):
    _ai = '17'
    _type = 'fixed'
    _lenght = 6


class Lot(Element):
    _ai = '10'
    _type = 'variable'
    _lenght = 20


class SerialNumber(Element):
    _ai = '21'
    _type = 'variable'
    _lenght = 20
