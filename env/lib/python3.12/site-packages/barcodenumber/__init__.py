# This file is part of barcodenumber. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
'''
Check and decode the barcodes
'''
from stdnum import ean, isbn
import re
from . import gs1datamatrix

__version__ = '0.5.0'


def barcodes():
    '''
    Return the list of barcodes that have check function
    '''
    res = [x.replace('check_code_', '').upper() for x in globals()
        if x.startswith('check_code_')]
    res.sort()
    return res


def is_pair(x):
    return not x % 2


def check_code_code39(number):
    '''
    Check code39 code.
    '''
    matches = re.findall(r"[A-Z\d*\s\-\$%\./\+]", number)
    return len(number) == len(matches)


def check_code_ean(number):
    '''
    Check ean code.
    '''
    return ean.is_valid(number) and len(number) == 12


def check_code_ean13(number):
    '''
    Check ean13 code.
    '''
    return ean.is_valid(number) and len(number) == 13


def check_code_ean8(number):
    '''
    Check ean8 code.
    '''
    return ean.is_valid(number) and len(number) == 8


def check_code_gs1(number):
    '''
    Check gs1 code.
    '''
    return True


def check_code_gtin(number):
    '''
    Check gtin code.
    '''
    return ean.is_valid(number) and len(number) == 13


def check_code_gtin14(number):
    '''
    Check gtin14 code.
    '''
    return ean.is_valid(number) and len(number) == 14


def check_code_isbn(number):
    '''
    Check isbn code.
    '''
    return isbn.is_valid(number)


def check_code_isbn10(number):
    '''
    Check isbn10 code.
    '''
    return isbn.isbn_type(number) == 'ISBN10'


def check_code_isbn13(number):
    '''
    Check isbn13 code.
    '''
    return isbn.isbn_type(number) == 'ISBN13'


def check_code_issn(number):
    '''
    Check issn code.
    '''
    return True


def check_code_jan(number):
    '''
    Check jan code.
    '''
    return True


def check_code_pzn(number):
    '''
    Check pzn code.
    '''
    return True


def check_code_upc(number):
    '''
    Check upc code.
    '''
    return ean.is_valid(number) and len(number) == 12


def check_code_upca(number):
    '''
    Check upca code.
    '''
    return True


def check_code_gs1_datamatrix(number):
    '''
    Check GS1 datamatrix
    '''
    gtin = gs1datamatrix.ProductCode.extract(number)
    # GTIN14 will never start with a zero.
    gtin_is_valid = ((check_code_gtin14(gtin)
            or check_code_gtin(gtin.lstrip('0'))) if gtin else False)
    return True if gtin_is_valid else False


def check_code(code, number):
    '''
    Check barcode
    '''
    try:
        checker = globals()['check_code_%s' % code.lower()]
    except KeyError:
        return False
    return checker(number)


def decode_code_gs1_datamatrix(number):
    result = {}
    gtin = gs1datamatrix.ProductCode.extract(number)
    if gtin:
        result['product_code'] = gtin
        _, unparsed_code = number.split(gtin, 1)
        expiration_date = gs1datamatrix.ExpirationDate.extract(
            unparsed_code)
        result['expiration_date'] = expiration_date
        _, unparsed_code = unparsed_code.split(expiration_date, 1)
        lot = gs1datamatrix.Lot.extract(unparsed_code)
        result['lot'] = lot
        _, unparsed_code = unparsed_code.split(lot, 1)
        # remove separators from variable elements
        unparsed_code = unparsed_code.replace(
            gs1datamatrix.SEPARATOR, '', 1).replace(
            gs1datamatrix.HUMAN_SEPARATOR, '', 1)
        serial_number = gs1datamatrix.SerialNumber.extract(unparsed_code)
        result['serial_number'] = serial_number

    return result


def decode_code(code, number):
    '''
    Decode Barcode
    '''
    if not check_code(code, number):
        return {}
    try:
        decoder = globals()['decode_code_%s' % code.lower()]
    except KeyError:
        return False
    return decoder(number)
