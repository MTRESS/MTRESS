from mtress.physics import COPReference
from mtress.technologies import HeatPump


def test_heat_pump_initialisation():
    hp_name = "test_hp"
    hp_thermal_power_limit = 5e3  # W
    hp_ref_cop = COPReference(4.6)

    hp = HeatPump(
        name=hp_name,
        thermal_power_limit=hp_thermal_power_limit,
        ref_cop=hp_ref_cop,
    )

    assert hp.name == hp_name
    assert hp.thermal_power_limit == hp_thermal_power_limit
    assert hp.ref_cop == hp_ref_cop


def test_heat_pump_init_custom_design_conditions():
    hp_name = "test_hp"
    hp_thermal_power_limit = 4e3  # W
    hp_ref_cop = COPReference(3.6, 5, -10, 40, 25)

    hp = HeatPump(
        name=hp_name,
        thermal_power_limit=hp_thermal_power_limit,
        ref_cop=hp_ref_cop,
    )

    assert hp.name == hp_name
    assert hp.thermal_power_limit == hp_thermal_power_limit
    assert hp.ref_cop == hp_ref_cop
