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
        self.north_bound_ready = []
        self.north_bound_hold = []
        self.south_bound_ready = []
        self.south_bound_hold = []
        self.must_be_together = []
        self.must_be_together_direction = None

    def receive_packages(self):
        for item in csv_reader.get_package_ids():
            pkg = Package(item)
            pkg.at_hub = time_delta.Time(8, 0).clock_time
            self.inventory.append(pkg)

    @staticmethod
    def reroute_truck(truck):
        truck.inventory = deque(nearest_neighbor(0, list(truck.inventory)))

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
                if 'delayed' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(9, 5):
                    self.north_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(10, 20):
                    self.north_bound_hold.append(pkg)
                else:
                    self.north_bound_ready.append(pkg)
            else:
                if 'delayed' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(9, 5):
                    self.south_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(10, 20):
                    self.south_bound_hold.append(pkg)
                else:
                    self.south_bound_ready.append(pkg)
        self.packages_must_be_together(['13', '14', '15', '16', '19', '20'])

    def load_north_bound(self, truck):
        reroute_needed = False
        truck.trip += 1
        if self.must_be_together_direction == 'North':
            while self.must_be_together:
                reroute_needed = True
                pkg = self.must_be_together.pop(0)
                pkg.en_route = truck.time.clock_time
                truck.inventory.append(pkg)
        if len(self.north_bound_ready) == 0:
            return
        while self.north_bound_ready:
            pkg = self.north_bound_ready.pop(0)
            pkg.en_route = truck.time.clock_time
            truck.inventory.append(pkg)
            if len(truck.inventory) == truck.capacity:
                break
        if reroute_needed:
            self.reroute_truck(truck)
        truck.log_route[truck.time.clock_time] = truck.name + ' En Route'
        if len(self.north_bound_ready) + len(self.north_bound_hold) > 0:
            truck.reload_needed = True
        else:
            truck.reload_needed = False

    def load_south_bound(self, truck):
        reroute_needed = False
        truck.trip += 1
        if self.must_be_together_direction == 'South':
            while self.must_be_together:
                reroute_needed = True
                pkg = self.must_be_together.pop(0)
                truck.inventory.append(pkg)
                pkg.en_route = truck.time.clock_time
        if len(self.south_bound_ready) == 0:
            return
        while self.south_bound_ready:
            pkg = self.south_bound_ready.pop(0)
            pkg.en_route = truck.time.clock_time
            truck.inventory.append(pkg)
            if len(truck.inventory) == truck.capacity:
                break
        if reroute_needed:
            self.reroute_truck(truck)
        truck.log_route[truck.time.clock_time] = ' Truck En Route'
        if len(self.south_bound_ready) + len(self.south_bound_hold) > 0:
            truck.reload_needed = True
        else:
            truck.reload_needed = False

    def ready_held_packages(self, n_truck, s_truck):
        count = 0
        n_length = len(self.north_bound_hold)
        while count < n_length:
            pkg = self.north_bound_hold[count]
            if 'delayed' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(9, 5):
                count += 1
            elif 'wrong address' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(10, 20):
                count += 1
            else:
                pkg = self.north_bound_hold.pop(count)
                self.north_bound_ready.append(pkg)
                n_length = len(self.north_bound_hold)
        count = 0
        s_length = len(self.south_bound_hold)
        while count < s_length:
            pkg = self.south_bound_hold[count]
            if 'delayed' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(9, 5):
                count += 1
            elif 'wrong address' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(10, 20):
                count += 1
            else:
                pkg = self.south_bound_hold.pop(count)
                self.south_bound_ready.append(pkg)
                s_length = len(self.south_bound_hold)
        if len(self.south_bound_ready) < 2 and len(self.north_bound_ready) <= n_truck.capacity - 2:
            while self.south_bound_ready:
                self.north_bound_ready.append(self.south_bound_ready.pop(0))
        elif len(self.north_bound_ready) < 2 and len(self.south_bound_ready) <= s_truck.capacity - 2:
            while self.north_bound_ready:
                self.south_bound_ready.append(self.north_bound_ready.pop(0))

    def packages_must_be_together(self, special_packages):
        must_be_together = []
        n_freq = 0
        s_freq = 0
        for pkg in self.inventory:
            if pkg.info['package ID number'] in special_packages:
                must_be_together.append(pkg)
        self.must_be_together = must_be_together
        for pkg in must_be_together:
            if pkg.info['delivery status'] == 'delivered':
                return
            if pkg in self.north_bound_ready:
                self.north_bound_ready.pop(self.north_bound_ready.index(pkg))
                n_freq += 1
            elif pkg in self.south_bound_ready:
                self.south_bound_ready.pop(self.south_bound_ready.index(pkg))
                s_freq += 1
        if n_freq > s_freq:
            self.must_be_together_direction = 'North'
        else:
            self.must_be_together_direction = 'South'

    def fix_wrong_address_display(self, time_input):
        if time_input.time() > time(10, 19):
            address = '410 S State St'
            zip_ = 'Salt Lake City'
            city = '84111'
        else:
            address = '300 State St'
            zip_ = 'Salt Lake City'
            city = '84103'
        for pkg in self.inventory:
            if 'wrong address' in pkg.info['Special Notes'].lower():
                pkg.info['delivery address'] = address
                pkg.info['delivery city'] = zip_
                pkg.info['delivery zip code'] = city


