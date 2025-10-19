"""Hazard data ingestion utilities."""
from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Dict, Iterable, List

import ee

from .config import HazardLayerConfig

LOGGER = logging.getLogger(__name__)


HAZARD_REDUCERS: Dict[str, ee.Reducer] = {
    "mean": ee.Reducer.mean(),
    "max": ee.Reducer.max(),
    "sum": ee.Reducer.sum(),
    "median": ee.Reducer.median(),
}


def _apply_filters(collection: ee.ImageCollection, filters: Dict[str, Dict]) -> ee.ImageCollection:
    for filter_type, params in filters.items():
        LOGGER.debug("Applying filter %s with params %s", filter_type, params)
        if filter_type == "date_range":
            collection = collection.filterDate(params["start"], params["end"])
        elif filter_type == "bounds":
            collection = collection.filterBounds(params["geometry"])
        elif filter_type == "metadata":
            collection = collection.filterMetadata(
                params["field"], params.get("operator", "equals"), params["value"]
            )
        else:
            raise ValueError(f"Unsupported filter type: {filter_type}")
    return collection


def load_hazard_layer(config: HazardLayerConfig, region: ee.FeatureCollection) -> ee.Image:
    """Load and preprocess a hazard layer according to the configuration."""

    LOGGER.info("Loading hazard layer %s", config.hazard_id)
    collection = ee.ImageCollection(config.collection)

    if config.filters:
        collection = _apply_filters(collection, config.filters)

    collection = collection.select(config.bands)

    reducer = HAZARD_REDUCERS.get(config.reducer)
    if not reducer:
        raise ValueError(f"Reducer {config.reducer} is not supported.")

    if config.temporal_aggregation:
        LOGGER.debug(
            "Applying temporal aggregation %s for hazard %s",
            config.temporal_aggregation,
            config.hazard_id,
        )
        if config.temporal_aggregation == "annual":
            image = collection.reduce(ee.Reducer.mean())
        elif config.temporal_aggregation == "seasonal":
            image = collection.reduce(ee.Reducer.median())
        else:
            raise ValueError(f"Unsupported temporal aggregation: {config.temporal_aggregation}")
    else:
        image = collection.reduce(reducer)

    if config.smoothing_radius_km:
        LOGGER.debug(
            "Applying smoothing radius %.1f km for hazard %s",
            config.smoothing_radius_km,
            config.hazard_id,
        )
        image = image.focal_mean(radius=config.smoothing_radius_km * 1000, units="meters")

    if config.classification_thresholds:
        for label, threshold in config.classification_thresholds.items():
            LOGGER.debug(
                "Generating classification band '%s' at threshold %.3f for %s",
                label,
                threshold,
                config.hazard_id,
            )
            class_band = image.gt(threshold).rename(f"{config.hazard_id}_{label}")
            image = image.addBands(class_band)

    image = image.clip(region)
    LOGGER.debug("Final hazard image metadata: %s", asdict(config))
    return image.set("hazard_id", config.hazard_id)


def load_hazard_stack(
    hazard_configs: Iterable[HazardLayerConfig],
    region: ee.FeatureCollection,
) -> List[ee.Image]:
    """Load hazard images for all configured hazards."""

    return [load_hazard_layer(config, region) for config in hazard_configs]
