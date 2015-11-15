from string import ascii_uppercase
from random import randrange #used for manual setup - allowing human choice of rotor positions creates bias
from .Enigma_Components import rotor, entry_wheel, reflector, rotor_array, plugboard
from .Default_Settings import reflector_sequences, rotor_sequences, ETW, cat_sort, numeral_sort

class enigma:
    """Broad container class for all enigma components and setup proceedures, acts to interface between the frontend and the subcomponents"""
    def __init__(self):
        self.main_entry_wheel = entry_wheel() 
        self.rotors = rotor_array()
        self.main_reflector = reflector()
        self.main_plugboard = plugboard()

    def default_setup(self):
        """Set of default rotors, reflectors and plugs, useful for testing"""
        pairs = "" #No point having a plugboard really, commercial Enigmas didn't have them.

        if pairs != "": #Incase anyone really wants one
            pairs = pairs.split(" ") 
            self.main_plugboard.set(pairs)
            
        self.main_entry_wheel.set(ETW['STANDARD'])

        rotor_spec = rotor_sequences['I']
        rotor_spec2 = rotor_sequences['II']
        rotor_spec3 = rotor_sequences['III']

        self.rotors.add_rotor(rotor_spec[0], 0, rotor_spec[1])
        self.rotors.add_rotor(rotor_spec2[0], 0, rotor_spec2[1])
        self.rotors.add_rotor(rotor_spec3[0], 0, rotor_spec3[1])

        self.main_reflector.set(reflector_sequences['A'])

    def manual_setup(self):
        """Allows the user to manually define all components of the device"""
        self.choose_entry_wheel()
        self.choose_rotors()
        self.choose_reflector()
        self.set_rotor_positions()
        self.configure_plugboard()

        print("\nCurrent Enigma Setup: \n")
        self.print_setup()
        
    def choose_entry_wheel(self):
        """Acts as part of the key in the naval version only"""
        available_ETW = list(ETW.keys())
        ETW_choice = None

        print("Available Entry Wheels: ", ', '.join(available_ETW))
        while ETW_choice not in available_ETW:
            ETW_choice = input("Choose Entry Wheel.\n> ").upper()
        self.main_entry_wheel.set(ETW[ETW_choice])

    def choose_rotors(self):
        """Choose rotors from the set of historic rotors in default_settings.py"""
        rotor_choice = None
        remaining_rotors = list(rotor_sequences.keys())
        remaining_rotors.sort(key=lambda x: (cat_sort(x), numeral_sort(x))) #Sort the rotors into three categories, then by numeral within categories

        #Choose number of rotor
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
        """The starting rotations of the rotors acts as a key for the the code"""
        rotor_position_start = None
        randomise = None
        while randomise not in ('manual', 'random'):
            randomise = input('Enter \'manual\' for custom positions or \'random\' for randomly generated positions:\n> ').lower() #non random rotor positions made crytoanalysis easier historically
        for index, rotor in enumerate(self.rotors.rotors):
            if randomise == 'manual':
                while rotor_position_start not in map(str, list(range(1,27))): #Check a valid number was entered
                    rotor_position_start = input('Please enter starting position for rotor {} between 1 and 26.\n> '.format(index + 1))
            elif randomise == 'random':
                rotor_position_start = randrange(1,27)
            rotor.set_position(int(rotor_position_start) - 1) #Subtract 1 from the index due to 0 indexing of rotors
            rotor_position_start = None #reset this so it works next time

    def choose_reflector(self):
        """Essentially acts as another part of the key"""
        available_reflectors = list(reflector_sequences.keys())
        reflector_choice = None

        print("Available Reflectors: ", ', '.join(available_reflectors))
        while reflector_choice not in available_reflectors:
            reflector_choice = input("Choose reflector.\n> ")
        self.main_reflector.set(reflector_sequences[reflector_choice])

    def configure_plugboard(self):
        """Allows for letter swapping hence greatly increases entropy"""
        plugs = None
        plugs_to_add = []
        used_letters = []
        letters = list(ascii_uppercase)

        #Choose number of plugs, 26 letter so 13 possible connections
        while plugs not in map(str, list(range(0,14))):
            plugs = input("Enter number of connections, Must be a number between 0 and 13.\n> ").upper()
        
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
        """Take a string and split it before feeding it through enigma element wise"""
        output = ''.join(list(map(self.encode, list(message))))
        return output

    def encode(self, letter):
        """Encoding a single letter, note that the process is mirrored before and after the reflector hence reversible"""
        self.rotors.rotate_rotors() #Historically occured before the letter is encoded
        letter = self.main_plugboard.substitute(letter)
        letter = self.main_entry_wheel.forwards_encode(letter)
        letter = self.rotors.encode(letter)
        letter = self.main_reflector.reflect(letter) #No letter can ever encode itself
        letter = self.rotors.reverse_encode(letter)
        letter = self.main_entry_wheel.backwards_encode(letter)
        letter = self.main_plugboard.substitute(letter)
        
        return letter

    def print_setup(self):
        """Print the current enigma component settings"""
        print(self.main_entry_wheel)
        for i, i_rotor in enumerate(self.rotors.rotors):
            print("Rotor ", i + 1)
            print(i_rotor)
        print(self.main_reflector)
        print(self.main_plugboard)
