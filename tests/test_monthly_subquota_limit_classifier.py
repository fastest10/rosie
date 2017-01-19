from unittest import TestCase

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal

from rosie.monthly_subquota_limit_classifier import MonthlySubquotaLimitClassifier


class TestMonthlySubquotaLimitClassifier(TestCase):

    def setUp(self):
        self.dataset = pd.read_csv('tests/fixtures/monthly_subquota_limit_classifier.csv',
                                   dtype={'subquota_number': np.str})
        self.subject = MonthlySubquotaLimitClassifier()
        self.subject.fit_transform(self.dataset)
        self.prediction = self.subject.predict(self.dataset)

    def test_predict_false_when_not_in_date_range(self):
        assert_array_equal(np.repeat(False, 4),
                           self.prediction[[0, 1, 9, 10]])

    def test_predict_false_when_under_the_limit(self):
        assert_array_equal(np.repeat(False, 4),
                           self.prediction[[2, 3, 11, 12]])

    def test_predict_false_when_exactly_on_the_limit(self):
        assert_array_equal(np.repeat(False, 4),
                           self.prediction[[4, 5, 13, 14]])

    def test_predict_true_when_over_the_limit(self):
        assert_array_equal(np.r_[[False, True, True]],
                           self.prediction[[6, 7, 8]])
        assert_array_equal(np.r_[[False, True, True]],
                           self.prediction[[15, 16, 17]])
