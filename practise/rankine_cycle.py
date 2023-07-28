from tespy.networks import Network
from tespy.components import (Turbine, Pump, Condenser, HeatExchangerSimple, CycleCloser, Source, Sink)
from tespy.connections import Connection, Bus
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI as PSI
import pandas as pd

# Here i will test the connection of two system.
# System 1 is turbine plus condenser
# System 2 ist feed pump plus steam generator

def easy_process():
    # network
    fluid_list = ['Water']
    rankine_nw = Network(fluids=fluid_list)
    rankine_nw.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

    # components
    turb = Turbine('turbine')
    cond = Condenser('condenser')
    so = Source('source')
    si = Sink('sink')
    pump = Pump('pump')
    stm_gen = HeatExchangerSimple('steam generator')
    cc = CycleCloser('cycle closer')
    so_A = Source('source A')
    si_A = Sink('sink A')

    # define connections and add to network
    conn_cc_turb = Connection(cc, 'out1', turb, 'in1', label='1')
    conn_turb_cond = Connection(turb, 'out1', cond, 'in1', label='2')
    conn_cond_pump = Connection(cond, 'out1', pump, 'in1', label='3')
    conn_pump_stm_gen = Connection(pump, 'out1', stm_gen, 'in1', label='4')
    conn_stm_gen_cc = Connection(stm_gen, 'out1', cc, 'in1', label='0')

    rankine_nw.add_conns(conn_cc_turb,
                         conn_turb_cond,
                         conn_cond_pump,
                         conn_pump_stm_gen,
                         conn_stm_gen_cc)


    # define connections and add to network
    conn_so_cond = Connection(so, 'out1', cond, 'in2', label='11')
    conn_cond_si = Connection(cond, 'out2', si, 'in1', label='12')

    rankine_nw.add_conns(conn_so_cond,
                         conn_cond_si)

    # set the component and connection parameters.
    # turbine
    # m input, P output or the opposite
    turb.set_attr(eta_s=0.9)
    conn_cc_turb.set_attr(m=5, p=100, T=500, fluid={'Water': 1})
    conn_turb_cond.set_attr(x=0.95)

    # condenser
    cond.set_attr(pr1=1, pr2=1)
    conn_so_cond.set_attr(m=1000, p=1, T=20, fluid={'Water': 1})

    # pump
    conn_pump_stm_gen.set_attr(x=0)
    stm_gen.set_attr(pr=1)

    return rankine_nw


def turbine_condenser_element():
    # Network
    fluid_list = ['Water']
    my_NW = Network(fluids=fluid_list)
    my_NW.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg')

    # Components
    turb = Turbine('Turbine')
    cond = Condenser('Condenser')
    so_cond = Source('Source for condenser')
    si_cond = Sink('Sink for condenser')
    join_in_turbine = Source('Connection in Turbine')
    join_out_cond = Sink('Connection out condenser')

    # define connections and add to network
    conn_join_so_turbine = Connection(join_in_turbine, 'out1', turb, 'in1', label='1')
    conn_turb_cond = Connection(turb, 'out1', cond, 'in1', label='2')
    conn_cond_join_si = Connection(cond, 'out1', join_out_cond, 'in1', label='3')
    conn_so_cond = Connection(so_cond, 'out1', cond, 'in2', label='11')
    conn_cond_si = Connection(cond, 'out2', si_cond, 'in1', label='12')

    my_NW.add_conns(
        conn_join_so_turbine,
        conn_turb_cond,
        conn_cond_join_si,
        conn_so_cond,
        conn_cond_si
    )

    # set the component and connection parameters.
    # join source turbine
    conn_join_so_turbine.set_attr(T=500, p=50, fluid={"Water": 1})
    # turbine Variante A
    # Variante A: Punkt 2 ist abhängig von punkt 1 --> Verlauf verschiebt sich rechts und links im T-s-Diagramm aber der Verlauf ist identisch:
    # Verlauf identisch da eta gegeben ist
    turb.set_attr(eta_s=0.7)

    # turbine condenser
    p_cond = PSI("P", "Q", 1, "T", 273.15 + 30 + 5, "Water") / 1e5  # 273.15 K + 90 feed flow T + 5 so that condensation temp higher than 90
    # Variante B: Punkt 2 ist unabhängig von Punkt 1 --> p und x direkt gegeben. Verlauf (also eta) ändert sich abhängig von Punkt 1
    conn_turb_cond.set_attr(p=p_cond)
    #conn_turb_cond.set_attr(p=p_cond, x=0.98)
    # condenser
    conn_cond_si.set_attr(T=30, fluid={"Water": 1})
    conn_so_cond.set_attr(T=15, p=1, m=100)
    cond.set_attr(pr1=0.99, pr2=0.99)


    return my_NW, conn_cond_join_si, conn_join_so_turbine,turb, cond, conn_turb_cond


