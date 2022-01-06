Week 1 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 1 Overview

Normally weekly notes will be released at beginning of each week. Since this is our first week together, however, the notes and lecture recordings will be release after our first class together on Tuesday the 4th. Check back here after class on Tuesday and Thursday for updates.

## Lecture Materials

### Live Class

#### Tuesday

<a href="../resources/Introduction-to-ICS32.pdf">Slides</a>

<a href="https://uci.zoom.us/rec/share/l-PIX0txfFz2aajBrs5EGmdq2eY8E3SycC2ZOi3irYbud3wNEt-6EBhuIGvUBX0n.1-LwI3ArDUPZ8R7M?startTime=1641329512000">Recording</a>

#### Thursday

Coming Soon

### Recorded Lectures

#### Handling Errors

##### Lecture Recording

[Error Handling Lecture](https://uci.yuja.com/V/Video?v=4086515&node=13881759&a=551849669&autoplay=1)

##### Lecture Notes

In this lecture we are going to talk about error handling and using the try/except statement. As you may already know, when we write programs errors are inevitable. Even in the most perfectly written programs, errors can occur. It's very difficult to predict every possible condition that we may encounter. Oftentimes, these are internal errors that occur due to the code we write and other times they are external forces that are beyond our control. Even when our code is perfect, something external to our code might happen, right? Imagine for a moment that your program is in the middle of downloading a file from a server on the internet. Take a minute, think about all the different conditions that might occur to prevent your file from downloading: 

* The server might crash. 
* The server might lose connection to the Internet. 
* You might lose connection to the Internet. 
* Your WiFi router could stop working. 
* Your network card could stop working.

There's a lot of reasons. These types of conditions are generally things that are out of your control, but you still need to think about them and handle them in your program. Unless you protect your code appropriately, it's likely that it will fail at some point during its operation. In this lecture, I want to talk about how you can go about protecting your code from both predictable errors and the unpredictable scenarios that we might not necessarily expect to happen. So let's start with a quick example:

```{note}
When you see the following characters, >>>, in the code examples, you do not have to type them in. They are used here to demonstrate that the code is run directly from the python shell. So if you are following along, just type whatever comes after the >>> characters.
```

```python3

>>> n = int(input("What is your age? "))
What is your age? 12

```
Here we simply ask the user for some input. We assume that the user will enter a numeric value, so we go ahead and cast that input to an integer so we can perform some mathematical operation with it. The program runs without issue, as long we enter a numeric value. But what happens if we enter a lexical value? Let's say, for example, that the person using our program prefers to write numerical values using lexical notation:

```python3

>>> n = int(input("What is your age? "))
What is your age? twelve

```

The user is still answering the question correctly, right? Unfortunately, the program we have written doesn't account for lexical inputs and the results are less than desirable:

```
Trackeback (most recent call last):
  File "<pyshell#1>, line 1, in <module>
	  n = int(input("What is your age? "))
ValueError: invalid literal for int() with base 10: 'twelve'
```

If you haven't seen this type of statement before, it's called a **`traceback`**. Traceback's are way for the Python interpreter to tell us information about why our program crashed. The program we have created only has one line of code, so the traceback is only going to go to the first line and report that that's where the error occurred. But it's also going to provide us with the code that was on that line and what type of error occurred. Finally, you will notice that the traceback also provides some information about the input that resulted in the error. So, looking at the last line of the traceback, we can see the error type is a **`ValueError`** and it occurred because we attempted to convert a lexical value to an integer. 

The important takeaway here is that these are the types of conditions you may encounter when writing a program. You might expect the user to enter what you think is obvious, like a numerical representation for an integer, but users aren't always as predictable as we think. They often do things differently and behave in ways that we don't intend. So what can we do to make sure that our code continues to work as we expect when a user engages in unpredictable behavior? 

Let's answer that question by starting with a slightly more robust program. We'll start with a function that collects user input and declare a **`error_handling.py`** program as a main module:

```python3
# error_handling.py

def run():
  a = input()
	b = input()

if __name__ == '__main__':
  run()
```

If we run this program, we will be able to input a value and have it assigned to the variable **`a`**, then enter a second value that will be assigned to the variable **`b`**. So far so good. The program runs, but doesn't actually do anything yet. So let's add another function that will be responsible for adding the two input values together.

```python3
# error_handling.py

def add(a, b):
  return int(a) + int(b)

def run():
  a = input()
	b = input()
	r = add(a,b)
	print(r)

if __name__ == '__main__':
  run()
```

Once again running the program under the assumption that inputs will always be numerical values, the program works just fine. However, if we attempt to use an invalid value, the program crashes and produces the following traceback:

```python3
Traceback (most recent call last):
  File "/usr/lib64/python3.10/idlelib/run.py", line 580, in runcode
    exec(code, self.locals)
  File "/home/mark/ics32/error_handling.py", line 12, in <module>
    run()
  File "/home/mark/ics32/error_handling.py", line 8, in run
    r = add(a,b)
  File "/home/mark/ics32/error_handling.py", line 3, in add
    return int(a) + int(b)
ValueError: invalid literal for int() with base 10: 'twelve'
```

Notice how now that the program operates through multiple function calls, the traceback is a little bit more complex. The error type is the same, but we can look at the traceback to identify where the error is occurring: line 3! So we need to make sure that the code we are writing does not attempt to cast a value input by the user to an integer. There are a few ways to go about solving this problem. We could first check to see if the variables the inputs have been assigned to can be represented as the type we desire (integer), but this would take quite a bit of code to account for all the possible input variations. The simplest approach is to simply attempt to perform the operation and _handle_ any potential errors that occur. If we look at the traceback we received above, we can see that root of the error in our module starts at line 12 with the call to the **`run`** function. So let's wrap that function call with some error handling:

```python3
# error_handling.py

if __name__ == '__main__':
  try:
		run()
  except:
		print("An error has occurred")

```

When the program is run again and a non-integer value is entered by the user, instead of a traceback the program will output the message we have written in the **`except`** statement above. The **`try/except`** statement tells Python how to handle code that might cause an error by providing it with alternative options. Let's look at the try statement a little more closely.

```python3
try:
	# Operation to perform
except:
	# Operation to perform if an error occurs on the first operation
else:
	# Operation to perform in an error does not occur on the first operation
finally:
	# Operation to perform regardless of what happes to the first operation
```

The **`try`** statement will execute up to four conditional operations based on the operation of the code placed in the try block. It's likely that you won't always use all four conditions, but depending on the type of operations your code is performing, it is possible. For now we will focus on the the **`try`** and **`except`** blocks. We'll cover the other conditions in more depth later in the course.

So with a try statement in place, our program can safely run without crashing. However, because we have placed the try statement at the root of our program, any and all errors that occur will be handled here. As a program grows in complexity, this approach will make managing your code quite difficult. A better approach would be to target that actual operation that _we know_ is causing the error. In our case, since we are receiving an exception of type **`ValueError`** whenever we attempt to cast a non-integer value to integer, perhaps we should locate the try statement closer to the source?

```python3
# error_handling.py

def add(a, b):
  r = 0
  try:
    r = int(a) + int(b)
  except:
    print("An error has occurred")
  return r 

def run():
  a = input()
	b = input()
	r = add(a,b)
	print(r)

if __name__ == '__main__':
  run()
```

This looks like a good start. Now the error is handled where it occurs, rather than waiting for it to pass up through the trace. However, it's not a very friendly experience. First, we have no way of knowing which variable could not be cast. Second, we print a message to the user from within the add function when our actual interaction with the user occurs in the run function. We could probably make a few changes here like adding a second try/except, putting some additional checks on the return value from the **`add`** function, give the user an opportunity to attempt to input new values, but the code would get overly complicated quickly.

We'll be talking a lot about abstraction, the process of unifying code to reduce repetition, this quarter. It is an important part of the programming process and one that is a useful for creating good code refactors (hint, hint). So to apply some light abstraction, rather than wrap the lines of code where we actually perform the type cast, let's create a new function that can perform this operation for us in one place.

```python3

def is_int(val):
  try:
		int(val)
		return True
	except ValueError:
    return False

```

Notice that we have also specified the exact error type that we want to handle in this function: **`ValueError`**. This means that all other exception types will not be handled here. So now we have a function designed with the sole purpose of checking whether or not a value is an integer. The rest of our original code is more or less free to operate as originally planned, with one minor change:

```python3
# error_handling.py

def is_int(val):
  try:
		int(val)
		return True
	except ValueError:
    return False

def add(a, b):
  return int(a) + int(b)

def run():
  a = input()
	b = input()
	if is_int(a) == False or is_int(b) == False:
    print("Unable to perform operation with supplied values")
	else:
		r = add(a,b)
		print(r)

if __name__ == '__main__':
  run()

```

Now we only need to add one conditional statement to check the user input values and provide some feedback to the user. We also now have a program that keeps all user input and output in one place (the run function) instead of scattering print statements throughout the program code.

Okay, if you haven't tried running this code yet, please do. My goal with these lectures and notes is to give you enough code to follow along and view the results on your computer in real time. If you have made it this far, play around with the code a bit more. How would you go about adding support for values of type float? How might you redesign the **`run`** function to allow the user to _fix_ their input error other than having to run the program again?
