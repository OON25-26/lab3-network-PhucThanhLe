class SignalInformation:
    def __init__(self, signal_power, path=None):
        if path is None:
            path = list()
        self.__signal_power = signal_power
        self.__noise_power = 0
        self.__latency = 0
        self.__path = path

    ## getter methods
    def get_signal_power(self):
        return self.__signal_power
    def get_noise_power(self):
        return self.__noise_power
    def get_latency(self):
        return self.__latency
    def get_path(self):
        return self.__path

    ## setter methods
    def set_signal_power(self, signal_power):
        self.__signal_power = signal_power
    def set_noise_power(self, noise_power):
        self.__noise_power = noise_power
    def set_latency(self, latency):
        self.__latency = latency
    def set_path(self, path):
        self.__path = path

    # Update methods
    def signal_update(self, signal_power):
        self.__signal_power = signal_power

    # noise accumulation
    def noise_update(self, noise_power):
        self.__noise_power += noise_power

     # latency accumulation
    def latency_update(self, latency):
        self.__latency += latency

    # Update the signal_information when crossing a node
    def path_update(self, node_crossing):
        self.__path.remove(node_crossing)
        #return self.__path