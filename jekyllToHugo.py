#!/usr/bin/env python

# Copyright (C) Fredrik Loch 2015  Jekyll-Hugo
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

__author__ = "Fredrik Loch"
__copyright__ = "Copyright 2015, Jekyll-Hugo"
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Fredrik Loch"
__email__ = "mail@fredrikloch.me"
__status__ = "Development"

import argparse
import subprocess
import re
import string, random
import shutil
import os
import sys
import logging
from datetime import datetime
import yaml
import types

def parseCLI():
    command_line = argparse.ArgumentParser(description='Options')
    command_line.add_argument("-o", "--output", type=str,
        help="Path to output folder, will be created if it does not exist. Defaults to content",
        default="content")
    command_line.add_argument("-v", "--verbose", action="store_true",
        help="Print extra logging output",
        default=False)
    command_line.add_argument("source", type=str,  help="Path to folder containing jekyll posts")
    args = command_line.parse_args()
    return args;

def printLog(level,message):
    if verbose:
        if level == 1:
            logger.info(message)
        elif level == 2:
            logger.warning(message)
    if level == 3:
        logger.error(message)

def handlePost(filename, path):
    printLog(1,"Trying to convert " + filename)
    try:
        time = datetime.strptime(filename[:10], "%Y-%m-%d")
    except:
        printLog(3, "Error parsing " + filename + " could not get date")
        return
    with open(path + filename) as f:
        printLog(1,"Parsing front matter")
        regex = re.compile("---\n([\s\S]*)---\n([\s\S]*)")
        content = f.read()
        r = regex.search(content)
        r.groups()
        y = yaml.load(r.groups()[0])
        if y["layout"]:
            printLog(1, "Creating folder for " + y["layout"] + " layout")
            if not os.path.exists(arguments.output + y["layout"]): os.makedirs(arguments.output + y["layout"])
            output_path = arguments.output + y["layout"] + "/"
        else:
            output_path = arguments.output
        with open(output_path + filename, 'w') as nf:
            nf.write("---" + os.linesep)
            for key in y:
                if key == 'date':
                    nf.write(key + ": \"" + time.strftime("%Y-%m-%d")  + "\"" + os.linesep)
                elif not  isinstance(y[key], types.StringTypes):
                    nf.write(key + ":" + str(y[key])  + os.linesep)
                elif key in ["tags","categories"]:
                    nf.write(key + ":" + str(y[key].split(" ")) + os.linesep)
                else:
                    nf.write(key + ": \"" + str(y[key])  + "\"" + os.linesep)
            nf.write("---" + os.linesep)

            # Uggly fix for syntax higlighting
            text = r.groups()[1].replace("{% highlight", "{{< highlight").replace("%}", ">}}").replace("{% endhighlight", "{{< /highlight")
            nf.write(text)


if __name__ == '__main__':
    logger = logging.getLogger("standard logger")
    logger.setLevel(logging.INFO)
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    arguments = parseCLI()
    verbose = arguments.verbose
    if os.path.exists(arguments.source):
        printLog(1,"Creating folder " + arguments.output + " for output")

        if not os.path.exists(arguments.output): os.makedirs(arguments.output)
        ## Clean up input
        if not arguments.source[-1] == '/': arguments.source = arguments.source + "/"
        if not arguments.output[-1] == '/': arguments.output = arguments.output + "/"
        for filename in os.listdir(arguments.source):
            handlePost(filename, arguments.source)
    else:
        printLog(3, "Source folder not found, make sure that the folder " + arguments.source + " exists")
        sys.exit(-1)

