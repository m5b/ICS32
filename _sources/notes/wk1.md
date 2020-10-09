Week 1 Notes
============================

```{note}
Keep an eye weekly pages as they might be updated throughout the week.
```

## Lecture Materials

Here are the slides for the week 0 introduction lecture:

<a href="../resources/Introduction-to-ICS32.pdf" >Introduction and History Slides</a>

<a href="https://uci.yuja.com/V/Video?v=1975716&node=7594516&a=891585813&autoplay=1" >Exceptions and Files Lecture Part 1</a>

<a href="https://uci.yuja.com/V/Video?v=1975640&node=7594284&a=1632415151&autoplay=1" >Exceptions and Files Lecture Part 2</a>

## Quiz Results

<a href="../resources/QZ_Week_1_Quiz_Results.pdf">Quiz Results</a>

### Some Thoughts

Overall, this weeks quiz was a good start! I was excited to see so many of you show up on Zoom and in Socrative. Although generally everyone performed well on the quiz, there were three questions that I think require some additional explanation. 

**Question 4**

Input arguments are string types by default. So rather than perform a mathematical operation, when the python interpreter detects a string the + operator concatenates two arguments. So for inputs 2 & 5:

```ipython3
def add(a,b):
    return a + b
		
print (add(input(),input()))
```
															
```ipython3
2
5
>>> 25
```
															
How would you go about changing the code to get the answer 7?

Take a minute to think about it, then click the button on the right to reveal one answer.

```{toggle}
Now here I have wrapped the two input functions with int() to cast them to integer type. It will work for our scenario here, but what happens when a non-integer type is entered? Yep, the program will crash, but more on that soon!

```ipython3
  def add(a,b):
      return a + b
		
  print (add(int(input()),int(input())))
	
  2
  5
  >>> 7
```

															


**Question 5**

A tuple is recognizable by it's structure and use of parentheses to enclose values. If you weren't sure about this one, take a look here: 


<a href="https://www.learnbyexample.org/python-tuple/">More on Tuples</a>

**Question 6**

In python, data structures are zero-based, meaning the indexer starts at 0.  So, referencing the tuple with at position 1 will return the second value in the structure.


In future quizzes, I will use the live time to provide these types of explanations in during the quiz.
