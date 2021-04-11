import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from math import log

class TemplateClassifier(BaseEstimator, RegressorMixin):

    def __init__(self, demo_param='demo'):
        self.demo_param = demo_param

    def fit(self, X, y):

        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        # Store the classes seen during fit
        
        # Return the classifier
        return self

    def predict(self, X):

        # Check is fit had been called
        #check_is_fitted(self)

        # Input validation
        predictions = X["ventas"] * X["peso_mes_por_categoria_calorica"] + X["ventas"].apply(log)

        return predictions