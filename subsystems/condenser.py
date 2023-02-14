from tespy.components import Sink, Source, Condenser
from tespy.connections import Connection
from tespy.networks import Network
from tespy.tools.fluid_properties import T_bp_p
import shutil

"""
Air is used to condensate water in a condenser. 1 kg/s waste steam is chilled with
a terminal temperature difference of 15 K.
"""

# network
nw = Network(fluids=['water', 'air'], T_unit='C', p_unit='bar',
    h_unit='kJ / kg', m_range=[0.01, 1000], iterinfo=False)

# components
amb_in = Source('ambient air inlet')
amb_out = Sink('air outlet')
waste_steam = Source('steam in')
c = Sink('condensate sink')
cond = Condenser('condenser')

# connections
amb_he = Connection(amb_in, 'out1', cond, 'in2', label='air in')
he_amb = Connection(cond, 'out2', amb_out, 'in1', label='air out')
ws_he = Connection(waste_steam, 'out1', cond, 'in1', label='steam in')
he_c = Connection(cond, 'out1', c, 'in1', label='condensate out ')
nw.add_conns(amb_he, he_amb, ws_he, he_c)

# parameters
# condenser
cond.set_attr(pr1=1, pr2=1, ttd_u=50)  # delta T cold out and hot out (min T)
# hot side
ws_he.set_attr(fluid={'water': 1, 'air': 0}, h=2700, m=1)
# cold side
amb_he.set_attr(fluid={'water': 0, 'air': 1}, T=20)
he_amb.set_attr(p=1, T=40)


nw.solve('design')
nw.print_results()

# round(amb_he.v.val, 2)
# 103.17
# round(ws_he.T.val - he_amb.T.val, 1)
# 66.9
# round(T_bp_p(ws_he.get_flow()) - 273.15 - he_amb.T.val, 1)
# 15.0
# ws_he.set_attr(m=0.7)
# amb_he.set_attr(T=30)
# nw.solve('offdesign', design_path='tmp')
# round(ws_he.T.val - he_amb.T.val, 1)
# 62.5
# round(T_bp_p(ws_he.get_flow()) - 273.15 - he_amb.T.val, 1)
# 11.3