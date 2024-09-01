#This file is part of barcodenumber. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
Unit test for barcodenumber
'''

import unittest
import barcodenumber

CODES = [
    ('ean13', '9788478290222', True),
    ('ean13', '9788478290221', False),
    ('gs1_datamatrix', '010123456789012815051231', True),
    ('gs1_datamatrix', '01012345678901', False),
    ]

class BarcodeNumberTest(unittest.TestCase):
    '''
    Test Case for barcodenumber
    '''

    def test_codes_numbers(self):
        '''
        Test Bank codes
        '''
        for code, number, result in CODES:
            if result:
                test = self.assertTrue
            else:
                test = self.assertFalse
            test(barcodenumber.check_code(code, number))

if __name__ == '__main__':
    unittest.main()
