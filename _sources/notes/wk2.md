Week 2 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 2 Overview

By now you should have turned in your first python program for ICS 32. Congrats! Now that you have your development environment setup and functioning properly, it's time to get to work on building your first real application. Completing Assignment 1 will require that you start to build a fundamental understanding of concepts that are a bit more complex than what you have learned so far. If you haven't already, be sure to read the overview for [Assignment 1](../assignments/a1.html) and watched the lectures posted in the [Week 1 Notes](../notes/wk1) before you dive into the lecture materials for this week.

Quick Links:
: {ref}`lecture-materials-2`
: {ref}`quiz-results-2`

(lecture-materials-2)=
## Lecture Materials

Lectures for Week 2
: {ref}`lectures:testing`
: {ref}`lectures:modules`

(lectures:testing)=
### Some Notes on Testing 

Although We will be diving into testing more formally around the mid-point of the quarter, I wanted to give you some notes on how to think about testing your code. We can discuss the topics here in a bit more detail after quiz in our next class.

#### Notes

Now that you have assignment 0 wrapped up, let's take a minute to reflect on the experience. 

Reviewing the discussions many of you have had over the past week on Zulip, it looks like you are starting to recognize the complexity that goes into writing even a small program. 

Interpreting and implementing program requirements is an essential part of the programming process that will become more familiar to you as you work through this course and many others. However, even with practice, you will find that it is important to develop strategies to reduce the uncertainty that accompanies the application of requirements. 

In a way, the validity checker for assignments 0 and 1 "tests" your program for you. It offered some sense of confidence that your program was functioning according to the assignment requirements. For the remaining assignments in this class, you will be responsible for checking the validity of your programs. So in this lecture, I want to talk about one of the ways that programmers go about accomplishing this goal.

In large programming projects where teams of programmers work together to write software, the practice of writing tests is quite common. In fact, there are programming paradigms such as Agile, Cleanroom, Spiral, and Waterfall that have integrated testing directly into their methodologies. We won't be learning about paradigms and models in this class, but it's important to recognize how pervasive testing is throughout the software development industry. As you might imagine, this pervasiveness exists because the process of writing tests against your code, works. Tests can significantly reduce the development time, code complexity, and bug tracking.

##### So how do we start?

Well, the first thing we do is create a hypothesis about how our program and the functions within it, are expected to behave. For example, one test might be to input a value and observe the output. Does the output align with the expectations set in the program requirements? If so, then the test can be said to 'pass.' If it doesn't, then obviously the test fails, but how do we determine why? This was a source of confusion for many of you while using the assignment 1 validity checker as the validity checker could only report a failure when the program did not return an expected output. A better test might have examined the input and output at the level of functions rather than the program.

Testing individual functions, however, does require some planning. If the functions in your program perform many operations, it can be difficult to configure a test that can be relied upon. So one of the benefits of thinking about tests before or in tandem with your program design is that the responsibilities of your functions will inevitably be scoped to a manageable size.

##### So how do we test at the level of functions?

Let's take, for example, a program that manages an email list. We'll assume that one of the requirements for this program is to support removing certain email addresses from the mail list.

We'll start by adapting this small function written by Alex Thornton for ICS 32. The **'remove_from'** function accepts two parameters: a list and a value. It returns the same list, except without the passed value, if it exists.

```ipython3
def remove_from(the_list: list, value) -> list:
	new_list = []

	for element in the_list:
		if element != value:
			new_list.append(element)
		
	return new_list
```

At least, that's what we hope it does. Rather than assume it does and continue to build our email list management program, we should test it first:

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user2@example.com")
["user1@example.com", "user3@example.com", "user4@example.com"]
>>> emails
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user4@example.com")
["user1@example.com", "user2@example.com", "user3@example.com"]
>>> emails
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]

```

So far so good. We start with a test list, then pass some test conditions to the function to see if it returns the results we expect. Here, after each call to **`remove_from`** we receive a new list with the value we passed to it missing. But have we tested every possible condition? What happens if a passed value does not exist?

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user5@example.com")
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]

```

