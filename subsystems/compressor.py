from tespy.networks import Network
from tespy.components import (Source, Sink, Compressor)
from tespy.connections import Connection

def main_func():
    # network
    fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2"]
    nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

    # components
    comp = Compressor("Compressor")
    so = Source("Source")
    si = Sink("Sink")

    # Connections
    so_2_comp = Connection(so, 'out1', comp, 'in1', label="Inlet")
    comp_2_si = Connection(comp, 'out1', si, 'in1', label="Outlet")

    nw.add_conns(so_2_comp, comp_2_si)

    # define parameters
    comp.set_attr(eta_s=0.9, P= 5000000)

    so_2_comp.set_attr(m =100,p=1, T=20,
    fluid={
        "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
        "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
    })

    # solve
    nw.solve(mode='design')
    nw.print_results()


"""
Leistung P, Massenstrom m, Druckverhältnis pr
A: Input  P,  m -> Output pr
B: Input  P,  pr -> Output m
C: Input  pr,  m -> Output P
"""
if __name__ == '__main__':
    main_func()
