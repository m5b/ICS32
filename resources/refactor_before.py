# blue, green, yellow, red
colors = ["#0000ff", "#008000", "#ffff00", "#ff0000"]

def main():
    option = input("Enter Color: ")

    if option == "all":
        for c in colors:
            print(c)
    elif option == "blue":
        for c in colors:
            if c == "#0000ff":
                print(c)
    elif option == "green":
        for c in colors:
            if c == "#008000":
                print(c)
    elif option == "yellow":
        for c in colors:
            if c == "#ffff00":
                print(c)
    elif option == "red":
        for c in colors:
            if c == "#ff0000":
                print(c)
    elif option.startswith("#"):
        for c in colors:
            if c == option:
                print("Color exists")
    elif option == "quit":
        return False
    else:
        print("Unknown option")
        
    return True

if __name__ == '__main__':
    run = True
    while run is True:
        run = main() 
