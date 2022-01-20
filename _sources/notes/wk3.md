Week 3 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 3 Overview

Welcome to week 3! This week you should be working on finalizing your first full assignment for the class, [a1](../assignments/a1.md). Be sure to leave yourself some time at the end of the week to test. We will be introducing assignment 2 on Thursday, so you will want to be prepared to shift gears slightly and start expanding your code in new directions. This week will be a bit different as we have some notes on testing to read and a lecture on classes that will be released on Wednesday. You have everything you need to complete assignment 1, so this weeks lectures will prepare you for upcoming work. 

I know I discussed making a few short touch up videos on VS Code and sorting last week. Unfortunately, I have not had a chance to create those videos. So we will use our live class time on Tuesday to cover those topics and anything else you might need to review.

The recorded lectures for this week will cover the following topics:

: {ref}`lectures:testing`
: {ref}`lectures:classestemp`

You might also take a look at the [lab schedule](../assignments/lab.md) for week 3 and see if any of the topics align with your learning needs.

See you in class!

## Lecture Materials

### Live Class

#### Tuesday

[Class Recording](https://uci.zoom.us/rec/share/cXcFpLTcspfx7nzsPbPV2KSuXUlkkOdnfEeKTDYNt1xNLakrqIx93dt-QZxwTU1L.hcUQBrUNmQEhyguN?startTime=1642538210000)

#### Thursday

[Class Recording]()
(Posted 1/20)

### Recorded Lectures

(lectures:testing)=
#### Some Notes on Testing 

Although we will be diving into testing more formally around the mid-point of the quarter, I wanted to give you some preliminary notes on how to think about testing your code right now. We will discuss the topics here in a bit more detail after the quiz in Thursday's class so check back for the recording when it posts.

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

```python3
def remove_from(the_list: list, value) -> list:
  new_list = []

  for element in the_list:
    if element != value:
      new_list.append(element)

  return new_list
```

At least, that's what we hope it does. Rather than assume it does and continue to build our email list management program, we should test it first:

```python3
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

```python3
>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user5@example.com")
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
```

Is that what we want to happen? What if our program needs to confirm that a removal actually occurred? Well, we could compare **`emails`** to the results, or we could give that responsibility to the **`remove_from`** function:


```python3
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

```python3
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

Now, having to write these tests cases each time we want to test a program can quickly become unwieldy. Fortunately, Python gives us a way to automate much of the work!

The **`assert`** statement is a convenient shortcut for inserting debugging tests into your program. Here we test a normal case, or case that represents typical behavior for the **`remove_from`** function:

```python3
assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]
```

And here we test an error case, or case that generates a result we don't expect:

```python3
try:
  remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user5@example.com")
  assert False, "ValueError should have been thrown"
except ValueError:
  pass
```

If both assertions pass, then we should not expect to see anything from the shell when running the program. However, if an assertion fails, the debugger will notify you of the failure:

```python3
>>> assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]

Traceback (most recent call last):
  File "maillist.py", line 38, in <module>
    assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user2@example.com"]
AssertionError
```

We will get into the more formal test driven approach to software development in a few more weeks, once you have had a chance to experience working with larger, more complex programs. But for now, focus on thinking about the how the code you write should behave, and then write some assertion statements to confirm that it behaves as you expected. I think you will find that new edge conditions will arise that you might not have otherwise considered. And remember, testing is not about quantity! A program with 100 tests is not necessarily better than one with 10. Your goal should be to identify _different_ conditions worth testing, not _variations_ on the same test.



(lectures:classestemp)=
#### Classes
In programming languages that support a class-orientation like Python, classes are used to create templates for objects that can perform state and behavior operations in program code. Classes contain attribute references that take the form of data attributes and methods. Class data attributes and methods are syntactically identical to the variables and functions that you have been writing in Python so far. The primary difference is that data attributes and methods are called and operate on the instance of the class in which they are contained.

A class is declared using syntax that is similar to a function:

```python3
class Fruit:
  pass
```

The example above represents the simplest class that can be created in Python. If we want to make use of this class, we can _instantiate_ or create an _instance_ of the **`Fruit`** that we created and treat it like any other object in Python:

```python3
class Fruit:
  pass

fruit = Fruit()

print(fruit)
```

Which will display something similar to the following in the Python shell:

```python3
>>> <__main__.Fruit object at 0x7ff56b3a78e0>
```

The Python interpreter recognizes the variable **`fruit`** as an instance of the **`Fruit`** class and prints its string representation. Of course, since the **`Fruit`** definition does not have any members, there isn't anything we can really do with it yet. Let's give it some purpose:

```python3
class Fruit:
  fruit_type:str
  color:str
  is_seedless:bool
  condition:str  

