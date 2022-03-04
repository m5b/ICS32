Week 9 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 9 Overview

The lectures for this week will get you ready for assignment 5. This week, we will use our in class time for slightly more formal lectures rather than QA. So you will not have to watch an pre-recorded lectures this week. 

However, I have included some notes that will prepare you for one of the quirks of moving your journaling program from the command line to the GUI:

{ref}`lectures:objectcopy`

## Lecture Materials

### Live Class

#### Tuesday

[Class Recording](https://uci.zoom.us/rec/share/YT7NrkpKX5zyx7IYIV-jkqLJSRIWNJRSMBE5Ge9PD10pjMcDVoKhvzvMOjMzwQ-H.LuimYbQ29bkbZczV)


#### Thursday

[Class Recording](https://uci.zoom.us/rec/share/Cwg3bjvV-BmHrbzHHbdTge0pj3AOhDCTnOgd0-d2_aidUthfQte67LTr6qj_yQ65.2f0EJJW48_4_JRVI?startTime=1646339613000)

<a href="../resources/gui_lecture.pdf">Slides</a>

<a href="../resources/a5-lecture-solution-eventloop.py">Event Loop Demo</a>

<a href="../resources/tkinter_geometry.py">Tkinter Geometry Demo</a>


### Recorded Lectures

(lectures:objectcopy)=
### Object Copy

##### Lecture Recording


##### Lecture Notes

Let's talk about assignment statements in Python.

At this point in the course, you likely have not had to think about how Python manages variable assignments. For the most part, save for any advanced functionality you might have implemented in one of the course assignments, you declare a variable, assign it a value, and continue writing your code. Perhaps you assigned one object to a new object, but you most likely have not encountered Python's default pass-by-reference assignment structure.

When a collection in Python is assigned to a new object, a _reference_ to its value is passed to the new object. Let's take a look at what that means with some code:

```python3
a1 = ["Hello","World"]
a2 = a1
a3 = a2

print (a3)

a1[1] = "Hello"

print (a3)
```

At a glance you might expect the second print statement to be the same as the first. But when we run the code:

```python3
>>> ['Hello', 'World']
>>> ['Hello', 'Hello']
```

The list assigned to a1, is referenced by both a2 and a3 variables. As a reference, when the source changes, so will all objects that it has been assigned to. Because it is a reference, changes to the assigned object will change the source as well:

```python3
a3[0] = "Goodbye"

print (a1)

>>> ['Goodbye', 'Hello']
```

Generally, pass-by-reference is the preferred way to manage data in a program. A reference ensures that there will only be one instance of object data in your program. This means that your programs will be faster, lighter, and your data easier to track. However, there are instances where you might need to make changes to one copy while leaving the original intact. We could approach this problem procedurally with the following code:

```python3

a1 = ["Hello","World"]
a2 = a1
a3 = [a2[0], a2[1]]

print (a3)

a1[1] = "Hello"

print (a3)

>>> ['Hello', 'World']
>>> ['Hello', 'World']

```

Notice how now, the change to index 1 in the object a1, does not affect the data stored in a3. That's because we have effectively made a copy of the original collection. A slightly more efficient (and expandable) approach would involve using a loop to copy each item in the collection, but this approach only gets us so far. As objects become increasingly complex, working out the logic to make a complete copy can quickly turn into painstakingly error prone work. Fortunately, Python has taken care of this for us! Let's return to our code snippet one more time:

```python3
import copy

a1 = ["Hello","World"]
a2 = a1
a3 = a2
a3 = copy.copy(a2)

print (a3)

a1[1] = "Hello"

print (a3)

>>> ['Hello', 'World']
>>> ['Hello', 'World']
```

The results are the same, but now we have moved the responsibility of making a copy from our own code to a well-tested module that is part of the Python standard library!

##### Shallow vs. Deep Copy

The copy library provides two types of object copy mechanisms, _shallow_ and _deep_. To understand the difference, let's draw from the [Python documents](https://docs.python.org/3/library/copy.html):

> A shallow copy constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original.
		
> A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.

In the code sample above we used a shallow copy when calling the **`copy()`** function. A deep copy would like:

```python3
a3 = copy.deepcopy(a2)
```

If your goal is to make a copy of a collection, then using a shallow copy should be sufficient. However, if you have a compound object, one that consists of classes _and_ collections (e.g., **`Profile`** or **`NaClProfile`**), you may need to make a deep copy to ensure that all attributes, and data collections are copied. Just be aware, when you make a deep copy of an object _everything_ is copied! So if in an object instantiated from a large nested inheritance hierarchy, you may want to consider other options.

To wrap up, it's worth mentioning that the reason we are discussing object copy is that you may encounter a situation in which you find pass-by-reference problematic while connecting your earlier work to the Tkinter GUI for [a5](../assignments/a5.md). So be aware, if you notice an issue with value references in your program, you might need to make a copy!


