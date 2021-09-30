# blue, green, yellow, red
colors = [["blue","#0000ff"], ["green","#008000"], ["yellow","#ffff00"], ["red","#ff0000"]]

def color_lookup(color: str) -> str:
    result = "None"
    for c in colors:
        if c[0] == color:
            result = c[1]
        
    return result

def main():
    option = input("Enter Color: ")

    if option == "all":
        for c in colors:
            print(c)
    elif option.startswith("#"):
        for c in colors:
            if c == option:
                print("Color exists")
    elif option == "quit":
        return False
    else:
        result = color_lookup(option)
        if result == "None":
            print("Unknown")
        else:
            print(result)
        
    return True

if __name__ == '__main__':
    run = True
    while run is True:
        run = main()
