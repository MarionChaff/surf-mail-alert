from xgboost import XGBClassifier

class ModelBuilder:

    """
    A class to build a XGBoost model.

    Attributes
    ----------
    max_depth : int, the maximum depth of the trees in the model.
    n_estimators : int, the number of trees (estimators) in the model.

    Methods
    -------
    build_model() : builds a XGBoost classifier model with the specified parameters (class attributes).
    """

    def __init__(self, max_depth=4, n_estimators=95):
        self.max_depth = max_depth
        self.n_estimators = n_estimators

    def build_model(self):
        model = XGBClassifier(
            objective='multi:softprob',
            max_depth = self.max_depth,
            n_estimators=self.n_estimators
            )
        return model
