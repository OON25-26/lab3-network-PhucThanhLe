class Node:
    def __init__(self, node_dict_input):
        self.__label = node_dict_input['label']
        self.__position = node_dict_input['position']
        self.__connected_nodes = node_dict_input['connected_nodes']
        self.__successive = dict()

    # get methods
    def get_label(self):
        return self.__label
    def get_position(self):
        return self.__position
    def get_connected_nodes(self):
        return self.__connected_nodes
    def get_successive(self):
        return self.__successive

    # set methods
    def set_label(self, label):
        self.__label = label
    def set_position(self, position):
        self.__position = position
    def set_connected_nodes(self, connected_nodes):
        self.__connected_nodes = connected_nodes
    def set_successive(self, successive):
        self.__successive = successive

    # Define a propagate method:
    def propagate(self, signal_information):
        # Update the path according to the current node:
        signal_information.path_update(self.__label)
        # call successive lines according to updated path:
        # Check if any node left in path:
        if signal_information.get_path():
            # Check if next line is valid:
            line_label_next = self.__label+signal_information.get_path()[0]
            if self.__successive.keys().__contains__(line_label_next):
                self.__successive[line_label_next].propagate(signal_information)
            else:
                print('Path invalid:')
                print(line_label_next)


    def successive_elements(self, path, lines):
        # Clear out successive dictionary
        self.__successive = dict()
        if path is None:
            for node_connected in self.__connected_nodes:
                line_successive = self.__label + node_connected
                self.__successive[line_successive] = lines[line_successive]
        else:
            for node_path in path:
                for node_connected in self.__connected_nodes:
                    if node_path == node_connected:
                        line_successive = self.__label + node_path
                        self.__successive[line_successive] = lines[line_successive]
                    else:
                        continue
        #return self.__successive




