Week 5 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

```{attention}
I have decided to update the lectures for this week. I will have them up by mid-day Tuesday. Thanks!
```
## Week 5 Overview

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results5`

(lecture-materials)=
## Lecture Materials

Lectures for Week 5
: {ref}`lectures:adv_classes`
: {ref}`lectures:inheritance`



(lectures:adv_classes)=
### Advanced Classes

In the week 3 lecture notes you learned about the concept of classes. In that lecture, we described a class as a

> template for objects that perform state and behavior operations in program code

You learned how to write code to define a class, how class construction works, and how to work with class attributes. If you are still feeling a little uncertain about how to _create_ a class, take a little time to review the first lecture and practice creating a few custom classes of your own design. When you're ready, return here and continue reading!

A class is a powerful structure to help you both reason about your program design and maintain a high level of code reuse. Let's jump into a familiar example. In A2, you were required to extract input commands from a user that determined what actions your program should take. Since we had not learned about classes when you started building your input processing logic, you likely started writing functions in your main module to fulfill the requirement. Now, as you begin work on A3, you might be feeling a bit overwhelmed by the need to maintain and extend your earlier work. So for this lecture, let's refactor our input processing code into a nice, clean, reusable class.

```{admonition} Hint
:class: tip

This lecture will provide you with a nice overview on how to perform a refactor! If you are interested in submitting an assignment 2 refactor, this should be a good guide. Just remember, you don't have to refactor the portion of your program covered here and refactors are always optional!
```

We'll start with a pseudo code example that loosely reflects the most common approach that we have seen in your programs.

```python3

def input_command(command):
    if command[:1] == "L":
        L(command)
    elif command[:1] == "C":
        C(command)
    elif command[:1] == "R":
        R(command)
    elif command[:1] == "D":
        D(command)
    else:
        #etc

```

As in the example above, the most common approach that we see in a1 and a2 is to break up the commands into their own functions, each running very similar operations. There are a couple of concerns with this approach. First, large conditional statements become increasingly complex as they grow. Individual statements typically need multiple branch points, nested conditionals, and new variables, all of which make tracking the flow of execution difficult. We can reduce some of these concerns by organizing our code into classes. Let's start by rethinking how commands are identified.

```python3
from enum import Enum

class CommandType(Enum):
    CREATE = "C"
    DELETE = "D"
    EDIT = "E"
    LIST = "L"
    OPEN = "O"
    PRINT = "P"
    READ = "R"
    QUIT = "Q"
```

The first class we'll create is an [enumeration](https://docs.python.org/3/library/enum.html). Enum's provide a set of symbolic names, tied to custom values, that are **`constant`** and support **`iteration`**. Notice that each of the required commands has now been tied to a programmatic name that is more expressive. This expressiveness is not required, but it certainly will make our code more readable. We also have a clear, straightforward way to extend our program with new commands when the need arises. Now, rather than use this enum of commands in a long conditional branch, we can take advantage of iteration to find the one that matches the user input.

```python3

for c in CommandType:
    if c.value == self._input_cmd[:1]:
        self._input_data.command = c

```

Notice how the **`CommandType`** class sort of accepts a parameter of type **`Enum`** in the class definition? This is called inheritance and it's a concept we will look at more closely in the next {ref}`lecture <lectures:inheritance>`. For now, just imagine that by _inheriting_ from **`Enum`** the **`CommandType`** class already has some functionality built-in, even before we add our custom command names and values. One of those functions is the ability to iterate, another is that we don't need to _instantiate_ this class to use it. Instead, we simply reference each member symbolically whenever we need to validate an input command.

In the code above, each member of the **`CommandType`** class is compared to the first character of an input command. If the command is found, then a variable is set. Hopefully this looks a little bit easier to understand than the conditional equivalent we started with above! Now let's take a look at the variable **`_input_data`**. Notice that it has an member called **`command`** that is used to store the **`CommandType`** identified in the for loop. So it must be an object of some type, right? Here's the declaration:

```python3
@dataclass
class InputData:
    command: CommandType = None
    path: Path = None
    isrecursive: bool = None
    isfileonly: bool = None
    suffix: str = None
    name: str = None
    param: str = None
```

The **`InputData`** class represents another way to think about using classes. Notice that there are no functions, just attributes that we can use to store the data we expect to receive from an input command. When using a class this way, it effectively becomes an object for storing data. If you plan on using a class as a data store, you can ask python to automatically configure it to behave like one by adding the **`@dataclass`** decorator. Take a look at the following two print statements, the first is the **`InputData`** class _with_ the **`@dataclass`** decorator and the second is without:

```python3
# shell output with @dataclass decorator
>>> InputData(command=<CommandType.LIST: 'L'>, path=PosixPath('/home/mark/ics32'), isrecursive=True, isfileonly=True, suffix='', name='', param=None)

