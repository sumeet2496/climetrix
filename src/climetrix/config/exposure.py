"""Sectoral exposure configuration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class SectoralExposureConfig:
    """Defines sectoral capital stock layers to overlay with hazards."""

    sector_id: str
    description: str
    collection: str
    band: str
    exposure_metric: str
    unit: str
    transformation: str = "identity"
    scale_m: int = 1000
    filters: Dict[str, Dict] | None = None
