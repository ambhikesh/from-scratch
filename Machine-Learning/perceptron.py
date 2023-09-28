import numpy as np

#random dataset
input_set = np.array([[0,1,0],
                      [0,0,1],
                      [1,0,0],
                      [1,1,0],
                      [1,1,1],
                      [0,1,1],
                      [0,1,0]])

labels = np.array([[1,
                    0,
                    0,
                    1,
                    1,
                    0,
                    1]])

labels = labels.reshape(7,1)

#Hyper-parameters
np.random.seed(13)
weights = np.random.rand(3,1)
bias = np.random.rand(1)
alpha = 0.05 #learing rate

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x)*(1-sigmoid(x))

for epoch in range(25000):
    inputs = input_set
    XW = np.dot(inputs,weights)+bias
    z = sigmoid(XW)
    error = z - labels
    print(error.sum())
    dcost = error
    dpred = sigmoid_derivative(z)
    z_del = dcost*dpred
    inputs = input_set.T
    weights = weights - alpha*np.dot(inputs, z_del)

    for num in z_del:
        bias = bias - alpha*num

test = np.array([0,1,0])
res = sigmoid(np.dot(test,weights)+bias)
print(res)
