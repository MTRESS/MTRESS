"""This module provides the boiler module"""

import logging

import numpy as np
from oemof.solph import Flow
from oemof.solph.components import Converter

from .._abstract_component import AbstractSolphRepresentation
from ..carriers import HeatCarrier, GasCarrier
from ..physics import Gas
from ._abstract_technology import AbstractTechnology

LOGGER = logging.getLogger(__file__)


class GasBoiler(AbstractTechnology, AbstractSolphRepresentation):
    """
    A boiler is a closed vessel in which fluid (generally water) is heated.
    """

    def __init__(
        self,
        name: str,
        gas_type: Gas,
        maximum_temperature: float,
        minimum_temperature: float,
        nominal_power: float,
        thermal_efficiency: float,
        input_pressure: float,
    ):
        """
        Initialize Boiler component.

        :param name: Set the name of the component
        :param gas_type: (Gas) type of gas from gas carrier and its share in
                         vol %
        :parma maximum_temperature: Temperature (in °C) of the heat output
        :parma minimum_temperature: Lowest possible temperature (in °C) of the inlet.
        :param nominal_power: Nominal heat output capacity (in Watts).
        :param input_pressure: Input pressure of gas or gases (in bar).
        :param thermal_efficiency: Thermal conversion efficiency (LHV).

        """
        super().__init__(name=name)

        self.gas_type = gas_type
        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature
        self.nominal_power = nominal_power
        self.input_pressure = input_pressure
        self.thermal_efficiency = thermal_efficiency

    def build_core(self):
        """Build core structure of oemof.solph representation."""

        gas_carrier = self.location.get_carrier(GasCarrier)
        _, pressure_level = gas_carrier.get_surrounding_levels(
            self.gas_type, self.input_pressure
        )
        gas_bus = gas_carrier.inputs[self.gas_type][pressure_level]

        # convert gas in kg to heat in Wh with thermal efficiency conversion
        heat_output = self.thermal_efficiency * self.gas_type.LHV

        heat_carrier = self.location.get_carrier(HeatCarrier)

        heat_bus_warm, heat_bus_cold, ratio = heat_carrier.get_connection_heat_transfer(
            self.maximum_temperature, self.minimum_temperature
        )

        temp_level, _ = heat_carrier.get_surrounding_levels(self.maximum_temperature)

        if np.isinf(temp_level):
            raise ValueError("No suitable temperature level available")

        if self.maximum_temperature - temp_level > 15:
            LOGGER.info("higher than suitable temperature level")

        nominal_gas_consumption = self.nominal_power / (
            self.thermal_efficiency * self.gas_type.LHV
        )

        self.create_solph_node(
            label="converter",
            node_type=Converter,
            inputs={
                gas_bus: Flow(nominal_value=nominal_gas_consumption),
                heat_bus_cold: Flow(),
            },
            outputs={
                heat_bus_warm: Flow(),
            },
            conversion_factors={
                gas_bus: (1 - ratio) * heat_output,
                heat_bus_cold: ratio,
                heat_bus_warm: 1,
            },
        )
