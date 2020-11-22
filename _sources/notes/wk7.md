Week 7 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 7 Overview


Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results`

(lecture-materials)=
## Lecture Materials

Lectures for Week 7
: {ref}`lectures:webapi`
: {ref}`lectures:inheritance`


(lectures:webapi)=
### Web APIs

#### Videos

[Web API Lecture Part 1](https://uci.yuja.com/V/Video?v=2242261&node=8181682&a=1186819191&autoplay=1)

[Web API Lecture Part 2](https://uci.yuja.com/V/Video?v=2242265&node=8181686&a=238466118&autoplay=1)

#### Notes

Finally! Now that you have had some time to practice working with API's, let's take a close look at some of the ways we can use the **`urllib`** module to expand the types of API's at our disposal.

Some API's, particularly those that are open or don't require a key, reject requests because they don't like the way it looks. For example, one of your classmates was attempting to work with the following API:

https://api.kanye.rest/

Which, when viewed in the browser works fine, but when requested using **`urlopen`** does not (it returns a 403 forbidden message).  What this tells us is that the API is likely looking for a little more information from the request. Requests without traditional HTTP headers are often interpreted as potential bot/malicious attack threats and so they are often automatically blocked by most API servers. So, we need to modify the request to behave more like a web browser.

```ipython3
import urllib, json
from urllib import request,error

def yeezy():
    url = "https://api.kanye.rest/"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    
    json_results = response.read()
    r_obj = json.loads(json_results)
    print(r_obj)

if __name__ == '__main__':
    yeezy()

```
In the code above, notice that a **`Request`** object is created using the **`url`** variable and a **`headers`** object that contains the same user agent that FireFox on Windows 10 would send. The request object is then passed to **`urlopen`** rather than the raw URL that we've used in previous examples. Now, with more a 'browser-like' appearance, the API can successfully return a quote from Kanye Rest:

```ipython3
{'quote': "I love sleep; it's my favorite."}
```
You may have also noticed the use of **`None`** in the **`Request`** object parameter list. We've used **`None`** here, because we are only interesting in __getting__ something from the supplied URL. But what if we also want to __send__ something? Let's take a look at the object definition adopted from [docs.python.org](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request):

```ipython3
 class urllib.request.Request(url, data=None, headers={}, 
	origin_req_host=None, unverifiable=False, method=None)
```
The data parameter, specified here, can used to send data to a URL. Since Yeezy doesn't require any particular information from us there was no need for us to use this parameter, however, there are cases where sending data might be necessary. If you've ever filled out and submitted a form in a browser, for example, you are sending data to a URL. Recall from the HTTP and URLs lecture that we talked about how HTTP is used to make GET requests to retrieve the content from a URL. Well, GET is one of many request methods made available in the HTTP specification. When data is submitted to a server using HTTP, the POST method is used to inform the server to expect a packet of data in the HTTP request. Let's take a look at how we can add data to a **`urllib`** request and send it to a server:

```ipython3
import urllib, json
from urllib import request,error

def send_data(data: str):
    # the url and port of the ICSHTTP Simple Server:
    url = 'http://localhost:8000'

    # create some data to send, we'll use json format
    json = {'data' : data}

    # properly encode the data for the request object
    data = urllib.parse.urlencode(json)
    data = data.encode('utf-8') 

    # set a header, with content type. We don't need to specify user agent here
    # since we are just sending to a custom server
    headers = {'content-type': 'application/json'}
    req = urllib.request.Request(url, data, headers)

    # make the call, and print the response
    with urllib.request.urlopen(req) as response:
        resp = response.read()
        print(resp)
    
if __name__ == '__main__':
    while True:
        send_data(input("What would you like to send? "))
```

In this program, we add JSON data to the **`Request`** object, though it doesn't have to be JSON. We could have also sent XML, HTML, a file, plain text, and [many more](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types). Once we have determined the type of data to send, the **`content-type`** should be set to match. **`content-type`** is specified in the header and accepts a descriptive value that follows very specific formatting rules (see the previous link for a table of the various types and how they match to data). Once the request object is prepared, as with the previous example, it is sent to the desired server using the **`urlopen`** function. In the example above, we use the **`with`** statement to handle the state of the response object.

To demonstrate how data is transferred over HTTP, let's create a simple HTTP server to listen for POST requests.

```ipython3
import http, socketserver
from http import server 

"""
This is a subclass of the BaseHTTPRequestHandler class which provdies methods
for various aspects of HTTP request management. Since our only goal is to 
show how POST data works, this class simply renders and prints data when a 
POST request is received.
"""
class ICSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.command + " received.")
        data = self.rfile.read(int(self.headers['content-length']))
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write("ok".encode(encoding = 'utf-8'))
        print(data.decode(encoding = 'utf-8'))


