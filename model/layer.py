import numpy as np
from model.cube import WALL_COLOR
from utils import isWithin
from utils import timeCheck
import model.type

class Layer:
    def __init__(self, y_bottom, h, cells):
        self.height = h
        self.y_bottom = y_bottom
        self.cells = cells
    def getPixels(self,x_bl,z_bl,x_tr,z_tr):
        #print("startpxlGet", timeCheck())

        list = [[WALL_COLOR for x in range(x_tr - x_bl)] for z in range(z_tr - z_bl)]
        #print("listcrt", timeCheck())

        #todo? multithreading filling
        for z in range(z_tr - z_bl):
            iter = self.cells[z_bl + z][x_bl]
            while iter is not None and isWithin(iter.coordinates,(x_bl,z_bl),(x_tr,z_tr)):
                coor = iter.coordinates
                list[z][coor[1]-x_bl]=iter.draw()
                iter = iter.nextAir
        #print("listfilled", timeCheck())

        list = np.array(list, dtype=object)
        #print("nparrd", timeCheck())


        """
        for z in range(z_tr-z_bl):
            for x in range(x_tr - x_bl):
                list[z][x]= self.cells[z_bl+z][x_bl+x].draw()
        replaced for inline construction above"""

        #print(arr.shape)#print("shape",arr.shape)
        #print(arr)
        #out = im.fromarray(arr, "L")
        #out.show()
        return list

    def calculateUpdate(self):
        for z in range(len(self.cells)):
            iter = self.cells[z][0]
            while iter is not None:
                #TODO : iter.update
                iter.updated = False
                iter = iter.nextAir

        for z in range(len(self.cells)):
            iter = self.cells[z][0]
            while iter is not None:
                #TODO : iter.update
                if iter.updated == False:
                    iter.update()
                    iter.updated = True
                iter = iter.nextAir

        print("updated layer with y_bottom=",self.y_bottom)
        #print("sum of pollution on layer:",self.y_bottom," ",self.pollutionSum())


    def initArray(self,arr,ind):
        for z in arr[ind]:
            for x in arr[ind][z]:
                arr[ind][z][x] = WALL_COLOR

    def getPixelsToArray(self,x_bl,z_bl,x_tr,z_tr,out_arr,ind, moved):
        # print("listcrt", timeCheck())
        if moved:
            out_arr[ind] = [[WALL_COLOR for x in range(x_tr - x_bl)] for z in range(z_tr - z_bl)]
            out_arr[ind] = np.array(out_arr[ind])

        # todo? multithreading filling
        for z in range(z_tr - z_bl):
            iter = self.cells[z_bl + z][x_bl]
            while iter is not None and isWithin(iter.coordinates, (x_bl, z_bl), (x_tr, z_tr)):
                coor = iter.coordinates
                out_arr[ind][z][coor[1] - x_bl] = iter.draw()
                iter = iter.nextAir
        # print("listfilled", timeCheck())
        # print("nparrd", timeCheck())
        # out_arr[ind] = self.getPixels(x_bl, z_bl, x_tr, z_tr)
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
