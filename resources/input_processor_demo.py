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
   
    # get length
    l = len(usr_input)
    
    # subtract 2 from l b/c we don't care about first two chars.
    for i in range(0,l-2):
        # work from right to left in 4 character segments
        seg = usr_input[(l-i)-4:l-i]
        print(seg)
        


TEST_INPUTS = [
    "L /home/mark 2",
    "L /home/mark -f",
    "L /home/mark -s bar.py",
    "L /home/mark -e py",
    "L /home/mark -r",
    "L /home/mark -r -f",
    "L /home/mark -r /foo -r -f",
    "L /home/mark -r /foo -f",
    "L /home/mark -r -s bar.py",
    "L /home/mark -r -e py",
    "C /home/mark -n foo.txt"
    ]

def main():
    #uncomment to test your own inputs
    #result = process_input(input())

    for t in TEST_INPUTS:
        print(t)
        
        print("------")
        print('\n')
        
        result = process_input(t)
    

if __name__ == '__main__':
    main()
