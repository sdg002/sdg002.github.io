# Overview
This is a common library of simple Python classes which represent 2d Geometry primitives

# How to run the unit tests?
## Running from Python command line
- Launch a CMD which has Python in the PATH
- Change the directory to the `simple-geometry` folder
```
python -m unittest discover -s .\tests\ -p "test_*.py
```

## Running from VS Code
- Ensure you have a `.vscode` file at the root of the project.
- The root would be inside the folder `simple-geometry`

# Structuring the folders into a module
Refer this article https://realpython.com/absolute-vs-relative-python-imports/#how-imports-work
We are not following the `__init__.py` but instead createing a module Python file 

