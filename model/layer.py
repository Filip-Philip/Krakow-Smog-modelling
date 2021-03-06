import numpy as np
from model.cube import WALL_COLOR
from utils import isWithin
from utils import timeCheck
import model.type
from model.SETTINGS import wind
from model.SETTINGS import wind_directions


class Layer:
    def __init__(self, y_bottom, h, cells):
        self.height = h
        self.y_bottom = y_bottom
        self.cells = cells

    def getPixels(self,x_bl,z_bl,x_tr,z_tr):

        list = [[WALL_COLOR for x in range(x_tr - x_bl+1)] for z in range(z_tr - z_bl+1)]

        print(len(list), len(list[0]))
        for z in range(z_tr - z_bl):
            iter = self.cells[z_bl + z][x_bl]
            while iter is not None and isWithin(iter.coordinates,(x_bl,z_bl),(x_tr,z_tr)):
                coor = iter.coordinates
                list[z][coor[1]-x_bl]=iter.draw()
                iter = iter.nextAir

        list = np.array(list, dtype=object)

        """
        for z in range(z_tr-z_bl):
            for x in range(x_tr - x_bl):
                list[z][x]= self.cells[z_bl+z][x_bl+x].draw()
        replaced for inline construction above"""

        return list

    def calculateUpdate(self):
        for z in range(len(self.cells)):
            iter = self.cells[z][0]
            while iter is not None:
                iter.updated = False
                iter = iter.nextAir

        for z in range(len(self.cells)):
            iter = self.cells[z][0]
            while iter is not None:
                if iter.updated == False:
                    iter.update()
                    iter.updated = True
                iter = iter.nextAir

        for z in range(len(self.cells)):
            iter = self.cells[z][0]
            while iter is not None:
                for i in range(len(wind_directions)):
                    iter.updateWind(wind_directions[i],wind[i]*(z/(len(self.cells)-1)))
                iter = iter.nextAir


    def initArray(self,arr,ind):
        for z in arr[ind]:
            for x in arr[ind][z]:
                arr[ind][z][x] = WALL_COLOR

    def getPixelsToArray(self,x_bl,z_bl,x_tr,z_tr,out_arr,ind, moved):
        if moved:
            out_arr[ind] = [[WALL_COLOR for x in range(x_tr - x_bl+1)] for z in range(z_tr - z_bl+1)]
            out_arr[ind] = np.array(out_arr[ind])

        for z in range(z_tr - z_bl):
            iter = self.cells[z_bl + z][x_bl]
            while iter is not None and isWithin(iter.coordinates, (x_bl, z_bl), (x_tr, z_tr)):
                coor = iter.coordinates
                out_arr[ind][z][coor[1] - x_bl] = iter.draw()
                iter = iter.nextAir

        print("Layer ",ind," getpixeled")
        return 1

    def wallCells(self):
        sum=0
        for _ in self.cells:
            for __ in _:
                if __.type == -1:
                    sum+=1
        return sum

    def pollutionSum(self):
        sum=0
        for _ in self.cells:
            for __ in _:
                    sum += __.pollution_rate
        return sum
