import model
from model import package

if __name__ == '__main__':
    print('------------------------------')
    print('WGUPS Routing Program')
    print('------------------------------\n')
    print(f'Route was completed in {100:.2f} miles.\n')
    new = model.package.Package()
    print(new.info['package ID number'])
    user_input = input("""
    Please select an option below to begin or type 'quit' to quit:
        1. Get info for all packages at a particular time
        2. Get info for a single package at a particular time
    """)