Is that what we want to happen? What if our program needs to confirm that a removal actually occurred? Well, we could compare **`emails`** to the results, or we could give that responsibility to the **`remove_from`** function:


```ipython3
def remove_from(the_list: list, value) -> list:
	new_list = []

	for element in the_list:
		if element != value:
			new_list.append(element)
		else:
			raise ValueError('value not found in list')
		
	return new_list
```

So now we have a function that will raise an exception if the passed value does not exist, providing us with a convention (exceptions) that we can use to handle this new condition. 

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user5@example.com")
Traceback (most recent call last):
  File "maillist.py", line 39, in <module> 
		remove_from(emails, "user5@example.com")
	File "maillist.py", line 33, in remove_from
		raise ValueError('value not found in list')
ValueError: value not found in list

```
Can you think of any others? What happens if the email list has multiple emails with the same address? Currently, all instances of value will be removed from the new list, but what if we only wanted to remove duplicates? By writing tests against our functions, we expose conditions that we might not otherwise think to consider.

Now, having to write create these tests cases each time we want to test a program can quickly become unwieldy. Fortunately, Python gives us a way to automate much of the work!

The **`assert`** statement is a convenient shortcut for inserting debugging tests into your program. Here we test a normal case, or case that represents typical behavior for the remove_from function:

```ipython3
assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]

```

And here we test an error case, or case that generates a result we don't expect:

```ipython3
try:
	remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user5@example.com")
	assert False, "ValueError should have been thrown"
except ValueError:
	pass
```

If both assertions pass, then we should not expect to see anything from the shell when running the program. However, if an assertion fails, the debugger will notify you of the failure:

```ipython3
>>> assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]

Traceback (most recent call last):
  File "maillist.py", line 38, in <module>
	    assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user2@example.com"]
AssertionError
```

We will get into the more formal test driven approach to software development in a few more weeks, once you have had a chance to experience working with larger, more complex programs. But for now, focus on thinking about the how the code you write should behave, and then write some assertion statements to confirm that it behaves as you expected. I think you will find that new edge conditions will arise that you might not have otherwise considered. And remember, testing is not about quantity! A program with 100 tests is not necessarily better than one with 10. Your goal should be to identify _different_ conditions worth testing, not _variations_ on the same test.

(lectures:modules)=
### Modules

In upcoming assignments, you will be required to start organizing your code a bit more than you have for [a0](../assignments/a0) and [a1](../assignments/a1). One way to organize code is to divide it into multiple files, or modules. In this lecture, we'll be focusing on how you should go about fulfilling this requirement.

The code that we write to create a program in Python is stored in plain text files. Aside from some common conventions such as file extensions (**`.py`**), syntax, and indentation, Python files are no different then any other plain text file that you might write. So far, you have probably written most of your Python programs in a single file with a **`.py`** extension. Generally speaking, this is a good practice. Having all of your code in a single file simplifies things quite a bit. When all of your code (and tests!) is in one location you don't have worry about connecting multiple files. However, as your programs grow in complexity and size, you will discover that managing all of your code in a single file quickly turns into a time consuming challenge. So let's turn to the lecture to learn how we can improve the readability and reuse of our code with modules.

#### Videos

[Modules Lecture](https://uci.yuja.com/V/Video?v=2060971&node=7796023&a=1224073848&autoplay=1)

#### Working with Modules

In Python, a module is nothing more than a file with the **`.py`** extension. However, unlike the programs you have written so far, a module does not produce output when executed directly from the shell. Let's take a look at the following example:


```ipython3
# basicmath.py

def add(a: int, b: int) -> int:
	result = int(a) + int(b)
	return result
		
def subtract(a: int, b: int) -> int:
	result = int(a) - int(b)
	return result
```

If we were to run this program, **`basicmath.py`**, on the shell we would not receive any output from the Python interpreter. We would, however, be able to call the modules functions directly:

```ipython3
>>> add(2, 5)
7
>>> subtract(9, 3)
6
```

If we attempt to call these functions before we load **`basicmath.py`** the interpreter will return a **`Traceback`** that tells us that 'add' (or 'subtract') is not defined. So what is the difference? Well, by executing the **`basicmath.py`** module first we have loaded it into our program, which in this case is the Python shell. The Python programs that we write in **`.py`** files, operate in much the same way. Let's write a small program that makes use of the **`basicmath.py`** module:

```ipython3
# mathrunner.py

