"""This module provides simple heater components (X to heat)"""

from oemof.solph import Bus
from oemof.solph import Flow
from oemof.solph.components import Converter

from .._abstract_component import AbstractSolphRepresentation
from ..carriers import ElectricityCarrier, HeatCarrier
from ._abstract_technology import AbstractTechnology


class AbstractHeater(AbstractTechnology, AbstractSolphRepresentation):
    def __init__(
        self,
        name: str,
        maximum_temperature: float,
        minimum_temperature: float,
    ):
        """
        :param name: Set the name of the component.
        :parma maximum_temperature: Temperature (in °C) of the heat output.
        :parma minimum_temperature: Lowest possible temperature (in °C) of the inlet.
        """
        super().__init__(name=name)

        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature

    def build_core(self):
        """Build core structure of oemof.solph representation."""

        self.heat_bus = heat_bus = self.create_solph_node(
            label="heat",
            node_type=Bus,
        )

        # Add heat connection
        heat_carrier = self.location.get_carrier(HeatCarrier)

        in_levels = heat_carrier.get_levels_between(
            self.minimum_temperature, self.maximum_temperature
        )
        out_levels = heat_carrier.get_levels_between(
            in_levels[1], self.maximum_temperature
        )

        for temp_in, temp_out in zip(in_levels, out_levels):
            bus_warm, bus_cold, ratio = heat_carrier.get_connection_heat_transfer(
                temp_out, temp_in
            )
            self.create_solph_node(
                label=f"heat_{temp_in:.0f}_{temp_out:.0f}",
                node_type=Converter,
                inputs={
                    bus_cold: Flow(),
                    heat_bus: Flow(),
                },
                outputs={
                    bus_warm: Flow(),
                },
                conversion_factors={
                    bus_warm: 1,
                    bus_cold: ratio,
                    heat_bus: 1 - ratio,
                },
            )


class ResistiveHeater(AbstractHeater):
    """
    ResistiveHeater converts electricity into heat at a given efficiency.
    """

    def __init__(
        self,
        name: str,
        maximum_temperature: float,
        minimum_temperature: float = 0,
        heating_power: float = None,
        efficiency: float = 1,
    ):
        """
        Initialize ResistiveHeater.

        :param name: Set the name of the component.
        :param maximum_temperature: Temperature (in °C) of the heat output.
        :param minimum_temperature: Lowest possible temperature (in °C) of the inlet.
        :param heating_power: Nominal heating capacity of the heating rod (in W).
        :param efficiency: Thermal conversion efficiency.
        """
        super().__init__(
            name=name,
            maximum_temperature=maximum_temperature,
            minimum_temperature=minimum_temperature,
        )

        self.heating_power = heating_power
        self.efficiency = efficiency

    def build_core(self):
        """Build core structure of oemof.solph representation."""

        super().build_core()

        # Add electrical connection
        electricity_carrier = self.location.get_carrier(ElectricityCarrier)
        electrical_bus = electricity_carrier.distribution

        self.create_solph_node(
            label="heater",
            node_type=Converter,
            inputs={electrical_bus: Flow()},
            outputs={self.heat_bus: Flow(nominal_value=self.heating_power)},
            conversion_factors={
                electrical_bus: 1,
                self.heat_bus: self.efficiency,
            },
        )