"""
This is just basic startup code to run the TCPServer that accompanies
the Python standard library.
"""
PORT = 8000

handler = ICSHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print ("serving at port", PORT)
httpd.serve_forever()

```

The server here is quite rudimentary, it can only handle the very specific requests that we will be sending to it using the client POST request program above. Since we are conducting a deep dive into the **`http`** library for this course, we will only take a cursory pass at the code here. However, if you would like to build out this small HTTP server program a little more, feel free to use this code.

To build a minimal viable HTTP server in Python, we can rely on the **`http`** and **`socketserver`** modules to manage most of the heavy lifting. The only code we will need to create is a custom request handler and a few lines to start the TCPServer that is included in the **`socketserver`** module. Python's **`http`** module includes a couple of request handlers for basic requests (**`SimpleHTTPRequestHandler`** and **`CGIHTTPRequestHandler`**), but neither of these support POST requests by default. So we have to create our own! Fortunately, the **`http`** module also provides a **`BaseHTTPRequestHandler`** that we can build upon (more on that in the Inheritance lecture).

The **`ICSHTTPRequestHandler`** class overrides the inherited method **`do_POST`** to process incoming POST requests. The details of how this is done, are bit out of scope for this course, but you'll notice that we are essentially extracting the data from the request, preparing and sending a response to the client, and then printing the data to the console. In a real application, we would likely need to do something other than print to console though. A traditional HTTP server might send that data to another process to be interpreted or stored somewhere.

The lecture video will contain a running example of all of these programs, but you are STRONGLY encouraged to try running them yourself too! If you would like to learn a little bit more about how to work with HTTP data in Python, you can start by [reading the overview at docs.python.org](https://docs.python.org/3/howto/urllib2.html#data).

I have included one additional look at Web API's using the Spotify API. A walkthrough can be found in Part 2 of the lecture. I don't plan on writing up notes for the Spotify API, but the files for the program are included below.

<a href="../resources/music_finder.py">MusicFinder</a>

<a href="../resources/spotify_credentials.py">Spotify Credentials</a>

 
(lectures:inheritance)=
### Inheritance

#### Videos

[Inheritance Lecture Video](https://uci.yuja.com/V/Video?v=2242269&node=8181690&a=1610946088&autoplay=1)

#### Notes

Did you know that a class can be a child of another class? That a child class can __inherit__ the attributes and methods of its parent? It can, and the process, which we call __inheritance__ is one of the fundamental paradigms of object oriented programming. Let's dive in to some code first, then we'll break down what all of this means.

In the Web API lecture, you may have noticed something odd with the way the **ICSHTTPRequestHanlder`** object was declared:

```ipython3
class ICSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):

```

It looks like the class is specifying a parameter! Well, it sort of is, but notice that the parameter only contains a type of object--it's missing a parameter name. This is the syntactic convention that Python uses to subclass, or inherit, from other classes. When a class __subclasses__ another class in this way, it becomes a __type__ of that class, thereby inheriting all of the parent classes members (attributes and methods). Let's take a quick look at how we can use inheritance to improve reusability of our code.


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

In this example, we have created a new class called **`MessageClass`**. This class is responsible for printing messages of the type **`BaseClass`**. But notice that we never actually passed an object instantiated from **`BaseClass`**, rather we passed it **`SubClass`** and **`AnotherSubClass`** and it worked! This is another fundamental concept of object-oriented programming called __composition__. Composing classes this way can be used to structure and organize the programs that we write while also reducing the amount of code we write. Code reuse is one of the best ways to reduce the likelihood of bugs in our programs.

A good way to think about composition is to consider some of the things we already know about the different types of objects we interact with every day. Take the smartphone for example. At an abstract level, every smartphone has a few common properties like a screen, buttons, microphone, speaker, cpu, gps, etc. So we can might think of all of those common attributes as members of a base class. So we could write a base class, let's call it **`SmartPhone`**, that will manage common attributes for us. Next, we might want to create a class that can do some things that only certain types of smartphones can do, let's call these classes **`iPhone`** and **`Android`**. Both classes can inherit from **`smartphone`** to make use of the common attributes. But each class will also implement its own attributes that are unique to it like touch interactions and apps. We can also go further and compose individual classes for all of the different types of iPhone's and Android phones that exist.


(quiz-results)=
## Quiz Results

The attendance quiz for this week was just a single question regarding the difficulty of assignment two. View the PDF for results.

<a href="../resources/QZ_Week_6_Quiz_Results.pdf">Quiz Results PDF</a>

