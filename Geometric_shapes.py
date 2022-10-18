# file contains the Geometric shapes classes, alongside the list of placed rectangles class

from Parameters import *

class Point:
    def __init__(self,x=0.0,y=0.0,other=None):
        if other!=None:
            self.x = other.x
            self.y = other.y
        else:
            self.x=x
            self.y=y

    def __repr__(self):
        return "Point("+str(self.x)+","+str(self.y)+")"

    def move_point(self,delta_x,delta_y):
        self.x-=delta_x
        self.y-=delta_y

class Rectangle:
    def __init__(self, upper_right_corner = Point(),upper_left_corner = Point(), lower_right_corner = Point(),lower_left_corner = Point()):
        self.upper_right_corner = upper_right_corner
        self.upper_left_corner  = upper_left_corner
        self.lower_right_corner = lower_right_corner
        self.lower_left_corner  = lower_left_corner
        self.width  = upper_right_corner.x - upper_left_corner.x
        self.height = upper_right_corner.y - lower_right_corner.y

    def __repr__(self):
        return "Rectangle("+str(self.upper_right_corner)+","+str( self.upper_left_corner)+","+str(self.lower_right_corner)+","+\
               str(self.lower_left_corner) +")"

    def update_location(self,point):
        x_diff = self.get_min_x()- point.x
        y_diff = self.get_min_y()- point.y
        self.upper_left_corner.move_point(x_diff,y_diff)
        self.lower_left_corner.move_point(x_diff,y_diff)
        self.upper_right_corner.move_point(x_diff,y_diff)
        self.lower_right_corner.move_point(x_diff,y_diff)

    def get_circumference(self):
        return 2*(self.height+self.width)

    def get_max_x(self):
        return self.upper_right_corner.x

    def get_max_y(self):
        return self.upper_right_corner.y

    def get_min_x(self):
        return self.lower_left_corner.x

    def get_min_y(self):
        return self.lower_left_corner.y

    def get_possible_neighbor_locations(self,rec):
        locations = []
        locations.append(Point(self.get_max_x()-rec.width,self.get_max_y())) #right upper corner 1st
        locations.append(Point(self.get_max_x(),self.get_max_y()-rec.height)) #right upper corner 2nd
        locations.append(Point(self.get_max_x(),self.get_min_y())) #right lower corner 1st
        locations.append(Point(self.get_max_x()-rec.width,self.get_min_y()-rec.height)) #right lower corner 2nd
        locations.append(Point(self.get_min_x(),self.get_max_y())) #left upper corner 1st
        locations.append(Point(self.get_min_x()-rec.width,self.get_max_y()-rec.height)) #left upper corner 2nd
        locations.append(Point(self.get_min_x()-rec.width,self.get_min_y())) #left lower corner 1st
        locations.append(Point(self.get_min_x(),self.get_min_y()-rec.height)) #left lower corner 2nd
        return locations

    def point_in_rectangle(self,point):
        return self.get_min_x()<=point.x<=self.get_max_x() and self.get_min_y()<=point.y<=self.get_max_y()

    def get_possible_hole_locations(self):
        possible_hole_locations = []
        for corner in [self.upper_right_corner,self.upper_left_corner,self.lower_left_corner,self.lower_right_corner]:
            
            # check all four points around each corner, and use half the resolution for testing; needed to avoid  
            # placing the possible hole indicator in a different rectangle
            for delta_x in [-Resolution/2,Resolution/2]:
                for delta_y in [-Resolution/2,Resolution/2]:
                    point_to_check = Point(other=corner)
                    point_to_check.move_point(delta_x,delta_y)
                    if not self.point_in_rectangle(point_to_check):
                        possible_hole_locations.append(point_to_check)

        return possible_hole_locations



    def overlap(self, rec, self_test=True):
        if rec.get_max_x() > self.get_min_x() and rec.get_min_x() < self.get_max_x():
            if (self.get_min_y() < rec.get_max_y() < self.get_max_y()) or (
                    self.get_min_y() < rec.get_min_y() < self.get_max_y()):
                return True

        if rec.get_max_y() > self.get_min_y() and rec.get_min_y() < self.get_max_y():
            if (self.get_min_x() < rec.get_max_x() < self.get_max_x()) or (
                    self.get_min_x() < rec.get_min_x() < self.get_max_x()):
                return True

        if self_test:
            return rec.overlap(self, False)

        return False


class Placed_Rectangles_List:
    def __init__(self,rec_list=None):
        self.rec_list = []
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0

        if rec_list!=None:
            self.max_x = rec_list[0].get_max_x()
            self.min_x = rec_list[0].get_min_x()
            self.max_y = rec_list[0].get_max_y()
            self.min_y = rec_list[0].get_min_y()
            for rec in rec_list:
                self.max_x = max(self.max_x,rec.get_max_x())
                self.min_x = min(self.min_x,rec.get_min_x())
                self.max_y = max(self.max_y,rec.get_max_y())
                self.min_y = min(self.min_y,rec.get_min_y())

    def __repr__(self):
        return "The current blocking rectangle circumference is:"+str(self.return_block_rec_circumference())


    def return_block_rec_circumference(self):
        return 2*((self.max_x-self.min_x)+(self.max_y-self.min_y))

    def add_rec_to_list(self,rec):
        self.max_x = max(self.max_x, rec.get_max_x())
        self.min_x = min(self.min_x, rec.get_min_x())
        self.max_y = max(self.max_y, rec.get_max_y())
        self.min_y = min(self.min_y, rec.get_min_y())
        self.rec_list.append(rec)

    def check_circumference_for_add_rec(self,rec):
        max_x = max(self.max_x, rec.get_max_x())
        min_x = min(self.min_x, rec.get_min_x())
        max_y = max(self.max_y, rec.get_max_y())
        min_y = min(self.min_y, rec.get_min_y())
        return 2*((max_x-min_x)+(max_y-min_y))


    def legal_to_add_rec(self,rec):
        for cur_rec in self.rec_list:
            if cur_rec.overlap(rec):
                return False
        return True

    def point_is_inside_hole(self,point):

        # check if the point is inside a rectangle
        for rec in self.rec_list:
            if rec.point_in_rectangle(point):
                return False

        # check if the point is surrounded by rectangles inside the rectangle structure
        upper_wall = False
        lower_wall = False
        left_wall = False
        right_wall = False

        for rec in self.rec_list:
            upper_wall = upper_wall or (rec.get_min_y() > point.y and rec.get_max_x()>=point.x>=rec.get_min_x())
            lower_wall = lower_wall or (rec.get_max_y() < point.y and rec.get_max_x()>=point.x>=rec.get_min_x())
            left_wall  = left_wall  or (rec.get_min_x() > point.x and rec.get_max_y()>=point.y>=rec.get_min_y())
            right_wall = right_wall or (rec.get_max_x() < point.x and rec.get_max_y()>=point.y>=rec.get_min_y())
        return upper_wall and lower_wall and left_wall and right_wall


    def get_hole_indicators_list(self,rec_to_check = None):
        if rec_to_check!=None:
            self.rec_list.append(rec_to_check)
        hole_list = []
        for rec in self.rec_list:
            for possible_hole_indicator in rec.get_possible_hole_locations():
                if self.point_is_inside_hole(possible_hole_indicator):
                    hole_list.append(possible_hole_indicator)

        if rec_to_check!=None:
            self.rec_list = self.rec_list[:-1]

        return hole_list