# -*- coding: utf-8 -*-
import os
import pandas as pd
from pandas import DataFrame

from .context import chamberplot

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_find_paren_pair(self):
        s = 'as (adjks) sdj(ds(dfsf)) fdd(dsd(dsdss(1))dsds)ddsd'
        s2 = '((()())'
        s3 = '(((((((())))))))'
        s4 = """(numDims 1)  (size 361)  (schema   (numFields 6)   (fieldName "Mag"    (type Real64)    (numDims 1)    (size 1867)   )   (fieldName "Phase"    (type Real64)    (numDims 1)    (size 1867)   )   (fieldName "Hpos"    (type Real64)   )   (fieldName "Vpos"    (type Real64)   )   (fieldName "HV"    (type Real64)   )   (fieldName "Freq"    (type Real64)    (numDims 1)    (size 1867)   )  )
        """
        self.assertEquals(chamberplot.find_close_paren(s), 9)
        self.assertEquals(chamberplot.find_close_paren(s, start=14), 23)
        self.assertEquals(chamberplot.find_close_paren(s, 17), 22)
        with self.assertRaises(IndexError) as ctx:
            chamberplot.find_close_paren(s2)
        self.assertEquals(chamberplot.find_close_paren(s3), 15)
        self.assertEquals(chamberplot.find_close_paren(s4), 10)
        self.assertEquals(chamberplot.find_close_paren(s4, start=13), 22)
        self.assertEquals(chamberplot.find_close_paren(s4, start=25), 384)


if __name__ == '__main__':
    unittest.main()