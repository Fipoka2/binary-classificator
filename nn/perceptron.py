import numpy as np


class ArraySizeException(Exception):
    def __init__(self, expected, recd):
        Exception.__init__(self, 'Expected array size = {0} but got {1}'.format(expected, recd))


class Perceptron:
    def __init__(self, n: int):
        self._input_size = n
        self._weights = (0.3 + 0.3) * np.random.random_sample((n + 1)) - 0.3

    def set_random_weights(self):
        self._weights = (0.3 + 0.3) * np.random.random_sample((self._input_size + 1)) - 0.3

    @staticmethod
    def _activation(value):
        return 1 if value >= 0 else 0

    def predict(self, data: np.ndarray):
        if data.size != self._input_size:
            raise ArraySizeException(self._input_size, data.size)
        data = np.append(data, 1)

        return Perceptron._activation(data @ self._weights)

    def _forward(self, data: np.ndarray):
        if data.size != self._weights.size:
            raise ArraySizeException(self._weights.size, data.size)

        return Perceptron._activation(data @ self._weights)

    def _add_bias(self, X):
        temp = np.ones((X.shape[0], X.shape[1] + 1))
        temp[:, :-1] = X
        return temp

    def train(self, X: np.ndarray, y: np.ndarray, learning_rate=0.2, epochs: int = 1, logger=None):
        X = self._add_bias(X)
        current_epoch = 0
        while current_epoch < epochs:

            for xi, yi in zip(X, y):
                output = self._forward(xi)
                error = output - yi
                if error != 0:
                    self._weights = self._weights + learning_rate * error * xi

            current_epoch += 1
            if logger:
                logger(current_epoch / epochs)

    def train_on_sample(self, x: np.ndarray, y: int, learning_rate=0.0002):
        x = np.append(x, 1)
        output = self._forward(x)
        error = y - output
        if error != 0:
            self._weights = self._weights + learning_rate * error * x
