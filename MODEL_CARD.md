# Model card: UAP Observation Model

## Snapshot and method

Version `model-0c4d4482fbe14409a8c24e46139da5a8`, model ID `0c4d4482fbe14409a8c24e46139da5a8`. Prepared 2026-10-30T18:56:31.305712+00:00. 337 manually labeled native crops, 336 usable templates, 19 source videos. Labels: `{"airplane": 1, "anomalous": 50, "bird": 51, "cloud": 235}`.

The saved artifact is a bank of native grayscale appearance templates plus label metadata. OpenCV normalized cross-correlation searches scales 0.65, 0.8, 1.0, 1.25, and 1.6; overlap suppression uses 0.35 intersection-over-smaller-box area. Default matching threshold is 0.97. Uniform templates with standard deviation below 2 are skipped. Native positive matches also require agreement of background-subtracted fine structure: Gaussian sigma 1.2, correlation at least 0.55. This rejects smooth cloud gradients that can have a high raw correlation. Cloud examples may still compete as background negatives. At most eight candidate peaks per template and scale are considered. The runner preserves this station inference algorithm.

## Data and provenance

Only completed, non-omitted reviews of credited credited source videos were eligible. Sources are listed in `sources.json`; crop time positions, labels, and normalized source bounds are in `annotations.json`. Native exemplars are copied without smoothing or enlargement. No full source videos, RF logs, local network addresses, or credentials are included. Only saved model snapshots are exported; full source videos and station logs are excluded. Dataset fingerprint: `19db8b21dfa00e0e64293945b4c2df909e3a7b4e33882ddebf2e900c7c8352e0`.

## Evaluation

Independent held-out precision, recall, false-positive rate, and camera-transfer accuracy have not been measured. Tests verify portable inference parity with the source algorithm and template integrity; these are software checks, not real-world performance benchmarks. Same-source re-identification is not evidence of generalization. Review targets may share the same physical object or recording, so crop count is not a count of independent encounters.

## Intended use and limitations

Exploratory re-identification and reproducible experiments on visually similar footage. Appearance is sensitive to viewpoint, object scale, background, sensor modality, contrast, compression, and occlusion. Correlation can match overlays, reticles, sensor artifacts, or conventional objects. Multiple objects can be returned; this runner does not establish persistent identity through crossings or occlusion. A single positive-only class provides no calibrated discrimination against birds, aircraft, or clouds. The model carries human labels and makes no determination about physical identity or origin.

## Reproducibility

Use `python -m unittest -v test_inference` after installing requirements. `SHA256SUMS` records release file hashes. Tested with the software versions in `verification.json`. A standalone CPU runner requires no station services, Mac worker, GPU, or private filesystem layout.

## Attribution

Apache 2.0 applies to the project's original code, annotations, and compilation. Source media retain their separate status and terms described by official source pages. See LICENSE, NOTICE, and sources.json. Third-party software is installed separately and retains its own licenses.
