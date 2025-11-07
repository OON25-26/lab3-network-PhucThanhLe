import json
import math
import matplotlib.pyplot as plt
import numpy as np
from Node import Node
from Line import Line

class Network:
    def __init__(self, node_json_file):
        # Read nodes.json file
        try:
            with open(node_json_file, 'r') as file:
                nodes_from_json = json.load(file)
            print("File node =", nodes_from_json)
#            print(dict.keys(nodes))

        except FileNotFoundError:
            print("Error: The file 'nodes.json' was not found.")

        self.__nodes = dict()
        self.__lines = dict()

        # loop through nodes to create instances of Node objects
        # access nodes dictionary with key(label)
        for key in dict.keys(nodes_from_json):
            # access data from each key
            connected_nodes = nodes_from_json[key]['connected_nodes']
            position = nodes_from_json[key]['position']
            # arrange key(label), position, connected_nodes into a dictionary
            n0_dict = {'label': key, 'connected_nodes': connected_nodes, 'position': position}
            self.__nodes[key] = Node(n0_dict)

            # in the same for loop above:
            # create instances of lines and put them in self.__lines
            for c_node in connected_nodes:
                # concatenate key and c_node into line label
                line_label = key + c_node
                # finding length of the line
                line_length = math.dist(nodes_from_json[key]['position'], nodes_from_json[c_node]['position'])
                # put Line instance into self.__lines
                self.__lines[line_label] = Line(line_label, line_length)

    # get methods
    def get_nodes(self):
        return self.__nodes
    def get_lines(self):
        return self.__lines

    #set methods
    def set_nodes(self, new_nodes):
        self.__nodes = new_nodes
    def set_lines(self, new_lines):
        self.__lines = new_lines

    # connect method
    def connect(self):
        for node in self.__nodes.values():
            node.successive_elements(None,self.__lines)
        for line in self.__lines.values():
            line.successive_elements(None,self.__nodes)

    def find_paths(self, node_label_start, node_label_end):
        # initiate empty lists to use later
        path_list = list()
        path_temp = list()
        # initially assign 2 nodes as a path
        path_temp.append(node_label_start)
        path_temp.append(node_label_end)
        ## Loop algorithm to find paths
        # create list containing non_completed paths
        # and append the first element which is a list containing only node_label_start
        path_non_complete = list()
        path_non_complete.append([node_label_start])
            # Loop through paths in path_non_complete list
        for path in path_non_complete:
            # extract the last element in the path list as the current nodeD
            node_label_current = path[-1]
            # list out nodes connected to current node:
            node_label_connected_current_list = self.__nodes[node_label_current].get_connected_nodes()
            # loop through connected nodes:
            for node_label_connected_current in node_label_connected_current_list:
                # assign path to path_temp:
                path_temp = path.copy()
                # if the end node is the same as one of the connected node of node_label_current
                if node_label_connected_current == node_label_end:
                    # append the node label to the path:
                    path_temp.append(node_label_connected_current)
                    # append the path to path_list
                    path_list.append(path_temp)
                    # raise False flag signifies stopping the loop
                else:
                    # check if the current node appeared in the path
                    if path_temp.count(node_label_connected_current) == 0:
                        # Append the node label to the path
                        path_temp.append(node_label_connected_current)
                        # append the path to path_non_complete list
                        path_non_complete.append(path_temp)
                        # raise True flag signifying continuing the loop
                    else:
                        continue
        return path_list

    def propagate(self, signal_information):
        # create empty spectral_information dictionary
        spectral_information = dict()
        if signal_information.get_path():
            self.__nodes[signal_information.get_path()[0]].propagate(signal_information)
            spectral_information['Latency(s)'] = signal_information.get_latency()
            spectral_information['Noise(W)'] = signal_information.get_noise_power()
            spectral_information['Signal(W)'] = signal_information.get_signal_power()
        else:
            print('Path not found!')
        return spectral_information

    def draw(self):
        # create subplot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # draw nodes
        for node in self.__nodes.values():
            plt.plot(node.get_position()[0], node.get_position()[1], 'o', markersize=10)
            # Add node label to the plot
            ax.text(node.get_position()[0], node.get_position()[1], node.get_label(), fontsize=20)
        for line in self.__lines.values():
            # For drawing line, plt.plot is tricky in a sense that
            # drawing from point A[a1,a2] to point B[b1,b2]
            # needs argument in the function as following:
            # plt.plot([a1,b1],[a2,b2])
            # This is similar to transposing a matrix [[a1,a2],[b1,b2]] => [[a1,b1],[a2,b2]]
            # Create the position matrix of 2 successive nodes of the line
            pos_matrix = [node.get_position() for node in line.get_successive().values()]
            # Transpose the matrix using numpy
            pos_matrix = np.transpose(pos_matrix)
            # plot the lines:
            plt.plot(pos_matrix[0], pos_matrix[1], linewidth=2)
        plt.savefig('..\\results\\lab3_network_topology.jpg')
        plt.show()
        return None