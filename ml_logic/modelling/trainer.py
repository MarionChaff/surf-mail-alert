from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

class Trainer:

    def __init__(self, model, target_categories):
        self.model = model
        self.target_categories = target_categories

    def accuracy_measures(self, y_test, y_pred):

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1score = f1_score(y_test, y_pred, average='weighted')

        print("Classification report")
        print("---------------------","\n")
        print(classification_report(y_test, y_pred,target_names = self.target_categories),"\n")
        print("Confusion Matrix")
        print("---------------------","\n")
        print(confusion_matrix(y_test, y_pred),"\n")

        return accuracy, precision, recall, f1score

    def fit_and_score(self, X_train, X_test, y_train, y_test):

        try:

            # Fit model
            self.model.fit(X_train, y_train)
            print('✅ Model fitted')

            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy, precision, recall, f1score = self.accuracy_measures(y_test,y_pred)
            print("🚀 Scores on test set:")
            print(f'Accuracy: {round(accuracy,2)}')
            print(f'Precision: {round(precision,2)}')
            print(f'Recall: {round(recall,2)}')
            print(f'F1 score: {round(f1score,2)}')
            print('✅ Model evaluated')

            return self.model

        except Exception as e:

            print('🚨 Exception occurred while training or scoring the model.')

            return None
