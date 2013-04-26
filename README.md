# Bayes Net Project
## Copyright (c) 2013, Avi Levy

# Source Files
* bayes.py *the main executable*
* net.py *bayes net class*
* event.py *represents the conditional probability table of an event*
* factor.py *represents a factor, for the elimination algorithm*
* output.py *handles all of the screen outputting*
* constants.py *project-wide constants and conventions*

# Platform
I developed this on Linux. Specifically: `Linux all-in 3.8.0-19-generic #29-Ubuntu SMP Wed Apr 17 18:16:28 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux`

# How to run
Ensure that Python installed. The code should run on either Python 2 or Python 3.
From the directory that the .py files are located, run: `$ ./bayes.py`
This will provide a usage method with more specific instructions.

# Documentation of Problems:
First of all, I want to point out that my output differs from the specification in one case. When you run the elimination algorithm and it encounters a factor involving N variables (N >= 3), I list out the 2^N entries in a different order than the official algorithm. I couldn't figure out what order was used by the official algorithm, otherwise I could have easily implemented the correct ordering. If you look in `output.py` (and also the constructor of the factor class in `factor.py`) I have actually meticulously ordered and sorted all variables when I knew which ordering to use. Anyway, I figured that this wasn't too big of a deal.
Another difference has to do with displaying floats, but this is outside of my control because Python and Java handle floats completely differently.

## Problems
I ran into a lot of subtle bugs while writing this, too many to mention here. The last bug I had was that I implemented the elimination algorithm differently than in the worked example. I still got the same answer, but it turned out that I was doing something inefficient. If a hidden variable was encountered, I would multiple ALL the factors before summing out, whereas the correct way is to only multiply the affected factors. After I made this change, all of my intermediate steps matched the specification correctly. Well, I also had to add a step where I filter out "empty" factors: these are factors that can still have a value, but no variables associated with them. After normalization, these factors don't affect anything so we can safely filter them out.
Once I was fully satisfied that my implementation was correct, I spent a lot of time rewriting my code to be more straightforward and easy to follow. In some places, I tried to write things in a "Pythonic" way so that the code was more or less self-documenting. However, in other places in the interest of consistency I used some advanced language features that make things tricky to follow. I tried to place adequate comments in these areas. For example, to make the file processing code shorter and self-contained, I ended up stringing together a bunch of lambda functions that each have a different purpose. In output.py, I tried to avoid listing out elements explicitly when I could use functional tools like map(), filter(), and sorted() instead.
A lot of my bugs ended up coming from dereferencing issues. For instance, one bug I had in the main loop of elimination came from how I initialized the filtered arrays depends and doesnt. I was trying to partition the list of factors into the lists depends and doesnt. But I initialized depends = doesnt = [], instead of the better way depends = [], doesnt = []. Basically in the former case, I ended up unifying the two variables, instead of initializing them to the same thing. By switching to the second case, I avoided this bug.
You can see other places in the code where issues like this were resolved. For example, in net.py the function enum() makes duplicates of its arguments before using them. Otherwise, I was repeatedly modifying the same arguments in the recursive function calls, which was messing things up.
By rewriting the code more effectively, I pushed myself to learn a lot more python than I previously knew. I hope you take a look at the code and try to figure out what was going on/why I was doing things a certain way, because I worked hard on it!
