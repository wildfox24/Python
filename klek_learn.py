#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Square(object):
    width=0
    height=0
    
    def __init__(self, width, height):
		self.width=width
		self.height=height
		
    def area(self):
        return self.width * self.height

    @staticmethod
    def get_area(width, height):
		return width * height


class Cube(Square):
	z=0
	
	def __init__(self, width, height, z):
		#Square.__init__(self, width, height)
		super(Cube, self).__init__(width, height)
		self.z=z
		
	def volume(self):
		return self.area() * self.z
		
def main():
    sq=Square(100, 40)
    #sq.width=100
    #sq.height=40
    #print sq.area()
    #print Square.get_area(100,40)
    
    cb=Cube(100, 40, 5)
    print "Площадь: " + str(cb.area())
    print "Объем: " + str(cb.volume())
    return 0
    
if __name__ == '__main__' :
	sys.exit( main() )
