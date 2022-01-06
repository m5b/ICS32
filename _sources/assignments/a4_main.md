Assignment 4: Extending the Platform
============================

## Introduction
In assignment 3, you learned how to write a program that connects to and shares information with a program running on another computer. The systems we write programs for today are almost always connected to other computers in some capacity. Whether it is your computer operating system sending data back to its creator, your web browser automatically downloading updates, or you reaching out to friends and family for a video chat, nearly all the programs we use today rely on networked communication to extend their capabilities.

While your Distributed Social (DS) program has the ability to accept, store, and distribute information written by your users, it doesn't yet take advantage of the vast wealth of information available to networked programs today. So for this assignment we are going to be extending the DS platform by adding some new features for the users of your program.

You have probably noticed how in programs like Slack, Discord, and Facebook Messenger, keywords can be entered into chat conversations that trigger some sort of automatic inclusion or formatting. In computer science, this process is called __transclusion__, which basically refers to the process of using a linking syntax to connect or include content from one source into the content of another. For this assignment, you will be enhancing the post writing feature you created in assignment 3 by adding support for keyword transclusion. 

By now, you should have had a chance to digest some of the core principles of networked communication. You have learned about protocols, sockets, and request/response communication with a server. Your work for assignment 4 will focus on locking in these concepts as well as exploring some new ones. 

### Summary of Program Requirements 
* Connect to and retrieve data from at least 2 web API's using Python's **`urllib`** module.
* Use transclusion to parse and replace keywords in a journal entry with content from web API's.
* Write classes to manage your APIs.

### Learning Goals
* How to work with public API's
* Know when and how to write a class
* Understand and handle failures when communicating over HTTP
* Use inheritance to extend class functionality

## Program Requirements

Your main entry point to your program will be from a module called **`a4.py`**. As with a3, you will not have a validity checker to use for testing and you will be largely responsible for program input and output. You are encouraged to continue to bring the user interface and other functions you created in your **`a1.py`** through **`a3.py`** modules, but you will not be re-graded on the features you implemented for those assignments.

Your final program should contain the following new modules:

1. **`OpenWeather.py`**: A module for interacting with the OpenWeather API. See {ref}`section:part1`
2. **`LastFM.py`**: A module for interacting with the Last.FM API. See {ref}`section:part2`
3. **`ExtraCreditAPI.py`**: A module for interacting with an API of your choice, should you choose to earn extra credit. See {ref}`section:extracredit`
3. **`WebAPI.py`**: A base class module that provides access to common features for your API modules. See {ref}`section:part3`

Since the code you write for this assignment will still be dependent on communication with the server, you should also include all modules you created or used for assignment 3.

```{note}
If you were unable to complete the **`send`** function requirement in a3, let us know. We will walk you through the steps required to send and receive messages with the DS server.
```

(section:part1)=
### Part 1

When introducing new features to a program or learning a new tool that is unfamiliar, a good place to start is with a test program. So for Part 1, you will temporarily set aside your DS program and focus on building a small test program that can successfully connect to and retrieve data from a public API. You are welcome to use the sample code below to get started.

```ipython3
import urllib, json
from urllib import request,error

def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))

    finally:
        if response != None:
            response.close()
    
    return r_obj

def main() -> None:
    zip = "92697"
    ccode = "US"
    apikey = "YOUR API KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"

    weather_obj = _download_url(url)
    if weather_obj is not None:
        print(weather_obj['weather'][0]['description'])


if __name__ == '__main__':
    main()
```

#### Connecting to the OpenWeather API

