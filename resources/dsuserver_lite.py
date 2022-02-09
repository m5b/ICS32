
import time
import socket, os, json, threading, uuid
from pathlib import Path

PORT = 3021
HOST = "127.0.0.1"

class User:
    username = ''
    password = ''
    token = ''

def join_response(req) -> str:
    """
    Parse join request, authenticate user, and store in database
    
    :param req: the request to be processed

    :returns: DS response message
    """
    token = ''
    message = ''
    
    # simulate the creation of an auth token
    token = str(uuid.uuid4())

    """
    uncomment one of the following to test the various messages returned on join requests
    """
    message = "Welcome to the ICS 32 Distributed Social!"
    # message = "Welcome back, " + req['join']['username']
    # return error_response("Invalid password or username already taken")
    # return error_response("Invalid join message. Missing parameters")

    msg = {"response": {"type": "ok", "message": message, "token":token}}
    return json.dumps(msg)

def post_response(req) -> str:
    """
    Parse post request and store post in database
    
    :param req: the request to be processed

    :returns: DS response message
    """
    
    """
    uncomment one of the following to test the various messages returned on join requests
    """
    msg = {"response": {"type": "ok", "message": "Post published to DS Server"}}
    # return error_response("Post rejected: invalid timestamp")
    # return error_response("Post rejected: invalid token")
    # return error_response("Invalid post message. Missing token parameter")

    return json.dumps(msg)

def bio_response(req) -> str:
    """
    Parse bio request and store bio in database
    
    :param req: the request to be processed

    :returns: DS response message
    """

    """
    uncomment one of the following to test the various messages returned on join requests
    """
    msg = {"response": {"type": "ok", "message": "Bio published to DS Server"}}
    # return error_response("Post rejected: invalid token")
    # return error_response("Invalid bio message. Missing parameters")
    
    return json.dumps(msg)

def error_response(err) -> str:
    """
    helper function to create DS protocol response message
    """
    msg = {"response": {"type": "error", "message": err}}
    return json.dumps(msg)

def process_request(json_clt: str) -> str:
    """
    Convert json message to python object and pass to appropriate message handler.

    :param json_clt: a json string received from a client

    :returns: stringified json response to be returned to the client
    """
    response = ''
    try:
        # Convert the json string to a python object
        req = json.loads(json_clt)
        if 'join' in req:
            response = join_response(req)
        elif 'post' in req:
            response = post_response(req)
        elif 'bio' in req:
            response = bio_response(req)
    except json.decoder.JSONDecodeError:
        response = error_response("Invalid DS Protocol format")
    except KeyError:
        response = error_response("Invalid or missing DS Protocol key")
    except Exception as ex:
        print(ex)
        #response = error_response("The following error occurred while processing your request: " + str(ex))
        response = error_response("An unknown error occurred while processing your request")
    return response

def handle_conn(accepted):
    '''
    Receive and process all messages send over connection.

    :param accepted: the active socket connection to client

    :returns: None
    '''
    connection,addr = accepted
    with connection:
        print("client connected")
        while True:
            rec_msg = connection.recv(4096)
            print("message received", rec_msg)
            if not rec_msg:
                break
            try:
                resp = process_request(rec_msg.decode('UTF-8'))
                print("request processed", resp)
                connection.sendall((resp + '\r\n').encode('UTF-8'))
                print("response sent, waiting...")
            except Exception as ex:
                print("exception processing message")
                print(ex)

        print("client disconnected")

def srv():
    '''
    Bind to localhost and default port and start threading model
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # if bind throws exception, wait 10 seconds and start over.        
        try:
            srv.bind(('', PORT))
        except:
            print("Error occurred while attempting to bind")
            time.sleep(10)
            srv()

        srv.listen()
        print("server listening on port", PORT)

        # start threading model. Each connection request will spawn a new thread in the handle_conn function.
        while True:
            threading.Thread(target=handle_conn, args=(srv.accept(),)).start()


srv()
