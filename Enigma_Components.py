from string import ascii_uppercase #I'll use the index of letters in this to create the rotors

class rotor:
    def __init__(self, output_sequence, position, turnover_notches):
        self.position = position
        self.input_sequence = ascii_uppercase[self.position:] + ascii_uppercase[:self.position] 
        self.output_sequence = output_sequence
        self.turnover_notches = turnover_notches #Only useful for debugging
        if turnover_notches != None:
            self.turnover_indexes = [self.input_sequence.index(i) + 1 for i in turnover_notches] #We need the turnover position as an int so it matches the position, + 1 as the rotation occurs after the letter not before
        else:
            self.turnover_indexes = None #will never turn

    def set_position(self, position): #Set the rotor so encoding/decoding starts on same setting
        self.position = position

    def rotate(self):
        self.position += 1

        if self.position == 26: #rotor has performed a full rotation so reset
            self.position = 0

        self.input_sequence = ascii_uppercase[self.position:] + ascii_uppercase[:self.position] 

    def encode_letter(self, letter): #First time through the rotors forwards
        input_index = self.input_sequence.index(letter)
        output_letter = self.output_sequence[input_index]

        return output_letter

    def reverse_encode_letter(self, letter):  # second time through rotors backwards
        input_index = self.output_sequence.index(letter)
        output_letter = self.input_sequence[input_index]

        return output_letter

    def __str__(self): #Print out the current rotor details for debugging
        variables = [self.input_sequence,
                     self.output_sequence,
                     self.position + 1,
                     self.input_sequence[self.position],
                     self.turnover_notches,
                     self.turnover_indexes
                    ]
        return('In:  {0[0]}\nOut: {0[1]}\nPosition {0[2]} ({0[3]})\nNotches {0[4]} ({0[5]})\n'.format(variables))
             
class reflector:
    def __init__(self):
        self.l_index = ascii_uppercase
        self.reciprocal = None

    def set(self, reciprocal):
        self.reciprocal = reciprocal

    def reflect(self, letter):
        letter_index = self.l_index.index(letter)
        return self.reciprocal[letter_index]

    def __str__(self):
        return "Reflector:\nIn:  {0}\nOut: {1}".format(self.l_index, self.reciprocal)

class rotor_array:
    def __init__(self):
        self.rotors = [] # a place to store any number of rotors!

    def add_rotor(self, output_sequence, position, turnover_notches):
        rotor_init = rotor(output_sequence, position, turnover_notches)
        self.rotors.append(rotor_init)

    def encode(self, letter): #Before reflector
        for i in self.rotors: #iterate through all rotors
            letter = i.encode_letter(letter)
        return letter

    def reverse_encode(self, letter):
        reverse_rotors = self.rotors[::-1] #after the reflector the letters are passed through the rotors backwards.
        for i in reverse_rotors: #iterate through all rotors
            letter = i.reverse_encode_letter(letter)
        return letter

    def rotate_rotors(self):
        current_rotor = 0
        self.rotors[current_rotor].rotate() #first rotor always rotates
        while self.rotors[current_rotor].position in self.rotors[current_rotor].turnover_indexes: #check if we need to rotate the next rotor
            current_rotor += 1 
            self.rotors[current_rotor].rotate()

#The plugboard swaps pairs of letters pre encoding. Usually supplied with 10 wires allowing for 10 AB pairs
class plugboard:
    def __init__(self):
        self.used_letters = []
        self.letter_pairs = {}

    def set(self, pairs):
        assert len(''.join(pairs)) == len(set(''.join(pairs))), "Letter contained in plugboard twice!"
        for pair in pairs:
            first, second = pair[0], pair[1]
            self.letter_pairs[first] = second
            self.letter_pairs[second] = first

    def substitute(self, letter):
        return self.letter_pairs.get(letter, letter) #if no plug set then letter passes through

    def __str__(self):
        return '\nPlugboard:\n' + ' '.join([''.join(i) for i in self.letter_pairs.items()])
