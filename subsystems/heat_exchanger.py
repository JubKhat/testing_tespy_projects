from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchangerSimple)
from tespy.connections import Connection
import CoolProp.CoolProp as CP

def main_func():
        # network
        hx_nw = Network(fluids=["Water"], T_unit="C", p_unit="bar", h_unit="kJ / kg")

        # components
        hx = HeatExchangerSimple("Heat Exchanger")
        so = Source("Source")
        si = Sink("Sink")

        # Connections
        so_2_hx = Connection(so, 'out1', hx, 'in1', label="Inlet")
        hx_2_si = Connection(hx, 'out1', si, 'in1', label="Outlet")

        hx_nw.add_conns(so_2_hx, hx_2_si)

        # define parameters
        hx.set_attr(pr=1,  Q=-50000)

        so_2_hx.set_attr(fluid={'Water':0.9}, T=50, p=1)
        hx_2_si.set_attr(T=10)

        # solve
        hx_nw.solve(mode='design')
        hx_nw.print_results()


if __name__ == '__main__':
    main_func()
