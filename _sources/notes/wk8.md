Week 8 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 8 Overview


The lectures for this week will help you with assignment 3 and get you ready for assignment 4.

: {ref}`lectures:adv_inheritance`

## Lecture Materials

### Live Class

#### Tuesday

[Class Recording](https://uci.zoom.us/rec/play/O_SUJRGPxuGDG6EMRL60tqKf_nEwqvCd1jCvYQACqyR9E3PkKdJOGecl2CvVn9a7Mtoi0XO6kcuKZqQ.affjnJb0JgSEdQbi?continueMode=true&_x_zm_rtaid=5d3zhtehQPC5yLIFTPfFTQ.1645593351975.c4df82b9dd3d921fc28ac28d9e251c1f&_x_zm_rhtaid=721)


#### Thursday

[Class Recording]()
Lecture recording will post on 2/18

### Recorded Lectures

(lectures:adv_inheritance)=
### Advanced Inheritance

##### Lecture Recording

[Advanced Inheritance Lecture](https://uci.yuja.com/V/Video?v=3900187&node=13324542&a=809406141&autoplay=1)

##### Lecture Notes

In the [week 4](../notes/wk4.md) lecture on inheritance, you learned how to take advantage of Python's support for deriving one class from another. We referred to these derived classes as **`subclasses`** or **`child`** classes and discussed some of the benefits of designing your around these concepts. If you haven't watched the inheritance lecture yet, please do before continuing as this lecture will assume you have a basic understanding of the material.

In the first lecture we looked at a couple trivial examples to learn how to write code to make use of inheritance. For this lecture, we will build a more meaningful program to highlight the advantages that inheritance offers your code.

##### Designing with Inheritance
Let's start with a brief discussion on design. As we have covered many times throughout the quarter, a major factor to a successful program is fast, reliable, robust code. The less code we write, the less code we have to worry about to meet these goals.

Inheritance provides our programs with one way to reduce the amount of code we need to write. 

One type of programming where inheritance is quite useful is with graphical user interfaces. Using the simplest definition, a graphical user interface or GUI provides a collection of widgets that collect input and display output to a user. Common widgets that you have no doubt interacted with include buttons, text boxes, pull down menus, checkboxes, and so on.

As you might imagine, many of these widgets share a lot of traits, which if implemented per widget, would create a great deal of repetitive code. Let's look at an example.

```python3
class ButtonWidget:
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""

class CheckboxWidget:
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""

class TextboxWidget:
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""
```

In the code above, we have three different types of widgets defined as classes. You will quickly notice that each class implements the same four attributes. Of course, all of these widgets need to support custom dimensions and colors, but using this design means that whenever one of these attributes needs to be changed, we will have to make the same change in each class.

So let's refactor each widget to make use of inheritance (this process should largely be familiar to you by now as it has been discussed in the inheritance lecture and assignment 4):

```python3
class BaseWidget:
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""

class ButtonWidget(BaseWidget):
    pass

class CheckboxWidget(BaseWidget):
    pass

class TextboxWidget(BaseWidget):
    pass
```

That's better. Now each widget retains access to the same attributes, but those attributes only need to be coded and maintained in a single location. If we decide to create a new widget, all we have to do is inherit from **`BaseWidget`**.

Let's take a look at an example from the [Web API](../notes/wk6.md) lecture. In that lecture, we implemented a custom **`HTTPRequestHandler`** called **`ICSHTTPRequestHandler`**:

```python3
class ICSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.command + " received.")
        data = self.rfile.read(int(self.headers['content-length']))
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write("ok".encode(encoding = 'utf-8'))
        print(data.decode(encoding = 'utf-8'))
``` 

Notice here, how even though an HTTP request handling class has far more functionality built into it ([more here:](https://docs.python.org/3/library/http.server.html?highlight=basehttprequesthandler#http.server.BaseHTTPRequestHandler)) we only need to implement the functionality we desire for our custom derived class (e.g., handling POST requests).

The advantages to this approach become more significant as widget complexity increases. For example, a common requirement for GUI widgets is the ability to change size based on an external set of conditions. Rather than code this functionality for each widget, by building on top of a base widget type, complex functions like resizing can be shared across all widget classes.

#####	Abstract Methods

In the [inheritance lecture](../notes/wk5.md), we talked about the concept of overriding base class methods to implement new functionality in a derived class. Overriding allows us to take control of the functionality provided by a base class, but what if a base class requires its derived classes to adhere to a particular set of operations or rules?

Let's build on our earlier example: 

```python3
class BaseWidget:
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""

    def render(self):
        pass

class ButtonWidget(BaseWidget):
    pass

class CheckboxWidget(BaseWidget):
    pass

class TextboxWidget(BaseWidget):
    pass


def build_ui(widgets:list[BaseWidget]):
    for w in widgets:
        w.render()

widgets = [ButtonWidget(), CheckboxWidget(), TextboxWidget()]

build_ui(widgets)
``` 

This is quite a simplistic overview of how a GUI might be rendered, but it covers the basic process. In most GUI toolkits, each widget is responsible for rendering how it should look on a screen. A base widget cannot know how a particular widget should look, but it should require a widget to implement the code necessary to render itself.

If we were to run the code above, it would run without error, but if these widgets were actually feature complete we still would not see anything on the screen. So can we ensure that a required method is actually implemented in a derived class?

We mitigate this concern by declaring that a method is required through the concept of _abstract methods_. In object oriented programming, an abstract method is one that is defined, but not implemented.

An abstract declaration is used to define a method that _must_ exist in a class, but its specific implementation does not or cannot be determined. In the example above, since **`BaseWidget`** does not specify a particular way to render, it is the responsibility of the derived class to define how rendering should be handled. If the **`render`** method were declared abstract, we could avoid some of the confusion around implementing a custom **`BaseWidget`** class. Let's take a look:

```python3
from abc import ABC, abstractmethod

class BaseWidget(ABC):
    width:int = 0
    height:int = 0
    forecolor:str= ""
    backcolor:str= ""

    @abstractmethod
    def render(self):
        pass
```

Abstract methods are not built-in to Python, so to get the functionality we desire, we must first import the **`ABC`** module and use inheritance to declare that we intend our base class to make use of the features that **`ABC`** includes. To define a method as abstract, we apply the **`@abstractmethod`** decorator to each method we want derived classes to implement.

Now when the revised code is run, the shell will output the following error for each method until they all implement the **`render`** method:

```
TypeError: Can't instantiate abstract class ButtonWidget with abstract method render
```

So what does this functionality give us? If you are writing a program that you do not ever expect to support code from programmers outside of your own organization, then there probably isn't much reason to design with abstract methods. However, if you are developing a library, API, or other modules intended for public use you might want to exert some control over how your code is used.

You have likely noticed that the **`WebAPI`** module used in [assignment 4](../assignments/a4.md) makes use of abstract methods, ensuring that your derived classes will operate according to the specification intended by the assignment creator :)

##### Multiple Inheritance

A derived class is not limited to inheriting from just one base. There are times where a class might need to take on the functionality from two distinct classes. Let's once again return to the simplified GUI example. 

Some widgets have features that are not common to all widgets, but are common enough to justify extracting into a common class. One good example of this is with widgets that need to support scrolling. The following code snippet contains two new widgets that contain a scrollable view pane.

```python3
class TextAreaWidget(BaseWidget):
    def scroll_up(distance:float):
        pass
    def scroll_down(distance:float):
        pass
    def render(self):
        # render widget
        pass

class ListItemWidget(BaseWidget):
    def scroll_up(distance:float):
        pass
    def scroll_down(distance:float):
        pass
    def render(self):
        # render widget
        pass
```

Both classes must implement code to handle scrolling up and down, taking us once again down the path where we have to manage the same code in multiple places. We _could_ move this code to **`BaseWidget`**, but then we introduce unnecessary code to widgets like the **`ButtonWidget`** that do not support scrolling.

Multiple inheritance allows us to get around this issue. Let's once again move our repetitive code to a common base class and use inheritance to add support to all derived classes that need scroll functionality.

```python3
class BaseScroll:
    def scroll_up(distance:float):
        pass
    def scroll_down(distance:float):
        pass

class TextAreaWidget(BaseWidget, BaseScroll):
    def render(self):
        # render widget
        pass

class ListItemWidget(BaseWidget, BaseScroll):
    def render(self):
        # render widget
        pass
```

Now we have a base scroll class where we can maintain all code required by any widget that needs to support scrolling, while still retaining all of the functionality that the base widget class provides.

Alright, one last thing that we should consider when using multiple inheritance. Remember in the first [inheritance](../notes/wk5.md) lecture we briefly discussed the role of **`super`** in the class hierarchy. Well, now we have two super classes! So how does Python decide which one to use?

We can check by taking a looking at the [method resolution order](http://python-history.blogspot.com/2010/06/method-resolution-order.html) (a tuple that Python adds to all classes):

```python3
print(TextAreaWidget.__mro__)
```

Which will output:

```
(<class '__main__.TextAreaWidget'>, <class '__main__.BaseWidget'>, <class 'abc.ABC'>, <class '__main__.BaseScroll'>, <class 'object'>)
```

So Python will work up the inheritance hierarchy working from left to right. We are now getting a bit beyond the scope of what you need to know and learn for this course, but it's worth noting that there is a process in place for calling **`super`**. Generally, though, unless you have a specific need to pass parameters to the init method of a parent class, it's best to just access parent methods using the class directly.

One final word of caution. Most object oriented languages do not support multiple inheritance...with good reason. You can imagine how complex the relationships between parent, child, grandchild classes can becomes as the class hierarchy grows. At some point, multiple inheritance can be counterproductive to our goal of reducing and simplifying code. So, if you use multiple inheritance, use with caution! 

##### Interfaces

One aspect of inheritance that we have discussed, but not explicitly described yet is the concept of an interface. When you inherit from a class, the derived class takes on the parent classes implementation (the code and functionality) and its interface (the signature). Interfaces provide one way to avoid a lot of the complexity that arises with multiple inheritance. In fact, other languages that do not support multiple inheritance, have no limitation on implementing multiple interfaces!

Once again, we will expand on our GUI code to demonstrate how to create an interface. Here is another widget that does not inherit from the **`BaseWidget`**, but still implements its _interface_:

```python3
class RadiobuttonWidget:
    def render(self):
        pass


def build_ui(widgets:list[BaseWidget]):
    for w in widgets:
        w.render()

widgets = [ButtonWidget(), CheckboxWidget(), TextboxWidget(), RadiobuttonWidget()]

build_ui(widgets)
```

Now of course, by not inheriting from the base widget the **`RadiobuttonWidget`** will not have the functionality, but since it does implement the **`render`** method, for all intents and purposes the function **`build_ui`** function considers it a widget. In Python, this is often referred to as Duck Typing, because if it walks like a duck and acts like a duck, it must be a duck!

Deciding when to use an interface vs. inheritance is largely dependent on the design approach you take with your code. Pouring over the reasons for and when an interface is more desirable is not something you need to worry about too much in this class. However, understanding the role of each will equip you with the knowledge to apply to your future program design.
