# Tyler Sanders #001230176
from interface import interface, run_simulator

if __name__ == '__main__':
    hub, truck1, truck2 = run_simulator()
    interface = interface(hub, truck1, truck2)
    try:
        interface.launch_interface()
    except ImportError:
        interface.launch_interface(pandas=False)
