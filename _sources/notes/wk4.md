Week 4 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 4 Overview

It's week 4 and you have successfully submitted your first major python program! Take a minute to reflect on the experience. What worked? What didn't? As we move forward, it's going to be even more important to stay on top of your responsibilities for each assignment. So I want to encourage you to take a few moments to think about your workflow for a1. Try and identify areas of improvement (e.g., participate in Zulip discussion, get an early start, outline your requirements, or set daily programming goals) and take action on them for a2.

If you missed live class or want to review the assignment 2 overview, here is the recording:

[Assignment 2 Overview](https://uci.yuja.com/V/Video?v=2476247&node=9030309&a=2105505015&autoplay=1)

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results3`

(lecture-materials)=
## Lecture Materials
: {ref}`lectures:http`

Lectures for Week 4

In light of some of our discussions during live quiz and discussion this week, I will be putting together a couple supplementary lectures that cover the following topics:

* Encoding/Decoding
* JSON processing

I should have them ready to go by the time of co-working class on Thursday.

(lectures:http)=
### HTTP and URLs

```{note}
I am releasing this lecture a little early for those interested in a little more discussion about protocols using a real world example. However, the Python related materials (e.g., urllib) will not be relevant until A3.
```

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


(quiz-results3)=
## Quiz Results

[Live Quiz and Discussion](https://uci.yuja.com/V/Video?v=2476234&node=9030272&a=362320989&autoplay=1)


<a href="../resources/QZ_Week_4_Quiz_Results.pdf">Quiz Results</a>

