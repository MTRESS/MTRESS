"""This module provides hydrogen electrolyser."""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np
from oemof import solph
from oemof.solph import Flow
from oemof.solph.components import Converter, OffsetConverter

from .._abstract_component import AbstractSolphRepresentation
from .._helpers._util import enable_templating
from ..carriers import Electricity, GasCarrier, HeatCarrier
from ..physics import HYDROGEN
from ._abstract_technology import AbstractTechnology

LOGGER = logging.getLogger(__file__)


@dataclass(frozen=True)
class ElectrolyserTemplate:
    """
    Here we define the template for different electrolyser technologies
    (PEM, AEL, AEM) with their specific parameter values.
    Users can modify the parameter values (e.g. hydrogen production
    efficiency, thermal efficiency, etc.) for a particular technology
    type if needed or can create user-defined electrolyser technology.

    Important references on technologies:
    1. https://en.wikipedia.org/wiki/Polymer_electrolyte_membrane_electrolysis
    2. https://www.h-tec.com/produkte/detail/h-tec-pem-elektrolyseur-me450/me450/
    3. "Assessment of the Future Waste Heat Potential from Electrolysers and its
    Utilisation in District Heating" by Stefan REUTER, Ralf-Roman SCHMIDT
    4. "A study on the potential of excess heat from medium­ to large­scale PEM
    electrolysis and the performance analysis of a dedicated cooling system"
    by W.J. Tiktak
    5. https://handbook.enapter.com/electrolyser/aem-flex120
    6. https://www.cummins.com/sites/default/files/2021-08/cummins-hystat-30-specsheet.pdf
    7. https://cellar-c2.services.clever-cloud.com/com-mcphy/uploads/2023/06/2023_McLyzer-Product-Line-EN.pdf
    8. https://nelhydrogen.com/product/atmospheric-alkaline-electrolyser-a-series/
    9. https://mart.cummins.com/imagelibrary/data/assetfiles/0070331.pdf
    10. https://hydrogen.johncockerill.com/en/products/electrolysers/

    """

    max_load_hydrogen_efficiency: float
    min_load_hydrogen_efficiency: float
    max_load_thermal_efficiency: float
    min_load_thermal_efficiency: float
    minimum_load: float
    maximum_temperature: float
    minimum_temperature: float
    hydrogen_output_pressure: float


#  Efficiency for each of the technology are based on Lower Heating Value (LHV).
#  The efficiency (hydrogen and thermal) assumed here are based on the Beginning
#  of Life (BoL). In Practice, both the efficiency values of electrolyser changes
#  as it gets older.

PEM_ELECTROLYSER = ElectrolyserTemplate(
    max_load_hydrogen_efficiency=0.63,
    min_load_hydrogen_efficiency=0.70,
    max_load_thermal_efficiency=0.25,
    min_load_thermal_efficiency=0.20,
    minimum_load=0.15,
    maximum_temperature=57,
    minimum_temperature=20,
    hydrogen_output_pressure=30,
)

ALKALINE_ELECTROLYSER = ElectrolyserTemplate(
    max_load_hydrogen_efficiency=0.66,
    min_load_hydrogen_efficiency=0.71,
    max_load_thermal_efficiency=0.20,
    min_load_thermal_efficiency=0.15,
    minimum_load=0.25,
    maximum_temperature=65,
    minimum_temperature=20,
    hydrogen_output_pressure=30,
)

AEM_ELECTROLYSER = ElectrolyserTemplate(
    max_load_hydrogen_efficiency=0.625,
    min_load_hydrogen_efficiency=0.71,
    max_load_thermal_efficiency=0.29,
    min_load_thermal_efficiency=0.20,
    minimum_load=0.30,
    maximum_temperature=50,
    minimum_temperature=20,
    hydrogen_output_pressure=35,
)


