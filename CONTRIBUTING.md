# Contributing

### Guidelines

Here's how to make it most likely that your pull request is accepted:

- Follow the **Puppy** [philosophy](README.md#philosophy)
- Emulate current code style
- Write tests. **Puppy** is striving for 100% code coverage
- Ensure compatibility for Python 2.7+ and Python 3.*
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
- If you want to add major functionality, [ask me](mailto:corey.r.girard@gmail.com) if it's within the scope of my vision for **Puppy**
- Don't be clever. The goal is a simple, unsurprising experience, both when using  the code and when reading the code

If you've got a bug fix or other change that is tiny (under 5 lines), feel free to just open an issue with the code included. Please clearly specify:

- Where the code should go 
- What should be changed
- What should stay the same (ie, include some unchanging lines before and after your example)

An example issue for a tiny change:

---

Came across this at line 42 of [`puppy/puppy.py`][source_link]:

[source_link]: https://github.com/crgirard/puppy/blob/0344ff4d2acb189d91e8439d96c3044dfacd43af/puppy/puppy.py

```
def doStuff(data):
    output = []

    for i in range(len(data)):
        for j in range(len(data)):
            temp = slowFunction(data[i])
	    if i == j:
	        output.append(temp)
    return output
```

It seems to me that the following might be faster with identical functionality:

```
def doStuff(data):
    output = []

    for i in range(len(data)):
        temp = slowFunction(data[i])
	output.append(temp)
    return output
```

---

### How do I pull request?

- Fork the repo
- Clone your fork

```
git clone git@github.com:your-username/puppy.git
```

- Make sure the tests pass

```
python2 puppy/test_puppy.py
python3 puppy/test_puppy.py
```

- Make your change
- Add tests for your change
- Make sure all tests pass

```
python2 puppy/test_puppy.py
python3 puppy/test_puppy.py
```

- Push to your fork
- [Submit a pull request](https://github.com/crgirard/puppy/compare/)
