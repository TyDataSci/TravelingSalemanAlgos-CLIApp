from collections import deque
from datetime import time
import algos
import csv_reader
import time_delta
from data_structs import HashTable
from package import Package
from algos import nearest_neighbor


# Delivery Hub used to create trucks, packages and manage both efficiently.
# Stores package id, map_direction, and adjacency_matrix hash tables as well as multiple lists packages
# so that algorithm will only need to be called one time initialization and used until program completion--> O(n^2)
class Depot:
    def __init__(self):
        self.inventory = []
        self.north_bound_ready = []
        self.north_bound_hold = []
        self.south_bound_ready = []
        self.south_bound_hold = []
        self.must_be_together = []
        self.must_be_together_direction = None
        self.correct_bad_address = [{'id': '9', 'address': '410 S State St',
                                     'zip': 'Salt Lake City', 'city': '84111',
                                     'vertex': 19}]
        self.package_id_lookup = HashTable()
        self.adjacency_matrix = csv_reader.adjacency_matrix()
        self.map_direction = algos.map_direction(self.adjacency_matrix)


    # Creates all packages, places them in inventory, creates package lookup hash table using package ID --> O(n)
    def receive_packages(self):
        for item in csv_reader.get_package_ids():
            pkg = Package(item)
            pkg.at_hub = time_delta.Time(8, 0).clock_time
            self.inventory.append(pkg)
            self.package_id_lookup.add(pkg.info['package ID number'], pkg)

    # Sorts truck inventory a second time to compensated for a special update to original order: Origin:hub --> O(n^2)
    @staticmethod
    def reroute_truck(truck):
        truck.inventory = deque(nearest_neighbor(0, truck.depot.adjacency_matrix, list(truck.inventory)))

    # Sorts north bound ready inventory original order: Origin:hub --> O(n^2)
    def route_north_bound(self):
        self.north_bound_ready = nearest_neighbor(0, self.adjacency_matrix, self.north_bound_ready)

    # Sorts north bound ready inventory original order: Origin:Parameterized vertex --> O(n^2)
    def route_north_bound_with_priority(self, priority):
        self.north_bound_ready = nearest_neighbor(priority, self.adjacency_matrix, self.north_bound_ready)

    # Sorts south bound ready inventory original order: Origin:hub --> O(n^2)
    def route_south_bound(self):
        self.south_bound_ready = nearest_neighbor(0, self.adjacency_matrix, self.south_bound_ready)

    # Sorts south bound ready inventory original order: Origin:Parameterized vertex --> O(n^2)
    def route_south_bound_with_priority(self, priority):
        self.south_bound_ready = nearest_neighbor(priority, self.adjacency_matrix, self.south_bound_ready)

    # Sort Packages by there direction and ready/hold requirements as well as other special requirements --> O(n)
    def determine_truck_ready_hold(self, n_truck, s_truck):
        map_direction_lookup = self.map_direction
        for pkg in self.inventory:
            if map_direction_lookup[pkg.vertex] == 'North':
                if 'delayed' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(9, 5):
                    pkg.at_hub = time_delta.Time(9, 5).clock_time
                    self.north_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and n_truck.time.time_delta < time(10, 20):
                    self.north_bound_hold.append(pkg)
                else:
                    self.north_bound_ready.append(pkg)
            else:
                if 'delayed' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(9, 5):
                    pkg.at_hub = time_delta.Time(9, 5).clock_time
                    self.south_bound_hold.append(pkg)
                elif 'wrong address' in pkg.info['Special Notes'].lower() and s_truck.time.time_delta < time(10, 20):
                    self.south_bound_hold.append(pkg)
                else:
                    self.south_bound_ready.append(pkg)
        self.packages_must_be_together(['13', '14', '15', '16', '19', '20'])

    # Loads the north truck with mandatory packages first if they exist then with sorted priority --> O(n)
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
        if len(self.north_bound_ready) + len(self.north_bound_hold) > 0:
            truck.reload_needed = True
        else:
            truck.reload_needed = False

    # Loads the south truck with mandatory packages first if they exist then with sorted priority --> O(n)
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
        if len(self.south_bound_ready) + len(self.south_bound_hold) > 0:
            truck.reload_needed = True
        else:
            truck.reload_needed = False

    # pops any package in a hold queue whose time requirement has been met and places in a ready queue --> O(n)
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

    # Creates a list of packages that are required to stay together on the same truck --> O(n)
    def packages_must_be_together(self, special_packages):
        n_freq = 0
        s_freq = 0
        if not self.must_be_together:
            for pkg_id in special_packages:
                self.must_be_together.append(self.package_id_lookup[pkg_id])
        for pkg in self.must_be_together:
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

    # Displays the time of package 9 as its wrong address or correct address given the time --> O(1)
    def fix_wrong_address_display(self, time_input, pkg_id):
        if time_input.time() > time(10, 19):
            address = '410 S State St'
            zip_ = 'Salt Lake City'
            city = '84111'
        else:
            address = '300 State St'
            zip_ = 'Salt Lake City'
            city = '84103'
        pkg = self.package_id_lookup.get(pkg_id)
        if pkg:
            pkg.info['delivery address'] = address
            pkg.info['delivery city'] = zip_
            pkg.info['delivery zip code'] = city


