#!/usr/bin/env python

#
# ICS 32 Fall 2020
# WS DS Server client example
#

import asyncio, time
import websockets

"""
joinmsg,biomsg,postmsg, take user values and generate the JSON
string format required by the DSU server.

"""
def joinmsg(username, pwd):
    msg = '{"join": {"username":"'+username+'", "password":"'+pwd+'"}}'
    return msg 

def biomsg(msg):
    msg = '{"bio": {"entry":"'+msg+'", "timestamp":"'+str(time.time())+'"}}'
    return msg 

def postmsg(msg):
    msg = '{"post": {"entry":"'+msg+'", "timestamp":"'+str(time.time())+'"}}'
    return msg 

"""
Don't worry too much about the keyword 'async' right now. We will rely on the 
asyncio module more in future assignments to ensure that our programs don't 
block when waiting for a server response. For now, we just want to get familiar
with the concept.
"""
async def init():
    # This is my personal server, so please keep this URI private!
    uri = "ASK ON SLACK FOR THE ADDRESS!"

    print("Welcome to ICS32 Social!\n\n") 

    """
    As with the sockets lecture, we can use websockets to connect to a remote
    server, and send and recv messages!
    """
    async with websockets.connect(uri) as websocket:
        while True:
            action = input(
                "Press 'N' to connect, 'B' to send your bio, and 'P' to post a message.\n")

            message = ''


            if action == 'N':
                message = joinmsg(
                    input("What is your username? "), 
                    input("What is your password? "))
            elif action == 'B':
                message = biomsg(input("What is your bio? "))
            elif action == 'P':
                message = postmsg(input("What is your message? "))
            else:
                message = '' #If no message is entered, the DSU server will return an error message, try it!
            
            await websocket.send(message)
            print(f"> {message}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(init())