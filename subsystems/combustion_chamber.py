from tespy.networks import Network
from tespy.components import (Source, DiabaticCombustionChamber, Sink)
from tespy.connections import Connection


def define():
    # network
    fluid_list = ["Ar", "N2", "O2", "CO2", "CH4", "H2O", "H2"]
    nw = Network(fluids=fluid_list, p_unit="bar", T_unit="C")

    # components
    chamber = DiabaticCombustionChamber('Combustion Chamber')
    air_source = Source('Air Inlet')
    exhaust_sink = Sink('Exhaust')
    fuel_source = Source('Fuel')

    # connections
    so_to_chamber = Connection(air_source, 'out1',  chamber,'in1', label='2')
    fuel_to_chamber = Connection(fuel_source, 'out1', chamber, 'in2', label='5')
    chamber_to_exhaust = Connection(chamber, 'out1', exhaust_sink, 'in1', label='3')

    nw.add_conns(fuel_to_chamber,so_to_chamber, chamber_to_exhaust)
    return nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust


def q_lambda_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust):
    # parameters
    # air source
    so_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
            "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
        }
    )

    # chamber
    fuel_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "CO2": 0.04, "Ar": 0, "N2": 0, "O2": 0,
            "H2O": 0, "CH4": 0.96, "H2": 0
        }
    )
    chamber.set_attr(pr=1, eta=1, lamb=1.5, ti=10e6)
    return nw


def mfuel_lambda_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust):
    # parameters
    # air source
    so_to_chamber.set_attr(
        p=1, T=20, m=20,
        fluid={
            "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
            "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
        }
    )

    # chamber
    fuel_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "CO2": 0.04, "Ar": 0, "N2": 0, "O2": 0,
            "H2O": 0, "CH4": 0.96, "H2": 0
        }
    )
    chamber.set_attr(pr=1, eta=1, lamb=1.5)
    return nw


def mfuel_T_aus_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust):
    # parameters
    # air source
    so_to_chamber.set_attr(
        p=1, T=20, m=20,
        fluid={
            "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
            "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
        }
    )

    # chamber
    fuel_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "CO2": 0.04, "Ar": 0, "N2": 0, "O2": 0,
            "H2O": 0, "CH4": 0.96, "H2": 0
        }
    )
    chamber.set_attr(pr=1, eta=1)

    # flue gas
    chamber_to_exhaust.set_attr(T=1500)
    return nw

def q_T_aus_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust):
    # parameters
    # air source
    so_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "Ar": 0.0129, "N2": 0.7553, "H2O": 0,
            "CH4": 0, "CO2": 0.0004, "O2": 0.2314, "H2": 0
        }
    )

    # chamber
    fuel_to_chamber.set_attr(
        p=1, T=20,
        fluid={
            "CO2": 0.04, "Ar": 0, "N2": 0, "O2": 0,
            "H2O": 0, "CH4": 0.96, "H2": 0
        }
    )
    chamber.set_attr(pr=1, eta=1, ti=1000000)

    # flue gas
    chamber_to_exhaust.set_attr(T=1500)
    return nw


if __name__ == '__main__':
    nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust = define()
    # nw = q_lambda_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust)
    # nw = mfuel_lambda_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust)
    # nw = mfuel_T_aus_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust)
    nw = q_T_aus_input(nw, chamber, air_source, fuel_source, exhaust_sink, so_to_chamber, fuel_to_chamber, chamber_to_exhaust)
    nw.solve(mode="design")
    df_results = nw.results
    nw.print_results()
    print(nw.results["Connection"])

