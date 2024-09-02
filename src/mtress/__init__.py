# -*- coding: utf-8 -*-
"""
.. include:: ../README.md
"""

"""
SPDX-FileCopyrightText: Deutsches Zentrum für Luft und Raumfahrt
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

from ._abstract_component import SolphLabel
from ._location import Location
from ._meta_model import Connection, MetaModel
from ._solph_model import SolphModel

__version__ = "3.0.0a2"

__all__ = ["Connection", "Location", "MetaModel", "SolphLabel", "SolphModel"]
