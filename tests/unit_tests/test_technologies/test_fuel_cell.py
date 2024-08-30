from mtress.technologies import AFC, PEMFC, FuelCell


def test_fuelcell():
    fc_name = ("PEMFC",)
    fc_nominal_power = (100e3,)

    # PEMFC
    fuelcell = FuelCell(
        name=fc_name,
        nominal_power=fc_nominal_power,
        template=PEMFC,
    )

    # Alkaline Fuel Cell (AFC)
    fuelcell_2 = FuelCell(
        name=fc_name,
        nominal_power=fc_nominal_power,
        template=AFC,
    )

    assert fuelcell.name == fc_name
    assert fuelcell.nominal_power == fc_nominal_power
    assert (
        fuelcell.full_load_electrical_efficiency
        == PEMFC.full_load_electrical_efficiency
    )
    assert (
        fuelcell.full_load_thermal_efficiency
        == PEMFC.full_load_thermal_efficiency
    )
    assert fuelcell.maximum_temperature == PEMFC.maximum_temperature
    assert fuelcell.gas_input_pressure == PEMFC.gas_input_pressure == 80
    assert fuelcell_2.gas_input_pressure == AFC.gas_input_pressure == 60
