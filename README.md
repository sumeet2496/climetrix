# Climetrix

Climetrix is a transdisciplinary climate risk exposure mapping framework. It
integrates 0.1° geospatial hazard footprints from Google Earth Engine (GEE) with
sectoral capital stock datasets to derive multi-hazard vulnerability indices,
spatio-temporal risk surfaces, and systemic climate fragility diagnostics.

## Features

- **Multi-hazard ingestion:** Configurable pipeline to access flood, cyclone,
  drought, heat, and other hazard layers hosted on GEE.
- **Sectoral exposure integration:** Overlay hazard intensity with sectoral
  capital stock proxies (GDP density, infrastructure assets, agricultural value).
- **Vulnerability modeling:** Normalize and weight hazards, combine with
  exposure layers via geometric or arithmetic aggregation, and produce
  standardized vulnerability indices.
- **Spatio-temporal risk analysis:** Generate annual or seasonal risk rasters and
  incorporate optional systemic shock layers.
- **Systemic fragility diagnostics:** Combine risk surfaces with network or
  infrastructure topology layers (e.g., power grids) to estimate cascading
  fragility.
- **Templated configuration:** JSON-based workflow definition ensures
  reproducible analyses and easy adaptation to new geographies.

## Repository layout

```
├── src/climetrix/
│   ├── cli.py                 # CLI entry point
│   ├── config/                # Dataclasses describing workflow configuration
│   ├── exposure.py            # Capital stock data ingestion
│   ├── gee.py                 # Earth Engine initialization and utilities
│   ├── hazard.py              # Hazard preprocessing and normalization
│   ├── risk.py                # Spatio-temporal risk & fragility modeling
│   ├── vulnerability.py       # Hazard weighting and vulnerability index
│   └── workflow.py            # High-level pipeline orchestration
├── templates/
│   └── sample_workflow.json   # Example workflow configuration
└── README.md
```

## Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. **Authenticate with Google Earth Engine**

   ```bash
   earthengine authenticate
   ```

3. **Prepare a workflow configuration**

   Copy the [`templates/sample_workflow.json`](templates/sample_workflow.json)
   file and update asset IDs, date filters, and sector definitions for your
   study area. The `output_scale_deg` parameter controls the 0.1° resampling
   scale of the resulting risk maps.

4. **Run the pipeline**

   ```bash
   python -m climetrix.cli path/to/workflow.json --log-level DEBUG
   ```

   The CLI logs the names of generated `ee.Image` layers. Use Earth Engine tasks
   or exports to persist the rasters to `Asset` or `Drive` destinations.

## Extending the framework

- Add new hazard sources by defining additional `HazardLayerConfig` entries in
  the workflow JSON. Custom reducers, smoothing kernels, or classification
  thresholds can be specified per hazard.
- Incorporate socio-economic or infrastructure datasets by adding
  `SectoralExposureConfig` entries. Apply log or square-root transformations to
  harmonize units and magnitude.
- Override aggregation strategies (e.g., hazard weighting scheme, vulnerability
  aggregation) by modifying `vulnerability.py`.
- Model additional systemic shocks (e.g., supply-chain disruptions) by passing
  extra `ee.Image` layers into `risk.compute_spatiotemporal_risk`.

## Disclaimer

This repository provides a scaffold for climate risk analysis. Analysts should
validate all datasets, ensure compliance with licensing, and evaluate model
assumptions before policy or investment decisions.
