"""Workflow-level configuration for Climetrix."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .hazard import HazardLayerConfig, HazardWeighting
from .exposure import SectoralExposureConfig


@dataclass
class WorkflowConfig:
    """Top-level configuration describing the multi-hazard workflow."""

    region_asset_id: str
    hazards: List[HazardLayerConfig]
    hazard_weights: List[HazardWeighting]
    exposures: List[SectoralExposureConfig]
    output_scale_deg: float = 0.1
    temporal_resolution: str = "annual"
    metadata: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict) -> "WorkflowConfig":
        hazards = [HazardLayerConfig(**item) for item in payload["hazards"]]
        weights = [HazardWeighting(**item) for item in payload["hazard_weights"]]
        exposures = [SectoralExposureConfig(**item) for item in payload["exposures"]]
        return cls(
            region_asset_id=payload["region_asset_id"],
            hazards=hazards,
            hazard_weights=weights,
            exposures=exposures,
            output_scale_deg=payload.get("output_scale_deg", 0.1),
            temporal_resolution=payload.get("temporal_resolution", "annual"),
            metadata=payload.get("metadata", {}),
        )
