import tespy as tp
from tespy.connections import connection
from tespy.components import (Sink as sink, Source as source, Pump as pump, Turbine as turbine, Condenser as condenser, HeatExchangerSimple as heat_exchanger_simple)
from tespy.networks import Network as network

# Initialisiere das Tespy-Netzwerk
nw = network(fluids=['water', 'steam'], p_unit='bar', T_unit='C', h_unit='kJ / kg')

# Komponenten erstellen
turb = turbine('Turbine')
cond = condenser('Condenser')
pump = pump('Pump')
hex = heat_exchanger_simple('Heat Exchanger')

# Verbindungen herstellen
source = source('Source')
sink = sink('Sink')

# Komponenten zum Netzwerk hinzufügen
nw.add_subnetwork(source, turb, cond, pump, sink)

# Verbindungen zum Netzwerk hinzufügen
nw.add_connections(
    connection(source, 'out1', turb, 'in1'),
    connection(turb, 'out1', cond, 'in1'),
    connection(cond, 'out1', pump, 'in1'),
    connection(pump, 'out1', hex, 'in1'),
    connection(hex, 'out1', turb, 'in2'),
    connection(hex, 'out2', cond, 'in2'),
    connection(cond, 'out2', sink, 'in1')
)

# Startwerte für die Komponenten festlegen
turb.set_attr(p=10, T=500, m=50)
cond.set_attr(p=0.1, T=30)
pump.set_attr(p=5, T=40, m=60)

# Berechnung durchführen
nw.solve('design')

# Ergebnisse anzeigen
nw.print_results()
