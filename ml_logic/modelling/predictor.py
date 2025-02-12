class Predictor:

    """
    A class to handle predictions using a pre-trained model for an API.

    Attributes
    ----------
    model : .pkl object, the sklearn pre-trained model used for making predictions.

    Methods
    -------
    predict: makes a prediction based on the input data and returns a response dictionary
    with the prediction and HTTP status code.

    """

    def __init__(self, model):
        self.model = model

    def predict(self, X):

        return_dict = {}

        try:
            prediction = self.model.predict(X)
            print(f'✅ Inference successful')

            return_dict['response'] = prediction
            return_dict['status'] = 200
            return return_dict

        except Exception as e:

            print(f'🚨 Exception occurred during inference: {str(e.__str__)}')

            return_dict['response'] = ''
            return_dict['status'] = 500
            return return_dict
