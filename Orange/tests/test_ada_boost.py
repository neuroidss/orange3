import unittest
import numpy as np
from Orange.data import Table
from Orange.classification import TreeLearner
from Orange.regression import TreeRegressionLearner
from Orange.ensembles import SklAdaBoostLearner, SklAdaBoostRegressionLearner
from Orange.evaluation import CrossValidation, CA, RMSE


class SklAdaBoostTest(unittest.TestCase):
    def setUp(self):
        self.iris = Table("iris")
        self.housing = Table("housing")

    def test_adaboost(self):
        learn = SklAdaBoostLearner()
        results = CrossValidation(self.iris, [learn], k=10)
        ca = CA(results)
        self.assertGreater(ca, 0.9)
        self.assertLess(ca, 0.99)

    def test_adaboost_base_estimator(self):
        np.random.seed(0)
        stump_estimator = TreeLearner(max_depth=1)
        tree_estimator = TreeLearner()
        stump = SklAdaBoostLearner(base_estimator=stump_estimator)
        tree = SklAdaBoostLearner(base_estimator=tree_estimator)
        results = CrossValidation(self.iris, [stump, tree], k=10)
        ca = CA(results)
        self.assertTrue(ca[0] < ca[1])

    def test_predict_single_instance(self):
        learn = SklAdaBoostLearner()
        m = learn(self.iris)
        for ins in self.iris:
            m(ins)
            _, _ = m(ins, m.ValueProbs)

    def test_predict_table(self):
        learn = SklAdaBoostLearner()
        m = learn(self.iris)
        m(self.iris)
        _, _ = m(self.iris, m.ValueProbs)

    def test_predict_numpy(self):
        learn = SklAdaBoostLearner()
        m = learn(self.iris)
        _, _ = m(self.iris.X, m.ValueProbs)

    def test_adaboost_adequacy(self):
        learner = SklAdaBoostLearner()
        self.assertRaises(ValueError, learner, self.housing)

    def test_adaboost_reg(self):
        learn = SklAdaBoostRegressionLearner()
        results = CrossValidation(self.housing, [learn], k=10)
        _ = RMSE(results)

    def test_adaboost_reg_base_estimator(self):
        np.random.seed(0)
        stump_estimator = TreeRegressionLearner(max_depth=1)
        tree_estimator = TreeRegressionLearner()
        stump = SklAdaBoostRegressionLearner(base_estimator=stump_estimator)
        tree = SklAdaBoostRegressionLearner(base_estimator=tree_estimator)
        results = CrossValidation(self.housing, [stump, tree], k=10)
        rmse = RMSE(results)
        self.assertTrue(rmse[0] >= rmse[1])

    def test_predict_single_instance_reg(self):
        learn = SklAdaBoostRegressionLearner()
        m = learn(self.housing)
        for ins in self.housing:
            pred = m(ins)
            self.assertTrue(pred > 0)

    def test_predict_table_reg(self):
        learn = SklAdaBoostRegressionLearner()
        m = learn(self.housing)
        pred = m(self.housing)
        self.assertEqual(len(self.housing), len(pred))
        self.assertTrue(all(pred) > 0)

    def test_predict_numpy_reg(self):
        learn = SklAdaBoostRegressionLearner()
        m = learn(self.housing)
        pred = m(self.housing.X)
        self.assertEqual(len(self.housing), len(pred))
        self.assertTrue(all(pred) > 0)

    def test_adaboost_adequacy_reg(self):
        learner = SklAdaBoostRegressionLearner()
        self.assertRaises(ValueError, learner, self.iris)
