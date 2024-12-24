
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
received_package = b''
for x, y, z in zip(list1, list2, list3):
    received_package += struct.pack('fff', x, y, z)  # Jeweils drei Werte entpacken und packen

sample_format = 'fff'
num_samples = 127
expected_size = struct.calcsize(sample_format) * num_samples

# Überprüfen, ob die Größe korrekt ist
if len(received_package) != expected_size:
    raise ValueError(f"Ungültige Datenlänge: Erwartet {expected_size}, erhalten {len(received_package)}")

print(len(received_package))

# Daten entpacken
floats = struct.unpack(sample_format * num_samples, received_package)