```

Now the **`Fruit`** class has some attributes that can be used to describe common characteristics of fruit. Until a class is instantiated it only exists as a kind of blueprint of what it should do and how it should work. If this sounds confusing, it might be helpful to think of a class as a __recipe__ and the instance of a class as the __edible food__ that it produces. Let's follow this food metaphor a bit further and use the **`Fruit`** blueprint created in the previous code snippet to create some different types of fruit:

```python3
apple = Fruit()
apple.fruit_type = "apple"
apple.color = "green"
apple.is_seedless = False
apple.condition = "ripe"

banana = Fruit()
banana.fruit_type = "banana"
banana.color = "brown"
banana.is_seedless = False
banana.condition = "rotten"

print(apple)
print(banana)
```

When run, the print statements at the bottom of the code snippet will display the following in the Python shell:

```python3
<__main__.Fruit object at 0x7f6f9366b880>
<__main__.Fruit object at 0x7f6f9366add0>
```

Notice that both variables are of the same _type_: **`Fruit`**, yet the string representation used by the Python interpreter is different. This tells us that although both of these objects are instances of Fruit, they are not the same object. This is one of the features that makes classes useful in Python. We can create our own _types_ that function according to rules that we determine.

So far the **`Fruit`** class has only been written to hold some simple attributes. The values of those attributes are fairly arbitrary. Since they are mostly of the type **`string`**, we can set them to any string value that we want. For example:

```python3
banana = Fruit()
banana.condition = "sick"
```

Even though programmatically the code snippet above is valid, it doesn't make much sense right? If we intended this class to be used by other programmers, or ensure that we always use it properly, we should lock down the available options for the class attribute **`condition`**. There are a number of ways to accomplish this task, but we are only going to discuss one in this lecture. We'll cover some others in the advanced classes lecture later in the quarter. For now, let's revisit the **`Fruit`** class:

```python3
class Fruit:
  fruit_type:str
  color:str
  is_seedless:bool
  picked_date:str

  def get_condition():
    condition = "unknown"
    age = check_age(self.picked_date)
    if age <= 4:
      condition = "unripe"  
    elif age > 4 and age < 10:
      condition = "ripe"
    elif age > 10:
      condition = "rotten"
    
    return condition
```

The first thing we do is add a new attribute for storing the picked date of the fruit. Then, we replace the **`condition`** attribute with a method (or class function) called **`get_condition`**. The new method will now have control over the kinds of conditions that are possible for the fruit. We'll assume that there is another method available called **`check_age`** that can calculate the age of the fruit based on the values stored in the new **`picked_date`** attribute. Note that to implement the **`check_age`** method, the code snippet would require the use of an additional module, some date/time calculations, and get us too far away from the goal of the lecture. Let's create an instance of this revised **`Fruit`** class and try the new **`get_condition`** method:

```python3
apple = Fruit()
apple.fruit_type = "apple"
apple.color = "green"
apple.is_seedless = False
apple.picked_date = "1/17/2022"

print(apple.get_condition())
```

Depending on the date that you are reading this lecture, your apple could be unripe, ripe, or possibly even rotten (though I hope not!). Okay, so now that you have a basic idea how to write a class, let's look at a more practical example.

##### Lecture Recording

[Classes Lecture](https://uci.yuja.com/V/Video?v=2184495&node=8074840&a=353799435&autoplay=1)

##### Lecture Notes

In assignment 2 you will be required to use a custom module called **`Profile.py`**. To use the **`Profile`** module, you will be required to _instantiate_ classes stored within the module and call its methods to perform certain tasks for you in your program similar to the following code:

```ipython3

server = "localhost"
profile = Profile(server)
profile.get_posts()

```

The term _instantiate_ refers to the action of creating an instance of a class for use within a program. When a class is instantiated, an instance of that class is created as an object upon which the methods and attributes of that class can be called. Consider the following code:

```ipython3

from Profile import Profile

p1 = Profile("")
p1.username = "usr1"

p2 = Profile("")
p2.username = "usr2"

Profile.username = "usr3"

Profile.username = "usr4"

print(p1.username)
print(p2.username)
print(Profile.username)

```

```ipython3
>>> usr1
>>> usr2
>>> usr4
```

Notice that when the statement **`Profile.username`** is printed, the data attribute **`username`** contains the most recently assigned value. This use of class members is called an attribute reference and is identical to the way you have been assigning and evaluating variable references in your program. However, when the same attribute is printed from different instances of the Profile class (p1 and p2), the original value is still assigned. p1 and p2 are object references, or references to attributes of an object (rather than of a class), and demonstrate one of the advantages of writing classes. The code that is written to form a class can be instantiated an infinite number of times and each instance of that class will be unique.

As you studied the Profile module, you learned that there is a second class called **`Post`** that is used to store text and a timestamp when a user writes a new journal entry. You may have noticed that for every post added to the Profile, a new instance of the Post class is created. The Post class, therefore, specifies a template for instances (or objects) of the type Post. The following snippet from the **`load_profile`** method of the Profile class highlights how this operation occurs:

```ipython3
for post_obj in obj['_Profile__posts']:
	post = Post(post_obj['entry'], post_obj['timestamp'])
	post.timestamp = post_obj['timestamp']
	self.add_post(post)
