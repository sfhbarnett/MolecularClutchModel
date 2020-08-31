import random
import math
import matplotlib.pyplot as plt

Nmyosin = 800
Fmyosin = 2e-12
Fs = Nmyosin*Fmyosin
talinclutch = 1200
talin_kon = 1 # s-1
talin_koff = 0.2
kT = 4.11e-12
clutch_binding_status = [0 for t in range(talinclutch)]
force = [0 for f in range(talinclutch)]
clutch_position = [0 for position in range(talinclutch)]
actin_flow = -90e-9
breakingforce = 50e-12
timepoints = 400
Fratio = 1


Nb = sum(clutch_binding_status)
ksub = 2e3 #substrate stiffness, 0.01-100 pN/nm, = 0.01e-3-100e-3 N/m
xsub = 0 #attachment point of the substrate
kclutch = 5e-3 #clutch spring constant (N/m),refered to as Kc in other models and 5 pN/nm
ts= 5e-3 #timestep (seconds)
Frupture = 2e-12 #clutch breaking point, (N) = 2pN
SubstrateForce = []
print(clutch_binding_status)
filament = []
for i in range(timepoints):
    Nb = sum(clutch_binding_status)
    #calculate engagement/disengagement
    for talin in range(talinclutch):
        if clutch_binding_status[talin] == 1: #if clutch is engages
            koff = math.exp(talin_koff*ts) * math.exp(force[talin] / Frupture)
            switch = random.random()
            if switch < koff: #check if clutch disengages
                clutch_binding_status[talin] = 0
        else: #check if clutch becomes engaged
            switch = random.random()
            if switch > math.exp(-talin_kon*ts):
                clutch_binding_status[talin] = 1

    # balance forces on the clutches by stretching the substrate
    xsub = (kclutch * sum([pos * bound for pos, bound in zip(clutch_position, clutch_binding_status)])) / (ksub + sum(clutch_binding_status) * kclutch)
    #update actin flow rate
    truevelocity = actin_flow * (1 - (ksub * xsub) / Fs)
    #Calculate new clutch positions for engaged clutches
    clutch_position = [(cp+truevelocity)*bs*ts if bs == 1 else xsub for cp,bs in zip(clutch_position,clutch_binding_status)]

    print(clutch_position)
    filament.append(truevelocity*1e9)
    SubstrateForce.append(sum(force))
    #Update the force on each clutch for the new substrate position
    force = [kclutch*(cp-xsub) for cp in clutch_position]

print(SubstrateForce)
plt.plot(filament)

plt.show()

