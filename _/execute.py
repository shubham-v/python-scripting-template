import config
config.init()

import logging
import logger
logger.init()

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--arg1', help='')
    parser.add_argument('--arg2', help='')
    parser.add_argument('--arg3', help='')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
