"""Systemic risk and fragility modeling."""
from __future__ import annotations

import logging
from typing import Iterable

import ee

LOGGER = logging.getLogger(__name__)


def compute_spatiotemporal_risk(
    vulnerability: ee.Image,
    temporal_scale: str,
    shocks: Iterable[ee.Image] | None = None,
) -> ee.Image:
    """Derive spatio-temporal risk surfaces from vulnerability and hazard shocks."""

    LOGGER.info("Computing %s risk surface", temporal_scale)
    risk = vulnerability.rename("risk")
    if shocks:
        shock_list = list(shocks)
        LOGGER.debug("Integrating %d systemic shock layers", len(shock_list))
        shock_collection = ee.ImageCollection(shock_list)
        shock_index = shock_collection.reduce(ee.Reducer.mean())
        risk = risk.multiply(shock_index)
    return risk


def model_systemic_fragility(risk_surface: ee.Image, infrastructure_layer: ee.Image) -> ee.Image:
    """Model network/system fragility by combining risk with infrastructure topology."""

    LOGGER.info("Modeling systemic fragility")
    fragility = risk_surface.multiply(infrastructure_layer)
    return fragility.rename("systemic_fragility")