# shell output without @dataclass decorator
>>> <__main__.InputData object at 0x7fc1c6354340>
```

If we wanted, we could reproduce the shell output that **`@dataclass`** provides by overriding the class's **`__repr__`** method like so:

```python3
class InputData:
    command: CommandType = None
    path: Path = None
    isrecursive: bool = None
    isfileonly: bool = None
    suffix: str = None
    name: str = None
    param: str = None

    def __repr__(self) -> str:
        return 'InputData('f'name={self.command!r}, path={self.path!r}, ' \
            f'isrecursive={self.isrecursive}, isfileonly={self.isfileonly}, ' \
            f'suffix={self.suffix}, name={self.name}, param={self.param})'
```

In addition to the string representation function, the **`@dataclass`** decorator also automatically generates a hash, equality, and comparison methods. When combined, the use of the **`@dataclass`** decorator conveniently reduces the amount of boilerplate code you have to write and look at when reasoning about your program.

Using a class to store data provides us with a few advantages. Now, we could accomplish the same thing with a **`namedtuple`**, in fact, you may have noticed in previous examples of the input processing code I demonstrated in class a **`namedtuple`** _was_ used to store processed data. Generally, either approach will work, but a **`dataclass`** ultimately provides your code with increased flexibility. Unlike a **`namedtuple`** _you_ can choose whether or not you want your data attributes to be immutable (they are mutable by default). There are other advantages too, for example, you might decide to expand a **`dataclass`** with an attribute type that needs some custom preparation on set (sorting a dictionary, validation, and so on). If needed, a **`dataclass`** can support class methods to handle this work internally to the class, rather than an external processing function.

Okay, so now that we have removed the need for a large branching conditional statement and established a convenient way to store the data we collect, let's zoom out a bit more and look at how this enumeration class can be used in a more complete program.

```python3

class InputHandlerException(Exception):
    pass

class InputHandler:
    _input_cmd: str = None
    _input_data: InputData = None

    def __init__(self, input_command: str):
        if input_command != None and \
                len(input_command) > 0:
            self._input_cmd = input_command
            self._input_data = InputData()
        else:
            raise ValueError(
                "input command must be a str with at least one character.")

    def process(self) -> InputData:
        try:
            self._extract_command()
            end_pos = self._extract_options()
            self._extract_path(end_pos)

            return self._input_data
        except Exception as e:
            raise InputHandlerException(e)

    def _extract_command(self):
        for c in CommandType:
            if c.value == self._input_cmd[:1]:
                self._input_data.command = c

        if self._input_data.command is None:
            raise ValueError("Command is either invalid or unsupported")

    def _extract_options(self) -> int:
        r_pos = 0
        es_pos = 0
        r = False
        f = False
        suffix = ''
        name = ''
				
        # insert missing processing code ;)

        self._input_data.isfileonly = f
        self._input_data.isrecursive = r
        self._input_data.suffix = suffix
        self._input_data.name = name

        return end_pos

    def _extract_path(self, end_pos: int):
        # get path
        p_str = self._input_cmd[2:end_pos].rstrip()

        # create a path object from path string
        # and check if valid
        path = Path(p_str)
        if path.exists():
            self._input_data.path = path
        else:
            raise NotADirectoryError("The specified path could not be found")
```

Our final two uses of the python class come in the form of a traditional class and a class inherited from an existing class. The latter is represented by the **`InputHandlerException`** class (_inherits_ from the base **`Exception`** class), which is used to narrow the types of exceptions the **`InputHandler`** class will raise. A discussion on the use of exceptions in this example is a bit beyond the scope of the lecture, so we won't spend too much time on the choices made here. However, you should pay attention to how the **`InputHandler`** class _bubbles_ the exceptions that it raises. The only _public_ method in this class is the **`process`** method, so it is expected that any calling code will handle it (typically communicated through documentation). Exceptions are raised when unexpected conditions occur in the _private_ methods. These exceptions are then added to the main **`InputHandlerException`** to complete the traceback so that the calling code can identify what went wrong without having to handle multiple exceptions (see the calling code sample below). 

Okay, let's look at the rest of the **`InputHandler`** class. Notice that we no longer have any nested conditional statements, the input command is contained within a single object, the calling code can decide _when_ to process, and we have a single object that represents a single input command (more on this shortly). Now if we need to add additional support for input commands, all we have to do is add a single line to the **`CommandType`** enumeration! We also gain the ability to write tests directly against this class, simplifying the testing and validation process required to ensure our program is free of bugs. Whenever an input command is received all we have to do is write the following code (print statements for demonstration purposes):

```python3
ih = InputHandler("L /home/mark/ics32 -r -f")

try:
    res = ih.process()
    print(res)
except InputHandlerException as e:
    print(e)
