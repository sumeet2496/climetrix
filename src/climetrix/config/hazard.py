"""Hazard configuration schemas."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class HazardWeighting:
    """Weight assigned to a hazard for aggregation in multi-hazard indices."""

    hazard_id: str
    weight: float
    temporal_window: Optional[int] = None


@dataclass
class HazardLayerConfig:
    """Configuration describing how to source and preprocess hazard layers."""

    hazard_id: str
    description: str
    collection: str
    reducer: str
    scale_m: int
    bands: List[str] = field(default_factory=list)
    filters: Dict[str, Dict] = field(default_factory=dict)
    temporal_aggregation: Optional[str] = None
    smoothing_radius_km: Optional[float] = None
    classification_thresholds: Optional[Dict[str, float]] = None
