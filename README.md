# Ivona, Speak!
[![Build Status](https://img.shields.io/travis/Pythonity/ivona-speak.svg)][ivona speak github]
[![PyPI Version](https://img.shields.io/pypi/v/ivona_speak.svg)][ivona speak pypi]
[![Python Versions](https://img.shields.io/pypi/pyversions/ivona_speak.svg)][ivona speak pypi]
[![License](https://img.shields.io/github/license/Pythonity/ivona-speak.svg)][license]

Python (3) script that lets you easily convert passed text to 
synthesized audio files, with help of Amazon's [IVONA][ivona]. All you
need is a pair of [keys][ivona keys] and this script. Yes, that's
*literally* everything you need to never speak again. If that's your
thing of course.

If you want to use IVONA Speech Cloud directly inside your (probably
awesome) Python project then have a look at
[python-ivona-api][ivona api github], which this script also uses.

## Installation
With `pip` (recommended):
```shell
$ pip3 install ivona_speak
```

Without `pip`:
```shell
$ git clone https://github.com/Pythonity/ivona-speak
$ pip install -r ivona-speak/requirements.txt
$ cd icon-font-to-png/bin
```

## Usage
The script comes with two subcommands (`synthesize` is the default one):
```
$ ivona-speak synthesize -h
Usage: ivona-speak synthesize [OPTIONS] TEXT

  Synthesize passed text and save it as an audio file

Options:
  --access-key TEXT          IVONA Speech Cloud access key.
  --secret-key TEXT          IVONA Speech Cloud secret key.
  -a, --auth-file FILENAME   Path to YAML file with 'access-key' and 'secret-
                             key' set.
  -o, --output-file PATH     Output audio file path.  [required]
  -n, --voice-name TEXT      Voice name (default: Salli).
  -l, --voice-language TEXT  Voice language (default: en-US).
  -c, --codec [ogg|mp3|mp4]  Used codec (default: mp3).
  -h, --help                 Show this message and exit.
```

```
$ ivona-speak list-voices -h
Usage: ivona-speak list-voices [OPTIONS]

  List available Ivona voices

Options:
  --access-key TEXT          IVONA Speech Cloud access key.
  --secret-key TEXT          IVONA Speech Cloud secret key.
  -a, --auth-file FILENAME   Path to YAML file with 'access-key' and 'secret-
                             key' set.
  -l, --voice-language TEXT  Filter voice by language.
  -h, --help                 Show this message and exit.
```

## Examples
With above usage everything should be pretty clear, but in case it 
isn't:  

You can provide keys either explicitly or put them in YAML file (one of
those ways is required):
```
$ ivona-speak list-voices --access-key 'YOUR_ACTUAL_ACCESS_KEY' --secret-key 'YOUR_ACTUAL_SECRET_KEY'
$ ivona-speak list-voices -a secrets.yaml
```

Also, `synthesized` is the default subcommand so those do the same:
```
$ ivona-speak synthesize -a secrets.yaml -o hello_world.mp3 'Hello world!'
$ ivona-speak -a secrets.yaml -o hello_world.mp3 'Hello world!'
```

List all available IVONA voices, and list them now:
```
$ ivona-speak list-voices -a secrets.yaml
```

I want someone to say 'Hello world!', and say it quick:
```
$ ivona-speak synthesize -a secrets.yaml -o hello_world.mp3 'Hello world!'
```

She sounds so nice. I want someone special to respond her:
```
$ ivona-speak synthesize -a secrets.yaml -o response.mp3 -n Joey 'How you doin?'
```

### Example auth file
```
$ cat secrets.yaml
access-key: YOUR_ACTUAL_ACCESS_KEY
secret-key: YOUR_ACTUAL_SECRET_KEY
```

## Tests
Package was tested with `pytest` and `tox` on Python 3.4
(see `tox.ini`).

To run tests yourself you need to set environment variables with secret
and access keys before running `tox` inside the repository:
```shell
export IVONA_ACCESS_KEY="YOUR_ACTUAL_ACCESS_KEY"
export IVONA_SECRET_KEY="YOUR_ACTUAL_SECRET_KEY"
```

## Contributions
Package source code is available at [GitHub][ivona speak github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest 
enhancements and point out any mistakes.

## Authors
Developed and maintained by [Pythonity][pythonity].

Written by [Paweł Adamczak][pawelad].

[ivona speak github]: https://github.com/Pythonity/ivona-speak
[ivona speak pypi]: https://pypi.python.org/pypi/ivona_speak
[license]: https://github.com/Pythonity/ivona-speak/blob/master/LICENSE
[ivona]: https://www.ivona.com/
[ivona keys]: http://developer.ivona.com/en/speechcloud/introduction.html#Credentials
[ivona api github]: https://github.com/Pythonity/python-ivona-api
[pythonity]: http://pythonity.com/
[pawelad]: https://github.com/pawelad