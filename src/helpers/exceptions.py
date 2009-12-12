'''
Created on Dec 10, 2009

@author: Anton Gorshkov
'''

class ValidationError(Exception):

    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)
        