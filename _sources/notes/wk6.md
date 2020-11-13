Week 6 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 6 Overview


Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results`

(lecture-materials)=
## Lecture Materials

Lectures for Week 6
: {ref}`lectures:classes`
: {ref}`lectures:http`
: {ref}`lectures:webapi`

(lectures:finalproject)=
### Final Project Discussion

[Live Discussion/Q&A](https://uci.yuja.com/V/Video?v=2173451&node=8053285&a=493975201&autoplay=1)

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
	self.__posts = []       

# The Post class constructor
def __init__(self, message = None, timestamp = None):
	if timestamp is None:
		timestamp = time.time()

	self.timestamp = timestamp
	self.__entry = message
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
	return self.__posts

def add_post(self, post: Post) -> None:
	self.__posts.append(post)
```

The **`get_posts`** and **`add_post`** methods in the example above are taken directly from the Profile class. At first glance, you'll notice that they look identical to the functions that you have been writing throughout this course. Like a function, the method is defined using the **`def`** keyword, accepts parameters, and supports the optional specification of a return type. However, notice that even if when we don't intend to use a parameter, as is the case with **`get_posts`**, the **`self`** parameter is specified. The purpose of a class method is to act upon the class instance in some way, therefore a method must have a way to access the attributes of its class. As with the class constructor, all method signatures (The signature of a method refers to the combination of name, parameters, and return type.) in a class must be assigned the self parameter. 

(lectures:http)=
### HTTP and URLs

#### Videos