# Requires name and depot to be initialized. Uses a deque data structure for efficient popleft functionality --> O(1)
class Truck:
    def __init__(self, name, depot):
        self.name = name
        self.depot = depot
        self.inventory = deque()
        self.time = time_delta.Time(8, 0)
        self.total_distance = 0
        self.speed = 18
        self.capacity = 16
        self.delivered = 0
        self.origin = 0
        self.reload_needed = False
        self.trip = 0

    # Checks inventory has room for additional package else stops load --> O(1)
    def load(self, package):
        if len(self.inventory) == self.capacity:
            return
        self.inventory.append(package)

    # Defines time as a function of miles --> O(1)
    def minutes_per_mile(self, distance):
        return round(60 / self.speed * distance, 0)

    # pops off the top package and delivers to package vertex. Given stored origin, calculates distance
    # traveled updating total distance and time --> O(1)
    def deliver(self):
        if len(self.inventory) == 0:
            return
        elif self.time.time_delta > time(10, 20):
            self.fix_wrong_address_package()
        current_package = self.inventory.popleft()
        current_package.info['trip'] = f'{self.name} Trip #{self.trip}'
        distance = float(self.depot.adjacency_matrix[current_package.vertex][self.origin])
        self.time.add(self.minutes_per_mile(distance))
        self.total_distance += distance
        current_package.info['delivery status'] = 'delivered'
        self.origin = current_package.vertex
        self.delivered += 1
        current_package.delivered = self.time.clock_time
        if len(self.inventory) == 0:
            self.return_to_hub()

    # Once truck is empty will return to hub, calculating distance by origin and hub, sets origin to hub --> O(1)
    def return_to_hub(self):
        distance = float(self.depot.adjacency_matrix[0][self.origin])
        self.time.add(self.minutes_per_mile(distance))
        self.total_distance += distance
        self.origin = 0

    # Return total distance of truck rounded to two decimals --> O(1)
    def get_total_distance(self):
        return round(self.total_distance, 2)

    # Once time requirement has been met, wrong address and vertex is updated to the correct address and vertex --> O(1)
    def fix_wrong_address_package(self):
        if self.depot.correct_bad_address:
            correct_address = self.depot.correct_bad_address[0]
            pkg = self.depot.package_id_lookup.get(correct_address['id'])
            if pkg:
                correct_address = self.depot.correct_bad_address.pop(0)
                pkg.info['vertex'] = correct_address['vertex']
                pkg.info['delivery address'] = correct_address['address']
                pkg.info['delivery city'] = correct_address['zip']
                pkg.info['delivery zip code'] = correct_address['city']
