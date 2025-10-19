"""High-level workflow orchestrating the Climetrix pipeline."""
from __future__ import annotations

import logging
from typing import Dict

import ee

from . import exposure, gee, hazard, risk, vulnerability
from .config import WorkflowConfig

LOGGER = logging.getLogger(__name__)


def run_pipeline(config: WorkflowConfig) -> Dict[str, ee.Image]:
    """Execute the configured workflow and return intermediate outputs."""

    LOGGER.info("Starting Climetrix pipeline")
    gee.initialize()
    region = gee.get_region(config.region_asset_id)

    hazard_layers = hazard.load_hazard_stack(config.hazards, region)
    exposure_layers = exposure.load_exposure_stack(config.exposures, region)

    hazard_index = vulnerability.aggregate_multi_hazard(
        hazard_layers, config.hazard_weights
    )
    hazard_index = gee.mosaic_and_scale(
        [hazard_index], config.output_scale_deg, ee.Reducer.mean()
    )

    vulnerability_index = vulnerability.compute_vulnerability_index(
        hazard_index, exposure_layers
    )
    vulnerability_index = gee.mosaic_and_scale(
        [vulnerability_index], config.output_scale_deg, ee.Reducer.mean()
    )

    risk_surface = risk.compute_spatiotemporal_risk(
        vulnerability_index, config.temporal_resolution
    )
    risk_surface = gee.mosaic_and_scale(
        [risk_surface], config.output_scale_deg, ee.Reducer.mean()
    )

    outputs = {
        "hazard_layers": hazard_layers,
        "hazard_index": hazard_index,
        "vulnerability_index": vulnerability_index,
        "risk_surface": risk_surface,
    }

    LOGGER.info("Climetrix pipeline completed successfully")
    return outputs
