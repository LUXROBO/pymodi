import time
from typing import Dict, List, Tuple

from modi.util.miscellaneous import ModuleList


class TopologyManager:

    class TopologyMap:
        def __init__(self, tp_data, nb_modules, modules):
            self._nb_modules = nb_modules
            self._tp_data = tp_data
            self._modules = modules
            """
            2D array that will contain the topology information of the modules.
            It store the module id.
            """
            self._tp_map = [
                ["" for _ in range(2 * self._nb_modules)]
                for _ in range(2 * self._nb_modules)
            ]
            self.__module_position = dict()
            self.__construct_map()

        @staticmethod
        def __get_module_orientation(
                mod_data: Dict[str, int], prev_id: int,
                toward: Tuple[int, int]
        ) -> Tuple[int, int]:
            """
            Finds out the upward direction based on the orientation of the
            module. When updating the map, it recursively traverses through
            modules to update the module_matrix. Since module's local top is
            not the same as the global top, we find out the true "top"
            direction based on the module's direction.

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
        def __get_rotated_direction(direction, up_vector):
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

            module_tp_data = self._tp_data[module_id]
            self._tp_map[y][x] = str(module_id)
            self.__module_position[module_id] = (x, y)
            visited.append(module_id)
            up_vector = self.__get_module_orientation(
                module_tp_data, prev_id, toward
            )

            for d in ['t', 'b', 'l', 'r']:
                if not module_tp_data.get(d):
                    continue
                # which direction should we move toward? one of 't,b,l,r'
                toward = self.__get_rotated_direction(d, up_vector)
                self.__update_map(
                    module_tp_data.get(d), x + toward[0], y + toward[1],
                    module_id, toward, visited
                )

        def __construct_map(self) -> None:
            """Construct the topology map

            :return: None
            """
            first_id = self.__get_network_id()
            visited = []
            self.__update_map(
                first_id, self._nb_modules, self._nb_modules,
                prev_id=-1, toward=(1, 0), visited=visited
            )

        def __trim_map(self, raw_map: List):
            """
            Trims the matrix to get rid of empty spaces, containing zeros only
            """
            x, y, w, h = -1, -1, 1, 1

            """
            x, y indicates the coordinate from which the topology map contains
            non-zero element where w, h indicates the width and height of
            non-zero elements in the map. Since most of the elements in the map
            are zeros, x, y, w, h represents the window in which module ids are
            the elements of the map.
            """

            """
            Iterates through the rows until it finds the first non-zero row.
            Saves the index to y, and increases h until it finds next all-zero
            row.
            """
            str_sum = self.__str_sum
            for i in range(len(raw_map)):
                if str_sum(raw_map[i]) and y < 0:
                    y = i
                elif str_sum(raw_map[i]) and y >= 0:
                    h += 1

            """
            Iterates through the columns until it finds the first non-zero
            column. Saves the index to x, and increases w until it finds next
            all-zero column.
            """
            for i in range(len(raw_map[0])):
                col = list(map(lambda m: m[i], raw_map))
                if str_sum(col) and x < 0:
                    x = i
                elif str_sum(col) and x >= 0:
                    w += 1
            return x, y, w, h

        @staticmethod
        def __str_sum(line):
            result = ""
            for c in line:
                result += c
            return result

        def __compose_line(self, module_id, padding, print_id):
            line = ""
            if not module_id:
                line += " " * padding
            else:
                module_id = int(module_id)
                module_type = self._tp_data[module_id]['type']
                module_idx = ModuleList(
                    self._modules, module_type.lower()
                ).find(module_id)
                if module_idx < 0:
                    module_idx = ''

                el = f"{module_type + str(module_idx) + f' ({module_id})':^17}"
                if print_id:
                    line += el
                else:
                    line += f"{module_type + str(module_idx):^10}"
            return line

        def print_map(self, print_id: bool = False) -> None:
            x, y, w, h = self.__trim_map(self._tp_map)
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
                for j in range(x, x + w):
                    curr_elem = row[j]
                    line += self.__compose_line(curr_elem, padding, print_id)
                print(line)

        def __get_network_id(self):
            for mid in self._tp_data:
                if self._tp_data[mid]['type'] == 'network':
                    return mid
            return list(self._tp_data.keys())[0]

        def update_module_data(self, modules):
            # This mainly updates module's position data, for sorting modules
            network_position = self.__module_position[self.__get_network_id()]
            for module in modules:
                module_position = self.__module_position[module.id]
                module.position = (
                    module_position[0] - network_position[0],
                    module_position[1] - network_position[1],
                )

    def __init__(self, topology_data, modules):
        self._tp_data = topology_data
        self._nb_modules = len(self._tp_data)
        self._modules = modules

    def is_topology_complete(self):
        """
        This method is called in the MODI object initialization, and will
        continue to run until all topology data are formed properly.
        """

        # If no entry exists in the dictionary
        if not self._tp_data:
            return False

        # Battery module id is defined to be 0
        if 0 in self._tp_data:
            print("Battery Module detected. Topology may by inaccurate.")
            time.sleep(2)

        try:
            self.__update_module_position()
        except KeyError:
            return False
        return (
            len(self._modules) == len(self._tp_data)
            and self.__is_type_complete()
        )

    def print_topology_map(self, print_id: bool = False) -> None:
        self._nb_modules = len(self._tp_data)
        tp_map = self.TopologyMap(
            self._tp_data, self._nb_modules, self._modules
        )
        tp_map.print_map(print_id)

    def __update_module_position(self):
        self._nb_modules = len(self._tp_data)
        tp_map = self.TopologyMap(
            self._tp_data, self._nb_modules, self._modules
        )
        tp_map.update_module_data(self._modules)

    def __is_type_complete(self):
        # return true if type of all modules are initialized
        for module in self._tp_data:
            if not self._tp_data[module]['type']:
                return False
        return True
