# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 21:42:10 2017

@author: Aakash
"""

import databaseOps

databaseOps.addDataToDb()
#databaseOps.showdb()
#h,t = databaseOps.getData()
a,b = databaseOps.calcDayMaximum("temperature")
print(a,b)