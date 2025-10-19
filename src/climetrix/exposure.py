"""Exposure (capital stock) data utilities."""
from __future__ import annotations

import logging
from typing import Iterable, List

import ee

from .config import SectoralExposureConfig

LOGGER = logging.getLogger(__name__)


TRANSFORMATIONS = {
    "log": lambda img: img.log(),
    "sqrt": lambda img: img.sqrt(),
    "identity": lambda img: img,
}


def load_sector_exposure(config: SectoralExposureConfig, region: ee.FeatureCollection) -> ee.Image:
    """Load sectoral exposure data from Earth Engine."""

    LOGGER.info("Loading sectoral exposure %s", config.sector_id)
    image = ee.ImageCollection(config.collection)
    if config.filters:
        for filter_type, params in config.filters.items():
            LOGGER.debug("Applying %s filter with params %s", filter_type, params)
            if filter_type == "date_range":
                image = image.filterDate(params["start"], params["end"])
            else:
                raise ValueError(f"Unsupported filter type for exposure: {filter_type}")

    image = image.select(config.band).first()
    transformation = TRANSFORMATIONS.get(config.transformation)
    if not transformation:
        raise ValueError(f"Unsupported transformation: {config.transformation}")
    image = transformation(image)

    image = (
        image.resample("bilinear")
        .reproject(crs="EPSG:4326", scale=config.scale_m)
        .clip(region)
        .set("sector_id", config.sector_id)
    )
    return image


def load_exposure_stack(
    exposure_configs: Iterable[SectoralExposureConfig],
    region: ee.FeatureCollection,
) -> List[ee.Image]:
    """Load exposure images for all configured sectors."""

    return [load_sector_exposure(config, region) for config in exposure_configs]
