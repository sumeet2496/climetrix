"""Utilities for interacting with Google Earth Engine (GEE)."""
from __future__ import annotations

import logging
from typing import Iterable, Optional

try:
    import ee
except ImportError as exc:  # pragma: no cover - runtime dependency
    raise RuntimeError(
        "The google-earth-engine package is required to use Climetrix."
    ) from exc

LOGGER = logging.getLogger(__name__)


def initialize(credentials: Optional[str] = None) -> None:
    """Initialise the Earth Engine API.

    Parameters
    ----------
    credentials:
        Optional path to a service account JSON file. If omitted, the user
        authentication flow (token-based) is triggered.
    """

    if getattr(ee.data, "_credentials", None) is not None:
        LOGGER.debug("Earth Engine already initialised; skipping re-authentication.")
        return

    if credentials:
        LOGGER.info("Authenticating to Earth Engine using service account credentials.")
        ee.Initialize(credentials=credentials)
    else:
        LOGGER.info("Authenticating to Earth Engine using interactive credentials.")
        ee.Initialize()


def get_region(asset_id: str) -> "ee.FeatureCollection":
    """Fetch the study region geometry from an Earth Engine asset."""

    LOGGER.debug("Loading region asset %s", asset_id)
    return ee.FeatureCollection(asset_id)


def mosaic_and_scale(
    images: Iterable["ee.Image"], scale_deg: float, reducer: "ee.Reducer"
) -> "ee.Image":
    """Merge and resample images to the desired spatial resolution."""

    image_collection = ee.ImageCollection(images)
    mosaic = image_collection.mosaic()
    LOGGER.debug("Applying reducer %s at %.2f° scale", reducer, scale_deg)
    return (
        mosaic.reduceResolution(reducer=reducer, maxPixels=1024)
        .reproject(crs="EPSG:4326", scale=scale_deg * 111_320)
        .focal_mean(radius=scale_deg, units="degrees")
    )
