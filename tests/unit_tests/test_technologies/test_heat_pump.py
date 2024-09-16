from src.mtress.technologies import HeatPump

def test_heat_pump_initialisation():
    hp_name = "test_hp"
    hp_thermal_power_limit = 5e3  # W
    hp_ref_cop = 4.6

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
    hp_ref_cop = 3.6

    hp = HeatPump(
        name=hp_name,
        thermal_power_limit=hp_thermal_power_limit,
        ref_cop=hp_ref_cop,
        ref_temp_secondary_out=40,
        ref_temp_secondary_in=25,
        ref_temp_primary_in=5,
        ref_temp_primary_out=-10

    )

    assert hp.name == hp_name
    assert hp.thermal_power_limit == hp_thermal_power_limit
    assert hp.ref_cop == hp_ref_cop
