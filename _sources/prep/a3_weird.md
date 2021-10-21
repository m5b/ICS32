Assignment 3: Publishing Online
============================

## Introduction

A journaling program, like the one you built for [assignment 2](../a2.md) is a nice way to record and manage personal information. However, there may be some occasions when your users want to share their thoughts with a broader audience. So for this assignment, you will be introducing an __online__ option to your program that allows your users to publish individual posts to a remote server where others can read what they have to say.

This means that your journal entries will be stored locally (on your computer) with an option to be shared to the Internet. Where on the Internet? Any server that supports the ICS32 distributed social platform (DSP) (for now that's just us)!

If you would like to take a quick look at the ICS32 DSP website, feel free to click through to the website:

[ICS32 Distributed Social](http://ics32distributedsocial.com)

The ICS32 DSP website is where you can view user posts published by your program. You don't need to do anything with this website in your program, it's simply here so that you can verify that posts published through your program are successful. Alright, so let's get started!

### Summary of Program Requirements 

1. Write code to support a communication protocol
2. Write code to communicate with a remote server over network sockets

### Learning Goals

1. Communicating with networks and sockets
2. Working with protocols

## Program Requirements

As with the previous assignment, you have a lot of flexibility with how you design your program's user interface. You will not have a validity checker for this assignment, so the input and output of your program is largely up to you. However, there are some conditions:

* You must divide your program into __at least three modules__, not including the Profile module included in the starter code. Your modules should be named and loosely modeled after the descriptions below.
	1. **`a3.py`**: Your first module will be the entry point to your program. It will be responsible for importing and using the other required modules.
	2. **`ds_protocol.py`**: Your adaptation of the DS Protocol. 
	3. **`ds_client.py`**: Your distributed social client module. It should contain all code required to exchange messages with the DS Server.
* You must retain the input command format for any new commands your program may need, which if you recall looks like this:
```ipython3
[COMMAND] [INPUT] [[-]OPTION] [INPUT]
```
* You must use the **`Profile.py`** module that accompanies this assignment without modification to store information about your user and the DS Server.
* You do not have to use the **`input_processor.py`** module you created for a2. However, since you will add new user interactions to your program, it makes sense to continue building out this module. 
* All modules that you edited must include the following comment on the first three lines:

```python3

# NAME
# EMAIL
# STUDENT ID

```

Otherwise, you are free to design your program any way you like. This means if you would like to provide more helpful feedback after error conditions, for example, you are free to do so.

The program you will be creating is divided into two parts. I strongly encourage you to read through both parts so that you have a clear picture of what the complete program will do. Then focus on completing part 1 first. Ensure that part 1 is reliably working before continuing on to part 2.

### Part 1


Much of the work you will need to do to connect to the DS Server using network sockets is covered in the Networks and Sockets lecture. If you haven't watched the lecture or looked through the notes yet, now is a good time!

Unlike the **`Profile.py`** module that is supplied to you, you will need to complete the **`ds_client.py`** module yourself. The starter code for this module contains the following function signature.

```ipython3
# ds_client.py

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  pass

```

You must ensure that the **`send`** function specified above can successfully communicate with the DS server using the parameters specified. You __must not__ change the signature of this function. If you do, you will likely not pass the grading tool that we use.

```{admonition} Tip
:class: tip

The **`send`** function does not have to include all the code required to communicate with the server. In fact, if you try to do everything with this function you will likely run into design problems. Instead, think about each of the steps that this function must perform and consider how thye might be organized into smaller single task functions.

```

The tool that we will use for grading will import your **`ds_client.py`** module and call this function with randomly generated values. When called, the information we supply should either successfully transmit the data to the DSP Server or, in the case of incorrect data, gracefully inform our program what went wrong.

```{admonition} Program Feature
Connect to, send, and receive information with a remote DSP server
```

When communicating with a server using sockets, it is common to establish a protocol for exchanging messages. A protocol is a predefined system of rules to transfer information between two or more systems. For this assignment, your program will need to support the DSP protocol to successfully communicate with the DSP server. Your protocol handling code should be placed in the **`ds_protocol.py`** module.

The DSP protocol supports the following send commands:

join
: Accepts either an existing user and password, or a new user and password

post
: Accepts a journal post for the currently connected user

bio
: Accepts a user bio, either adding or replacing existing user bio


All protocol messages must be sent in JavaScript Object Notation (JSON) format. All responses from the DSP server will be in JSON format as well.

```{admonition} Tip
:class: tip

You don't have to concern your self too much with JSON for this class. However, if you would like to learn more about JSON and why it is a great format for storing and transporting data, visit:

<a href="https://www.json.org/json-en.html">JSON.org</a>

```

The following code snippets demonstrate how each of the DSP commands should be wrapped in JSON. You are free to adopt these templates for your program.

```ipython3
# join as existing or new user
{"join": {"username": "ohhimark","password": "password123","token":"user_token"}}


# timestamp is generate automatically in the Profile module using Python's 
# time.time() function
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}


# for bio, you will have to generate the timestamp yourself or leave it empty.
{"token":"user_token", "bio": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
```

The DSP protocol also supports response commands:

error
: Will be received when a send command is unable to be completed

ok
: Will be received when a send command is successful

Your program should expect one of these two responses after sending a command. The following code snippet demonstrates how the response command should be wrapped in JSON. Again, you are free to adopt this template for your program.

```ipython3

# Error messages will primarily be received when a user has not been 
# established for the active session. For example, sending 'bio' or 'post' 
# before 'join'
{"response": {"type": "error", "message": "An error message will be contained here."}}

# Ok messages will be receieved after every successful send command. 
# They likely will not be accompanied by a message.
{"response": {"type": "ok", "message": "", "token":"user_token"}}
```

```{admonition} Program Feature
Adapt the DSP protocol for use in your program.
```

A typical exchange between a program and a DS server might look like the following:

```ipython3

join_msg = '{"join": {"username": "ohhimark","password": "password123", "token":""}}'

send = client.makefile('w')
recv = client.makefile('r')

send.write(join_msg + '\r\n')
send.flush()

resp = recv.readline()
print(resp)
	
>>> b{"response": {"type": "ok", "message": "Welcome back, ohhimark", "token": "07da3ddc-6b9a-4734-b3ca-f0aa7ff22360"}}
```

In your Python code, you will treat JSON messages as type string. In the snippets above, you will likely need to replace the hard coded values (_e.g.,_ ohhimark, password123, etc.) with the variables in your program that store the actual data you intend to send to the DSP server. There are many ways to do this, but you should focus your efforts on using the string formatting functions found in the Python Standard Library.

To process the messages from the DSP server you will need to adapt the following function, which can be found in your starter code, to reduce some of the extra work of parsing strings:

```ipython3
import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['foo','baz'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

# Example Test
json_msg = '{"foo":"value1", "bar": {"baz": "value2"}}'
print(extract_json(json_msg))

>>> DataTuple(foo='value1', baz='value2')
```

Finally, if you have made it this far, you are probably wondering about the information required to connect to the DSP server. Since this project page is public and I would like to avoid undesirable traffic aimed at my server, I will be communicating server details via Zulip only. In the meantime, you should be able to run some client side tests using the echo server covered in lecture. 

### Part 2

At this point you should be able to run the following small program and successfully see a message posted to the [ICS32 Distributed Social](http://ics32distributedsocial.com) website.

```python3
# dsp_demo.py

import ds_client
server = "127.0.0.1" # replace with actual server ip address
port = 8080 # replace with actual port
ds_client.send(server, port, "f21demo", "pwd123", "Hello World!")
```

Feel free to change the username and password used in the previous example to anything you like. Once a username is registered to a password, however, you must always use the same password when sending information to the DSP server.

Now that you are able to connect and send content to the server, it's time to integrate the functionality into your user interface. In assignment 2, you built a local-first journaling program. Your interface enabled a user to write and save journal entries to a custom file using the **`Profile`** module. For part 2 of this assignment, you will extend your journaling program to allow your user to optionally choose to post journal entries to the DSP server.

```{admonition} Program Feature
Extend your journal user interface to support posting journal entries to the DSP server.
```

You may recall that the **`Profile`** class included an attribute called **`dsuserver`** that was not required for assignment 2. You will use this parameter to store the IP Address of the DSP server. For this course, we will assume that value for **`port`** will never change, so you can safely hard code the port number that you will receive into your code somewhere. Just be sure that your **`ds_client`** **`send`** function uses the port parameter, not your hard coded port. You do not have to store the port in the user profile.

```{admonition} Program Feature
Extend your journal user interface to collect the desired DSP server from the user.
```

Your user interface will allow the user to specify which server they want to use for publishing journal entries. Once this feature is complete the only thing left to do is add support for posting journal entries to the server. How you approach this requirement will depend on how you have implemented your program so far. For example, you might decide to prompt the user to post online after every new entry. Or you might prefer to let the user select a journal entry (perhaps by using the Print feature from a2) to post from a list of all entries. Think it through and do what you think makes the most sense for your program.

The ICS32 DSP website is where you can view user posts published by your program. You don't need to do anything with this website in your program, it's simply here so that you can verify that posts published through your program are successful. Alright, so let's get started!

### Summary of Program Requirements 

1. Write code to support a communication protocol
2. Write code to communicate with a remote server over network sockets

### Learning Goals

1. Communicating with networks and sockets
2. Working with protocols

## Program Requirements

As with the previous assignment, you have a lot of flexibility with how you design your program's user interface. You will not have a validity checker for this assignment, so the input and output of your program is largely up to you. However, there are some conditions:

* You must divide your program into __at least three modules__, not including the Profile module included in the starter code. Your modules should be named and loosely modeled after the descriptions below.
	1. **`a3.py`**: Your first module will be the entry point to your program. It will be responsible for importing and using the other required modules.
	2. **`ds_protocol.py`**: Your adaptation of the DS Protocol. 
	3. **`ds_client.py`**: Your distributed social client module. It should contain all code required to exchange messages with the DS Server.
* You must retain the input command format for any new commands your program may need, which if you recall looks like this:
```ipython3
[COMMAND] [INPUT] [[-]OPTION] [INPUT]
```
* You must use the **`Profile.py`** module that accompanies this assignment without modification to store information about your user and the DS Server.
* You do not have to use the **`input_processor.py`** module you created for a2. However, since you will add new user interactions to your program, it makes sense to continue building out this module. 
* All modules that you edited must include the following comment on the first three lines:

```python3

# NAME
# EMAIL
# STUDENT ID

```

Otherwise, you are free to design your program any way you like. This means if you would like to provide more helpful feedback after error conditions, for example, you are free to do so.

The program you will be creating is divided into two parts. I strongly encourage you to read through both parts so that you have a clear picture of what the complete program will do. Then focus on completing part 1 first. Ensure that part 1 is reliably working before continuing on to part 2.

### Part 1


Much of the work you will need to do to connect to the DS Server using network sockets is covered in the Networks and Sockets lecture. If you haven't watched the lecture or looked through the notes yet, now is a good time!

Unlike the **`Profile.py`** module that is supplied to you, you will need to complete the **`ds_client.py`** module yourself. The starter code for this module contains the following function signature.

```ipython3
# ds_client.py

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  pass

```

You must ensure that the **`send`** function specified above can successfully communicate with the DS server using the parameters specified. You __must not__ change the signature of this function. If you do, you will likely not pass the grading tool that we use.

```{admonition} Tip
:class: tip

The **`send`** function does not have to include all the code required to communicate with the server. In fact, if you try to do everything with this function you will likely run into design problems. Instead, think about each of the steps that this function must perform and consider how thye might be organized into smaller single task functions.

```

The tool that we will use for grading will import your **`ds_client.py`** module and call this function with randomly generated values. When called, the information we supply should either successfully transmit the data to the DSP Server or, in the case of incorrect data, gracefully inform our program what went wrong.

```{admonition} Program Feature
Connect to, send, and receive information with a remote DSP server
```

When communicating with a server using sockets, it is common to establish a protocol for exchanging messages. A protocol is a predefined system of rules to transfer information between two or more systems. For this assignment, your program will need to support the DSP protocol to successfully communicate with the DSP server. Your protocol handling code should be placed in the **`ds_protocol.py`** module.

The DSP protocol supports the following send commands:

join
: Accepts either an existing user and password, or a new user and password

post
: Accepts a journal post for the currently connected user

bio
: Accepts a user bio, either adding or replacing existing user bio


All protocol messages must be sent in JavaScript Object Notation (JSON) format. All responses from the DSP server will be in JSON format as well.

```{admonition} Tip
:class: tip

You don't have to concern your self too much with JSON for this class. However, if you would like to learn more about JSON and why it is a great format for storing and transporting data, visit:

<a href="https://www.json.org/json-en.html">JSON.org</a>

```

The following code snippets demonstrate how each of the DSP commands should be wrapped in JSON. You are free to adopt these templates for your program.

```ipython3
# join as existing or new user
{"join": {"username": "ohhimark","password": "password123","token":"user_token"}}


# timestamp is generate automatically in the Profile module using Python's 
# time.time() function
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}


# for bio, you will have to generate the timestamp yourself or leave it empty.
{"token":"user_token", "bio": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
```

The DSP protocol also supports response commands:

error
: Will be received when a send command is unable to be completed

ok
: Will be received when a send command is successful

Your program should expect one of these two responses after sending a command. The following code snippet demonstrates how the response command should be wrapped in JSON. Again, you are free to adopt this template for your program.

```ipython3

# Error messages will primarily be received when a user has not been 
# established for the active session. For example, sending 'bio' or 'post' 
# before 'join'
{"response": {"type": "error", "message": "An error message will be contained here."}}

# Ok messages will be receieved after every successful send command. 
# They likely will not be accompanied by a message.
{"response": {"type": "ok", "message": "", "token":"user_token"}}
```

```{admonition} Program Feature
Adapt the DSP protocol for use in your program.
```

A typical exchange between a program and a DS server might look like the following:

```ipython3

join_msg = '{"join": {"username": "ohhimark","password": "password123", "token":""}}'

send = client.makefile('w')
recv = client.makefile('r')

send.write(join_msg + '\r\n')
send.flush()

resp = recv.readline()
print(resp)
	
>>> b{"response": {"type": "ok", "message": "Welcome back, ohhimark", "token": "07da3ddc-6b9a-4734-b3ca-f0aa7ff22360"}}
```

In your Python code, you will treat JSON messages as type string. In the snippets above, you will likely need to replace the hard coded values (_e.g.,_ ohhimark, password123, etc.) with the variables in your program that store the actual data you intend to send to the DSP server. There are many ways to do this, but you should focus your efforts on using the string formatting functions found in the Python Standard Library.

To process the messages from the DSP server you will need to adapt the following function, which can be found in your starter code, to reduce some of the extra work of parsing strings:

```ipython3
import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['foo','baz'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

# Example Test
json_msg = '{"foo":"value1", "bar": {"baz": "value2"}}'
print(extract_json(json_msg))

>>> DataTuple(foo='value1', baz='value2')
```

Finally, if you have made it this far, you are probably wondering about the information required to connect to the DSP server. Since this project page is public and I would like to avoid undesirable traffic aimed at my server, I will be communicating server details via Zulip only. In the meantime, you should be able to run some client side tests using the echo server covered in lecture. 

### Part 2

At this point you should be able to run the following small program and successfully see a message posted to the 


You may also be wondering, what happens to all the messages you send...Well, since we are using networked sockets, you may have guessed, all of your messages will be published to a publicly available web page. So be kind and respectful in the messages you write!



### Starter Project

<a href="https://classroom.github.com/a/09MqKJt1">Assignment 3 Starter Repository</a>

### How we will grade your submission
																		
This assignment will be graded on a 150 point scale, with the 150 points being allocated completely to whether or not you submitted something that meets all of the above requirements. The following rubric will be used:

Requirements and Function | 100 pts
: Does the program do what it is supposed to do?
: Does the ds_client module function independently of the rest of the program?
: Are there any bugs or errors?

You may also be wondering, what happens to all the messages you send...Well, since we are using networked sockets, you may have guessed, all of your messages will be published to a publicly available web page. So be kind and respectful in the messages you write!



### Starter Project

<a href="https://classroom.github.com/a/09MqKJt1">Assignment 3 Starter Repository</a>

### How we will grade your submission
																		
This assignment will be graded on a 150 point scale, with the 150 points being allocated completely to whether or not you submitted something that meets all of the above requirements. The following rubric will be used:

Requirements and Function | 100 pts
: Does the program do what it is supposed to do?
: Does the ds_client module function independently of the rest of the program?
: Are there any bugs or errors?

Module Usage | 30 pts
: Are all required modules named and used as specified?

Quality and Design        | 20 pts 
: Is the code well designed?
: Is the code clearly documented?

Now that you have successfully completed a few large programs, we will be applying a rigid assessment of your program design and quality. If you have not been putting time into organizing and documenting your code, now is a good time to start.

