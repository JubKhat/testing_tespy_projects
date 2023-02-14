from tespy.networks import Network
from tespy.components import (Source, Sink, Pump)
from tespy.connections import Connection

def start_end_points():
        # network
        turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        pump = Pump("Pump")
        so = Source("Source")
        si = Sink("Sink")

        # Connections
        so_2_pump = Connection(so, 'out1', pump, 'in1', label="Inlet")
        pump_2_si = Connection(pump, 'out1', si, 'in1', label="Outlet")

        turbine_nw.add_conns(so_2_pump,
                             pump_2_si)

        # define parameters
        pump.set_attr(pr=7)  # """eta_s=0.75"""

        so_2_pump.set_attr(fluid={'Water': 1}, T=120, p=100,  m=5)
        pump_2_si.set_attr(T=190)


        # solve
        turbine_nw.solve(mode='design')
        turbine_nw.print_results()


def start_to_end_way():
    # network
    turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

    # components
    pump = Pump("Pump")
    so = Source("Source")
    si = Sink("Sink")

    # Connections
    so_2_pump = Connection(so, 'out1', pump, 'in1', label="Inlet")
    pump_2_si = Connection(pump, 'out1', si, 'in1', label="Outlet")

    turbine_nw.add_conns(so_2_pump,
                         pump_2_si)

    # define parameters
    pump.set_attr(eta_s=0.75, pr=7)

    so_2_pump.set_attr(fluid={'Water': 1}, T=120, p=100, m=5)
    # """pump_2_si.set_attr(T=190)"""

    # solve
    turbine_nw.solve(mode='design')
    turbine_nw.print_results()


if __name__ == '__main__':
    # start_end_points()
    start_to_end_way()
