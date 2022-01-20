from collections import deque
from datetime import time
import algos
import csv_reader
import time_delta
from package import Package
from algos import nearest_neighbor


class Depot:
    def __init__(self):
        self.inventory = []
        self.priority_ready = []
        self.north_bound_ready = []
        self.north_bound_hold = []
        self.south_bound_priority = []
        self.south_bound_ready = []
        self.south_bound_hold = []

    def receive_packages(self):
        for item in csv_reader.get_package_ids():
            pkg = Package(item)
            pkg.at_hub = time_delta.Time(8, 0).clock_time
            self.inventory.append(pkg)

    def route_priority(self):
        self.priority_ready = nearest_neighbor(0, self.priority_ready)

    def route_north_bound(self):
        self.north_bound_ready = nearest_neighbor(0, self.north_bound_ready)

    def route_north_bound_with_priority(self, priority):
        self.north_bound_ready = nearest_neighbor(priority, self.north_bound_ready)

    def route_south_bound(self):
        self.south_bound_ready = nearest_neighbor(0, self.south_bound_ready)

    def route_south_bound_with_priority(self, priority):
        self.south_bound_ready = nearest_neighbor(priority, self.south_bound_ready)

    def determine_truck_ready_hold(self, n_truck, s_truck):
        north_bound, south_bound = algos.map_direction()
        for pkg in self.inventory:
            if pkg.vertex in north_bound:
                if 'delayed' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(9,5):
                    self.north_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(10,20):
                    self.north_bound_hold.append(pkg)
                else:
                    self.north_bound_ready.append(pkg)
            else:
                if 'delayed' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(9,5):
                    self.south_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(10,20):
                    self.south_bound_hold.append(pkg)
                else:
                    self.south_bound_ready.append(pkg)

    def load_priority(self, truck):
        while self.priority_ready:
            pkg = self.priority_ready.pop(0)
            pkg.en_route = truck.time.clock_time
            truck.inventory.append(pkg)
            if len(truck.inventory) == truck.capacity:
                print('Truck is full')
                break

    def load_north_bound(self, truck):
        while self.north_bound_ready:
            pkg = self.north_bound_ready.pop(0)
            pkg.en_route = truck.time.clock_time
            truck.inventory.append(pkg)
            if len(truck.inventory) == truck.capacity:
                print('Truck is full')
                break
        if len(self.north_bound_ready) + len(self.north_bound_hold) > 0:
            truck.return_needed = True
        else:
            truck.return_needed = False

    def load_south_bound(self, truck):
        while self.south_bound_ready:
            pkg = self.south_bound_ready.pop(0)
            pkg.en_route = truck.time.clock_time
            truck.inventory.append(pkg)
            if len(truck.inventory) == truck.capacity:
                print('Truck is full')
                break
        if len(self.south_bound_ready) + len(self.south_bound_hold) > 0:
            truck.return_needed = True
        else:
            truck.return_needed = False

    def ready_held_packages(self,n_truck,s_truck):
        while self.north_bound_hold:
            pkg = self.north_bound_hold[0]
            if 'delayed' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(9, 5):
                continue
            elif 'wrong address' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(10, 20):
                continue
            pkg = self.north_bound_hold.pop(0)
            self.north_bound_ready.append(pkg)
        while self.south_bound_hold:
            pkg = self.south_bound_hold[0]
            if 'delayed' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(9, 5):
                continue
            elif 'wrong address' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(10, 20):
                continue
            pkg = self.south_bound_hold.pop(0)
            self.south_bound_ready.append(pkg)

    def place_package_on_hold(self, pkg_id):
        pass

    def special_case_packages(self, special_case_list):
        for pkg in self.inventory:
            if pkg.info['package ID number'] in special_case_list:
                pass


class Truck:
    def __init__(self):
        self.inventory = deque()
        self.time = time_delta.Time(8, 0)
        self.total_distance = 0
        self.speed = 18
        self.capacity = 16
        self.delivered = 0
        self.origin = 0
        self.return_needed = False

    def load(self, package):
        if len(self.inventory) == self.capacity:
            print('Truck is full')
            return
        self.inventory.append(package)

    def minutes_per_mile(self, distance):
        return round(60 / self.speed * distance, 0)

    def deliver(self):
        dict_dict = csv_reader.adjacency_matrix()
        if len(self.inventory) == 0:
            print('Empty')
            return
        elif self.time.time_delta > time(10, 20):
            self.fix_wrong_address_package()
        current_package = self.inventory.popleft()
        print(current_package)
        print(self.origin, '--->', current_package.info['vertex'])
        distance = float(dict_dict[current_package.vertex][self.origin])
        print('+', distance)
        self.time.add(self.minutes_per_mile(distance))
        self.total_distance += distance
        print(round(self.total_distance, 2))
        self.origin = current_package.vertex
        self.delivered += 1
        print(self.delivered, ' packages delivered')
        current_package.delivered = self.time.clock_time
        if len(self.inventory) == 0:
            self.return_to_hub()

    def return_to_hub(self):
        print('Returning to Hub')
        dict_dict = csv_reader.adjacency_matrix()
        distance = float(dict_dict[0][self.origin])
        self.time.add(self.minutes_per_mile(distance))
        self.total_distance += distance
        self.origin = 0
        print(round(self.total_distance, 2))
        print(self.time.clock_time)

    def get_total_distance(self):
        return round(self.total_distance, 2)

    def fix_wrong_address_package(self):
        for pkg in self.inventory:
            if 'wrong address' in pkg.info['Special Notes'].lower():
                pkg.info['vertex'] = 19

