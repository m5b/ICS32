from collections import namedtuple
import re #for regex operations

# Create a nametuple to store the results of the input processing.
# The namedtuple provides us with one convenient object to pass to
# other functions in the program that need to act on user inputs.
InputCommand = namedtuple('InputCommand', ['cmd','path','name','param','suffix','r','s','e','f'])

'''
Regular expression input processor
'''
regex = re.compile('\\s-(\\w+)')
def regex_processor(usr_input) -> InputCommand:
    inputs = regex.split(usr_input[2:])
    r = False
    e = False
    s = False
    f = False
    suffix = ''
    param = ''
    name = ''

    i=0
    for c in inputs:
        if c == 'r':
            r = True
        elif c == 'f':
            f = True
        elif c == 's':
            s = True
            param = inputs[i+1].strip()
        elif c == 'e':
            e = True
            suffix = inputs[i+1].strip()
        elif c == 'n':
            name = inputs[i+1].strip()
        i=i+1

    ic = InputCommand(usr_input[:1], inputs[0], name, param, suffix, r,s,e,f)
    return ic
    
