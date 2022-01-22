# Tyler Sanders #001230176
from interface import interface, run_simulator

if __name__ == '__main__':
    hub, truck1, truck2 = run_simulator()
    interface = interface(hub, truck1, truck2)
    interface.launch_interface()