To use the sample code, you must first create an account and generate an API key at [OpenWeather](https://openweathermap.org/): 

* Create an account at: [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up). If you are prompted to input a reason, just enter UCI and Education/Science.
* Once registered, find your API by clicking the "API Keys" link on your account page. Copy your API key and store it somewhere (as a comment in your code, for example).
* Next visit the [current weather page](https://openweathermap.org/current). Read through the instructions and build your API call. A basic call should look like this:
```ipython3
api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}
```
* You will likely want to customize this based on your personal preferences, so read through the documentation thoroughly to understand the various options for weather data available through the API.

Once you have your own API key, copy it into the **`apikey`** variable in the sample code above and run the program to see the result. Notice that the data response from the API is in JSON format. Most web API's use the JSON format for storing and sending data and since we are already familiar with JSON from a3, we will continue using it here (though it's worth noting that the OpenWeather API does support HTML and XML formats too). The **`loads`** function in Python's json module should be all you need to use for converting the JSON responses you received into a Python object (you are free to adapt the **` extract_json`** helper code example provided in a3). Also notice, that in the sample code, the print out only contains the **`description`** attribute for the weather. A more complete output might contain detailed information like temperature, barometric pressure, and humidity. To see all the data available from the API response, you can update the sample code to simply print the **`weather_obj`** variable.

Now that you have a functioning API call in place, you should start thinking about how to make this information more accessible for your DS program. A good way to go about doing this is to create a class that abstracts away the processing logic you need to write to gain access to weather data. So for the remainder of this part of the assignment, you will write a weather class called **`OpenWeather`** that accepts location information and an API key to store weather information in data attributes.

Your class must include and implement the following two methods:

```ipython3

def set_apikey(self, apikey:str) -> None:
  '''
  Sets the apikey required to make requests to a web API.
  :param apikey: The apikey supplied by the API service
	
  '''
  #TODO: assign apikey value to a class data attribute that can be accessed by class members
  pass

def load_data(self) -> None:
  '''
  Calls the web api using the required values and stores the response in class data attributes.
	
  '''
  #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
  #TODO: assign the necessary response data to the required class data attributes
  pass
```

Your class should be written such that the following validity code runs without error:

```ipython3

from OpenWeather import OpenWeather

zipcode = "92697"
ccode = "US"
apikey = "YOUR API KEY"

open_weather = OpenWeather(zipcode, ccode)
open_weather.set_apikey(apikey)
open_weather.load_data()

print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
print(f"The current weather for {zipcode} is {open_weather.description}")
print(f"The current humidity for {zipcode} is {open_weather.humidity}")
print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")

```

Although the sample code included in this assignment does have some error handling, you will likely want to attend to the various errors that can arise when connecting to remote API's more gracefully than what is provided. You will need to understand the different types of errors that occur when communicating over HTTP. Many different conditions can arise that your program may or may not need to communicate to your end user. For example, an invalid API key requires a different set of actions to resolve compared to the API service going down. Therefore, your OpenWeather class should be able to cleanly handle and inform a user about the following conditions:

* Loss of local connection to the Internet
* 404 or 503 HTTP response codes (indicating that the remote API is unavailable)
* Invalid data formatting from the remote API

There are many ways to approach handling these types of errors. If you consider that the bulk of the work occurs in the **`load_data`** method, one good strategy might be to throw an exception when an error occurs when this method is called. However, your exception handling MUST explicitly handle each of the conditions listed by providing a custom message. For example, if your code catches an HTTP exception, it should raise a new exception with a custom message related to the operation that is being performed.

We will run code that creates these error conditions to evaluate your OpenWeather class as well as your second API (see next section).

#### Connect to the Last.FM API 

Once you have finished creating your OpenWeather class, you will repeat the process with a new API from [Last.FM](https://www.last.fm/api#getting-started). The Last.FM API is large and full of interesting bits of data about music that you can pull into your DS Program. The main consideration here is to think about how you will present your API data in a DS journal post. The current limitations of the DS server and journaling platform, for example, would prevent you from using the search feature of the API. Take a few minutes to look through the documentation and decide on what type of information you want to support with your keyword.

Once you settle on at least one API method from the [Last.FM website](https://www.last.fm/api#getting-started), you will repeat the steps used in the previous section. Read through the API documentation, register to get an API key, and build a supporting class called **`LastFM`** to abstract the underlying API complexities from your program (and don't forget the error handling!).

You are free to include as many methods from the Last.FM API as you like, each assigned to their own keyword. However, you must connect one method to the predefined keyword listed in Part 2 so that our automated tests can verify that you successfully connected to the API.

Finally, since we are not specifying how to write the class for your custom API, you will need to ensure that your class is documented sufficiently enough for us to understand how it works.

(section:part2)=
### Part 2

Alright, at this point you should have two classes that retrieve data from web API's. For the second part of the assignment you will incorporate these classes into the current version of your DS program (where you left off after a3).

You goal for part 2 should be to allow your user to write journal posts with optional keywords that are transcluded into data from your API classes. You must create at least two keywords, one for each API, using the keywords listed below:

```ipython3

@weather
@lastfm

```
You may discover that once you have one keyword connected to an API method that adding more is pretty easy. So, if you choose, you may create your own keywords for any additional API methods that you want to support as long as they adhere to the following format:

```ipython3

@[KEYWORD]

```
So for example, the following journal post:

> Hello World! Today is the first day of the rest of my life. It is @weather outside and I am thrilled!

Should transclude to:

> Hello World! Today is the first day of the rest of my life. It is sunny outside and I am thrilled!

Okay, that's a pretty bad example, but you get the idea:) Here, the OpenWeather API feature 'description' was assigned to the @weather keyword so that when the message was transcluded the keyword was replaced with the description 'sunny.' You ARE NOT REQUIRED to bind 'description' to the @weather keyword, but you are required to bind some data from the OpenWeather API to the **`@weather`** keyword.

When your user writes a post, you will also want to inform them about the keywords your program makes available. There are a number of ways to go about accomplishing this task, the most straightforward being a print out of the keywords. However, you might also consider making keyword selection a little more interactive. Either way, you will not be graded on how you inform your user about keyword options, only that you have added this feature.

Finally, so that we may accurately test your program, all of your API classes (**`OpenWeather`**, **`LastFM`**, and **`ExtraCreditAPI`**) must also implement the following function:

```ipython3

def transclude(self, message:str) -> str:
  '''
  Replaces keywords in a message with associated API data.
  :param message: The message to transclude
	
  :returns: The transcluded message
  '''
  #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
  pass

```

```{admonition} Attention
:class: warning
The grading tool will import and call the required functions automatically using its own API keys. You must take care to not change the file name or the function parameters (though you can safely add parameters as long as they are given default values). If you do make changes, it is likely that your code will not pass the grading tool.

```

(section:part3)=
### Part 3: The Refactor!

At this point you should have two classes that look similar to the following psuedocode:

```python3

class MyAPI:
  def __init__(...):
    # creates required class attribute apikey
    # creates API specific class attributes like zip, ccode
    pass

  def _download_url (...):
    pass

  def set_apikey(...):
    pass

  def load_data(...):
    pass

  def transclude(...):
    pass

```

If you compare both classes you will likely find that both contain some redundant code. It is likely that the **`set_apikey`** and **`_download_url`** (or whatever you call the function that handles api requests) methods perform very similar operations. If so, you have a good indication that it might be time to refactor! 

```{tip}
Often times when we write programs it is difficult to foresee all the features and code we will require to make our program function the way we want. But as the program and our understanding of the code we have written evolves, we gradually begin to find points of redundancy. The more redundant code that we put into our program, the greater the likelihood we face undesirable conditions such as poor performance, bugs, and confusing logic.

As programmers, it is our job to ensure that our code is performant as possible, given our knowledge and abilities. One way that we accomplish this is by **refactoring** our code: reworking the code that we have written to reduce unneccessary logic, repetition, and errors.
```

For this final part of the assignment, you will refactor your code to reduce redundancy. You will do this by creating a base class that all of your api classes inherit, so if you have not watched the lecture on inheritance yet, now is a good time to do it!

Your base class will start with the following template:

```python3
from abc import ABC, abstractmethod

class WebAPI(ABC):

  def _download_url(self, url: str) -> dict:
    #TODO: Implement web api request code in a way that supports ALL types of web APIs
    pass
	
  def set_apikey(self, apikey:str) -> None:
    pass
	
  @abstractmethod
  def load_data(self):
    pass
	
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass

```

You will be required to add the necessary code to each of methods in the **`WebAPI`** class. Notice that the **`load_data`** and **`transclude`** methods have been assigned the **`@abstractmethod`** decorator. If you inherit this class and do not implement either of the abstract methods, you will receive an error from the python interpreter. Therefore, all code that is unique to the API used in the child class (or class that inherits from the base class) should be contained within the these methods.

When complete, the following code should be able to run using any of your API modules:

```python3

def test_api(message:str, apikey:str, webapi:WebAPI):
  webapi.set_apikey(apikey)
  webapi.load_data()
  result = webapi.transclude(message)
	print(result)


open_weather = OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
lastfm = LastFM()

test_api("Testing the weather: @weather", MY_APIKEY, open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm, MY_APIKEY, lastfm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword
```

(section:extracredit)=
### Extra Credit

We will be awarding 5 extra credit points for the successful inclusion of a third API from a source that has not been used for this class. If you choose to add a third API, you must explicitly define how to use it in your program and let us know via submission page comment that you would like to us to review your third API for extra credit. Your API should be built in a module named **`ExtraCreditAPI.py`** and make use of at least one keyword named:

```ipython3

@extracredit

```

Since it will be near impossible for us to create a unique key for every extra credit API, you MUST hard code your key into your **`ExtraCreditAPI`** class. To ensure consistency across all submissions, your extra credit API must include the following global variable:

```ipython3

EXTRACREDITAPIKEY = "YOUR API KEY" # replace with the key required for your custom api.

```

The grading tool will import your **`ExtraCreditAPI.py`** module and call the **`set_apikey`** function using the **`EXTRACREDITAPIKEY`** global variable as the value for the **`apikey`** parameter. So make sure your module supports this behavior!

### Submitting
Upload all of your program files in a single .zip file to Canvas by the due date. NAME YOUR MAIN FILE **`a4.py`**. If you complete the extra credit, be sure to add a comment on your submission page that notifies us. Failure to leave a comment means that we may not notice the extra credit feature when grading.

Additionally, all modules that you create or edit must include the following comment on the first three lines:

```python3

# NAME
# EMAIL
# STUDENT ID

```

### Starter Project

<a href="https://classroom.github.com/a/DJg05tcx">Assignment 4 Starter Repository</a>

### How we will grade your submission
																		
This assignment will be graded on a 150 point scale, with the 150 points being allocated completely to whether or not you submitted something that meets all of the above requirements. The following rubric will be used:

Requirements and Function | 120 pts
: Does the program do what it is supposed to do?
: Does the program make use of required APIs?
: Does the program adhere to the principles of inheritance?
: Are there any bugs or errors?

Quality and Design        | 30 pts 
: Is the code well designed?
: Is the code clearly documented?

Extra Credit							| 5 pts
: Does the program makes use of a third API?
: Does the API work?

By now you should be clearly documenting your code and expending effort to ensure that your code design follows the conventions we have been discussing throughout the class. Therefore, we will continue increasing the strictness of our stance on quality and design than we have in previous assignments.
