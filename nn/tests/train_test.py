import numpy as np

from nn.perceptron import Perceptron

nn = Perceptron(4)
cls0 = np.array([0, 1, 0, 1])
cls1 = np.array([1, 0, 1, 0])

for i in range(10):
    nn.train_on_sample(cls0, 0, learning_rate=0.5)
    nn.train_on_sample(cls1, 1, learning_rate=0.5)

print("-------")
print("class 0")
print("predicted:{}".format(nn.predict(cls0)))
print("class 1")
print("predicted:{}".format(nn.predict(cls1)))
