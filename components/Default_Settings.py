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
ETW = {
    'STANDARD': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'NAVY': 'QWERTZUIOPASDFGHJKLYXCVBNM'
    }

#Functions used to sort rotor_sequences.keys() into a logical order in frontend
def cat_sort(x):
    '''Sort by categories (Civilian, Main, 1942)'''
    score_x = 0
    if x[-1] == 'C':
        score_x = -1
    elif x in ('BETA', 'GAMMA'):
        score_x = 1
    return score_x
    
def numeral_sort(x):
    '''Lazy numeral sort, not worth making a proper parser for so few values'''
    numerals = {
                'I': 1,
                'II': 2,
                'III': 3,
                'IV': 4,
                'V': 5,
                'VI': 6,
                'VII': 7,
                'VII': 8,
                'IX': 9,
                'X': 10
                }
    string = ''.join([i for i in x if i in ('I','V','X')])
    return(numerals.get(string, 0))