import depot
import pandas as pd
from datetime import datetime


def run_simulator():
    delivery_hub = depot.Depot()
    delivery_hub.receive_packages()
    north_bound_truck = depot.Truck('North')
    south_bound_truck = depot.Truck('South')
    delivery_hub.determine_truck_ready_hold(north_bound_truck, south_bound_truck)
    south_bound_truck.time.add(66)
    delivery_hub.ready_held_packages(north_bound_truck, south_bound_truck)
    delivery_hub.route_north_bound()
    delivery_hub.load_north_bound(north_bound_truck)
    for pkg in list(north_bound_truck.inventory):
        north_bound_truck.deliver()
    delivery_hub.route_south_bound()
    delivery_hub.load_south_bound(south_bound_truck)
    for pkg in list(south_bound_truck.inventory):
        south_bound_truck.deliver()
    delivery_hub.ready_held_packages(north_bound_truck, south_bound_truck)
    delivery_hub.route_north_bound()
    delivery_hub.load_north_bound(north_bound_truck)
    delivery_hub.load_south_bound(south_bound_truck)
    for pkg in list(north_bound_truck.inventory):
        north_bound_truck.deliver()
    for pkg in list(south_bound_truck.inventory):
        south_bound_truck.deliver()

    return delivery_hub, north_bound_truck, south_bound_truck


class interface:
    def __init__(self, hub, truck1, truck2):
        self.hub = hub
        self.truck1 = truck1
        self.truck2 = truck2

    def launch_interface(self):
        print('------------------------------')
        print('Welcome to WGUPS')
        print('------------------------------')
        self.display_mileage()

    def display_mileage(self):
        print(
            f'\nAll packages were delivered in {round(self.truck1.get_total_distance() + self.truck2.get_total_distance(), 2)} miles.')
        print(
            f'North Truck miles: {self.truck1.get_total_distance()}\nSouth Truck miles: {self.truck2.get_total_distance()}\n')
        self.menu()

    def menu(self):
        print('------------------------------')
        print('Program Menu')
        print('------------------------------')
        print('[1] Display Mileage Totals')
        print('[2] Display All Packages Data')
        print('[3] Display Package Deadline and Arrival Times')
        print('[4] Display Delayed Packages and En Route Times')
        print('[5] Display Special Requirements and Truck Trip')
        print('[0] Exit Program')
        self.menu_input()

    def menu_input(self):
        acceptable_input = ['0', '1', '2', '3', '4', '5']
        menu_input = str(input('Enter Command:'))
        if menu_input not in acceptable_input:
            print('Command not recognized. Please try again.')
            self.menu_input()
        if menu_input == '1':
            self.display_mileage()
        elif menu_input == '2':
            self.display_pkg_table()
        elif menu_input == '3':
            self.display_arrival_times()
        elif menu_input == '4':
            self.display_delayed_times()
        elif menu_input == '5':
            self.display_special_trip()
        elif menu_input == '0':
            return

    def display_pkg_table(self):
        time_input = input('Enter a time in HH:MM format:')
        try:
            time_input = datetime.strptime(time_input, '%H:%M')
        except ValueError:
            print('Format must be HH:MM. Please try again.')
            self.display_pkg_table()

        _id = []
        _vx = []
        _dd = []
        _dcty = []
        _dzip = []
        _dwt = []
        _dvt = []
        _sts = []
        _sts_time = []
        _trp = []
        self.hub.fix_wrong_address_display(time_input)
        for pkg in self.hub.inventory:
            if datetime.strptime(pkg.delivered, '%H:%M %p') > time_input:
                if datetime.strptime(pkg.en_route, '%H:%M %p') > time_input:
                    _sts.append('at hub')
                    _sts_time.append(pkg.at_hub)
                else:
                    _sts.append('en route')
                    _sts_time.append(pkg.en_route)
            else:
                _sts.append('delivered')
                _sts_time.append(pkg.delivered)

            _id.append(pkg.info['package ID number'])
            _vx.append(pkg.info['delivery address'])
            _dcty.append(pkg.info['delivery city'])
            _dzip.append(pkg.info['delivery zip code'])
            _dwt.append(pkg.info['package weight'])
            _dd.append(pkg.info['delivery deadline'])
            _dvt.append(pkg.delivered)
            _trp.append(pkg.info['trip'])

        df = pd.DataFrame({'package ID number': _id, 'delivery Address': _vx, 'delivery deadline': _dd,
                           'delivery city': _dcty, 'delivery zip code': _dzip, 'package weight': _dwt,
                           'delivery status': _sts, 'delivery status time': _sts_time
                           })
        print('\n', df.to_string(col_space=20,
                                 index=False))
        self.menu()

    def display_arrival_times(self):
        _id = []
        _dd = []
        _dvt = []
        _trp = []
        for pkg in self.hub.inventory:
            _id.append(pkg.info['package ID number'])
            _dd.append(pkg.info['delivery deadline'])
            _dvt.append(pkg.delivered)

        df = pd.DataFrame({'package ID number': _id,
                           'delivery deadline': _dd,
                           'delivered time': _dvt
                           })

        print('\n', df.to_string(col_space=20,
                                 index=False))
        self.menu()

    def display_delayed_times(self):
        _id = []
        _ent = []
        _spcn = []
        for pkg in self.hub.inventory:
            if 'delayed' in pkg.info['Special Notes'].lower():
                _id.append(pkg.info['package ID number'])
                _ent.append(pkg.en_route)
                _spcn.append(pkg.info['Special Notes'])

        df = pd.DataFrame({'special notes': _spcn,
                           'package ID number': _id,
                           'en route time': _ent

                           })

        print('\n', df.to_string(col_space=25,
                                 index=False))
        self.menu()

    def display_special_trip(self):
        _id = []
        _spcn = []
        _trp = []
        must_be_together = ['13', '14', '15', '16', '19', '20']
        for pkg in self.hub.inventory:
            if 'can only' in pkg.info['Special Notes'].lower() or 'must be' in pkg.info['Special Notes'].lower():
                _id.append(pkg.info['package ID number'])
                _spcn.append(pkg.info['Special Notes'])
                _trp.append(pkg.info['trip'])
            elif pkg.info['package ID number'] in must_be_together:
                _id.append(pkg.info['package ID number'])
                _spcn.append(pkg.info['Special Notes'])
                _trp.append(pkg.info['trip'])
        df = pd.DataFrame({'package ID number': _id,
                           'trip': _trp,
                           'special notes': _spcn
                           })
        print('\nTruck #1: North Truck')
        print('Truck #2: South Truck')
        print(df.to_string(col_space=30,
                           index=False))
        self.menu()
