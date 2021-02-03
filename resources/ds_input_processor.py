from collections import namedtuple
import re #for regex operations

# Create a nametuple to store the results of the input processing.
# The namedtuple provides us with one convenient object to pass to
# other functions in the program that need to act on user inputs.
InputCommand = namedtuple('InputCommand', ['cmd','path','name','param','suffix','r','s','e','f'])

'''
Right to left input processor using string manipulation
'''
def process_input(usr_input) -> InputCommand:
    r_pos = 0
    es_pos = 0
    end_post = 0
    r = False
    e = False
    s = False
    f = False
    suffix = ''
    param = ''
    name = ''

    # get len
    l = len(usr_input)
    
    # subtract 2 from l b/c we don't care about first two chars.
    for i in range(0,l-2):
        # work from right to left in 4 character segments
        seg = usr_input[(l-i)-4:l-i]

        # check that r is false in case of path containing '-r'
        # to be sure that we have an option and not path
        if ' -r' in seg and r is False:
            r = True            
            r_pos = (l-i)-3
            
        # if a second option exists, then this r will be detected
        elif ' -r ' in seg and r is False:
            r = True            
            r_pos = (l-i)-4 #set current position to determine end of path
        elif ' -s ' in seg:
            s = True
            # set current position and assign remaining characters to name
            param = usr_input[(l-i):l]
            es_pos = (l-i)-4
        elif ' -e ' in seg:
            e = True
            # set current position and assign remaining characters to suffix
            suffix = usr_input[(l-i):l]
            es_pos = (l-i)-4
        # the f option will never have whitespace after it as it is always
        # the last option.
        elif ' -f' in seg:
            f = True
            es_pos = (l-i)-3
        # the f option will never have whitespace after it as it is always
        # the last option.
        elif ' -n ' in seg:
            name = usr_input[(l-i):l]
            es_pos = (l-i)-4

    #check results of loop, if no r was detected, then use es_pos
    if r_pos == 0:
        end_pos = es_pos
    else:
        end_pos = r_pos

    #if end_pos is still 0, then assume no options and set length of input as end point of path
    if end_pos == 0:
        end_pos = l

    ic = InputCommand(usr_input[:1], usr_input[2:end_pos],
                      name,param,suffix,r,s,e,f)
    return ic

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
    

TEST_INPUTS = [
    "L /home/mark 2",
    "L /home/mark -f",
    "L /home/mark -s bar.py",
    "L /home/mark -e py",
    "L /home/mark -r",
    "L /home/mark -r -f",
    "L /home/mark -r /foo -r -f",
    "L /home/mark -r -s bar.py",
    "L /home/mark -r -e py",
    "C /home/mark -n foo.txt"
    ]

def main():
    #uncomment to test your own inputs
    #result = process_input(input())

    for t in TEST_INPUTS:
        print(t)
        #uncomment to use regex or string manip
        result = process_input(t)
        #result = regex_processor(t)
        print("------")
        print("command", result.cmd)
        print("path", result.path)
        print("param", result.param)
        print("name", result.name)
        print("suffix", result.suffix)
        print("r",result.r)
        print("e",result.e)
        print("s",result.s)
        print("f",result.f)
        print("------")
        print('\n')
    
    #main()

if __name__ == '__main__':
    main()
