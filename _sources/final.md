Final Project
============================

## Overview

As discussed in the course overview, you will not be required to take a midterm or final exam. Rather, we will be assessing your understanding of the course material by asking you to apply what you have learned through a final project. At this point in the class you have learned how to work with the computer file system, modules, sockets, and APIs. You have also learned how to write simple tests for your code, classes, apply recursive function calls, and handle exceptions that occur when your program runs. Therefore, your final project should build upon and extend what you have learned so far and completed in your assignments.

The final project is worth a total of 30 points, more than double what you will earn for all course assignments, which means you should target an individual project workload that is equal to or greater than what you have completed for any two assignments in the course. You will have roughly five and a half weeks to complete your final project, so take this into account when planning your work. To help you manage the final project alongside your remaining three assignments, you will be allowed to work in groups. Working in a group is __optional__ and will be limited to a __maximum of three__. 

```{note}
If you choose to work in a group you must create a team name and nominate a leader. The leader will be responsible for communication and submission. Once you have a group and name, notify your TA so that they can create a final project group for you in Canvas. DO NOT wait until the last week of class to formalize your group. Take care of this step as soon as possible.
```

For your final project you will develop your own module that enables a program to send and receive direct messages with another user on the DS platform. You will then incorporate this module into a graphical user interface (GUI) using Tkinter.

## Part 1: The DS Direct Messenger Module

The first thing you will do is write the direct messenger module. Your module must adhere to the following rules:

* Must be named **`ds_messenger.py`**
* Must implement the following classes and methods

```ipython3

class DirectMessage:
  def __init__(self):
    recipient = None
    message = None
    timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
		
  def send(self, message:str, recipient:str) -> bool:
    pass
		
  def retrieve_new(self) -> DirectMessage:
    pass
 
  def retrieve_all(self) -> List:
    pass

```

You are free to add as many supporting methods to either of these classes that you need, but a program should be able to import your module and use these functions to send direct messages with a DS server.

To support this new feature, the DSP protocol will be expanded to support direct messaging using the following commands:

directmessage
: Accepts a message to be sent directly to another user. 

```ipython3
# Send a directmessage to another DS user
{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

# Request unread message from the DS server
{"token":"user_token", "directmessage": "new"}

# Request all messages from the DS server
{"token":"user_token", "directmessage": "all"}
```

The DS server will respond to **`directmessage`** requests with the following **`ok`** response messages:

```ipython3
# Sending of direct message was successful
{"response": {"type": "ok", "message": "Direct message sent", "token":"user_token"}}

# Response to request for **`new`** message. Timestamp is time in seconds 
# of when the message was originally sent.
{"response": {"type": "ok", "message": "Hello User!", "from":"markb" "timestamp":"1603167689.3928561"}}

# Response to request for **`all`** messages.
{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb" "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript" "timestamp":"1603167689.3928561"}]}}
```

The **`ds_messenger.py`** module should stand on its own. You may reuse the code you have written for other modules like **`ds_client.py`** and **`ds_protocol.py`**, but they should not be required to use the direct message feature of the DS server. You will also need to migrate existing message protocol formats to perform join operations and parse error messages used in previous assignments.

## Part 2: The Graphical User Interface

For the second part of the assignment you will write a graphical user interface (GUI) for your module using Tkinter. You are free to implement the interface however you like or adapt the Tkinter GUI that you were given in assignment 5. 

There are many ways to create a graphical interface for a direct messaging program. You are not required to follow the example below. However, if you are not sure where to start the following wireframe should point you in the right direction.

![tkinterexample](resources/final_project_tk_example.png)			

In the wireframe model presented above, there are 5 widgets that are responsible for all of the input and output in the program:

1. On the left is a treeview widget that displays all of the DS users that have sent you messages.Selecting a user will display the messages that they have sent in (2).
2. On the upper right is the display widget that contains the messages sent by the user selected in (1).
3. On the lower right is the text input widget where new messages are written.
4. The 'Add User' button is where new users can be added for direct messages.
5. The 'Send' button sends the message entered in (3).

```{tip}
The layout used in this wireframe is nearly identical to the layout provided to you in assignment 5. You may reuse that existing code to save you some steps.
```

## Final Submission
To receive full credit your final project must make __informed__ use of the following:

Classes
: You have been provided with some skeletal classes to use in your module. However, there will undoubtedly be other areas of the program where a class improves your program design. You must use at least one new class in addition to what has already been provided for you.

Custom Exceptions
: Your **`ds_messenger.py`** module should implement _at least one_ custom exception class.

Use of try/except
: Areas of code prone to exceptions (sockets, file i/o, etc.) should be wrapped in try/except statements.

Commenting and Documentation 
: Your overall final program should contain sufficient code comments for a new programmer to be able to understand what your code does.
: All methods and classes in your **`ds_messenger`** module _must_ adhere to the reStructuredText (reST) docstring format. You will be required to generate your own module documentation in PDF format and submit alongside your program.

Function
: Your program must work. Functionality of your program will be assessed in two ways. First, a user should be able to run your program and send and receive direct messages with a DS server. Second, your **`ds_messenger.py`** module must work outsider of your main program. We will use a validity checker program for grading that imports your module and makes calls on the required classes and methods.

```{note}
Informed use means that you have thoughtfully applied the requirements in a way that is beneficial to your program. In other words, do not simply make up pointless tests or classes to check a box for the assignment.
```

You will submit all files required to run your project along with a README file that details any required instructions on how to build and run it. You must also include all references and sources that you used to build your project. If you included code in your project from an external source (__e.g.__, StackOverflow, text books, sample programs, and so on), you must cite these sources in the readme as well as leave comments in your code files indicating where it was found by you or your group members.

#### Grading

The majority of your grade will be based on whether or not you completed the "core" requirements listed in your project requirements document.

Requirements (25 points)
: Does the program fulfill the requirements agreed upon by the client (your Professor and TA's). Requirements will be assessed on implementation (does it exist) and functionality (does it work).

Validity (2.5 points)
: Does the project adhere to the principles taught in class for creating robust and bug free code. 

Documentation (2.5 points)
: Does the project provide sufficient documentation. Your code should be well commented so that we can understand what purpose it serves in your project. Your README should clearly explain how to run your project. And when run, the functionality of your project should be clear and intuitive.

In total you will be able to receive 30/30 points for this final project. Your final submission should include all materials described in Parts 1 and 2, zipped and uploaded to the Canvas submission page by the due date. Since this is the last assignment for the course, there will be no late submissions accepted.


