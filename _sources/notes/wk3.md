Week 3 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 3 Overview

It's week 3. You should be finalizing your work on assignment 1 right about now and getting ready to start assignment 2. The lectures for this week include topics that you will need to start learning for assignment 2. 

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results`

(lecture-materials)=
## Lecture Materials

Lectures for Week 3
: {ref}`lectures:networks`
: {ref}`lectures:protocols`

(lectures:networks)=
### Networks and Sockets

#### Videos

[Networking and Sockets Lecture](https://uci.yuja.com/V/Video?v=2093512&node=7861887&a=1763099740&autoplay=1)

#### Working with Sockets

In a1 and a2, you are tasked with storing and retrieving data from the file system by opening, reading or writing, and closing a file using Python's built-in functions for file management. **`open()`**, **`close()`**, **`read()`**, and **`write()`**, as examples, allow us to open a _stream_ to a file to send and receive data to a file located in our computer's file system

But what if we wanted to send and receive data to a different computer? We could continue to use the file system to store the data and then find a way to transfer the file over a network connection. Or, we could create a direct connection to a networked computer and _stream_ the data directly. Since we are not going to concern ourselves with the transfer of files just yet, let's look at how we can use Python's networking interface to send data to another computer.

In Python, we can think of a _networking_ interface as any tool that facilitates communication with another computer over an ethernet connection. In the following diagram, a network connection has been established between two computers. Although the diagram does not specify, we can assume that the client (laptop) and server (box) are both connected to a common network (_e.g.,_ a corporate lan, wan, or the Internet). In order to communicate with each other, the server exposes a unique IP address (168.235.86.101, as depicted here for example) and the client must know of that IP address.

![networking](../resources/sockets_overview.png)			

When the client is ready to connect, it first checks to see if the server's address is available for connections. If available, the server sends a _response_ to confirm and then waits for data to be sent from the client. Communication is performed using a socket, which in Python, is a wrapper on many of the underlying details that computers must establish to stream data. For the purposes of this lecture, we will focus on a fairly narrow set of the many ways that sockets can be used. So our primary concern here is how sockets send and receive data. Notice in the diagram above, that each computing system has two sockets: a response socket and a send socket, which represent the _input stream_ of data from a remote computer and the _output stream_ of data that is sent from the local computer. When data is streamed to the socket, Python's socket library attempts to ensure that all data is sent or received arrives intact and in the order it was written.

The following diagram illustrates the primary Python functions required to establish a socket between two computers. Notice how the **`send()`** and **`recv()`** functions at the end are iterative. In this example, after a response is sent, the server waits until the client sends data again, establish a send and receive loop until either the client disconnects or the server rejects the connection.

![networking](../resources/python_sockets_diagram.png)			

So now let's take a look at how the code for these two computer systems could be written using Python's **`socket`** library.

```ipython3
import socket

PORT = 2020
HOST = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
	srv.bind((HOST, PORT))
	srv.listen()

	print("server listening on port", PORT)

	connection, address = srv.accept()

	with connection:
		print("client connected")
		
		while True:
			rec_msg = connection.recv(4096)
			
			print("echo", rec_msg)

			if not rec_msg:
				break
			connection.sendall(rec_msg)
			
		print("client disconnected")
```

In the code above, we start by importing the socket module to the program, and set a **`PORT`** and **`HOST`** variable that contain the IP address of the server and the desired port (port numbers are unrestricted, however, there are some common conventions for ports where you might find conflicts, so choose wisely).

Then, a **`with`** statement is used to instantiate a socket object and assign it to the variable **`srv`**. **`with`** will handle the responsibility of properly closing the socket and connection. The socket is first bound to the desired address and port, then set to listen for incoming socket connection requests. The code, as is, will block at this point until a it _hears_ a remote connection, at which point the socket will _accept_ the connection and store the socket connection and remote address in the variables **`connection`** and **`address`** respectively.

Now that a connection between a remote computer and server is established, the program can begin to exchange data. The server depicted by the code here is a lightweight _echo_ server whose only responsibility is to send the data it receives as a response. Because Python sockets use the same underlying tools for establishing network connections as other programming languages and networking tools, we can connect to this server in a number of different ways. If you are on Windows, you can download a program called "PUTTY" to connect to this server and send it messages. If you are on Linux or OSX, you should have a preinstalled tool called _ncat_ that will allow you to connect. In the following example, I use ncat to connect to the server and send a few messages.

![networking](../resources/ncat_echo_test.gif)			

Take a minute and try it for yourself. Grab [PUTTY](https://www.putty.org/) or fire up ncat, copy the server code sample into IDLE, and send some messages!

Oh, one more thing before we move on. In networking, there are some IP addresses that have special meaning. One of those address that will be relevant to you here is the _loopback_ address:

![networking](../resources/sockets_loopback.png)			

The loopback address, **`127.0.0.1`** is networking convention that allows a computer to connect to itself using its network connection. And just like domain names on the Internet, the 'name' **`localhost`** is an alphanumeric map to the loopback IP address. In the example above, I bind the Python server to the loopback address and connect to it using ncat. This provides a simple and straightforward way to test our socket programming without having to maintain code on two separate systems.

Okay, so we have seen how we can connect to the Python server with an existing client, now let's take a look at how we can write our own.

```ipython3
import socket


