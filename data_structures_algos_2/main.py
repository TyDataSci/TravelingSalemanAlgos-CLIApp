import csv_reader
import depot
from algos import nearest_neighbor
from time_delta import Time
if __name__ == '__main__':
    print('------------------------------')
    print('WGUPS Routing Program')
    print('------------------------------\n')
    print(f'Route was completed in {100:.2f} miles.\n')

    delivery_hub = depot.Depot()
    delivery_hub.receive_packages()
    north_bound_truck = depot.Truck()
    south_bound_truck = depot.Truck()
    south_bound_truck.time.add(66)
    delivery_hub.determine_truck_ready_hold(north_bound_truck, south_bound_truck)
    delivery_hub.route_south_bound()
    delivery_hub.route_north_bound()
    print('hub north ready: ', len(delivery_hub.north_bound_ready))
    print('hub south ready: ', len(delivery_hub.south_bound_ready))

    delivery_hub.load_north_bound(north_bound_truck)
    print('north truck inv:', len(north_bound_truck.inventory))
    delivery_hub.route_south_bound()
    print('south truck inv:', len(south_bound_truck.inventory))

    for pkg in list(north_bound_truck.inventory):
        print('North Delivery')
        north_bound_truck.deliver()

    delivery_hub.load_south_bound(south_bound_truck)
    for pkg in list(south_bound_truck.inventory):
        print('South Delivery')
        south_bound_truck.deliver()
    print('South packages hold remaining =', len(delivery_hub.south_bound_hold))
    print('South packages ready remaining =', len(delivery_hub.south_bound_ready))
    print('North packages hold remaining =', len(delivery_hub.north_bound_hold))
    print('North packages ready remaining =', len(delivery_hub.north_bound_ready))
    print('South Truck Total ', south_bound_truck.get_total_distance())
    print('North Truck Total ', north_bound_truck.get_total_distance())
    print('South Truck Total ', south_bound_truck.time.clock_time)
    print('North Truck Total ', north_bound_truck.time.clock_time)
    delivery_hub.ready_held_packages(north_bound_truck, south_bound_truck)
    delivery_hub.route_north_bound()
    delivery_hub.load_north_bound(north_bound_truck)
    delivery_hub.load_south_bound(south_bound_truck)
    for pkg in list(north_bound_truck.inventory):
        print('North Delivery')
        north_bound_truck.deliver()
    for pkg in list(south_bound_truck.inventory):
        print('South Delivery')
        south_bound_truck.deliver()
    print('South Truck Total ', south_bound_truck.get_total_distance())
    print('North Truck Total ', north_bound_truck.get_total_distance())
    print('South Truck Complete Time ', south_bound_truck.time.clock_time)
    print('North Truck Complete Time ', north_bound_truck.time.clock_time)

    #for pkg in delivery_hub.inventory:
    #    print(pkg)
    #    print(pkg.info)
    #    print('At hub:',pkg.at_hub)
    #    print('En Route:',pkg.en_route)
    #    print('Delivered:', pkg.delivered)
