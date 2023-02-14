import matplotlib.pyplot as plt
from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import (Source, Sink, Condenser, Pump)

# Create a TESPy network
nw = Network(fluids=['water', 'NH3'])

# Add components and connections to the network
source = Source('source')
sink = Sink('sink')
condenser = Condenser('condenser')
pump = Pump('pump')

nw.add_conns(Connection(source, 'out1', condenser, 'in1'))
nw.add_conns(Connection(condenser, 'out1', sink, 'in1'))
nw.add_conns(Connection(condenser, 'out2', pump, 'in1'))
nw.add_conns(Connection(pump, 'out1', condenser, 'in2'))

# Solve the network
nw.solve('design')

# Extract the components and connections information
components = nw.components.keys()
connections = nw.connections.keys()

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the components
for component in components:
    x = nw.components[component].x
    y = nw.components[component].y
    ax.scatter(x, y, label=component)

# Plot the connections
for connection in connections:
    x = [nw.connections[connection].inl.x, nw.connections[connection].outl.x]
    y = [nw.connections[connection].inl.y, nw.connections[connection].outl.y]
    ax.plot(x, y, '-', label=connection)

# Add labels and legend
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()

# Show the plot
plt.show()
