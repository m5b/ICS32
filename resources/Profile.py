# Profile.py
#
# ICS 32 Fall 2020
# Assignment #2: Chatting with Friends
#
# v0.1.1
# Revisions:
#   v0.1.1 - added property assignment for dsuserver during deserialization
#
# You should review this code to identify what features you need to support
# in your program for assignment 2. I could tell you what they are, but
# it is critical to becoming a good programmer that you are able to identify 
# the capabilities of external modules on your own. However, I recognize that
# this might seem like a lot. So will leave you with one clue: there are five points
# of data supported by the two classes in this module that you will need to collect
# through your program user interface.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE, 
# though can you certainly feel free to take a look at it.
#
# NOTE: There may be bugs in this module! I have only conducted some light testing
# so far. If there are, I will revise the file and send an announcement.
import json, time, os
from pathlib import Path


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Post(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently supports two features: A timestamp property that is set upon instantiation and when the entry object is set, or updated, and an entry property that stores the post message.

    """
    def __init__(self, message = None):
        self.timestamp = time.time()
        self.__entry = message

        # We must subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self.__entry, timestamp=self.timestamp)
    
    def setpost(self, message):
        self.__entry = message
        dict.__setitem__(self, 'entry', message)
        self.timestamp = time.time()

    def getpost(self):
        return self.__entry

    """

    The property method is used to support get and set capability for the entry object.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.

    """ 
    entry = property(getpost, setpost)
    
    
class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You will need to use this class to manage the information provided by each new user created within your program for a2. Pay close attention to the properties and functions in this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the properties exposed by this class. A Profile class should ensure that a username and password are set, but contains no conventions to do so. You should make sure that your code checks that required properties are set.

    """

    def __init__(self, dsuserver, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        self.__posts = []         # OPTIONAL
    
    """

    add_post accepts a Post object as parameter and appends it to the posts list. Posts are stored in a list object in the order they are added. So if multiple Posts objects are created, but added to the Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property. So take caution as to how you implement your add_post code.

    """

    def add_post(self, post: Post) -> None:
        self.__posts.append(post)

    """

    del_post removes a Post at a given index and returns True if successful and False if an invalid index was supplied. 

    To determine which post to delete you must implement your own search operation on the posts returned from the get_posts function to find the correct index.

    """

    def del_post(self, index: int) -> bool:
        try:
            del self.__posts[index]
            return True
        except IndexError:
            return False
        
    """
    
    get_posts returns the list object containing all posts that have been added to the Profile object

    """
    def get_posts(self) -> list:
        return self.__posts

    """

    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_Profile__posts']:
                    post = Post(post_obj['entry'])
                    post.timestamp = post_obj['timestamp']
                    self.add_post(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()