```

What's great about this approach is that now we have a single object, **`ih`**, that contains everything we want need to know about the user input command. We can be confident that the command is valid because if it was not, an exception would be thrown. Storing the input command as an object also has other benefits. We could easily add support for an input history, delayed execution, and automation by storing **`InputHandler`** objects in a list, for example. We could also follow the approach used in the **`Profile`** module and serialize **`InputHandler`** objects to a text file. There are many more advantages, but we will leave that for you to explore in future assignments.

If you would like to see a running an example of the code above, feel free to copy and paste into your own python module and give it a run.


(lectures:inheritance)=
### Inheritance

#### Videos

[Inheritance Lecture Video]()

#### Notes

Did you know that a class can be a child of another class? That a child class can __inherit__ the attributes and methods of its parent? It can, and the process, which we call __inheritance__ is one of the fundamental paradigms of object oriented programming. Let's dive in to some code first, then we'll break down what all of this means.

In the {ref}`Advanced Classes lecture <lectures:adv_classes>`, you may have noticed something odd with the way the **`CommandType`** and **`InputHandlerException`** classes were declared:

```ipython3
class InputHandlerException(Exception):

class CommandType(Enum):

```

It looks like the class is specifying a parameter! Well, it sort of is, but notice that the parameter only contains a _type_--it's missing a parameter name. This is the syntactic convention that Python uses to inherit, _or_ subclass, from other classes. When a class __subclasses__ another class in this way, it becomes a __type__ of that class, thereby inheriting all of the parent classes members (attributes and methods). Let's take a quick look at how we can use inheritance to improve the re-usability of our code.

```ipython3
class BaseClass:
    def __init__(self):
        self.base_attr = "I am a base attribute!"
        self.data = 0
    
    def base_method(self):
        print("the base method number is: ",self.data)

class SubClass(BaseClass):
    def sub_method(self, data: int):
        self.data = data 

class AnotherSubClass(BaseClass):
    def base_method(self):
        print("the custom base method number is: ",self.data)

sc = SubClass()
sc.base_method()
sc.sub_method(5)
sc.base_method()

ac = AnotherSubClass()
ac.base_method()

print(sc.base_attr)
print(type(sc))
print(isinstance(sc, BaseClass))

```

And the resulting output when run:

```ipython3
>>> the base method number is:  0
>>> the base method number is:  5
>>> the custom base method number is:  0
>>> I am a base attribute!
>>> <class '__main__.SubClass'>
>>> True
```
In this example, we have a **`BaseClass`** which implements some initialization code and a method that prints the value of its data attribute member, **`data`**. We have a **`SubClass`** which inherits from **`BaseClass`** and implements its own method for changing the **`data`** attribute. And we have a **`AnotherSubClass`** which __overrides__ the **`base_method`** of the **`BaseClass`** and implements its own print statement.

There is a lot to breakdown here, so let's go through the shell statement's one by one. First, notice that the **`base_method()`** method is a member of the **`sc`** object that we instantiated from **`SubClass`**. This is because, as we discussed earlier, the subclass inherits all of the members of the parent class. Next, notice that the new method that is created in the subclass can act upon the data attributes of the parent class, so here the **`data`** object is updated according to value passed into the **`base_method`**, therefore the next time that **`base_method`** is called the print statement reflects this change.

The **`AnotherSubClass`** class demonstrates one of the more powerful examples of inheritance, overriding. A subclass can override, or change the expected behavior, of a parent class method by implementing its own version of the same method, with the same signature.

The final three print statements simply demonstrate how Python treats subclasses. Notice how even though the object **`sc`** is of type **`SubClass`**, it is also an instance of **`BaseClass`**. Why is that important? Let's take a look:

```ipython3
class MessageClass:
    def print_message(self, bc:BaseClass):
        bc.base_method()

mc = MessageClass()

mc.print_message(sc)
mc.print_message(ac)

```
```ipython3
>>> the base method number is:  5
>>> the custom base method number is:  0
```

In this example, we have created a new class called **`MessageClass`**. This class is responsible for printing messages of the type **`BaseClass`**. But notice that we never actually passed an object instantiated from **`BaseClass`**, rather we passed it **`SubClass`** and **`AnotherSubClass`** and it worked! Inheriting from classes this way can be used to structure and organize our programs while also reducing the amount of code we write. Code reuse is one of the best ways to reduce the likelihood of bugs in our programs.

A good way to think about class inheritance is to consider some of the things we already know about the different types of objects we interact with every day. Take the smartphone for example. At an abstract level, every smartphone has a few common properties like a screen, buttons, microphone, speaker, cpu, gps, etc. So we can might think of all of those common attributes as members of a base class. So we could write a base class, let's call it **`SmartPhone`**, that will manage common attributes for us. Next, we might want to create a class that can do some things that only certain types of smartphones can do, let's call these classes **`iPhone`** and **`Android`**. Both classes can inherit from **`smartphone`** to make use of the common attributes. But each class will also implement its own attributes that are unique to it like touch interactions and apps. We can also go further and compose individual classes for all of the different types of iPhone's and Android phones that exist.


