from tespy.networks import Network
from tespy.components import (Source, Sink, HeatExchanger)
from tespy.connections import Connection


def main_func():
    # network
    hx_nw = Network(fluids=["Water",'Air'], T_unit="C", p_unit="bar", h_unit="kJ / kg")

    # components
    hx = HeatExchanger('Heat Exchanger')
    so_h = Source("Source Hot")
    si_h = Sink("Sink Hot")
    so_c = Source("Source Cold")
    si_c = Sink("Sink Cold")

    # connections
    hot_in_2_hx = Connection(so_h, 'out1', hx, 'in1', label='Hot In')
    cold_in_2_hx = Connection(so_c, 'out1', hx, 'in2', label='Cold In')
    hot_hx_2_out = Connection(hx, 'out1', si_h, 'in1', label='Hot Out')
    cold_hx_2_out = Connection(hx, 'out2', si_c, 'in1', label='Cold Out')

    hx_nw.add_conns(hot_in_2_hx, hot_hx_2_out)
    hx_nw.add_conns(cold_in_2_hx, cold_hx_2_out)

    # parameters
    # hx
    hx.set_attr(pr1=1, pr2=1)
    # hot
    hot_in_2_hx.set_attr(T=90, p=1, fluid={'Water': 1, 'Air': 1}, m=5)
    hot_hx_2_out.set_attr(T=50)
    # cold
    cold_in_2_hx.set_attr(T=15, p=1, fluid={'Air': 1, 'Water': 0})
    cold_hx_2_out.set_attr(T=50)

    # solve
    hx_nw.solve(mode='design')
    hx_nw.print_results()


if __name__ == '__main__':
    main_func()