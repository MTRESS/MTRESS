# -*- coding: utf-8 -*-
"""
Tests for MTRESS FixedTemperatureHeat Demand.
"""
import os

from oemof.solph.processing import results
import pytest

from mtress import carriers, Location, MetaModel, SolphModel, technologies, demands
from mtress._helpers import get_flows


n_days = 30


@pytest.mark.skip(reason="Not adjusted to new HeatCarrier.")
def test_layered_heat_storage():

    house_1 = Location(name="house_1")
    house_1.add(
        carriers.HeatCarrier(
            temperature_levels=[5, 10, 20, 30],
            reference_temperature=0,
        )
    )

    reservoir_temperature = np.zeros(n_days * 24)
    reservoir_temperature[0] = 40

    house_1.add(
        technologies.HeatSource(
            name="source",
            reservoir_temperature=reservoir_temperature,
            nominal_power=1e6,
            maximum_working_temperature=40,
            minimum_working_temperature=0,
        )
    )

    house_1.add(
        demands.FixedTemperatureHeating(
            name="HD",
            min_flow_temperature=20,
            return_temperature=10,
            time_series=1,
        )
    )

    house_1.add(
        technologies.LayeredHeatStorage(
            name="stor",
            diameter=1,
            volume=10,
            ambient_temperature=25,
            u_value=None,
            power_limit=1e6,
            max_temperature=30,
            min_temperature=10,
        )
    )
    meta_model = MetaModel(locations=[house_1])

    solph_representation = SolphModel(
        meta_model=meta_model,
        timeindex={
            "start": "2021-01-01 00:00:00",
            "end": f"2021-01-{n_days+1} 00:00:00",
            "freq": "60T",
        },
    )

    solph_representation.build_solph_model()

    solved_model = solph_representation.solve(solve_kwargs={"tee": True})

    return solph_representation, solved_model


if __name__ == "__main__":
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    matplotlib.use("Qt5Agg")

    os.chdir(os.path.dirname(__file__))

    solph_representation, solved_model = test_layered_heat_storage()

    myresults = results(solved_model)
    flows = get_flows(myresults)

    total_content = np.zeros(n_days * 24 + 1)
    index = None
    for key, result in myresults.items():
        if "storage_content" in result["sequences"]:
            plt.plot(result["sequences"]["storage_content"], label=str(key))
            total_content += result["sequences"]["storage_content"]
            index = result["sequences"].index
    plt.plot(index, total_content, label="total")

    plt.legend()

    plot = solph_representation.graph(detail=True, flow_results=flows)
    plot.render(outfile="layered_heat_demand.png")

    plt.show()
