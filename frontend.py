from copy import deepcopy
from components import Enigma_Machine

def main():
    print("Enigma Simulator")
    
    encoding_enigma = Enigma_Machine.enigma() #Create engima with no settings
    closed = False #Used to end the script
    original_settings = None # Used to store a copy of original settings, allows for decoding
    setup_mode = None #Manual or custom setup
    
    help = '''\n\'Encode\': Encode/Decode a message
    \'Rotors\': Change rotor positions
    \'Reset\': Go to original settings
    \'Settings\': Display current settings
    \'Help\': Show this message again
    \'Close\': Close the simulator'''

    while setup_mode not in ['manual', 'default']:
        print('Type manual for manual setup or default for default settings.')
        setup_mode = input('> ').lower()
        
    if setup_mode == 'manual':
        encoding_enigma.manual_setup()
    else:
        encoding_enigma.default_setup()
    original_settings = deepcopy(encoding_enigma) #much easier than keeping a record of settings

    print(help)
    while not closed:
        user_input = input('> ').lower() #From hereon its really simple text detection
        
        if user_input == 'encode':
            message = input('Enter message using acsii letters only: ')
            print('Encoding \'{}\''.format(message))
            message = encoding_enigma.run(message)
            print('Encoded string \'{}\''.format(message))
        elif user_input == 'rotors':
            encoding_enigma.set_rotor_positions()
        elif user_input == 'reset':
            encoding_enigma = deepcopy(original_settings)
        elif user_input == 'settings':
            encoding_enigma.print_setup()
        elif user_input == 'help':
            print(help)
        elif user_input == 'close':
            closed = True
        else:
            print('Input unknown, use \'help\' for a list of commands. ')

if __name__ == '__main__':      
    main()
