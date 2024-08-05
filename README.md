# Model Template for Renewable Energy Supply Systems (MTRESS)

## Introduction
The DLR Institute of Networked Energy Systems has developed the MTRESS tool that can be 
used to optimise energy supply systems for new and existing projects at any location. 
MTRESS facilitates the creation of energy system optimisation models for individual 
residential and commercial buildings, as well as for neighbourhoods and entire industrial
properties.  It enables users to include a wide range of influencing factors and energy
options in the simulation and minimises the planning effort.

This is a generic model for community-based open source [oemof.solph](https://github.com/oemof/oemof-solph/) tool.
MTRESS offers a variety of possible technology combinations for energy supply systems.
It includes pre-built technologies that are commonly considered in energy systems, such as:
 - Photovoltaic (PV) and/or Renewable Energy Source (with generation time series)
 - Heat Pumps
 - Heat Exchangers
 - Electrolysers (PEM, Alkaline, AEM)
 - Fuel Cells (PEM, Alkaline, AEM)
 - Compressors
 - Combined Heat and Power (CHP) with various gas types inputs
 - Storages (Battery, Heat Storage, Gas Storage (Hydrogen))
 - Resistive Heater and Gas Boiler

It covers different sectors including Electricity, Heat and Gas (e.g., H2, Natural Gas,
Biogas, etc.). It is tailored for optimising control strategies fulfilling fixed 
demand time series for electricity, heat, gas (including hydrogen), and domestic hot 
water using any selected combination of the implemented supply technologies.

MTRESS requires appropriately prepared initial data on the boundary conditions of the 
respective project. A wide range of data sources can be used, including 
historical energy consumption data for the project, but also higher-level data 
on the location, for example from climate models or the solar cadastre. Moreover, the
forecasted demands and renewable generations could also be used for scheduling optimized
operation for next days. 
It could be used for long-term planning and the assumptions about the development of 
costs and the CO2 impact of the future energy mix can also be incorporated into the 
modelling.

As an open-source model, MTRESS is available to users in a wide range of areas. It can
be utilized for both research and commercial purposes. Researchers, utility owners, and
policymakers can all benefit from this tool for energy system planning and operation. 
Applications are not just limited to municipal heating plans, home automation offerings,
hydrogen infrastructure planning, and optimized operation of sector-coupled energy 
systems, but extend to any scenario requiring comprehensive energy optimization and 
management.

## Installation

MTRESS depends on solph, which is automatically installed using pip
```bash 
pip install mtress
``` 
However, pip will not install a solver,
to perform the actual optimisation. Please refer to the
[documentation of solph](https://oemof-solph.readthedocs.io/en/v0.4.4/readme.html#installing-a-solver)
to learn how to install a solver.

Install all the other dependencies:
```bash 
pip install -r requirements.txt
``` 

## Documentation

The auto-generated documentation can be found on the [GitLab pages](https://mtress-ecosystem.pages.gitlab.dlr.de/mtress).

## Usage and Tutorials
Please refer to the examples folder in this repository to get acquainted with building 
and optimizing energy systems in MTRESS. These examples will help you understand the 
basics and guide you through the process before you start creating your own energy system. 

Please feel free to contact us if you have any questions or need further assistance. 
Contact information can be found below. 

## Acknowledgements
The development of Version 2 was funded by the Federal Ministry for Economic Affairs and Energy (BMWi)
and the Federal Ministry of Education and Research (BMBF) of Germany
in the project [ENaQ](https://www.enaq-fliegerhorst.de/) (project number 03SBE111).
The development of the heat sector formulations in Version 3 was funded by the Federal Ministry of
Education and Research (BMBF) of Germany in the project [Wärmewende Nordwest](https://www.waermewende-nordwest.de/) (project number 03SF0624).
The development of the gas sector formulations in Version 3 was funded by the Federal 
Ministry of Education and Research (BMBF) of Germany in the project [H2Giga-Systogen100](https://www.region-heide.de/projekte/systogen100.html)  (project number 03HY115E).

## Contributing

You are welcome to contribute to MTRESS. We use [Black code style](https://black.readthedocs.io/),
and put our code under [MIT license](LICENSE). When contributing, you need to do the same.
For smaller changes, you can just open a merge request. If you plan something bigger,
please open an issue first, so that we can discuss beforehand and avoid double work. 
Also, please report bugs by opening an issue.

## Citation
If you use MTRESS Software for your research, please consider citation as follows:
```bash 
@misc{https://doi.org/10.5281/zenodo.11205762,
  doi = {10.5281/ZENODO.11205762},
  url = {https://zenodo.org/doi/10.5281/zenodo.11205762},
  author = {Schönfeldt, Patrik and Schlüters, Sunke and Upadhaya, Ajay and Oltmanns, Keno},
  title = {Model Template for Residential Energy Supply Systems (MTRESS)},
  publisher = {Zenodo},
  year = {2024},
  copyright = {MIT License}
}
``` 

## Reference
<a id="1">[1]</a>
Schönfeldt, Patrik and Schlüters, Sunke and Oltmanns, Keno,"MTRESS 3.0--Modell Template for Residential Energy Supply Systems",
arXiv preprint, 2022, [arXiv:2211.14080](https://arxiv.org/abs/2211.14080).

## Contact

The software development is administrated by [Patrik Schönfeldt](mailto:patrik.schoenfeldt@dlr.de),
for general questions please contact him. Individual authors may leave their contact information
in the [citation.cff](CITATION.cff).