class Electrolyser(AbstractTechnology, AbstractSolphRepresentation):
    """
    Electrolyser split water into hydrogen and oxygen with the electricity as input
    source of energy. Hydrogen can be used as an energy carrier for various applications.
    Excess heat from low-temperature electrolyser (PEM, Alk, AEM) can also be utilised for
    space heating and hot water in: offices, commercial building, residential applications,
    either directly or via a district heating network. Heat requirement for Anaerobic Digestion
    (AD) Plant or some industrial processes can also be provided via Electrolysers. Waste heat
    utilisation can increase the system efficiency of up to 91 %. Oxygen produced in the
    electrolysis process is not considered in MTRESS.

    There are various types of electrolyser : PEM, Alkaline, AEM, etc. The SOEC technology is
    not yet considered in MTRESS. This class module takes PEM electrolyser as default technology,
    but user can select different technology type or can also user-defined their own technology
    as per the requirements.
    """

    @enable_templating(ElectrolyserTemplate)
    def __init__(
        self,
        name: str,
        nominal_power: float,
        max_load_hydrogen_efficiency: float,
        max_load_thermal_efficiency: float,
        maximum_temperature: float,
        minimum_temperature: float,
        hydrogen_output_pressure: float,
        min_load_hydrogen_efficiency: Optional[float] = None,
        min_load_thermal_efficiency: Optional[float] = None,
        minimum_load: Optional[float] = None,
        maximum_load: float = 1,
        offset: bool = False,
    ):
        """
        Initialize Electrolyser

        :param name: Name of the component
        :param nominal_power: Nominal electrical power (in W) of the component
        :param hydrogen_efficiency: Hydrogen production efficiency of the electrolyser,
            i.e., the ratio of hydrogen output and electrical input
        :param thermal_efficiency: Thermal efficiency of the electrolyser,
            i.e., ratio of thermal output and electrical input
        :param maximum_temperature: Maximum waste heat temperature level (in °C).
        :param minimum_temperature: Minimum return temperature level (in °C)
        :param hydrogen_output_pressure: Hydrogen output pressure (in bar)
        """
        super().__init__(name=name)

        self.nominal_power = nominal_power
        self.max_load_hydrogen_efficiency = max_load_hydrogen_efficiency
        self.max_load_thermal_efficiency = max_load_thermal_efficiency
        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature
        self.hydrogen_output_pressure = hydrogen_output_pressure
        self.min_load_hydrogen_efficiency = min_load_hydrogen_efficiency
        self.min_load_thermal_efficiency = min_load_thermal_efficiency
        self.minimum_load = minimum_load
        self.maximum_load = maximum_load
        self.offset = offset

    def build_core(self):
        """Build core structure of oemof.solph representation."""
        # Electrical connection
        electricity_carrier = self.location.get_carrier(Electricity)
        electrical_bus = electricity_carrier.distribution

        # Hydrogen connection
        gas_carrier = self.location.get_carrier(GasCarrier)

        pressure, _ = gas_carrier.get_surrounding_levels(
            HYDROGEN, self.hydrogen_output_pressure
        )

        h2_bus = gas_carrier.inputs[HYDROGEN][pressure]

        # H2 output in kg at max load
        max_load_h2_output = self.max_load_hydrogen_efficiency / HYDROGEN.LHV

        # H2 output in kg at min load
        min_load_h2_output = self.min_load_hydrogen_efficiency / HYDROGEN.LHV

        # Heat connection
        heat_carrier = self.location.get_carrier(HeatCarrier)
        heat_bus_warm, heat_bus_cold, ratio = heat_carrier.get_connection_heat_transfer(
            self.maximum_temperature,
            self.minimum_temperature,
        )

        # If offset is not desired
        if self.offset is False:
            self.create_solph_node(
                label="converter",
                node_type=Converter,
                inputs={
                    electrical_bus: Flow(nominal_value=self.nominal_power),
                    heat_bus_cold: Flow(),
                },
                outputs={
                    h2_bus: Flow(),
                    heat_bus_warm: Flow(),
                },
                conversion_factors={
                    electrical_bus: 1,
                    heat_bus_cold: self.max_load_thermal_efficiency
                    * ratio
                    / (1 - ratio),
                    h2_bus: max_load_h2_output,
                    heat_bus_warm: self.max_load_thermal_efficiency / (1 - ratio),
                },
            )
        else:
            slope_h2, offset_h2 = solph.components.slope_offset_from_nonconvex_input(
                self.maximum_load,
                self.minimum_load,
                max_load_h2_output,
                min_load_h2_output,
            )

            slope_th, offset_th = solph.components.slope_offset_from_nonconvex_input(
                self.maximum_load,
                self.minimum_load,
                self.max_load_thermal_efficiency,
                self.min_load_thermal_efficiency,
            )

            self.create_solph_node(
                label="Offset_conv",
                node_type=OffsetConverter,
                inputs={
                    electrical_bus: Flow(
                        nominal_value=self.nominal_power,
                        max=self.maximum_load,
                        min=self.minimum_load,
                        nonconvex=solph.NonConvex(),
                    ),
                },
                outputs={h2_bus: Flow(), heat_bus_warm: Flow()},
                conversion_factors={
                    h2_bus: slope_h2,
                    heat_bus_warm: slope_th,
                    heat_bus_cold: slope_th,
                },
                normed_offsets={
                    h2_bus: offset_h2,
                    heat_bus_warm: offset_th,
                },
            )
