data = "0.08936,-0.01147,1.15430\n 0.08936,-0.01147,1.15430"

print(data)
ax = []
ay = []
az = []




#Splitten je Datensatz alle drei Beschleunigungskomponenten (getrennt mit Komma)
data = data.split('\n')
#data = data.split(',')

for i in data:
    splitted = i.split(',')

    #Alle einzelnen Elemente in die Liste gepackt
    lengthdata = len(splitted)
    if lengthdata > 0:
        if len(splitted[0]) > 1:
            ax.append(float(splitted[0]))
    if lengthdata > 1:
        if len(splitted[1]) > 1:
            ay.append(float(splitted[1]))
    if lengthdata > 2:
        if len(splitted[2]) > 1:
            az.append(float(splitted[2]))

#print(f"Werte ax: {ax}")
#print(f"Werte ay: {ay}")

import sys
import numpy as np
import struct

x = [324234, 5331231,234,543,234]
y = [321231,432231,643,235,654]
z = [643,233,457,876,454]

import struct

# Beispiel-Daten
list1 = [1.1 * i for i in range(127)]
list2 = [2.2 * i for i in range(127)]
list3 = [3.3 * i for i in range(127)]

# Binärdaten für alle Werte erstellen
packed_data = b''
for x, y, z in zip(list1, list2, list3):
    packed_data += struct.pack('fff', x, y, z)  # Jeweils drei Werte entpacken und packen

floats = struct.unpack('fff' * 127, packed_data)

