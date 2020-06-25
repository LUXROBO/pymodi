from typing import Dict, List, Tuple


class TopologyMap:
    def __init__(self, tp_data, nb_modules):
        self._nb_modules = nb_modules
        self._tp_data = tp_data

        # 2D array that will contain the topology information of the modules.
        # It stores the module id
        self._tp_map = [[0 for _ in range(2 * self._nb_modules)]
                        for _ in range(2 * self._nb_modules)]
        self.__module_position = dict()

    @staticmethod
    def __get_module_orientation(mod_data: Dict[str, int], prev_id: int,
                                 toward: Tuple[int, int]) -> Tuple[int, int]:
        """Finds out the upward direction based on the orientation of the
        module. When updating the map, it recursively traverses through modules
        to update the module_matrix. Since module's local top is not the same
        as the global top, we find out the true "top" direction based on the
        module's direction.

        :param mod_data: module's topology data
        :param prev_id: module id from which the module traversed
        :param toward: direction to which the module traversed
        :return: upward vector of the module in Tuple[int, int]
        """
        dirs = [bottom, right, top, left] = ['b', 'r', 't', 'l']

        # Finds out the direction of the previous module
        prev_module_dir = 'l'
        for d in dirs:
            if mod_data[d] == prev_id:
                prev_module_dir = d

        # Based on the direction, find out the top vector, by rotating the
        # toward vector accordingly
        nb_rotations = dirs.index(prev_module_dir)
        for _ in range(nb_rotations):
            toward = (toward[1], -toward[0])
        return toward

    @staticmethod
    def __get_rotated_direction(direction: str, up_vector: Tuple[int, int]):
        """Rotate the top_vector to get the required direction.
        Ex) direction == 'r' and up_vector == (0, 1) => then returns (1, 0)

        :param direction: char notation of the direction
        :param up_vector: up_vector direction
        :return: rotated vector pointing at the desired direction
        """
        nb_rotation = {'t': 0, 'r': 1, 'b': 2, 'l': 3}.get(direction)
        for _ in range(nb_rotation):
            up_vector = (up_vector[1], -up_vector[0])
        return up_vector

    def __update_map(self, module_id: int, x: int, y: int, prev_id: int,
                     toward: Tuple[int, int], visited: List[int]):
        """Recursively updates the map

        :param module_id: id of the current module
        :param x: x coordinate on the map
        :param y: y coordinate on the map
        :param prev_id: id of the previously traversed module
        :param toward: direction from which the module traversed
        :param visited: list of visited modules
        :return: None
        """
        if module_id in visited:
            return
        module_data = self._tp_data[module_id]
        self._tp_map[y][x] = module_id
        self.__module_position[module_id] = (x, y)
        visited.append(module_id)
        up_vector = self.__get_module_orientation(module_data, prev_id, toward)
        for d in ['t', 'b', 'l', 'r']:
            if module_data.get(d) is not None:
                toward = self.__get_rotated_direction(d, up_vector)
                self.__update_map(module_data.get(d), x + toward[0],
                                  y + toward[1], module_id, toward, visited)

    def construct_map(self) -> None:
        """Construct the topology map

        :return: None
        """
        first_id = list(self._tp_data.keys())[0]
        visited = []
        self.__update_map(first_id, self._nb_modules, self._nb_modules,
                          prev_id=-1, toward=(1, 0), visited=visited)

    def print_map(self, print_id: bool = False) -> None:
        """ Prints out the topology map

        :param print_id: If True, the result includes id in the topology map
        :type print_id: bool
        :return: None
        """
        # Trims the matrix to get rid of empty spaces, containing zeros only
        x, y, w, h = -1, -1, 1, 1

        """
        x, y indicates the coordinate from which the topology map contains
         non-zero element
        w, h indicates the width and height of non-zero elements in the map
        Since most of the elements in the map are zeros, x, y, w, h represents
        the window in which module ids are the elements of the map.
        """

        # Iterates through the rows until it finds the first non-zero row.
        # Saves the index to y, and increases h until it finds next all-zero
        # row
        for i in range(len(self._tp_map)):
            if sum(self._tp_map[i]) > 0 and y < 0:
                y = i
            elif sum(self._tp_map[i]) > 0 and y >= 0:
                h += 1

        # Iterates through the columns until it finds the first non-zero column
        # Saves the index to x, and increases w until it finds next all-zero
        # column.
        for i in range(len(self._tp_map[0])):
            col = list(map(lambda m: m[i], self._tp_map))
            if sum(col) > 0 and x < 0:
                x = i
            elif sum(col) > 0 and x >= 0:
                w += 1

        """
        Prints out the map by a format
        padding is the length of the placeholder for the module names.
        if we want to print id as well, padding should be longer to 17.
        The method prints out the window determined by x, y, w, h.
        """
        padding = 10
        if print_id:
            padding = 17
        title = "<<MODI Topology Map>>"
        print(" " * ((padding * w - len(title)) // 2) + title)
        print("=" * padding * w)
        for i in range(y + h - 1, y - 1, -1):
            line = ""
            row = self._tp_map[i]
            for j in range(x, x + w + 1):
                curr_elem = row[j]
                if not curr_elem:
                    line += " " * padding
                else:
                    if print_id:
                        line += "{0:^17s}".format(
                            TopologyManager.get_type_from_uuid(
                                self._tp_data[curr_elem]['uuid']) + ":" +
                            str(curr_elem))
                    else:
                        name = TopologyManager.get_type_from_uuid(
                            self._tp_data[curr_elem]['uuid'])
                        line += f"{name:^10}"
            print(line)

    @property
    def network_id(self):
        for mid in self._tp_data:
            if TopologyManager.get_type_from_uuid(self._tp_data[mid]['uuid']) \
                    == 'Network':
                return mid

    def get_distance(self, module_id):
        module_position = self.__module_position[module_id]
        network_position = self.__module_position[self.network_id]
        return (module_position[0] - network_position[0])**2 \
            + (module_position[1] - network_position[1])**2


class TopologyManager:

    def __init__(self, topology_data):
        self._tp_data = topology_data
        self._nb_modules = len(self._tp_data)

    def print_topology_map(self, print_id: bool = False) -> None:
        """ Print the topology map

        :param print_id: If True, the result includes module ids
        :return: None
        """
        self._nb_modules = len(self._tp_data)
        tp_map = TopologyMap(self._tp_data, self._nb_modules)
        tp_map.construct_map()
        tp_map.print_map(print_id)

    @staticmethod
    def get_type_from_uuid(uuid: int) -> str:
        """Returns type based on uuid

        :param uuid: UUID of the required type
        :type uuid: int
        :return: Corresponding type
        :rtype: str
        """
        if uuid is None:
            return 'Network'

        hexadecimal = hex(uuid).lstrip("0x")
        type_indicator = str(hexadecimal)[:4]
        module_type = {
            # Input modules
            '2000': 'Env',
            '2010': 'Gyro',
            '2020': 'Mic',
            '2030': 'Button',
            '2040': 'Dial',
            '2050': 'Ultrasonic',
            '2060': 'Infrared',

            # Output modules
            '4000': 'Display',
            '4010': 'Motor',
            '4020': 'Led',
            '4030': 'Speaker',
        }.get(type_indicator)
        return module_type
