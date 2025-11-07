class Line:
    def __init__(self, label, length):
        self.__label = label
        self.__length = length
        self.__successive = dict()

    # get method
    def get_successive(self):
        return self.__successive
    def set_successive(self, successive):
        self.__successive = successive

    def get_label(self):
        return self.__label
    def set_label(self, label):
        self.__label = label

    def get_length(self):
        return self.__length
    def set_length(self, length):
        self.__length = length

    # latency_generation method (m, s and m/s)
    def latency_generation(self):
        return float(self.__length / (2/3 * 3 * pow(10,8)))
    # noise_generation method (W)
    def noise_generation(self, signal_power):
        return float(1e-9 * signal_power * self.__length)

    # propagate method of line:
    def propagate(self, signal_information):
        # Call latency and noise power update methods
        signal_information.latency_update(self.latency_generation())
        signal_information.noise_update(self.noise_generation(signal_information.get_signal_power()))
        # Call propagate method of the next node according to the current path
        self.__successive[signal_information.get_path()[0]].propagate(signal_information)

    # create a dict of successive nodes to the current line
    def successive_elements(self, path, nodes):
        # Clear out current successive nodes attribute:
        self.__successive = dict()
        # Get the label of one unique next node of the current line
        node_successive_labels = list(self.__label)
        for node_label in node_successive_labels:
            if path is not None:
                # list out only the next node destination
                for node_path in path:
                    if node_label == node_path:
                        self.__successive[node_label] = nodes[node_label]
                    else:
                        continue
            else:
                # list out successive nodes
                self.__successive[node_label] = nodes[node_label]
        #return self.__successive