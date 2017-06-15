# Ivona, Speak!
[![Build status](https://img.shields.io/travis/Pythonity/ivona-speak.svg)][travis]
[![Test coverage](https://img.shields.io/coveralls/Pythonity/ivona-speak.svg)][coveralls]
[![PyPI version](https://img.shields.io/pypi/v/ivona_speak.svg)][pypi]
[![Python versions](https://img.shields.io/pypi/pyversions/ivona_speak.svg)][pypi]
[![License](https://img.shields.io/github/license/Pythonity/ivona-speak.svg)][license]

Python script that lets you easily convert passed text to synthesized audio
files, with help of Amazon's [IVONA][ivona]. All you need is a pair of 
[keys][ivona keys] and this script. Yes, that's *literally* everything you need
to never speak again. If that's your thing of course.

If you want to use IVONA Speech Cloud directly inside your Python project then
you should have a look at [python-ivona-api][ivona api], which this script
uses in the background.

## Installation
From PyPI (recommended):

```
$ pip install ivona_speak
```

With `git clone`:

```
$ git clone https://github.com/Pythonity/ivona-speak
$ pip install -r ivona-speak/requirements.txt
$ cd ivona-speak/bin
```

## Usage

```
$ ivona-speak --help

  Easily convert passed text to synthesized audio files, with help of
  Amazon's IVONA. All you need is a pair of auth keys.

  See https://github.com/Pythonity/ivona-speak for more info.

Options:
  --help  Show this message and exit.

Commands:
  synthesize*  Synthesize passed text and save it as an...
  list-voices  List available Ivona voices

```

## Examples
You can provide keys either explicitly: 

```
$ ivona-speak --access-key 'YOUR_ACTUAL_ACCESS_KEY' --secret-key 'YOUR_ACTUAL_SECRET_KEY' list-voices
```

or export them as environment variables:

```
$ export IVONA_ACCESS_KEY='...'
$ export IVONA_SECRET_KEY='...'
$ ivona-speak list-voices
```

The default subcommand is `synthesize`, so these do the same:

```
$ ivona-speak synthesize -o hello_world.mp3 'Hello world!'
$ ivona-speak -o hello_world.mp3 'Hello world!'
```

I want someone to say 'Hello world!', and say it quick:

```
$ ivona-speak synthesize -o hello_world.mp3 'Hello world!'
```

She sounds so nice. I want someone special to respond her:

```
$ ivona-speak synthesize -o response.mp3 -n Joey 'How you doin?'
```

## Tests
Package was tested with the help of `py.test` and `tox` on Python 2.7, 3.4, 3.5
and 3.6 (see `tox.ini`).

Code coverage is available at [Coveralls][coveralls].

To run tests yourself you need to set environment variables with secret
and access keys before running `tox` inside the repository:

```shell
$ pip install tox
$ export IVONA_ACCESS_KEY='..'
$ export IVONA_SECRET_KEY='..'
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes. Thanks!

## Authors
Developed and maintained by [Pythonity][pythonity], a group of Python
enthusiasts who love open source, have a neat [blog][pythonity blog] and are
available [for hire][pythonity].

Written by [Paweł Adamczak][pawelad].

Released under [MIT License][license].


[coveralls]: https://coveralls.io/github/Pythonity/ivona-speak
[github]: https://github.com/Pythonity/ivona-speak
[ivona]: https://www.ivona.com/
[ivona api]: https://github.com/Pythonity/python-ivona-api
[ivona keys]: http://developer.ivona.com/en/speechcloud/introduction.html#Credentials
[license]: https://github.com/Pythonity/ivona-speak/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[pypi]: https://pypi.python.org/pypi/ivona_speak
[pythonity]: https://pythonity.com/
[pythonity blog]: http://blog.pythonity.com/
[travis]: https://travis-ci.org/Pythonity/ivona-speak
