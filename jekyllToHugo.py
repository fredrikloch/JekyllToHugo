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
import re
import os
import sys
import logging
import yaml

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
    return args

def printLog(level,message):
    if verbose:
        if level == 1:
            logger.info(message)
        elif level == 2:
            logger.warning(message)

    if level == 3:
        logger.error(message)

def handlePost(source_file):
    filename = os.path.basename(source_file)
    printLog(1, "Trying to convert: " + filename)

    date_in_filename_match = re.search(r"^\d{4}\-\d{1,2}\-\d{1,2}", filename)
    if not date_in_filename_match:
        printLog(2, "Unable to parse date from filename")


    with open(source_file) as f:
        printLog(1, "Parsing front matter")

        # Fixed Regex when content contains --- other than the frontmatter sepator
        frontmatter_regex = re.compile("---\n([\s\S]*?)---\n([\s\S]*)")
        date_regex = re.compile("^\s+(\d+\-\d+\d+)")

        content = f.read()

        frontmatter_regex_search_result = frontmatter_regex.search(content)
        # Expected to have a frontmatter for further processing
        if not frontmatter_regex_search_result:
            printLog(3, "Unable to read Frontmatter")
            f.close()
            return

        frontmatter_yaml = yaml.safe_load(frontmatter_regex_search_result.group(1))

        output_path = arguments.output
        if frontmatter_yaml["layout"]:
            output_path = os.path.join(arguments.output, frontmatter_yaml["layout"])
            if not os.path.exists(output_path): 
                printLog(1, "Creating folder for " + frontmatter_yaml["layout"] + " layout")
                os.makedirs(output_path)

        output_filename = os.path.join(output_path, filename)
        with open(output_filename, 'w') as nf:
            nf.write("---" + os.linesep)

            for key in frontmatter_yaml:
                if not frontmatter_yaml[key] is None:
                    if key == 'date':
                        # Hugo expects to have only YYYY-MM-DD but Jekyll can have time as well 
                        date_regex_search_result = re.search(date_regex, str(frontmatter_yaml[key]))
                        if date_regex_search_result:
                            printLog(1, "Date found in Frontmatter: {}".format(date_regex_search_result.group(1)))
                            nf.write('{}: "{}"{}'.format(key,date_regex_search_result.group(1) + "\"", os.linesep))
                    elif key in ["tags","categories"]:
                        value = frontmatter_yaml[key]
                        # Hugo expects a Go list for tags and categories
                        nf.write('{}: "{}"{}'.format(key, str(value.split(" ") if isinstance(value, str) else (value if isinstance(value, list) else [])), os.linesep))
                    elif key == "status":
                        if frontmatter_yaml[key] == "draft":
                            nf.write('draft: true{}'.format(os.linesep))
                    elif  key == "summary":
                        nf.write('description: "{}"{}'.format(str(frontmatter_yaml[key]), os.linesep))
                    elif  key == "permalink":
                        nf.write('url: "{}"{}'.format(str(frontmatter_yaml[key]), os.linesep))
                    elif  key == "layout":
                        nf.write('type: "{}"{}'.format(str(frontmatter_yaml[key]), os.linesep))
                    else:
                        nf.write(yaml.dump({key: frontmatter_yaml[key]}, default_flow_style=False))
            
            if not "date" in frontmatter_yaml and date_in_filename_match:
                printLog(1, "Unable to find date from Frontmatter, using date from filename")
                nf.write('date: "{}"{}'.format(date_in_filename_match.group(0), os.linesep))

            nf.write("---" + os.linesep)

            # Ugly fix for syntax highlighting.
            text = frontmatter_regex_search_result.group(2).replace(
                "{% highlight", 
                "{{< highlight").replace("%}", ">}}").replace("{% endhighlight",
                "{{< /highlight"
            )
            nf.write(text)
            printLog(1, "Converted file: {}".format(output_filename))


if __name__ == '__main__':
    logger = logging.getLogger("standard logger")
    logger.setLevel(logging.INFO)
    format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=format)

    arguments = parseCLI()
    arguments.source = os.path.abspath(arguments.source)
    arguments.output = os.path.abspath(arguments.output)
    verbose = arguments.verbose

    if os.path.exists(arguments.source):
        printLog(1, "Creating folder: {} for output".format(arguments.output))

        if not os.path.exists(arguments.output):
            os.makedirs(arguments.output)

        for r, d, f in os.walk(arguments.source):
                for f1 in f:
                    if re.match(r".*\.md$", f1):
                        handlePost(os.path.join(r, f1))
    else:
        printLog(3, "Source folder not found, make sure that the folder {} exists.".format(arguments.source))
        sys.exit(-1)