def feedpump_steamgenerator_element(rankine_nw, conn_cond_join_si, cond, conn_join_so_turbine, turb):
    pump = Pump('Feed pump')
    steam_gen = HeatExchangerSimple('Steam generator')
    join_sink_steam_gen = Sink('Connection out Steam generator')
    cc = CycleCloser('CycleCloser 0-1')

    # connections

    # del source from cons cycle und define new one
    rankine_nw.del_conns(conn_cond_join_si)
    conn_cond_pump = Connection(cond, 'out1', pump, 'in1', label='3')
    conn_pump_steam_gen = Connection(pump, 'out1', steam_gen, 'in1', label='4')
    conn_steam_gen_join_out = Connection(steam_gen, 'out1', join_sink_steam_gen, 'in1', label='0')

    rankine_nw.add_conns(
        conn_cond_pump,
        conn_pump_steam_gen,
        conn_steam_gen_join_out
    )

    # parameters
    pump.set_attr(pr=1000, eta_s=1) #pr=950
    #pump.set_attr(pr=897.1828459, eta_s=1) #pr=950
    steam_gen.set_attr(pr=1)
    conn_steam_gen_join_out.set_attr(T=500)
    # for join you cant provide too many parameters (from both sides) --> here comment out and under 'join' define again
    # was:
    # pump.set_attr(pr=950, eta_s=1)
    # steam_gen.set_attr(pr=1)
    # conn_steam_gen_join_out.set_attr(T=500)


    # JOIN
    rankine_nw.del_conns(conn_join_so_turbine, conn_steam_gen_join_out)
    conn_steam_gen_cc = Connection(steam_gen, 'out1', cc, 'in1', label='0')
    conn_cc_turb = Connection(cc, 'out1', turb, 'in1', label='1')
    rankine_nw.add_conns(conn_steam_gen_cc, conn_cc_turb)
    #pump.set_attr(pr=949.937, eta_s=1)
    #conn_steam_gen_cc.set_attr(T=500, p=50) #fluid={"Water": 1} this wont work because the p is given two times (turbine here and pump by pr)
    conn_steam_gen_cc.set_attr(T=500, fluid={"Water": 1}) #fluid={"Water": 1}

    return rankine_nw


def solve(rankine_nw, conn_turb_cond):
    # solve
    rankine_nw.set_attr(iterinfo=True)  # disable the printout of the convergence history
    rankine_nw.solve(mode='design')
    rankine_nw.print_results()
    x = conn_turb_cond.x.val
    print(x)
    d_dict = rankine_nw.results
    #d_df = pd.DataFrame.from_dict(d_dict, orient='index')
    #d = pd.DataFrame(rankine_nw.results)
    #print(d)
    #df = pd.DataFrame(rankine_nw.results)
    #df.to_csv('results.csv', index=False)
    #rankine_nw.save('exports')



if __name__ =='__main__':
    #rankine_nw = easy_process()
    rankine_nw, conn_cond_join_si,conn_join_so_turbine,turb, cond, conn_turb_cond = turbine_condenser_element()
    rankine_nw = feedpump_steamgenerator_element(rankine_nw, conn_cond_join_si, cond, conn_join_so_turbine, turb)
    solve(rankine_nw, conn_turb_cond)