PORT = 2020
HOST = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	client.connect((HOST, PORT))

	print("client connected to {HOST} on {PORT}")

	while True:
		msg = input("Enter message to send: ")

		client.sendall(msg.encode('utf-8'))
		srv_msg = client.recv(4096)

		print("Response",srv_msg.decode('utf-8'))
```

So in the client example, just like the server code, we first instantiate a **`socket`** object and assign it to a variable, in this case we will use **`client`** for differentiation. However, rather than **`bind()`** and **`listen()`** on an address and port, we tell the socket to **`connect()`** to the location that we expect to be listening. Then we simply create a **`while`** loop to continuously collect user input, send it using the connected socket, and print the response from the server.

Go ahead, take a minute to copy the client code into a new instance of IDLE. You should be to run both the server and client at the same time. Just make sure that you start the server first so the client can connect.

One final concern that we have not discussed yet is the format in which we are sending and receiving data. You have probably noticed that prior to the client sending the user input string, it is encoded. The **`encode()`** function converts the its string object to bytes in the format that is passed as a parameter (utf-8) in our example. Likewise, the response from the server is decoded again before printing to the shell. This process can become quite burdensome when a program needs to send and receive larger, complex data sets. Fortunately, Python makes this process much easier for us by exposing some additional functions that abstract much of the work for us. Let's take a look at the revised code first:

```ipython3
import socket


PORT = 2020
HOST = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	client.connect((HOST, PORT))

	send = client.makefile('w')
	recv = client.makefile('r')

	print("client connected to {HOST} on {PORT}")

	while True:
		msg = input("Enter message to send: ")

		send.write(msg + '\r\n')
		send.flush()

		srv_msg = recv.readline()

		print("Response",srv_msg)
```

Here we make use of the **`socket`** module's **`makefile`** function to create a read and write convention that more closely resembles what we have learned from file operations. Makefile abstracts much of the work required to convert string-like data into bytes. Notice, we no longer have to conduct any encoding or decoding operations. Rather, we simply create readable (**`.makefile('r')`**) and writeable (**`.makefile('w')`**) _file objects_ on our connected socket. The only additional responsibility required here is to tell the remote connection when we have completed writing operations. Write operations will typically store data in a buffer prior to sending, often, buffered data will not be sent until the buffer is full. Therefore, it is always important to remember _flush_ the buffer when write operations have completed. The socket's **`.flush()`** function will conduct this operation for you.


(lectures:protocols)=
### Protocols

The protocols lecture makes use of three Python programs. While various parts of the programs are included in this section, you will want to download the actual files if you plan on running them yourself in IDLE.

<a href="../resources/symptom_monitoring.py">SMP Protocol</a>

<a href="../resources/symptom_monitoring_ui.py">SMP Client Program</a>

<a href="../resources/symptom_monitoring_server.py">SMP Server Program</a>

#### Videos

[Protocols Lecture](https://uci.yuja.com/V/Video?v=2102790&node=7910449&a=3002510&autoplay=1)

#### Notes

In assignment 2, you are provided with the **`Profile`** module for storing and loading user data. In this module, we make use of a particular format for storing information called [JSON](https://www.json.org/json-en.html), which wraps Profile object data in a style of notation using the rules and conventions set forth by the creators of the format. 

All the files that you find on your computer adhere to a similar process: a format is created that specifies how data should be stored and retrieved and programs that make use of the format adhere to the format conventions. A file's format is typically specified by it's extension, or suffix (_e.g._, .jpg, .doc, .py), providing the program that wants to use it with some clue as to how to interpret the file contents. A good example of this is an image editing program that can display different image formats.

Programs that talk to each other over networks follow a similar process. A format is agreed upon and the programs that want to talk to each other must follow this format to successfully communicate. In networking, this format is called a _protocol_. The Hypertext Transfer Protocol or HTTP, for example, is one way that servers and the clients that connect to them can communicate (if you are reading this web page right now, you have no doubt accessed it using HTTP).

So, now that we have established a preliminary understanding of what constitutes a protocol. Let's create one of our own. After all, there is really nothing special about a protocol, it's just a set of requests and responses agreed upon by two or more programs.

Let's start by building a protocol for UCI's Working Well Daily Symptom check tool. Now, I am not sure if you receive these emails as a student, but employees at UCI are required to answer these emails everyday. How might we go about converting this tool to a program?  And how might we extract some common language to be used by the program (_e.g._, create a protocol)?

![uciemail](../resources/symptomcheck_email.png)			

(watch the lecture for more detail about the wellness check email. <a href="../resources/smp.pdf">Download the full email</a>)

Well, we can start by asking a few high level questions: What information does the tool need to collect? What are the conditions that need to be handled? What actions must be taken in response to those conditions? Certainly, there are many different ways to answer these questions, so the path we take here is likely not the only direction we could go, but it should be sufficient to demonstrate the underlying concepts of networking protocols.

First, we need to know who is submitting a daily wellness check. Then, by reading through the email we can determine which conditions determine the next steps required by the user. Notice in the email how every question is constructed to respond to either a yes or no answer. We can use this boolean like response to construct the type of data we need for the protocol. Also notice how there are only two actions for each response: no further action is required, or continue to next question.

The following table lays out what we can expect from a typical client-server interaction using the protocol. We first assume the typical handshaking process that must occur when sockets are establishing a connection. The handshake process is then followed by the first requirement of the transaction: identification (or authentication) of the user. We then proceed to check off the various steps as laid out in the original email. Since we only need to give the server a yes or no answer, the structure for the protocol messages can be fairly simple. Here, we construct a command using the following schema:

```code
SMP_[TYPE] [VALUE]
```

The only command that we do not require a 1 or 0 value for is **`SMP_AUTH`** since we must pass some form of user identification to the server.

```code

