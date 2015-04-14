## Artificial Intelligence Programming Assignment

#### How to Run
* Prepare the run
 * Install Python 2.7
 * Install Tkinter 
 * Install unittest
 * Install nosetest

* Run
```
python playcc.py
```

#### How to Test
We use unittest and nosetest to test this code base
```
# nosetests
...
----------------------------------------------------------------------
Ran 3 tests in 0.012s

OK

```

#### Coding Validation
the source code of this project is formatted with Google yapf (https://github.com/google/yapf)
with the following settings:

yapf --style yapf.ini
```
[style]

based_on_style = google
indent_width = 2
split_before_logical_operator = true
```

source code is checked with pylint
with the following settings:
```
pylint --disable=locally-disabled --max-line-length=100 --indent-string='  ' *.py
```

#### Screenshot

