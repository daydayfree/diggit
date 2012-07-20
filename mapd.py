#!/usr/bin/env python

from daemon import TagsMapReduced

def main():
    TagsMapReduced.instance().process()

if __name__ == "__main__":
    main()