| client          | server     |
|-----------------|------------|
| connect         |            |
|                 | accept     |
| SMP_AUTH userid |            |
|                 | WELCOME    |
| SMP_STATUS 0    |            |
|                 | COMPLETE   |
| SMP_STATUS 1    |            |
|                 | CONTINUE   |
| SMP_SYMPTOMS 0  |            |
|                 | COMPLETE   |
| SMP_SYMPTOMS 1  |            |
|                 | CONTINUE   |
| SMP_TESTED 0    |            |
|                 | CONTINUE   |
| SMP_PROXIMITY 0 |            |
|                 | COMPLETE   |
| disconnect      |            |
|                 | disconnect |


```

And that's our protocol. There are a few more conditions not listed in the previous table, such as when the **`SMP_TESTED`** or **`SMP_PROXIMITY`** commands are 1 on 0, that if we wanted to provide a formal protocol specification we would probably want to explain in greater detail.

You may be wondering why we even need a protocol for this program. Why not just collect the required data from the user and send it over to a server all at once? While that might work fine within the constraints of the UC system wellness checking needs, what if we needed to support other universities, organizations, and governments around the world? Perhaps it would be easier to give all of those outlets the ability to build their own platforms, rather than modify a single program to support all of them. By creating (and standardizing) a protocol, we don't have to depend on the capabilities of a single program from a single source. Rather, as long as a program adheres to the protocol, anyone can create their own custom interfaces, programs, and platforms.

Okay, so now that we have a protocol, let's take a look at how it is implemented in Python. I won't be putting the entire project into the notes here, but you can download the protocol file at the top of this section. We will be calling this protocol the Symptom Monitoring Protocol (SMP).

```{note}
Unlike previous snippets, those used in this lecture are not feature complete. They will not run on their own if you copy and paste from here. To run the programs and view all of the code, please download the files listed at the top of this section.
```

```ipython3
AUTH = "SMP_AUTH"
STATUS = "SMP_STATUS"
SYMPTOMS = "SMP_SYMPTOMS"
TESTED = "SMP_TESTED"
PROXIMITY = "SMP_PROXIMITY"

WELCOME = "WELCOME"
CONTINUE = "CONTINUE"
COMPLETE = "COMPLETE"
NOUSER = "NOUSER"
ERROR = "ERROR"
```
Here we specify some constant variables to hold the commands we created for the protocol. Constant variables will help us keep the string representations of the commands together and make updating the protocol commands a little easier if the need arises.

In the following section, we create a namedtuple object to hold the objects derived from the socket. A namedtuple is a convenient way to pass multiple objects without having to manage individual variables for each one. The protocol is first initialized by placing a call to the init method and passing it a socket that has been connected to the desired SMP supported endpoint (a client, or a server). 

```ipython3

