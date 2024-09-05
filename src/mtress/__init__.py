# -*- coding: utf-8 -*-
"""
.. include:: ../../README.md
"""

from ._abstract_component import SolphLabel
from ._location import Location
from ._meta_model import Connection, MetaModel
from ._solph_model import SolphModel

"""
SPDX-FileCopyrightText: Deutsches Zentrum für Luft und Raumfahrt
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

__version__ = "3.0.0a2"

__all__ = ["Connection", "Location", "MetaModel", "SolphLabel", "SolphModel"]
