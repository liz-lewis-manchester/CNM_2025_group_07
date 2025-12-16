print(">>> SCRIPT STARTED <<<")

import csv
import numpy as np
import matplotlib.pyplot as grf
def dtheta_dt_calc(Conc,Dist,U):
    Y=[]
    try:
        for itr in range(1,len(Conc)):
            dtheta_dt=(-U*(Conc[itr+1]-Conc[itr])/(Dist[itr+1]-Dist[itr]))
            Y.append(dtheta_dt)
    except IndexError:
        pass
    return Y
with open('initial_conditions.csv', encoding="latin1") as F:
    D = list(csv.reader(F))
#Dist=np.array([])
Concentration=[float(D[itr][1]) for itr in range(1,len(D)) ]
Distance=[float(D[itr][0]) for itr in range(1,len(D)) ]
#Concentration_intital=250 #ug/m^3
Data=dtheta_dt_calc(Concentration,Distance,U=0.3)
grf.plot(Distance[0:len(Data)],Data)
grf.title('Pollutant Concentrion')
grf.xlabel('x')
grf.ylabel('$\u0398$')
grf.grid(True)
grf.savefig("initial_plot.png", dpi=300)
print("Plot saved as initial_plot.png")

print(">>> SCRIPT FINISHED <<<")
input("Press ENTER to exit")
