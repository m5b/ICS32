Week 3 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Week 3 Overview

For week 3, you have finally turned in your first program for ICS 32. Congrats! Now it's time to start building that first program into a real application. Be sure to read the overview for [Assignment 2](../assignments/a1.html) before you dive into the lecture materials.

Quick Links:
: {ref}`lecture-materials`
: {ref}`quiz-results`

(lecture-materials)=
## Lecture Materials

Lectures for Week 3
: {ref}`lectures:testing`
: {ref}`lectures:modules`
: {ref}`lectures:protocols`
: {ref}`lectures:networks`

(lectures:testing)=
### Testing Lecture

#### Videos

I have decided not to record a video for this lecture. We will be diving into testing more formally after the mid-point of the quarter, but I wanted to give you some notes on how to go about thinking about tests. We can discuss the topics here in a bit more detail after quiz in our next class.

#### Notes

Now that you have assignment 1 wrapped up, let's take a minute to reflect on the experience. 

Looking at the questions and conversations many of you have had over the past two weeks, my guess is that you now have a better understanding of the complexity that goes into writing even a small program.

Interpreting and implementing program requirements is an essential part of the programming process that will become more familiar to you as you work through this course and many others. However, even with practice, you will find that it is important to develop strategies to reduce the uncertainty that accompanies the application of requirements. 

In a way, the validity checker for assignment 1 tested your program for you. It offered some sense of confidence that your program was functioning according to the assignment requirements. For the remaining assignments in this class, you will be responsible for checking the validity of your programs. So in this lecture, I want to talk about one of the ways that programmers go about accomplishing this goal.

In large programming projects where teams of programmers work together to write software, the practice of writing tests is quite common. In fact, there are programming paradigms such as Agile, Cleanroom, Spiral, and Waterfall that have integrated testing directly into their methodologies. We won't learning about paradigms and models in this class, but it's important to recognize how pervasive testing is throughout the software development industry. As you might imagine, this pervasiveness exists because the process of writing tests against your code, works. Tests can significantly reduce the development time, code complexity, and bug tracking.

##### So how do we start?

Well, the first thing we do is create a hypothesis about how our program and the functions within it, are expected to behave. For example, one test might be to input a value and observe the output. Does the output align with the expectations set in the program requirements? If so, then the test can be said to 'pass.' If it doesn't, then obviously the test fails, but how do we determine why? This was a source of confusion for many of you while using the assignment 1 validity checker as the validity checker could only report a failure when the program did not return an expected output. A better test might have examined the input and output at the level of functions rather than the program.

Testing individual functions, however, does require some planning. If the functions in your program perform many operations, it can be difficult to configure a test that can be relied upon. So one of the benefits of thinking about tests before or in tandem with your program design is that the responsibilities of your functions will inevitably be scoped to a manageable size.

##### So how do we test at the level of functions?

Let's take, for example, a program that manages an email list. We'll assume that one of the requirements for this program is to support removing certain email addresses from the mail list.

We'll start by adapting this small function written by Alex Thornton for ICS 32. The **'remove_from'** function accepts two parameters: a list and a value. It returns the same list, except without the passed value, if it exists.

```ipython3
def remove_from(the_list: list, value) -> list:
	new_list = []

	for element in the_list:
		if element != value:
			new_list.append(element)
		
	return new_list
```

At least, that's what we hope it does. Rather than assume it does and continue to build our email list management program, we should test it first:

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user2@example.com")
["user1@example.com", "user3@example.com", "user4@example.com"]
>>> emails
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user4@example.com")
["user1@example.com", "user2@example.com", "user3@example.com"]
>>> emails
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]

```

So far so good. We start with a test list, then pass some test conditions to the function to see if it returns the results we expect. Here, after each call to **`remove_from`** we receive a new list with the value we passed to it missing. But have we tested every possible condition? What happens if a passed value does not exist?

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user5@example.com")
["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]

```

Is that what we want to happen? What if our program needs to confirm that a removal actually occurred? Well, we could compare **`emails`** to the results, or we could give that responsibility to the **`remove_from`** function:


```ipython3
def remove_from(the_list: list, value) -> list:
	new_list = []

	for element in the_list:
		if element != value:
			new_list.append(element)
		else:
			raise ValueError('value not found in list')
		
	return new_list
```

So now we have a function that will raise an exception if the passed value does not exist, providing us with a convention (exceptions) that we can use to handle this new condition. 

```code

>>> emails = ["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"]
>>> remove_from(emails, "user5@example.com")
Traceback (most recent call last):
  File "maillist.py", line 39, in <module> 
		remove_from(emails, "user5@example.com")
	File "maillist.py", line 33, in remove_from
		raise ValueError('value not found in list')
ValueError: value not found in list

```
Can you think of any others? What happens if the email list has multiple emails with the same address? Currently, all instances of value will be removed from the new list, but what if we only wanted to remove duplicates? By writing tests against our functions, we expose conditions that we might not otherwise think to consider.

Now, having to write create these tests cases each time we want to test a program can quickly become unwieldy. Fortunately, Python gives us a way to automate much of the work!

The **`assert`** statement are a convenient shortcut for inserting debugging tests into your program. Here we test a normal case, or case that represents typical behavior for the remove_from function:

```ipython3
assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]

```

And here we test an error case, or case that generates a result we don't expect:

```ipython3
try:
	remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user5@example.com")
	assert False, "ValueError should have been thrown"
except ValueError:
	pass
```

If both assertions pass, then we should not expect to see anything from the shell when running the program. However, if an assertion fails, the debugger will notify you of the failure:

```ipython3
>>> assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user3@example.com"]

Traceback (most recent call last):
  File "maillist.py", line 38, in <module>
	    assert remove_from(["user1@example.com", "user2@example.com", "user3@example.com", "user4@example.com"], "user4@example.com") == ["user1@example.com", "user2@example.com", "user2@example.com"]
AssertionError
```

We will get into the more formal test driven approach to software development in a few more weeks, once you have had a chance to experience working with larger, more complex programs. But for now, focus on thinking about the how the code you write should behave, and then write some assertion statements to confirm that it behaves as you expected. I think you will find that new edge conditions will arise that you might not have otherwise considered. And remember, testing is not about quantity! A program with 100 tests is not necessarily better than one with 10. Your goal should be to identify _different_ conditions worth testing, not _variations_ on the same test.

(lectures:modules)=
### Modules

Material Coming Soon.

#### Videos

#### Notes

(lectures:protocols)=
### Protocols

Material Coming Soon.

#### Videos

#### Notes

(lectures:networks)=
### Networks and Sockets

Material Coming Soon.

#### Videos

#### Notes

(quiz-results)=
## Quiz Results

<a href="../resources/QZ_Week_3_Quiz_Results.pdf">Quiz Results PDF</a>

### Some Thoughts

Some pretty straightforward questions this week. The majority of you answered correctly on the three multiple choice questions. Questions 6 & 7 were primarily used as a metric for gauging your experience with debugging, but still worth checking out if you missed the class.