[HTTP and URLs Lecture](https://uci.yuja.com/V/Video?v=2192198&node=8090501&a=890308300&autoplay=1)

#### Notes

In the protocols lecture, we used the HyperText Transfer Protocol (HTTP) as an example of a common type of protocol that is used to send and receive data between a client and server computer. HTTP is a request/response protocol that is used by nearly all web traffic for communication and behaves roughly according to the following diagram:

![http diagram](../resources/http_diagram.png)

A client (the laptop) initiates a connection with a server (the black box) to which the server can either accept or, for a variety of reasons, reject. If the server accepts the connection, the client then proceeds to issue requests. Each request issued by the client receives a response from the server. This basic request/response dialogue is occurring every time you visit a website. The URLs that you type into your browser represent the address or location of the server you would like to connect to. Now digging into the underlying infrastructure of the Internet is a bit beyond the scope of this course, but it's important to understand that the textual URLs that we use are primarily designed to make finding and recalling servers easier for humans. The actual identifier the server responds to is a numerical address called an Internet Protocol Address, or IP Address. Every URL that we type into a browser is associated with an IP Address. You can discover this for yourself by using the **`ping`** program that is packaged with most operating systems:

![ping](../resources/ping.png)

The association between IP Address and the human readable URLs that we use is called a Domain Name Server or DNS. DNS is operated by numerous third party organizations who ensure that the human readable domain names are unique and connect to the correct server IP Addresses.

Alright, now that we have a basic understanding of HTTP, URLs, and IP Addresses, let's take a closer look at how HTTP actually works. In the example below, a program called telnet was used to issue a GET request to the ICS 32 Distributed Social website. The response from the server begins with the following line that reads "HTTP/1.1 200 OK". Everything before that was input and output with the telnet program. (If you are on Linux or OSX you should have telnet installed by default. On Windows you can try this with a program called [Putty](https://putty.org).

![telnet](../resources/telnet_get.png)

The server responds with an HTTP header that contains some information about the web page we are requesting. What we are primarily concerned with here is the first line, particularly the use of the status code 200. The specification for HTTP 1.1 includes over forty status codes that a fully featured program that makes use of HTTP should be able to handle. However, for our discussion here, as well as the work required in assignment 3, you will only need to be concerned with a few of the most common status codes:

200 OK
: Indicates the status is OK.

400 Bad Request
: Indicates the HTTP request sent to the server contains invalid syntax

401 Unauthorized
: Indicates that the requested resource is not authorized to be returned in a response

403 Forbidden
: Indicates that a requested resource is protected by the server

404 Not Found
: Indicates that a requested resource is not available on the server

500 Internal Server Error
: Indicates that the server is unable to process the request

504 Gateway Timeout
: Indicates that the server was unable to respond to a request within the allowed time period

You have likely encountered at least one of these while browsing the web (and the 400 level errors might sound familiar if you watched the final season of Mr. Robot!). 

So far we have been discussing HTTP within the context of programs like telnet, Putty, and your web browser. However, there is nothing particularly special about any of these programs. They are just programs, written in a programming language, and understand how to communicate with servers using HTTP. So, just like your browser, we can use a programming language to accomplish the same goals. While Python does have libraries available for building robust programs that leverage the full HTTP specification, it also includes some higher level abstractions modules that can be used by programs that only need to perform some basic HTTP requests with a server. So for the remainder of this lecture, we will focus on working with the simplest of those modules, **`urllib`**.

##### urllib

The urllib package contains several modules that are useful for working with and requesting information from URLs:

* urllib.request
* urllib.error
* urllib.parse
* urllib.robotparser

You can read more about each in detail at the [Python Documentation website](https://docs.python.org/3/library/urllib.html). For this lecture, we will be focusing on the **`urllib.request`** and **`urllibparse`**, however, you will want to familiarize your self with the **`urllib.error`** module as well for handling exceptions raised by **`urllib.request`**.

###### urllib.parse

The **`urllib.parse`** module provides functions for parsing URLs:

```ipython3
from urllib.parse import *

u = urlparse("https://ics32-fa20.markbaldw.in/notes/wk6.html")
print(u)

```
```ipython3
>>> ParseResult(scheme='https', netloc='ics32-fa20.markbaldw.in', path='/notes/wk6.html', params='', query='', fragment='')
```
The **`urlparse`** function accepts a URL string as a parameter and returns a named tuple containing the attributes and values of the supplied url. You can read more about what each of the attributes means at the Python Documentation page linked above.

In the classes lecture, we learned about how to use constructor parameters to control how the classes we write are instantiated. We discussed the **`dsuserver`** parameter and how we might want to validate the parameter before we allow the Profile class to be instantiated. Well, the **`urllib.parse`** module provides one way to go about performing that validation. Let's try and parse our URL for the Distributed Social server:

```ipython3
uri = "ws://168.235.86.101:9996/ws"
u = urlparse(uri)
print(u)

u = urlparse("")
print(u)

```
```ipython3
>>> ParseResult(scheme='ws', netloc='168.235.86.101:9996', path='/ws', params='', query='', fragment='')
>>> ParseResult(scheme='', netloc='', path='', params='', query='', fragment='')
```

Notice how when the correct URL is specified we receive a named tuple with the scheme attribute set to 'ws' (because we are using the websocket protocol for communication). Yet, when an empty string is supplied, the scheme is an empty string. So this is just one way we could ensure that the **`dsuserver`** parameter is valid. Of course, it would be much simpler just to check if the parameter is an empty string, however, that is only one of many possible error conditions that may arise when someone uses the Profile class. Therefore, applying a robust validation process like **`urlparse`** can protect us from a variety of error conditions.

Let's try to parse one more URL, but this time something a little more complex. In the next example I will borrow a URL from the assignment 3 overview:

```ipython3

uri = "https://api.openweathermap.org/data/2.5/weather?zip=92697,US&appid=b64a375a083d857905dad51eb470980a"
u = urlparse(uri)
print(u)
print(u.hostname)
print(u.scheme)
print(u.query)

```
```ipython3
>>> ParseResult(scheme='https', netloc='api.openweathermap.org', path='/data/2.5/weather', params='', query='zip=92697,US&appid=b64a375a083d857905dad51eb470980a', fragment='')
>>> api.openweathermap.org
>>> https
>>> zip=92697,US&appid=b64a375a083d857905dad51eb470980a
```

Now the **`ParseResult`** named tuple also contains a value for the **`query`** attribute. And because we are working with a named tuple, using dot notation, we have direct access to each of the values parsed from the supplied URL. Alright, in the next section we will conclude with a closer look at **`urllib.request`**.
 
###### urllib.request


The **`urllib.request`** module provides a variety of functions for creating and working with HTTP requests. Most of these functions support features that we will not be concerned with in this course. Instead, we will focus on the core function in module, **`urlopen`**, that accepts a URL as a parameter and returns an **`HTTPResponse`** object that contains the response from the server specified by the URL. Let's start by calling **`urlopen`** on the ICS32 Distributed Social website:

```ipython3
from urllib.request import urlopen
uri = "http://168.235.86.101:9996"
res = urlopen(uri)
data = res.read()
res.close()

print(data)
```
```ipython3
b'<html lang="en">\n  <head>\n    <title>ICS 32 Distributed Social</title>\n    <meta name=\'viewport\' content=\'width=device-width initial-scale=1\' />\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n    <link rel=\'stylesheet\' href=\'./css/source-sans-pro.min.css\' type=\'text/css\' />...\n\n'
```

First, notice that the **`HTTPResponse`** object is closed when operations on it are complete. As with file objects and sockets, **`HTTPResponse`** makes use of a binary stream to retrieve and store data. Since it is a stream, we have access to many of the same operations, like **`read()`**. Calling the **`read`** function returns the response body returned from the **`urlopen`** request. The response body is basically whatever content existed at the specified URL, which in this case is the HTML stored in the root file on the server. Looking at the print out of the response data, however, you will notice that it is prepended by the character 'b' (also note that the response data has been manually trimmed down for aesthetic purposes, indicated by the addition of the '...' characters). When we print data to the shell, the addition of the 'b' character indicates that what we are looking are bytes, not a string. To work with the bytes stored in the variable **`data`** like a string, we must first convert from a type of bytes to a type of string:

```ipython3
print(type(data))

text = data.decode(encoding = 'utf-8')
print(type(text))

```
```ipython3
>>> <class 'bytes'>
>>> <class 'str'>
```

**`decode`** and **`encode`** are built-in functions of the **`bytes`** type that support converting between bytes and strings. The encoding type of UTF-8 tells the encoding and decoding functions what type of bytes we expect. For the most part, in the work we do in this course, it is safe to assume that strings will be encoded using UTF-8. However, in the real world, different computing systems and regions of the world quite frequently use different types of encoding, so it is always good practice to ensure you are using the right encoding. How do we know? Well, take a minute to scroll back up to the telnet example. You will notice in the screen shot that the HTTP header we received from our GET request has an attribute called **`Content-Type`** which specifies the encoding character set for the page! Fortunately, **`HTTPResponse`** makes it easy to retrieve the header content:
```ipython3
header = res.getheader("Content-Type")
print(header)
```
```ipython3
>>> text/html; charset=UTF-8
```

So now, with a little string manipulation on the header value, we can specify our encoding type without having to guess.

(lectures:webapi)=
### Web APIs

Will try to release by Saturday. Might get bumped to Week 7, Monday.

#### Videos


(quiz-results)=
## Quiz Results

The attendance quiz for this week was just a single question regarding the difficulty of assignment two. View the PDF for results.

<a href="../resources/QZ_Week_6_Quiz_Results.pdf">Quiz Results PDF</a>

