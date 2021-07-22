Week 5 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 5 Overview

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results5`

(lecture-materials)=
## Lecture Materials

### Notes on Completing Assignment 4

The following notes have been released to provide you with additional guidance on how to approach completing the TODO requirements for assignment 4. You should take a pass at the starter code on your own first. Try and complete each TODO on your own, but if you get stuck come here for further guidance. I strongly encourage you to follow this approach as you will receive much less guidance working with TKinter in ICS 33. It is in your best interest to think through the TODO's without help!

```{note}
The line number references here might be off by 1 or 2, but should still generally take you to the associated section of the starter code. Of course, as you edit the file, the line numbers will continue to fall out of sync, so you might find it useful to keep a reference copy of the original starter code.
```

#### TODO: Line 271
Let's start with the **`online_clicked`** callback. (all line numbers are from unmodified starter code file)

```python3
self.footer = Footer(self.root, save_callback=self.save_profile)
```

The goal here is to update the Footer initializer to support a callback for the online checkbox widget. The solution is to replicate the existing **`save_callback`** functionality:

1. Add a new parameter to Footer (...) after **`save_callback`**, using the same conventions as **`save_callback`**. Check line 119, see the statement **`save_callback=None`**? Add another parameter called **`online_callback`**.

2. Now we need to do something with that new parameter. So check line 122, see how the value of the **`save_callback`** parameter is assigned to a private attribute called **`self.savecallback`**? Replicate that for **`online_callback`**. Notice, we already have a method we can use called **`online_click`**. The only difference, however, is that the **`online_changed`** method in MainApp has a parameter: value:bool. So we also need to pass a parameter when we call the callback. Fortunately the parameter already exists for us and can be found in the initializer for footer.

3. Next, we need to add code to **`online_click`**, line 137. Remove the 'pass' keyword, and reproduce the code used in **`save_click`**, but change your attribute and method call to the new online parameter and attribute we created in step 1.

4. Return to line 271 (though, this line number has changed now that we have added code). Update the Footer(...) initializer by adding a new parameter. The parameter name should match the parameter name you added in step 2. The value for that parameter should match the name of the **`online_changed`** method in the Main class.

When done, run your program. When you click the checkbox, the footer status label should toggle between online and offline.

#### TODO: Line 237

```python3
def online_changed(self, value:bool):
```

If all went well in the last step, you are read to move on. I left the following code here on purpose so that you could verify that the callback you added worked:

```python3
if value == 1:
  self.footer.set_status("Online")
else:
  self.footer.set_status("Offline")
