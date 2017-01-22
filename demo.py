from numpy import exp, array, random, dot, genfromtxt, apply_along_axis
import pdb

class NeuralNetwork():
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.
        random.seed(1)

        # We model a single neuron, with 22 input connections and 1 output connection.
        # We assign random weights to a 22 x 1 matrix, with values in the range -1 to 1
        # and mean 0.
        self.synaptic_weights = 2 * random.random((22, 1)) - 1

    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # We train the neural network through a process of trial and error.
    # Adjusting the synaptic weights each time.
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in xrange(number_of_training_iterations):
            # Pass the training set through our neural network (a single neuron).
            output = self.think(training_set_inputs)

            # Calculate the error (The difference between the desired output
            # and the predicted output).
            error = training_set_outputs - output

            learning_rate = 100.0/(iteration+1)

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            #adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            adjustment = dot(training_set_inputs.T, error * learning_rate)

            # Adjust the weights.
            self.synaptic_weights += adjustment

    # The neural network thinks.
    def think(self, inputs):
        # Pass inputs through our neural network (our single neuron).
        return self.__sigmoid(dot(inputs, self.synaptic_weights))


if __name__ == "__main__":

    #Intialise a single neuron neural network.
    neural_network = NeuralNetwork()

    print "Random starting synaptic weights: "
    print neural_network.synaptic_weights

    # Load Mushroom Data
    shrooms = genfromtxt('shrooms.csv', delimiter=',')
    shrooms_inputs = shrooms[:,1:]
    shrooms_outputs = shrooms[:,0]

    # Split Traning Data
    split_point = 6500
    training_set_inputs, test_inputs = shrooms_inputs[:split_point,:], shrooms_inputs[split_point:,:]
    training_set_outputs, test_outputs = array([shrooms_outputs[:split_point]]).T, array([shrooms_outputs[split_point:]]).T

    # Train the neural network using a training set.
    # Do it 10,000 times and make small adjustments each time.
    neural_network.train(training_set_inputs, training_set_outputs, 10000)

    print "New synaptic weights after training: "
    print neural_network.synaptic_weights

    # Calculate Correctness
    predictions = apply_along_axis(neural_network.think, axis=1, arr=test_inputs)
    correct_count = (predictions == test_outputs).sum()
    print "Correct percentage: {}".format(float(correct_count)/len(test_outputs))
