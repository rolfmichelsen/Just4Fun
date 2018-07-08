#! /usr/bin/env python3
#
# See https://github.com/rolfmichelsen/Just4Fun for latest
# version, licensing terms and more.
#
# © Rolf Michelsen, 2018.  All rights reserved.

import frequencyanalysis
import unittest

class FrequencyAnalysisTest(unittest.TestCase):

    def testFrequencyAnalysis1(self):
        """
        Test for 1-gram frequency analysis.
        """
        text = "abcdefabcde"
        freq = frequencyanalysis.analyseFrequencies(text)
        self.assertEqual(2, freq["a"])
        self.assertEqual(2, freq["b"])
        self.assertEqual(1, freq["f"])


    def testFrequencyAnalysis2(self):
        """
        Test for 2-gram fequency analysis.
        """
        text = "abcdefabcde"
        freq = frequencyanalysis.analyseFrequencies(text, order=2)
        self.assertEqual(2, freq["ab"])
        self.assertEqual(2, freq["bc"])
        self.assertEqual(2, freq["de"])
        self.assertEqual(1, freq["ef"])
        self.assertEqual(1, freq["fa"])


    def testFrequencyAnalysis3(self):
        """
        Test for 3-gram fequency analysis.
        """
        text = "abcdefabcde"
        freq = frequencyanalysis.analyseFrequencies(text, order=3)
        self.assertEqual(2, freq["abc"])
        self.assertEqual(2, freq["bcd"])


if __name__ == "__main__":
    unittest.main()
