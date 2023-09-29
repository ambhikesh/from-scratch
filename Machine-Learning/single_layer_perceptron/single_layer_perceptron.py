import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_set, labels):
        self.input_set = input_set
        self.labels = labels
        self.num_samples, self.num_features = input_set.shape
        self._weights = np.random.rand(self.num_features, 1)
        self._bias = np.random.rand(1, 1)
        self._learning_rate = 0.05
        self.errors = []

    def sigmoid(self, x) -> float:
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x) -> float:
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def train(self, num_epochs=25000) -> None:
        for _ in range(num_epochs):
            indices = np.arange(self.num_samples)
            np.random.shuffle(indices)
            shuffled_inputs = self.input_set[indices]
            shuffled_labels = self.labels[indices]

            XW = np.dot(shuffled_inputs, self._weights) + self._bias
            z = self.sigmoid(XW)
            error = z - shuffled_labels
            self.errors.append(error.sum())

            dcost = error
            dpred = self.sigmoid_derivative(z)
            z_del = dcost * dpred
            inputs = shuffled_inputs.T

            self._weights -= self._learning_rate * np.dot(inputs, z_del)
            self._bias -= self._learning_rate * np.sum(z_del)

    def predict(self, input_data):
        XW = np.dot(input_data, self._weights) + self._bias
        prediction = self.sigmoid(XW)
        return prediction

    def plot(self,x:list) -> None:
        plt.plot(x)
        plt.xlabel('Epochs')
        plt.ylabel('Error')
        plt.title('Error during training')
        plt.savefig('epochVSerror.png')

#training
input_set = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
labels = np.array([[0], [0], [0], [1]])
perceptron = Perceptron(input_set, labels)
perceptron.train(num_epochs=850)
perceptron.plot(perceptron.errors)

#testing
test_inputs = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
expected_outputs = np.array([[0], [0], [0], [1]])

for i in range(len(test_inputs)):
    predicted_output = perceptron.predict(test_inputs[i])
    if(predicted_output<0.5):
        output = 0
    else:
        output = 1
    expected_output = expected_outputs[i]
    
    print(f"Input: {test_inputs[i]}, Predicted: {[output]}, Expected: {expected_output}")
