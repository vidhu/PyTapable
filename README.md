<h1 align="center" style="text-align: center">
  <br>
  <a href="http://github.com/vidhu/PyTapable">
    <img src="https://raw.githubusercontent.com/vidhu/PyTapable/master/docs/pirate.svg" alt="Pirate" width="200">
  </a>
  <br>
  PyTapable
  <br>
</h1>

<h4 align="center">
A Library to Implement Hookable Interfaces
</h4>

<p align="center">  
  <!-- Test Status -->
  <a href="https://github.com/vidhu/PyTapable/actions?query=branch%3Amaster+event%3Apush">
      <img src="https://github.com/vidhu/PyTapable/workflows/Tests/badge.svg" alt="Test Status" />
  </a>
  
  <!-- PyPI Badge -->
  <a href="https://pypi.org/project/PyTapable/">
    <img src="https://img.shields.io/pypi/v/PyTapable" alt="pypi" />
  </a>
  
  <!-- CodeCov -->
  <a href="https://codecov.io/gh/vidhu/pytapable">
      <img src="https://img.shields.io/codecov/c/github/vidhu/PyTapable" alt="codecov" />
  </a>
  
  <!-- Python Versions -->
  <a href="https://pypi.org/project/PyTapable/">
      <img src="https://img.shields.io/pypi/pyversions/PyTapable" alt="python versions" />
  </a>
  
  <!-- Maintainability / Code Quality -->
  <a href="https://codeclimate.com/github/vidhu/PyTapable/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/f26988bb91b39a67c08e/maintainability" />
  </a>
  
  <!-- Downloads a day -->
  <a href="https://pypi.org/project/PyTapable/">
    <img src="https://img.shields.io/pypi/dd/PyTapable" alt="Downloads a Day" />
  </a>
  
  <!-- License -->
  <a href="https://github.com/vidhu/PyTapable/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/pytapable" alt="License" />
  </a>
  
  <!-- Maintained Status -->
  <img src="https://img.shields.io/badge/Maintained-yes-green.svg" alt="Maintained" />
  
</p>

## :corn: Table of Contents
 - [About The Project](#about-the-project)
 - [Getting Started](#getting-started)
    - [Inline Hooks Example](#inline-hooks)
    - [Functional Hooks Example](#inline-hooks)
 - [Documentation](#documentation)
 - [Contributing](#contributing)
 - [License](#license)

## :strawberry: About The Project
PyTapable  provides a set of utility to help you implement hookable interfaces in your classes. This opens up the
posibility for solving a number of usecases such as

 - Providing plugable interfaces for your libraries and frameworks
 - Code seperation by functional and service domains

## :sun_with_face: Getting Started
This project can be used in python 2.7, 3.5 and greater

```bash
$ pip install pytapable
```

### Example
#### Inline hooks
We first create our hook called `my_hook`
```python
from pytapable import Hook

my_hook = Hook()
```

As a consumer, we can tap into this hook by passing a name for our tap and a callback function
```python
def my_callback(context, greeting):
    print(f"Hook says: {greeting}")
    
my_hook.tap('My Tap Name', my_callback)
```
Our callback is executed when the `hook.call(...)` is executed. The callback receives whatever args were passed in the
`hook.call` method in addition to a context `dict`
```python
my_hook.call(greeting="Hi Callback")
```

#### Functional Hooks
Functional hooks are different from inline hooks in that the callback args are predefined.
```python
from pytapable import CreateHook, HookableMixin, create_hook_name


class Car(HookableMixin):
    HOOK_ON_MOVE = create_hook_name('on_move')
    
    @CreateHook(name=HOOK_ON_MOVE)
    def move(self, speed=10):
        return f"Moving at {speed} Mph"
```
 - Start adding the `HookableMixin` to the Car Class. This is necessary to install hooks on class methods.
 - Decorate the `Car.move` method using the `@CreateHook` decorator. In the decorator, give it a name. As best practice 
 we define the name as a Class Constant so consumers can easily refer to it.
 - The value of the hook can be anything. We use the `create_hook_name(str)` utility to generate a unique name. 
 Generating a unique name is not required but becomes important when inheriting hooks from other Classes.

```python
def callback(context, fn_args, fn_output):
    kmph_speed = fn_args['speed'] * 1.61
    print(f"The car is moving {kmph_speed} kmph")

c = Car()
c.hooks[Car.HOOK_ON_MOVE].tap('log_metric_speed', callback, before=False)

c.move(10)

```

 - Here we tap into the `on_move` hook which fires our callback after the `c.move` method has executed
 - The `c.move()` arguments are passed as `fn_args` to the callback and return value, if any, is passed as `fn_output`
 - The context holds a `is_before` and `is_after` flag it signify if the callback was executed before or after `c.move()`

## :tropical_drink: Documentation

Full documentation is available here
https://pytapable.readthedocs.io/en/latest

## :satisfied: Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. 
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

To tests on your changes locally, run:
```bash
$ pip install -r test_requirements.txt
$ tox .
```
This will run your changes on python-2 and python-3

Documentation for any new changes are a must. We use [Sphinx](https://www.sphinx-doc.org/en/master/) and to build the
documentation locally, run:

```bash
$ cd docs/
$ make html
    # or on windows
$ make.bat html

```

## :v: License
Distributed under the [Apache License](LICENSE)
