from sklearn.model_selection import train_test_split

class Splitter:

    def __init__(self, features, target):
        self.features = features
        self.target = target

    def create_train_and_test_set(self, dataset, test_size=0.2, random_state=42):

        try:
            # Define features and target
            X = dataset[self.features]
            y = dataset[self.target].to_numpy().flatten()
            print('✅ features and target defined')

            # Define train and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
            print('✅ train and test sets created')

            return X_train, X_test, y_train, y_test

        except Exception:
            print('🚨 Error creating train and test sets')
            return None
