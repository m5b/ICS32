Week 3 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 3 Overview

It's week 3. You should be finalizing your work on assignment 1 right about now and getting ready to start assignment 2. The lectures for this week include topics that you will need to start learning for assignment 2. 

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results3`

(lecture-materials)=
## Lecture Materials

Lectures for Week 3
: {ref}`lectures:classes`

(lectures:classes)=
### Classes

#### Videos

[Classes Lecture](https://uci.yuja.com/V/Video?v=2184495&node=8074840&a=353799435&autoplay=1)

#### Notes

In programming languages that support a class-orientation like Python, classes are used to create templates for objects that can perform state and behavior operations in program code. Classes contain attribute references that take the form of data attributes and methods. Class data attributes and methods are syntactically identical to the variables and functions that you have been writing in Python so far. The primary difference is that data attributes and methods are called and operate on the instance of the class in which they are contained.

In assignment 2 you were asked to make use of a module called Profile.py. To use that module, you were required to _instantiate_ it and call its methods to perform certain tasks for you in your program.

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


(quiz-results3)=
## Quiz Results