```

Each instance of Post is added to a member of the Profile class that is of type **`dict`** using a helper method called **`add_post`**. We'll dive into methods and other features of classes like the keyword **`self`** a little further on. The important thing to recognize for now is how the Post class is used to represent all of the journal posts a user has created. Once loaded from the DSU file, each post becomes it's own object that can be operated on within a program, making classes suitable for storing and passing multiple types of data as a single object. Additionally, because the class is a template of an object, it is also extensible. Let's say, for example, that a new feature requirement was added to the DSU program: 

> add support for titles to journal entries

Since we already have a template for journal entries, all we have to do as add a new attribute reference to the template, the Post class.

```ipython3
# A simplified version of the Post class used in assignment 2

class Post:
	timestamp = time.time()
	entry = ""
	title = ""
```

Now, when all instances of the Post class are instantiated by the load_profile method, they will have the data attribute **`title`** available for getting and setting a title for post entries.

Alright, so now let's look at some of the rules for writing classes. So far we have been referring to the implementation of a class as a template for creating object instances of the type defined by that class. The action of creating an instance or instantiating a class comes with some built-in functionality that can be quite useful. By default, the instantiation of a class creates an empty object. However, there is a special method, **`__init__()`**, that if defined in a class will automatically be called whenever a new instance of a class is created. This type of special method is often referred to as a _constructor_, because it performs operations as the class is being "constructed."

If you studied the Profile module you likely noticed that both the Profile class and Post class made use of this special method:

```ipython3
# Example of a minimal class constructor
def __init__(self):
	pass

# The Profile class constructor
def __init__(self, dsuserver, username=None, password=None):
	self.dsuserver = dsuserver 
	self.username = username 
	self.password = password 
	self.bio = ''           
	self._posts = []       

# The Post class constructor
def __init__(self, message = None, timestamp = None):
	if timestamp is None:
		timestamp = time.time()

	self.timestamp = timestamp
	self._entry = message
```

The first example in the above code demonstrates the basic structure of the **`__init__`** method. The **`self`** parameter is a built-in attribute reference of the object's instance. In order to access the attributes and methods of a class instance, the **`self`** parameter must be specified. We can see how **`self`** works in the second example above pulled from the Profile class. Notice how the names **`dsuserver`**, **`username`**, and **`password`** are used twice. Although they share the same name, they are distinctly different. One is a parameter of the **`__init__`** method, and the other is an attribute reference of the Profile class. We then distinguish between these like named variables by applying the instance attribute of the class, **`self`**, to the variable using dot notation. When a variable is assigned to the class instance using **`self`**, it automatically becomes an attribute reference of the class instance:

```ipython3
# Example of how the init constructor can be used to create attribute references for class instances.
p = Profile("a server address")
p.username = "usr1"
```

Alright, let's return to the previous example above and discuss the parameters a little bit more. Notice how in both the Profile and Post examples there are additional parameters, some of which are assigned a default value of **`None`**. When writing a class, you may desire to provide the code that makes use of its objects some flexibility in how the class is instantiated. For example, in the Profile class constructor, the parameter **`dsuserver`** is not assigned a default value, therefore the only way to create an instance of the class is to pass a value for the parameter. Whereas, since the other two parameters have been assigned default values, they can be optionally assigned.

The use of default values can be a useful way to guarantee that your class is used the way you intended. However, without adequate protections in place, parameter requirements can be ignored. To get around this constraint, many of you opted to pass in empty strings rather than an actual server address in assignment 2. For the most part, this workaround was largely acceptable because you also had the ability to assign the required parameter to the attribute reference. But what if upon instantiation, the Profile class called code that either validated the parameter value or attempted to use it for it's intended purpose? Without error handling, the program would crash whenever the class was instanced. So it's important to take these types of use cases and outcomes into consideration when writing a class. Given the way the **`dsuserver`** variable is used by the Profile class, do you think it should be assigned a default value rather than be a required parameter?

The last aspect of classes that we will discuss for this lecture is the role of methods in class objects. Again, we'll return to the Profile class as our reference point:

```ipython3
def get_posts(self) -> list:
	return self._posts

def add_post(self, post: Post) -> None:
	self._posts.append(post)
```

The **`get_posts`** and **`add_post`** methods in the example above are taken directly from the Profile class. At first glance, you'll notice that they look identical to the functions that you have been writing throughout this course. Like a function, the method is defined using the **`def`** keyword, accepts parameters, and supports the optional specification of a return type. However, notice that even if when we don't intend to use a parameter, as is the case with **`get_posts`**, the **`self`** parameter is specified. The purpose of a class method is to act upon the class instance in some way, therefore a method must have a way to access the attributes of its class. As with the class constructor, all method signatures (The signature of a method refers to the combination of name, parameters, and return type.) in a class must be assigned the self parameter. 
