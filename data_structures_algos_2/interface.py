import depot
from datetime import datetime


def run_simulator():
    delivery_hub = depot.Depot()
    delivery_hub.receive_packages()
    north_bound_truck = depot.Truck('North', delivery_hub)
    south_bound_truck = depot.Truck('South', delivery_hub)
    delivery_hub.determine_truck_ready_hold(north_bound_truck, south_bound_truck)
    south_bound_truck.time.add(_minutes_=66)
    delivery_hub.ready_held_packages(north_bound_truck, south_bound_truck)
    while delivery_hub.north_bound_ready or delivery_hub.south_bound_ready:
        delivery_hub.route_north_bound()
        delivery_hub.load_north_bound(north_bound_truck)
        delivery_hub.route_south_bound()
        delivery_hub.load_south_bound(south_bound_truck)
        while north_bound_truck.inventory:
            north_bound_truck.deliver()
        while south_bound_truck.inventory:
            south_bound_truck.deliver()
        delivery_hub.ready_held_packages(north_bound_truck, south_bound_truck)

    return delivery_hub, north_bound_truck, south_bound_truck


class Interface:
    def __init__(self, hub, truck1, truck2):
        self.hub = hub
        self.truck1 = truck1
        self.truck2 = truck2
        self.acceptable_input = ['0', '1', '2', '3', '4', '5', '6', 'p']
        self.command_not_allowed = []
        self.pandas = True

    def launch_interface(self, pandas=True):
        if pandas:
            try:
                from pandas import DataFrame
            except ImportError:
                print('This feature is not available.')
                self.command_not_allowed.append(self.acceptable_input.pop(self.acceptable_input.index('p')))
                self.launch_interface(pandas=False)
        self.pandas = pandas
        space = '\n' * 4
        print(space)
        print(f'-------------------------' * 2)
        print('\t\t\tWelcome to WGUPS')
        print('-------------------------' * 2)
        self.display_mileage()

    def display_mileage(self):
        total = f'\nAll packages were delivered in'
        total = f'{total} {round(self.truck1.get_total_distance() + self.truck2.get_total_distance(), 2)} miles.'
        total_each_trk = f'North Truck miles: {self.truck1.get_total_distance()}'
        total_each_trk = f'{total_each_trk}\nSouth Truck miles: {self.truck2.get_total_distance()}\n'
        print(total)
        print(total_each_trk)
        self.menu()

    def menu(self):
        print('-------------------------' * 2)
        print('\t\t\tWGUPS Program Menu')
        print('-------------------------' * 2)
        print('[1] Display Mileage Totals')
        print('[2] Display All Packages Info at Time of Day')
        print('[3] Display Package Deadline and Arrival Times')
        print('[4] Display Delayed Packages and En Route Times')
        print('[5] Display Special Requirements and Truck Trip')
        print('[6] Display Single Package By ID')
        if self.pandas:
            print('[p] Turn Pandas Table Display Off')
        else:
            print('[p] Turn Pandas Table Display On')
        print('[0] Exit Program')
        self.menu_input()

    def menu_input(self):
        acceptable_input = self.acceptable_input
        menu_input = str(input('Enter a Command:')).lower()
        if menu_input in self.command_not_allowed:
            print('This command is no longer accepted. Please try another.')
            self.menu_input()
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
        elif menu_input == '6':
            self.display_single_package()
        elif self.pandas and menu_input == 'p':
            self.launch_interface(pandas=False)
        elif not self.pandas and menu_input == 'p':
            self.launch_interface(pandas=True)
        elif menu_input == '0':
            print('Good bye.')
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
        self.hub.fix_wrong_address_display(time_input, '9')
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

        dict_table = {'package ID number': _id, 'delivery Address': _vx, 'delivery city': _dcty,
                      'delivery zip code': _dzip, 'package weight': _dwt, 'delivery deadline': _dd,
                      'delivery status': _sts, 'delivery status time': _sts_time
                      }
        if self.pandas:
            from pandas import DataFrame
            df = DataFrame(dict_table)
            print('\n', df.to_string(col_space=20,
                                     index=False))
        else:
            print('\n')
            for k, v in dict_table.items():
                temp = []
                for i in range(len(v)):
                    key_len = len(k)
                    val_len = len(str(dict_table[k][i]))
                    space_len = key_len - val_len
                    if space_len < 0:
                        temp.append(dict_table[k][i] + '|')
                    else:
                        space = ' '*space_len
                        temp.append(dict_table[k][i] + space + '\t|')
                dict_table[k] = temp
            for k in list(dict_table.keys()):
                key = k + '\t|'
                dict_table[key] = dict_table.pop(k)
            for each_row in zip(*([i] + j
                                  for i, j in dict_table.items())):
                print(*each_row, " ")

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
        dict_table = {'package ID number': _id,
                      'delivery deadline': _dd,
                      'delivered time': _dvt
                      }
        if self.pandas:
            from pandas import DataFrame
            df = DataFrame(dict_table)

            print('\n', df.to_string(col_space=20,
                                     index=False))
        else:
            print('\n')
            for k, v in dict_table.items():
                temp = []
                for i in range(len(v)):
                    key_len = len(k)
                    val_len = len(str(dict_table[k][i]))
                    space_len = key_len - val_len
                    if space_len < 0:
                        temp.append(dict_table[k][i] + '|')
                    else:
                        space = ' ' * space_len
                        temp.append(dict_table[k][i] + space + '\t|')
                dict_table[k] = temp
            for k in list(dict_table.keys()):
                key = k + '\t|'
                dict_table[key] = dict_table.pop(k)
            for each_row in zip(*([i] + j
                                  for i, j in dict_table.items())):
                print(*each_row, "  ")
        self.menu()

    def display_delayed_times(self):
        _id = []
        _athb = []
        _ent = []
        _spcn = []
        for pkg in self.hub.inventory:
            if 'delayed' in pkg.info['Special Notes'].lower():
                _id.append(pkg.info['package ID number'])
                _athb.append(pkg.at_hub)
                _ent.append(pkg.en_route)
                _spcn.append(pkg.info['Special Notes'])

        dict_table = {'package ID number': _id,
                      'special notes': _spcn,
                      'at hub time': _athb,
                      'en route time': _ent
                      }
        if self.pandas:
            from pandas import DataFrame
            df = DataFrame(dict_table)
            print('\n', df.to_string(col_space=25,
                                     index=False))
        else:
            print('\n')
            for k, v in dict_table.items():
                temp = []
                for i in range(len(v)):
                    key_len = len(k)
                    val_len = len(str(dict_table[k][i]))
                    space_len = key_len - val_len
                    if space_len < 0:
                        temp.append(dict_table[k][i] + '|')
                    else:
                        space = ' ' * space_len
                        temp.append(dict_table[k][i] + space + '\t|')
                dict_table[k] = temp
            for k in list(dict_table.keys()):
                key = k + '\t|'
                dict_table[key] = dict_table.pop(k)
            for each_row in zip(*([i] + j
                                  for i, j in dict_table.items())):
                print(*each_row, "  ")
        self.menu()

    def display_special_trip(self):

        _id = []
        _spcn = []
        _trp = []
        must_be_together = ['13', '14', '15', '16', '19', '20']
        for pkg in self.hub.inventory:
            if pkg.info['package ID number'] in must_be_together:
                _id.append(pkg.info['package ID number'])
                _spcn.append(pkg.info['Special Notes'])
                _trp.append(pkg.info['trip'])
            elif 'can only be' in pkg.info['Special Notes'].lower():
                _id.append(pkg.info['package ID number'])
                _spcn.append(pkg.info['Special Notes'])
                _trp.append(pkg.info['trip'])

        dict_table = {'package ID number': _id,
                      'trip': _trp,
                      'special notes': _spcn
                      }
        print('\nTruck #1: North Truck')
        print('Truck #2: South Truck')
        if self.pandas:
            from pandas import DataFrame
            df = DataFrame(dict_table)
            print(df.to_string(col_space=30,
                               index=False))
        else:
            for k, v in dict_table.items():
                temp = []
                for i in range(len(v)):
                    key_len = len(k)
                    val_len = len(str(dict_table[k][i]))
                    space_len = key_len - val_len
                    if space_len < 0:
                        temp.append(dict_table[k][i] + '|')
                    else:
                        space = ' ' * space_len
                        temp.append(dict_table[k][i] + space + '\t|')
                dict_table[k] = temp
            for k in list(dict_table.keys()):
                key = k + '\t|'
                dict_table[key] = dict_table.pop(k)
            for each_row in zip(*([i] + j
                                  for i, j in dict_table.items())):
                print(*each_row, " ")

        self.menu()

    def display_single_package(self):
        id_input = input('Enter a package ID:')
        try:
            check_id = int(id_input)
            if not 1 <= check_id <= 40:
                print('No package found. Please try again.')
                self.display_single_package()
        except ValueError:
            print('No package found. Please try again.')
            self.display_single_package()

        _id = []
        _vx = []
        _dd = []
        _dcty = []
        _dzip = []
        _dwt = []
        _sts = []
        _athub = []
        _enrt = []
        _dvt = []
        _spcn = []
        _trp = []
        pkg = self.hub.package_id_lookup.get(str(id_input))
        if pkg:
            _id.append(pkg.info['package ID number'])
            _vx.append(pkg.info['delivery address'])
            _dcty.append(pkg.info['delivery city'])
            _dzip.append(pkg.info['delivery zip code'])
            _dwt.append(pkg.info['package weight'])
            _dd.append(pkg.info['delivery deadline'])
            _sts.append(pkg.info['delivery status'])
            _athub.append(pkg.at_hub)
            _enrt.append(pkg.en_route)
            _dvt.append(pkg.delivered)
            _spcn.append(pkg.info['Special Notes'])
            _trp.append(pkg.info['trip'])

        dict_table = {'package ID': _id, 'delivery address': _vx, 'delivery city': _dcty,
                      'delivery zip code': _dzip, 'delivery weight': _dwt, 'delivery deadline': _dd,
                      'at hub time': _athub, 'en route time': _enrt, 'delivered time': _dvt,
                      'delivery status': _sts, 'truck trip': _trp, 'special notes': _spcn}
        if self.pandas:
            from pandas import DataFrame
            df = DataFrame(dict_table)
            print('\n', df.to_string(col_space=20,
                                     index=False))
        else:
            print('\n')
            for k, v in dict_table.items():
                temp = []
                for i in range(len(v)):
                    key_len = len(k)
                    val_len = len(str(dict_table[k][i]))
                    space_len = key_len - val_len
                    if space_len < 0:
                        temp.append(dict_table[k][i] + '|')
                    else:
                        space = ' ' * space_len
                        temp.append(dict_table[k][i] + space + '\t|')
                dict_table[k] = temp
            for k in list(dict_table.keys()):
                key = k + '\t|'
                dict_table[key] = dict_table.pop(k)
            for each_row in zip(*([i] + j
                                  for i, j in dict_table.items())):
                print(*each_row, " ")

        self.menu()
