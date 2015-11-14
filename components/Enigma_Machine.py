from string import ascii_uppercase
from .Enigma_Components import rotor, reflector, rotor_array, plugboard
from .Default_Settings import reflector_sequences, rotor_sequences, ETW

class enigma:
    """Broad container class for all enigma components and setup proceedures, acts to interface between the frontend and the subcomponents"""
    def __init__(self):
        self.rotors = rotor_array()
        self.main_reflector = reflector()
        self.main_plugboard = plugboard()

    def default_setup(self):
        pairs = "" #No point having a plugboard really, commercial Enigmas didn't have them.

        if pairs != "": #Incase anyone really wants one
            pairs = pairs.split(" ") 
            self.main_plugboard.set(pairs)

        rotor_spec = rotor_sequences['I']
        rotor_spec2 = rotor_sequences['II']
        rotor_spec3 = rotor_sequences['III']

        self.rotors.add_rotor(rotor_spec[0], 0, rotor_spec[1])
        self.rotors.add_rotor(rotor_spec2[0], 0, rotor_spec2[1])
        self.rotors.add_rotor(rotor_spec3[0], 0, rotor_spec3[1])

        self.main_reflector.set(reflector_sequences['A'])

    def manual_setup(self):
        self.choose_rotors()
        self.choose_reflector()
        self.set_rotor_positions()
        self.configure_plugboard()

        print("\nCurrent Enigma Setup: \n")
        self.print_setup()

    def choose_rotors(self):
        rotor_choice = None
        remaining_rotors = list(rotor_sequences.keys())

        #Choose number of rotors
        #limited to 4 for historic reasons and because additional rotors lose functionality due to rarity of turning
        Num_Rotors = input("Enter Desired Number of Rotors (up to 4).\n> ")
        while Num_Rotors not in ["1", "2", "3", "4"]:
            Num_Rotors = input("Entry Must be a number between 1 and 4.\n> ")

        for i in range(1, int(Num_Rotors) + 1):
            print("Available rotors: ", ', '.join(remaining_rotors))
            while rotor_choice not in remaining_rotors: #Only allow user to select one of each rotor
                rotor_choice = input("Enter Rotor {} name.\n> ".format(i)).upper()
                
            self.rotors.add_rotor(rotor_sequences[rotor_choice][0], 0, rotor_sequences[rotor_choice][1]) #add the desired rotor
            remaining_rotors.remove(rotor_choice)

    def set_rotor_positions(self):
        rotor_position_start = None
        for index, rotor in enumerate(self.rotors.rotors):
            while rotor_position_start not in map(str, list(range(1,27))): #Check a valid number was entered
                rotor_position_start = input('Please enter starting position for rotor {}.\n> '.format(index + 1))
            rotor.set_position(int(rotor_position_start) - 1) #Subtract 1 from the index due to 0 indexing of rotors
            rotor_position_start = None #reset this so it works next time

    def choose_reflector(self):
        available_reflectors = list(reflector_sequences.keys())
        reflector_choice = None

        print("Available Reflectors: ", ', '.join(available_reflectors))
        while reflector_choice not in available_reflectors:
            reflector_choice = input("Choose reflector.\n> ")
        self.main_reflector.set(reflector_sequences[reflector_choice])

    def configure_plugboard(self):
        plugs = None
        plugs_to_add = []
        used_letters = []
        letters = list(ascii_uppercase)

        #Choose number of plugs, 26 letter so 13 possible connections
        while plugs not in map(str, list(range(0,14))):
            plugs = input("Enter number of connections, Must be a number between 0 and 13.\n> ")
        
        if plugs != '0':
            for i in range(int(plugs)):
              pair = 'aa'
              while pair[0] not in letters or pair[1] not in letters:
                    pair = input("Enter plug pair, should be in the format AB. \nAvailable plugs: {}.\n> ".format(''.join(letters)))
              letters.remove(pair[0])
              letters.remove(pair[1])
              plugs_to_add.append(pair.upper())

            self.main_plugboard.set(plugs_to_add)

    def run(self, message):
        message = list(message.upper().replace(' ', '')) #convert to a list so we can map it
        assert len([i for i in message if i not in ascii_uppercase]) == 0, 'String contains invalid characters! Only letters are allowed.'

        output = ''.join(list(map(self.encode, message)))
        return output

    def encode(self, letter):
        self.rotors.rotate_rotors() #Occurs before the letter is encoded
        letter = self.main_plugboard.substitute(letter)
        letter = self.rotors.encode(letter)
        letter = self.main_reflector.reflect(letter) #No letter can ever encode itself
        letter = self.rotors.reverse_encode(letter)
        letter = self.main_plugboard.substitute(letter)
        
        return letter

    def print_setup(self):
        for i, i_rotor in enumerate(self.rotors.rotors):
            print("Rotor ", i)
            print(i_rotor)
        print(self.main_reflector)
        print(self.main_plugboard)
