from tespy.networks import Network
from tespy.components import (Source, Sink, Turbine)
from tespy.connections import Connection

def main_func1():
        # network
        turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        turb = Turbine("Turbine")
        so = Source("Source")
        si = Sink("Sink")

        # Connections
        so_2_turb = Connection(so, 'out1', turb, 'in1', label="Inlet")
        turb_2_si = Connection(turb, 'out1', si, 'in1', label="Outlet")

        turbine_nw.add_conns(so_2_turb,
                             turb_2_si)

        # define parameters
        turb.set_attr(eta_s=0.9)

        so_2_turb.set_attr(fluid={'Water': 1}, T=500, p=100,  m=5)
        turb_2_si.set_attr(x=0.8)

        # solve
        turbine_nw.solve(mode='design')
        turbine_nw.print_results()


def main_func2():
        # network
        turbine_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        turb = Turbine("Turbine")
        so = Source("Source")
        si = Sink("Sink")

        # Connections
        so_2_turb = Connection(so, 'out1', turb, 'in1', label="Inlet")
        turb_2_si = Connection(turb, 'out1', si, 'in1', label="Outlet")

        turbine_nw.add_conns(so_2_turb,
                             turb_2_si)

        # define parameters
        turb.set_attr(eta_s=0.9, P=-600000)#-6.74e+06

        so_2_turb.set_attr(fluid={'Water': 1}, T=500, p=100,  m=5)
        #turb_2_si.set_attr(x=0.8)

        # solve
        turbine_nw.solve(mode='design')
        turbine_nw.print_results()

if __name__ == '__main__':
    # main_func1()
    main_func2()
