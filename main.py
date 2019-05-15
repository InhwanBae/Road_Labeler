#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
from argparse import ArgumentParser
from ui import *


def inputArg():
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", help="source image name", required=True)
    args = ap.parse_args()

    return args.image


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    # inputPath = inputArg()
    inputPath = "data"

    # generate application window
    w = genWindow(inputPath)