import basicmath

a = input("Enter your first value: ")
b = input("Enter your second value: ")

result = basicmath.add(a,b)
print(result)

result = basicmath.subtract(a,b)
print(result)

```

Notice that the first line of code is an **`import`** statement followed by the name of our basicmath python module. We don't need to specify the **`.py`** extension as it is implied that we are importing Python files. So, in the same way that you "imported" the **`Path`** module into your program for a1, we are able to import python files that we write. 

##### Scope

Another important convention to consider in this code is how the add and subtract functions are accessed. You will see that when the variables are passed to the basicmath functions, the name of the module must first be referenced. Python, as well as most programming languages, operate under a concept called _scope_. Scope refers to the availability of classes (we will cover these in more detail later in the quarter), functions, and variables at a given point of execution in a program. In the example above, notice how the variable **`result`** is used in the add and subtract functions of the **`basicmath`** module as well as the **`mathrunner`** program. We can reuse variable names in this way due to Python's scoping rules. **`result`** is locally scoped to the add and subtract functions, meaning that it only exists in the moment that each of those functions is being called. Now, if we wanted to make use of **`result`** outside of the add and subtract functions, we could modify the basicmath program like so:

```ipython3
# basicmath.py

result = 0

def add(a: int, b: int) -> int:
	result = int(a) + int(b)
	return result
		
def subtract(a: int, b: int) -> int:
	result = int(a) - int(b)
	return result

def get_last_result() -> int:
	return result
```

```ipython3
# mathrunner.py

import basicmath

a = input("Enter your first value: ")
b = input("Enter your second value: ")

result = basicmath.add(a,b)
print(result)

result = basicmath.subtract(a,b)
print(result)

print(basicmath.get_last_result())

```

Which will output:


```ipython3
Enter your first value: 5
Enter your second value: 2
7
3
0
```

Wait, why is the value of **`result`** still zero? Well, even though the variable **`result`** is scoped outside of both functions, or _global_, Python still gives precedence to the _local_ instance of **`result`**. So the add and subtract functions create a local instance of **`result`** while get_last_result, in absence of any instantiation of a local **`result`** instance, defers to the global instance of **`result`**. To use the globally scoped variable, we need to tell Python that is our intention:

```ipython3
# basicmath.py

result = 0

def add(a: int, b: int) -> int:
	global result 
	result = int(a) + int(b)
	return result
		
def subtract(a: int, b: int) -> int:
	global result
	result = int(a) - int(b)
	return result

def get_last_result() -> int:
	return result
```

Which will output:


```ipython3
Enter your first value: 5
Enter your second value: 2
7
3
3
```

There we go! So by setting the scope of the **`result`** variable inside each function to _global_ we change the scope from _local_ to _global_, allowing us to store a value in a shared variable. So scope can be thought of as consisting at two levels: _global_ and _local_. The Python interpreter assumes a _local_ first stance when interpreting program code and when a local instance is unavailable it assumes _global_.

```{important}
Scope refers to the availability of a particular object in a program. That availability is interepreted locally first and then globally.
```

##### Definition Access

When writing modules that contain many functions performing many different types of operations you will find that you need some of those functions to perform operations _within_ your module, but you might not necessarily want those functions to be called _outside_ of your module. In programming terms, we describe these two types of functions as _private_ and _public_. While some programming languages do provide modifiers for declaring this intention at the point of compilation, Python does not. Rather, all functions in Python are public by default. There is no way to prevent another program from calling functions in your module that should not be called!

To get around this feature, and the absence of such modifiers is considered a feature in Python, programmers have adopted some formal conventions for communicating _intent_. When writing functions that you don't intend to be used outside your module, they should be prepended with a single underscore (**`_`**) character. This convention is used for functions, constants, and classes in Python:

```ipython3
# Specifying private intent

def _myprivatefunction():

_myprivateconstant = "525600" # minutes in a year

