import logging
from typing import Optional

from oemof.solph import Bus, Flow, Investment
from oemof.solph.components import Sink, Source

from mtress._abstract_component import AbstractSolphRepresentation
from mtress.carriers import GasCarrier
from mtress.physics import Gas

LOGGER = logging.getLogger(__file__)


class GasGridConnection(AbstractSolphRepresentation):
    """
    The gas grid connection represents the distribution pipelines for
    a specific gas type, identified by the `gas_type` parameter. It
    allows gas import at a specific pressure level, making it essential
    to provide the `grid_pressure` parameter for connecting to the
    GasCarrier bus associated with the specified gas type at the given
    pressure level.

    Note: Working_rate must be defined to enable gas import for your
          energy system.
    """

    def __init__(
        self,
        *,
        gas_type: Gas,
        grid_pressure: float,
        working_rate: Optional[float] = None,
        demand_rate: Optional[float] = 0,
        revenue: float = 0,
        **kwargs,
    ):
        """
        :gas_type: import a gas constant e.g. HYDROGEN
        :grid_pressure: in bar
        :working_rate: in currency/Wh
        :demand_rate: in currency/Wh
        :revenue: in currency/Wh
        """

        super().__init__(**kwargs)
        self.gas_type = gas_type
        self.grid_pressure = grid_pressure
        self.working_rate = working_rate
        self.demand_rate = demand_rate
        self.revenue = revenue

    def build_core(self):
        gas_carrier = self.location.get_carrier(GasCarrier)

        _, pressure_level = gas_carrier.get_surrounding_levels(
            self.gas_type, self.grid_pressure
        )

        pressure_levels = gas_carrier.pressure_levels[self.gas_type]

        pressure_index = pressure_levels.index(pressure_level)

        # Get the adjacent levels
        adjacent_levels = pressure_levels[
            max(0, pressure_index - 1) : min(len(pressure_levels), pressure_index + 2)
        ]

        _b_grid_export = {}
        _b_grid_import = {}

        for level in adjacent_levels:
            if self.revenue is not None:
                _b_grid_export[level] = self.create_solph_node(
                    label=f"grid_export_{level}",
                    node_type=Bus,
                    inputs={gas_carrier.inputs[self.gas_type][level]: Flow()},
                )

            _b_grid_import[level] = self.create_solph_node(
                label=f"grid_import_{level}",
                node_type=Bus,
                outputs={gas_carrier.inputs[self.gas_type][level]: Flow()},
            )

        if self.working_rate is not None:
            if self.demand_rate:
                demand_rate = Investment(ep_costs=self.demand_rate)
            else:
                demand_rate = None

            grid_import_bus = self.create_solph_node(
                label="grid_import_bus",
                node_type=Bus,
                outputs={_b_grid_import[level]: Flow() for level in adjacent_levels},
            )

            self.create_solph_node(
                label="source_import",
                node_type=Source,
                outputs={
                    grid_import_bus: Flow(
                        variable_costs=self.working_rate,
                        investment=demand_rate,
                    )
                },
            )

        if self.revenue is not None:
            grid_export_bus = self.create_solph_node(
                label="grid_export_bus",
                node_type=Bus,
                inputs={_b_grid_export[level]: Flow() for level in adjacent_levels},
            )

            self.create_solph_node(
                label="grid_export",
                node_type=Sink,
                inputs={
                    grid_export_bus: Flow(
                        variable_costs=-self.revenue,
                    )
                },
            )