SMPConnection = namedtuple('SMPConnection',['socket','send','recv'])

def init(sock:socket) -> SMPConnection:
    '''
    The init method should be called for every program that uses the SMP Protocol. The calling program should first establish a connection with a socket object, then pass that open socket to init. init will then create file objects to handle input and output.
    '''
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except:
        raise SMPProtocolError("Invalid socket connection")

    return SMPConnection(
        socket = sock,
        send = f_send,
        recv = f_recv
    )

def listen(smp_conn: SMPConnection) -> str:
    '''
    listen will block until a new message has been received
    '''
    return _read_command(smp_conn)


def authenticate(smp_conn: SMPConnection, userid: str) -> str:
    '''
    a helper method to authenticate a userid with a server
    '''
    cmd = '{} {}'.format(AUTH, userid)
    _write_command(smp_conn, cmd)
    result = _read_command(smp_conn)
    
    return result

def report(smp_conn: SMPConnection, report: str, status: str) -> str:
    '''
    report will send the command specified by the parameters and return a response to the command using the SMP Protocol.

    report: one of the SMP_X commands provided by the module
    status: either 0 or 1 to indicate the status of the command specified in the report parameter
    '''
    cmd = '{} {}'.format(report, status)
    _write_command(smp_conn, cmd)
    return _read_command(smp_conn)


def nouser(smp_conn: SMPConnection):
    '''
    a send only wrapper for the NOUSER command
    '''
    _write_command(smp_conn, NOUSER)

def _write_command(smp_conn: SMPConnection, cmd: str):
    '''
    performs the required steps to send a message, including appending a newline sequence and flushing the socket to ensure
    the message is sent immediately.
    '''
    try:
        smp_conn.send.write(cmd + '\r\n')
        smp_conn.send.flush()
    except:
        raise SMPProtocolError

def _read_command(smp_conn: SMPConnection) -> str:
    '''
    performs the required steps to receive a message. Trims the 
    newline sequence before returning
    '''
    cmd = smp_conn.recv.readline()[:-1]
    return cmd
```

This code contains just a few of the functions in the protocol, however, most of the remaining functions are similar to the ones represented here. In particular, the function **`nouser`** is one of several helper functions that send specific commands. Also notice how the write and read operations have been abstracted to their own function (**`_write_command`**, **`_read_command`**). By moving this required, but repetitive code to its own function, we can consolidate purely structural operations (_e.g._, appending or trimming socket messages) to a single location.

Okay, so that is the bulk of the SMP protocol module. Now let's take a look at how we might go about incorporating it into our programs. We will be building upon the code used in the Networks and Sockets lecture, so be sure to watch it before continuing.

```ipython3
print("Welcome to the UCI Working Well Daily Symptom Checker")
print()
print("To get started, enter your UCI provided email address")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
_smp_conn = smp.init(sock)

try:
  while True:
    userid = input()

    res = smp.authenticate(_smp_conn, userid)
    if res == smp.NOUSER:
        print('Unable to find user. Check your ID and try again.')
    else:
        break

  while True:
    if _report_status(_smp_conn) == smp.COMPLETE:
        print('Thank you. No further action is required.')
        break
    
    if _report_symptoms(_smp_conn) == smp.COMPLETE:
        print('Thank you. No further action is required.')
        break
    
    if _report_tested(_smp_conn) == smp.CONTINUE:
        if _report_proximity(_smp_conn) == smp.COMPLETE:
            print('Thank you. It is advised that you do not come to campus today.')
            break
        else:
            print('Thank you. No further action is required.')
            break
    else:
        print('Thank you. No further action is required.')
        break
except SMPProtocolError:
  print("An error occurred while attempting to communicate with the remote server.")    
else:
  # only disconnect if an SMPProtocolError did not occur
  smp.disconnect(_smp_conn)
finally:
  sock.close()

```

Just as with the client server we created, we start by connecting a socket to the desired host and port. Once we have a connected socket, we can use that socket to initialize the SMP protocol. Recall that upon initialization, the protocol module returns a namedtuple called **`SMPConnection`** that contains the socket, a writable file object, and a readable file object. Now that we have an SMPConnection, we can begin conducting operations using the protocol module. If we refer to the table from earlier, we know that the first thing we need to do is authenticate as a user. So the program first collects the required data from the user and then sends it to the remote endpoint for processing. An invalid id will cause the user to be prompted again, otherwise, the program will continue with the protocol.

For more detail on how the client program works, as well as a peak at the server program, please watch the lecture videos!


#### Notes
(quiz-results)=
## Quiz Results

[TO BE POSTED on 1/20/21]