```
But really, it's not entirely necessary here. If you like it, leave it. If you don't, delete it. However, we already know the online status by looking at the checkmark in the checkbox.

So the goal here is to create a 'flag' that we can use later to check whether the user wants to submit a post to the server. So the first thing we need is a variable to server as that flag!

1. Go to the initializer for the MainApp class and add a new attribute, let's call it **`self._is_online`** and set it to a default value of False (since the widget also starts as unchecked). 

2. Return to online changed and add the attribute from step 1, so that the 'value' parameter sets the value of it.

3. Add a print(**`self._is_online`**) to the end of the method and run the program. You should see output on the shell that changes from true to false when the checkbox widget is checked and unchecked.

#### TODO: Line 43 - edit set_text_entry method

```python3
def set_text_entry(self, text:str):
```

For this task, we just need to add some cleanup code for the editor widget.
1. Start by removing the 'pass' keyword.
2. Next, we need to add two lines of code: one to delete the content of the editor and one to insert new content. To the docs!

https://tkdocs.com/tutorial/widgets.html#entry

3. Under the Entry Contents section on the linked page above, you will see an example of how to delete and insert. Using those examples as a reference, add a delete and insert operations to the method.
4. To test this functionality, let's temporarily add some sample code to your **`online_changed`** method:

```python3
self.body.set_text_entry("Hello World")
```

5. Run the program. When the checkbox widget is clicked the words "Hello World" should appear in your editor.

6. If you get an error of something like "bad text index", then change the first parameter in your delete and insert function calls from 0 to 0.0, it's a weird quirk of this widget (0, works in python < 3, 0.0 works in python > 3) 

#### TODO: Line ~197 - new profile!

```python3
def new_profile(self):
```

This really isn't that hard. It's mostly code you have already written. Let's take advantage of the **`Profile`** class attribute in MainApp for this task.

So when a NEW profile is created, we need to do three things:
1. Create a new profile.
3. Reset the UI.

We probably also want to keep track of the location of the file. So let's start by creating a class attribute to hold our file path and name in the initializer for the MainApp class:
```python3
self._profile_filename = None
```
There's some sample code in the new_profile method that demonstrates what we need to do, so let's update it to fit our new attribute:
```python3
self._profile_filename = filename.name
```
I just changed profile_filename to **`self._profile_filename`**

Now let's create a new **`Profile`** object:

```python3
self._current_profile = Profile()
```
And reset the UI, just in case a profile has already been loaded:

```python3
self.body.reset_ui()
```
And that's it! Not so bad, right?


#### TODO: Line ~ 212 - open profile!
```python3
def open_profile(self):
```

This task is nearly identical to the previous one, with two exceptions:
1. We need to load an existing profile. So rather than generating a new **`Profile`**, we will load: 

```python3
self._profile_filename = filename.name
self._current_profile = Profile()
self._current_profile.load_profile(self._profile_filename)
```

2. Next we need to add our profile data to the UI. So we reset the UI just as with the new_profile method, and then send all existing posts to the set_posts method:

```python3
self.body.set_posts(self._current_profile.get_posts())
```
I am not showing you ALL the code in these snippets, so remember to clear the UI!

#### TODO: Line ~52 - set_posts!

```python3
def set_posts(self, posts:list):
```

Fortunately for this task, we have almost all the code we need to make it happen already written. We need to do two things:
1. Populate the **`_posts`** attribute that has already been written for us with posts.
2. Add those posts to the **`treeview`** widget

For 1, well...this task should be well within your skill set by now. So I am going to leave it to you. It's one line of code that assigns the parameter to the class attribute. Read the TODO comments if you get stuck.

For 2, we need to iterate on our newly populated **`_posts`** class attribute. So a for a loop that iterates on **`self._posts`** and inserts each post to the **`treeview`** widget. How do we do that? Check out the **`_insert_post_tree`** method! It takes an id and a post as parameters. You have the post, so what about the id? It can be any value, but it needs to be unique. The best way to do this is to use the length of the **`_posts`** array as the id.

Okay, less guidance now, but you have written this type of code before...so I am sure you can get this one worked out.


#### TODO: line ~240 - edit the save_profile method.
```python3
def save_profile(self):
```

_Saving_ the best for last, pun intended. Let's do this in two parts Part 1 is offline only, Part 2 is online support.

##### PART 1:
1. A new post has been written and is ready to save. The first step is to create a new post object using the text that was written. Fortunately (yes I use that a lot), we have a method in our Body class to get the text for us!

```python3
post = Post(self.body.get_text_entry())
```

2.  Next, we need to update our GUI by adding the new post object. Are there any methods in the Body class that we can use? Take a look.

3. Next, we should also update our **`_current_profile`** object and save it. You know how to do this, you have been doing it since a2. (**`add_post, save_profile`**)

4. Finally, let's reset the text editor:
```python3
self.body.set_text_entry("")
```

Okay, we have enough code completed to run some tests:
1. Create a new file, write a post, and save it.
2. Close the program, restart it.
3. Open the file created in 1. You should see your post in the treeview.

##### PART 2:

Let's get this thing online.

So at this point, your program should be saving posts to whatever dsu file is loaded into the program when the user clicks the Save Post button. If not, STOP and go back through these posts until you get there.

The last thing we need to do for a4 is send our post to the DS server when the online checkbox widget is checked, or is true. So, let's write a conditional statement that evaluates the MainApp class attribute that we added earlier:

```python3
if self._is_online is True:
    #call your server connect code.
```

Remember, we are still in the **`save_profile`** method, we are just adding new lines after the code we wrote in PART 1.

To complete this task, at a bare minimum we need to call the server communication code we wrote in a2. 

Finally, we need to call this **`send`** function or whatever process you created in **`ds_client`** to send messages to the server from the GUI. To keep our event handling code clean, let's create a new method called 'publish'. In that method we will make the call to 'send':

```python3
def publish(self, post:Post):
    ds_client.send(...)
```
It might be nice to add some GUI updates for usability in the **`self._is_online`** conditional. Perhaps, updating the footer label using the set_status method of the Footer class? And perhaps calling update() function to make sure all widgets refresh before the potentially long call to the server.

And that's it. Most of what I have shared here is code you have already written. I am just providing you with a quick overview of one of many ways to go about implementing it. If you can think of a better way, go for it!

(quiz-results5)=
## Live Class Recordings

<a href="../resources/Graphical User Interfaces Live Lecture.pdf">Lecture Slides</a>

[Monday Live Class Recording](https://uci.yuja.com/V/Video?v=3358301&node=11216998&a=1007171856&autoplay=1)

[Wednesday Live Class Recording](https://uci.yuja.com/V/Video?v=3364814&node=11237139&a=1867777338&autoplay=1)