class _myprivateclass():
```

We will be looking more closely at your use of naming conventions like private and public access as we move forward with assignments this quarter. Not only do we want to you to continue to adopt formal Python programming conventions, but thinking about access will help you to improve the structure of your modules. So start considering what operations in your program need to be conducted outside the scope of your module and more importantly, what code should not be accessed.


##### Namespaces

As your programs grow in size and complexity the importance of understanding scope will become increasingly relevant. Without the ability to scope the objects that we create, every Python programmer would have to create unique object names! Imagine if object naming behaved like Internet domain names, each one having to be recorded in a central registry to avoid duplicates. Through scope, and a convention called _namespaces_, most programming languages can avoid this unnecessary complication. A namespace is a dictionary-like collection of symbolic names tied to the object in which they are currently defined.

Namespaces are not a perfect solution, but they serve well to help programmers identify and differentiate the modules and programs that they write. It is important to avoid using known namespaces, particularly those that are used by Python's built-in objects. For example, you should avoid creating an object named **`int`** or **`tuple`** because they already exist in every instance of a Python program. Imagine if we had named our **`basicmath`** module **`math`**, which is part of the standard library! To put it more concretely, what if we also had an **`add`** function in our **`mathrunner.py`** program? Namespaces allow us to differentiate between like named objects:

```ipython3
# mathrunner.py

import basicmath as m

def add(a, b): 
	print(a + b)

a = input("Enter your first value: ")
b = input("Enter your second value: ")

print(m.add(a,b))
print(add(a,b))

```

The two **`add`** functions being printed will produce distinctly different results, namespaces allow us to differentiate between them in the code we write. Python also provides us with a naming convention for the modules that we import. Notice how the import statement and subsequent use of namespace differ in this revised version of **`mathrunner.py`**. This can be useful when the modules you are importing make use of a longer namespace that you might not want to type every time it is used.

Python makes use of four types of namespaces, listed in order of precedence:

Local
: Inside a class method or function

Enclosed
: Inside an enclosing function in instances when one function is nested within another

Global
: Outside all functions or class methods

Built-In
: The built-in namespace consists of all of the Python objects that are available to your program at runtime. Try running **`dir(__builtins__)`** on the IDLE shell to see the full list of built-ins. Many of the names should look familiar to you.

I have included the following tip originally written by Alex Thornton, who also teaches this class at UCI. I think it's a great explanation of how modules make use of the **`__name__`** variable in Python and wanted to share it with you.

```{admonition} Alex Thornton's Explanation of Executable Modules
:class: tip
When you load a module in IDLE and execute it (by pressing F5), the code in that module is executed. If it generates any observable result, like printing output or asking the user for input, you'll see that in the interpreter. Otherwise, you'll see a standard >>> interpreter prompt, and all of the module's definitions will now be available — so, for example, if the module defines a function, you could now call it.

As we've seen, modules in Python have names. We can check the name of the currently-executing module at any time by accessing the global variable **`__name__`**, which is present in every module.

In general, the names of modules are indicated by their filenames; a module written in a file **`boo.py`** has the name **`boo`**. But there's one special case that we haven't talked about: When you execute a module in Python (i.e., by pressing F5 in IDLE), it's given the special name **`__main__`** while it runs. (Anything you define in the Python interpreter will be considered part of the **`__main__`** module, as well.)

This little fact can be a useful way of differentiating between whether a module has been executed (i.e., is it the "entry point" of a program?) or whether it's been imported. In general, importing a module shouldn't suddenly cause things to happen — output to be generated, input to be read, and so on — but should, instead, simply make definitions available that weren't previously. Even executable modules, the ones we expect to be able to execute as programs, should behave differently when imported than they do when executed.
s
To facilitate this distinction, we can simply check the module's name by accessing the **`__name__`** variable. If its value is **`__main__`**, the module has been executed; if not, the module has been imported. So, in an executable module, we typically write the code that causes things to happen when the module is executed in an **`if __name__ == '__main__':`** block, so that it will only happen if the module has been executed. Meanwhile, if the module is imported, its definitions will become available to another module, but there will otherwise be no effect.
```

(quiz-results-2)=
## Quiz Results

To be posted on 1/13
