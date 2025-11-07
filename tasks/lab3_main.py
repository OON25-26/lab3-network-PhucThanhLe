import math
from SignalInformation import SignalInformation
from Network import Network
import pandas as pd

# function to make nice path string from nodes:
def path_string_maker(p):
    path_string = str()
    for node_label in p:
        path_string += node_label
        if node_label != p[-1]:
            path_string += '->'
    return path_string

# data dictionary and keys for panda dataframe
Latency = 'Latency(s)'
Noise = 'Noise(W)'
Signal = 'Signal(W)'
SnR = 'SNR(dB)'
data = dict()
data[Latency] = list()
data[Noise] = list()
data[Signal] = list()
data[SnR] = list()
# Create paths_string list to store nodes put together into a path string
paths_string = list()

# Instantiate the network with json file input
net0 = Network('../resources/nodes.json')
# 'connect' all nodes and lines
net0.connect()
# Draw the network
net0.draw()

# Signal power:
signal_power = 0.001
# spectral_information
spectral_information = dict()

# Loop through all possible node combinations to obtain required data for dataframe
for node_label_start in net0.get_nodes().keys():
    for node_label_end in net0.get_nodes().keys():
        if node_label_start != node_label_end:
            paths = net0.find_paths(node_label_start, node_label_end)
            for path in paths:
                paths_string.append(path_string_maker(path))
                # Instantiate signal with 1mW power:
                signal = SignalInformation(signal_power, path)
                # propagate the signal with the given path:
                spectral_information = net0.propagate(signal)
                # collect data:
                data[Latency].append(spectral_information[Latency])
                data[Noise].append(spectral_information[Noise])
                data[Signal].append(spectral_information[Signal])
                data[SnR].append(10*math.log10(spectral_information[Signal]/spectral_information[Noise]))

# Create panda Dataframe:
df = pd.DataFrame(data, paths_string)
#print(df.to_string())
df.to_csv('..\\results\\lab3_network_propagation_data.csv')

