# Climetrix Architecture

The Climetrix framework is organised into modular components that mirror the
standard disaster risk equation: **Risk = Hazard × Exposure × Vulnerability**.
Each module is implemented as a Python file under `src/climetrix/` and operates
on Google Earth Engine (GEE) `ee.Image` objects.

## Modules

### `gee.py`

Initialises the GEE client, loads study regions, and resamples imagery to the
standard 0.1° (~11 km) grid using configurable reducers.

### `hazard.py`

Loads hazard imagery using `HazardLayerConfig` definitions. Supported reducers
include mean, max, sum, and median. Optional temporal aggregation (annual or
seasonal) and spatial smoothing can be applied per hazard.

### `exposure.py`

Ingests sectoral capital stock layers (e.g., GDP density, infrastructure value).
Each exposure layer can undergo log, square-root, or identity transformation
before resampling and clipping to the region geometry.

### `vulnerability.py`

Normalises hazard layers, applies analyst-provided weights, and combines them
with exposure stacks through geometric or arithmetic aggregation. The resulting
`vulnerability_index` is dimensionless and ranges from 0–1.

### `risk.py`

Transforms vulnerability into a spatio-temporal risk surface. Optional systemic
shock rasters (e.g., ENSO anomalies, supply-chain disruption indicators) can be
incorporated. The module also provides systemic fragility modeling by merging
risk with infrastructure topology layers.

### `workflow.py`

Coordinates the end-to-end pipeline: initialises GEE, loads hazards and
exposures, computes vulnerability, derives risk, and returns intermediate
layers for export or further analysis.

## Configuration

Workflow settings are defined via JSON using dataclasses located in
`src/climetrix/config/`. Analysts specify hazard sources, weights, sectoral
exposures, temporal resolution, and metadata.

## Extensibility

- Integrate new hazards by extending `HazardLayerConfig` entries and optionally
  adding new reducers.
- Introduce socio-economic indicators as exposures with new transformations.
- Implement alternative normalization or aggregation strategies inside
  `vulnerability.py`.
- Add post-processing routines (e.g., percentile thresholds, clustering) by
  extending `workflow.run_pipeline`.
