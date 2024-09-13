# -*- coding: utf-8 -*-
"""
Tests for coefficient of performance calculations.
"""
import math
from src.mtress.physics._helper_functions import lorenz_cop
from src.mtress.physics._helper_functions import logarithmic_mean_temperature
from src.mtress.physics._helper_functions import calc_cop

class TestCOP:
    
    def test_theoretical_cop(self):
        
        # source: 10.18462/iir.gl.2018.1380
        
        # source: 40 to 15 ºC
        # sink: 60 to 90 ºC
        t_source_low = 15+273.15
        t_source_high = 40+273.15
        t_sink_low = 60+273.15
        t_sink_high = 90+273.15
        
        cop_carnot_true = 4.84
        cop_lorenz_true = 7.33
        
        # test carnot cop
        cop_carnot = t_sink_high/(t_sink_high-t_source_low)
        assert math.isclose(cop_carnot, cop_carnot_true, abs_tol=3e-3)
        
        # test lorenz cop
        lmt_low = logarithmic_mean_temperature(temp_high=t_source_high, temp_low=t_source_low)
        lmt_high = logarithmic_mean_temperature(temp_high=t_sink_high, temp_low=t_sink_low)
        cop_lorenz = lorenz_cop(temp_high=lmt_high, temp_low=lmt_low)
        assert math.isclose(cop_lorenz, cop_lorenz_true, abs_tol=2e-3)
        
        
        # bulk test
        test_data = [
            (43, 15, 50, 90, 4.84, 8.40),
            (43, 15, 50, 80, 5.43, 9.39),
            (43, 15, 50, 70, 6.24, 10.70),
            (5, 3, 50, 90, 4.17, 5.22),
            (20, 10, 50, 70, 5.72, 7.41),
            (28, 4, 7, 90, 4.22, 10.36),
            (40, 15, 42, 46, 10.30, 19.03),
            (18, 6, 37, 67, 5.58, 8.16),
            (14, 3, 43, 75, 4.84, 6.60),
            (18, 3, 43, 75, 4.84, 6.87),
            (9, 2, 35, 90, 4.13, 5.95),
            (9, 2, 35, 75, 4.77, 6.67),
            (5, 2, 30, 70, 5.05, 7.00),
            (17, 13, 35, 75, 5.62, 8.28),
            (12, 7, 30, 35, 11.01, 13.29),
            (20, 4, 20, 65, 5.54, 10.49),
            ]
        
        for tsoh, tsol, tsil, tsih, cop_carnot_true, cop_lorenz_true in test_data:
            
            # convert to kelvin
            t_source_low = tsol+273.15
            t_source_high = tsoh+273.15
            t_sink_low = tsil+273.15
            t_sink_high = tsih+273.15
            
            # test carnot cop
            cop_carnot = t_sink_high/(t_sink_high-t_source_low)
            assert math.isclose(cop_carnot, cop_carnot_true, abs_tol=5e-3)
            
            # test lorenz cop
            lmt_low = logarithmic_mean_temperature(temp_high=t_source_high, temp_low=t_source_low)
            lmt_high = logarithmic_mean_temperature(temp_high=t_sink_high, temp_low=t_sink_low)
            cop_lorenz = lorenz_cop(temp_high=lmt_high, temp_low=lmt_low)
            assert math.isclose(cop_lorenz, cop_lorenz_true, abs_tol=5e-3)
            
        
    # TODO: test the near zero value
    
    # TODO: test negative temperatures in Kelvin
        
    def test_theoretical_cop_pinch(self):
        
        # source: 10.18462/iir.gl.2018.1380
        
        pass
        test_data = [
            (43, 15, 50, 90, 4.52, 7.38),
            (43, 15, 50, 80, 5.02, 8.12),
            (43, 15, 50, 70, 5.67, 9.05),
            (5, 3, 50, 90, 3.94, 4.83),
            (20, 10, 50, 70, 5.24, 6.60),
            (28, 4, 7, 90, 3.98, 8.75),
            (40, 15, 42, 46, 8.71, 14.12),
            (18, 6, 37, 67, 5.12, 7.16),
            (14, 3, 43, 75, 4.50, 5.95),
            (18, 3, 43, 75, 4.50, 6.17),
            (9, 2, 35, 90, 3.90, 5.43),
            (9, 2, 35, 75, 4.44, 6.00),
            (5, 2, 30, 70, 4.68, 6.25),
            (17, 13, 35, 75, 5.16, 7.25),
            (12, 7, 30, 35, 9.15, 10.64),
            (20, 4, 20, 65, 5.09, 8.83),
            (30, 25, 40, 80, 5.84, 8.81)
            ]
        
        dt_pinch_source = 3
        dt_pinch_sink = 3
        
        for tsoh, tsol, tsil, tsih, cop_carnot_true, cop_lorenz_true in test_data:
            
            # convert to kelvin
            t_source_low = tsol+273.15-dt_pinch_source
            t_source_high = tsoh+273.15-dt_pinch_source
            t_sink_low = tsil+273.15+dt_pinch_sink
            t_sink_high = tsih+273.15+dt_pinch_sink
            
            # test carnot cop
            cop_carnot = t_sink_high/(t_sink_high-t_source_low)
            assert math.isclose(cop_carnot, cop_carnot_true, abs_tol=5e-3)
            
            # test lorenz cop
            lmt_low = logarithmic_mean_temperature(temp_high=t_source_high, temp_low=t_source_low)
            lmt_high = logarithmic_mean_temperature(temp_high=t_sink_high, temp_low=t_sink_low)
            cop_lorenz = lorenz_cop(temp_high=lmt_high, temp_low=lmt_low)
            assert math.isclose(cop_lorenz, cop_lorenz_true, abs_tol=5e-3)
            
            
    def test_different_cop_conditions(self):
        
        # TODO: find published/peer-reviewed source
        
        # source: 40 to 15 ºC
        # sink: 60 to 90 ºC
        t_source_low = 15
        t_source_high = 40
        t_sink_low = 60
        t_sink_high = 90
        cop = 5
        
        # test same cop
        new_cop = calc_cop(
            temp_primary_in=t_source_low+273.15, 
            temp_secondary_out=t_sink_high+273.15,
            temp_primary_out=t_source_high+273.15,
            temp_secondary_in=t_sink_low+273.15,
            ref_cop=cop,
            ref_temp_sink_high=t_sink_high,
            ref_temp_sink_low=t_sink_low,
            ref_temp_source_high=t_source_high,
            ref_temp_source_low=t_source_low
            )
        assert math.isclose(new_cop, cop, abs_tol=1e-3)
        
        # test higher lift
        additional_lift = 10
        new_cop = calc_cop(
            temp_primary_in=t_source_low+273.15, 
            temp_secondary_out=t_sink_high+273.15+additional_lift,
            temp_primary_out=t_source_high+273.15,
            temp_secondary_in=t_sink_low+273.15,
            ref_cop=cop,
            ref_temp_sink_high=t_sink_high,
            ref_temp_sink_low=t_sink_low,
            ref_temp_source_high=t_source_high,
            ref_temp_source_low=t_source_low
            )
        true_cop = 4.6
        assert math.isclose(new_cop, true_cop, abs_tol=1e-3)
        
        # test lower lift
        additional_lift =- 10
        new_cop = calc_cop(
            temp_primary_in=t_source_low+273.15, 
            temp_secondary_out=t_sink_high+273.15+additional_lift,
            temp_primary_out=t_source_high+273.15,
            temp_secondary_in=t_sink_low+273.15,
            ref_cop=cop,
            ref_temp_sink_high=t_sink_high,
            ref_temp_sink_low=t_sink_low,
            ref_temp_source_high=t_source_high,
            ref_temp_source_low=t_source_low
            )
        true_cop = 5.495
        assert math.isclose(new_cop, true_cop, abs_tol=1e-3)