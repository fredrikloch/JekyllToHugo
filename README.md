# Jekyll To Hugo

This is a small script for converting [jekyll](https://jekyllrb.com) posts to [hugo](https://gohugo.io)

It requires Python and should work on all Unix-like systems, possibly also on Windows machines.
However, it's only been tested on debian using Python 2.7.


## Limitations

It currently does not handle static resources such as images and scripts, these will have to be moved to
their correct locations manually.

As for Jekyll-specific code, it only handles `{% highlight %}`, converting it into the Hugo format

## Usage

```
$ jekyllToHugo.py [-h] [-o OUTPUT] [-v] source
```

**PS:** If you are unable to execute the `jekyllToHugo.py` directly, then use this:

```
$ python jekyllToHugo.py [-h] [-o OUTPUT] [-v] source
```

If you have both Python 2 and Python 3 installed in your Linux system, you can use this:

```
$ python2 jekyllToHugo.py [-h] [-o OUTPUT] [-v] source
```

## Options

```
positional arguments:
  source                Path to folder containing jekyll posts

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to output folder, will be created if it does not
                        exist. Defaults to content
  -v, --verbose         Print extra logging output
```
