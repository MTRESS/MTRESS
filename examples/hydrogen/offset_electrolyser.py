"""Example to illustrate hydrogen production to meet hydrogen demand."""

import logging
import os

import pandas as pd
from oemof.solph.processing import results

from mtress import Location, MetaModel, SolphModel, carriers, demands, technologies
from mtress.physics import HYDROGEN
from mtress.technologies import PEM_ELECTROLYSER

LOGGER = logging.getLogger(__file__)
from mtress._helpers import get_flows

energy_system = MetaModel()

os.chdir(os.path.dirname(__file__))

house_1 = Location(name="house_1")

energy_system.add_location(house_1)


house_1.add(carriers.Electricity())
house_1.add(technologies.ElectricityGridConnection(working_rate=70e-6))

house_1.add(
    carriers.GasCarrier(
        gases={
            HYDROGEN: [30],
        }
    )
)

house_1.add(
    demands.GasDemand(
        name="H2_demand",
        gas_type=HYDROGEN,
        time_series=[0.5, 2.5, 1.5],
        pressure=30,
    )
)

house_1.add(
    carriers.HeatCarrier(
        temperature_levels=[20, 40],
        reference_temperature=10,
    )
)

house_1.add(
    technologies.Electrolyser(
        name="PEM_Ely",
        nominal_power=150e3,
        template=PEM_ELECTROLYSER,
        offset=True,
    )
)

solph_representation = SolphModel(
    energy_system,
    timeindex={
        "start": "2022-06-01 08:00:00",
        "end": "2022-06-01 11:00:00",
        "freq": "60T",
        "tz": "Europe/Berlin",
    },
)

solph_representation.build_solph_model()

plot = solph_representation.graph(detail=True)
plot.render(outfile="offset_ely_detail.png")

plot = solph_representation.graph(detail=False)
plot.render(outfile="offset_ely_simple.png")

solved_model = solph_representation.solve(solve_kwargs={"tee": True})

logging.info("Optimise the energy system")
myresults = results(solved_model)
flows = get_flows(myresults)

results_df = pd.DataFrame(flows)

solved_model.write("offset.lp", io_options={"symbolic_solver_labels": True})
