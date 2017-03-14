import unittest
import lsh
import pandas as pd

class LSHTest(unittest.TestCase):

    def setUp(self):
        self.lsh = lsh.LSH(n_features = 10)

    def test_insert_document(self):
        with self.assertRaisesRegexp(ValueError, "Expected size 10"):
            self.lsh.insert_document([1,2,3])
        self.lsh.insert_document([1]*5+[0]*5)
        self.assertEquals(len(self.lsh.df), 1)

    def test_get_similarities(self):
        self.lsh.insert_document([1]*5+[0]*5)
        self.lsh.insert_document([1]*4+[0]*6)
        self.assertEquals(len(self.lsh.df), 2)
        table = self.lsh.get_similarities()
        self.assertEquals(table.shape, (2, 2))
        self.assertEquals(table.ix[0,0], 1)
        self.assertEquals(table.ix[1,1], 1)
        self.assertEquals(table.ix[0,1], 0.8)
        self.assertEquals(table.ix[1,0], 0.8)