class Truck:
    def __init__(self, name):
        self.name = name
        self.inventory = deque()
        self.time = time_delta.Time(8, 0)
        self.total_distance = 0
        self.speed = 18
        self.capacity = 16
        self.delivered = 0
        self.origin = 0
        self.reload_needed = False
        self.trip = 0
        self.log_route = {}
        self.log_packages = {}
        self.log_marginal_dist = {}
        self.log_total_dist = {}

    def load(self, package):
        if len(self.inventory) == self.capacity:
            return
        self.inventory.append(package)

    def minutes_per_mile(self, distance):
        return round(60 / self.speed * distance, 0)

    def deliver(self):
        dict_dict = csv_reader.adjacency_matrix()
        if len(self.inventory) == 0:
            return
        elif self.time.time_delta > time(10, 20):
            self.fix_wrong_address_package()
        current_package = self.inventory.popleft()
        current_package.info['trip'] = f'{self.name} Trip #{self.trip}'
        self.log_packages[self.time.clock_time] = str(current_package)
        self.log_route[self.time.clock_time] = self.origin, '--->', current_package.info['vertex']
        distance = float(dict_dict[current_package.vertex][self.origin])
        self.time.add(self.minutes_per_mile(distance))
        self.log_marginal_dist[self.time.clock_time] = '+' + str(distance)
        self.total_distance += distance
        self.log_total_dist[self.time.clock_time] = round(self.total_distance, 2)
        current_package.info['delivery status'] = 'delivered'
        self.origin = current_package.vertex
        self.delivered += 1
        current_package.delivered = self.time.clock_time
        if len(self.inventory) == 0:
            self.return_to_hub()

    def return_to_hub(self):
        self.log_route[self.time.clock_time] = 'Returning to Hub'
        dict_dict = csv_reader.adjacency_matrix()
        distance = float(dict_dict[0][self.origin])
        self.log_marginal_dist[self.time.clock_time] = '+' + str(distance)
        self.time.add(self.minutes_per_mile(distance))
        self.total_distance += distance
        self.origin = 0
        self.log_total_dist[self.time.clock_time] = round(self.total_distance, 2)

    def get_total_distance(self):
        return round(self.total_distance, 2)

    def fix_wrong_address_package(self):
        for pkg in self.inventory:
            if 'wrong address' in pkg.info['Special Notes'].lower():
                pkg.info['vertex'] = 19

