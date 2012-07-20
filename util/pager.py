# -*- coding: utf-8 -*-

class Pager(object):
    length = 7
    def __init__(self, size, total, index=1, url="/"):
        self.size = size
        self.total = total
        self.index = index
        self.url = url
        self.pages = int(self.total / self.size)
        if self.pages * self.size < self.total:
            self.pages += 1
        self.start_index = self.index
        self.end_index = self.length
        self.show_previous = False
        self.show_next = False
        self._initialize()


    def _initialize(self):
        if self.index <= (self.length - 1) / 2:
            self.start_index = 1
        else:
            if self.index > (self.length + 1) / 2:
                self.show_previous = True
            _link_length = (self.pages - self.index + 1) + (self.length-1)/2
            self.start_index = self.index - (self.length-1)/2
            while(_link_length < self.length and self.start_index > 1):
                _link_length += 1
                self.start_index -= 1
            
        if (self.index + (self.length - 1) / 2) >= self.pages:
            self.end_index = self.pages
        else:
            _link_length = (self.index-self.start_index+1) + (self.length-1)/2
            self.end_index = self.index + (self.length-1)/2
            while(_link_length < self.length and self.end_index < self.pages):
                _link_length += 1
                self.end_index += 1
            if self.end_index < self.pages:
                self.show_next = True


    def display(self):
        links = "%s %s %s %s %s" % (
            ("1..." if self.show_previous else ""), 
            self.start_index,self.index, 
            self.end_index,
            ("...%s" % self.pages if self.show_next else ""))
        print links
