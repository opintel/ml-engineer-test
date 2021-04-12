import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from math import log

class BaseModel(BaseEstimator, RegressorMixin):
    
    def __init__(self, alpha, l1_ratio):
        self.alpha = alpha
        self.l1_ratio = l1_ratio

    def fit(self, X, y):

        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        # Store the classes seen during fit
        
        # Return the classifier
        return self

    def predict(self, X):

        # Check is fit had been called
        #check_is_fitted(self)
        X = check_array(X)
        # Input validation
        predictions = X[:, 0] * X[:, 1] + np.log(X[:, 0])

        return predictions