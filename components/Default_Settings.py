#Sequences of actual rotors used in WWII, format is name, sequences, turnover notch(es)
rotor_sequences = { 
    'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', ('Q')), 
    'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', ('E')),
    'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', ('V')),
    'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', ('J')), 
    'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', ('Z')),
    'VI': ('JPGVOUMFYQBENHZRDKASXLICTW', ('Z', 'M')),
    'VII': ('NZJHGRCXMYSWBOUFAIVLPEKQDT', ('Z', 'M')),
    'VIII': ('FKQHTLXOCBJSPDZRAMEWNIUYGV', ('Z', 'M')),
    'IC': ('DMTWSILRUYQNKFEJCAZBPGXOHV', ('Q')), #civilian
    'IIC': ('HQZGPJTMOBLNCIFDYAWVEUSRKX', ('Q')), #civilian
    'IIIC': ('UQNTLSZFMREHDPXKIBVYGJCWOA', ('Q')), #civilian
    'BETA': ('LEYJVCNIXWPBQMDRTAKZGFUHOS', None), #Position 4 Only
    'GAMMA': ('FSOKANUERHMBTIYCWLQPZXVGJD', None) #Position 4 Only
}

#Simple letter substitutions before the sequence is sent back through the rotors. Notably a letter cannot be encoded as itself here. 
reflector_sequences = {
    'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    'B Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
    'C Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
    'None': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #Early models had no reflector
}

#Entry wheel for Enigma I 
ETW = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
