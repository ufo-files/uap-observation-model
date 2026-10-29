# Model card: UAP Appearance Model

## Snapshot and method

Version `v0.1.0-preview`, model ID `e87a4acea5d149790eab57742cd8c10b`. Prepared 2026-10-29T00:44:26.647532+00:00. 440 manually labeled native crops, 437 usable templates, 67 source videos. Labels: `{"anomalous": 440}`.

The saved artifact is a bank of native grayscale appearance templates plus label metadata. OpenCV normalized cross-correlation searches scales 0.65, 0.8, 1.0, 1.25, and 1.6; overlap suppression uses 0.35 intersection-over-smaller-box area. Default matching threshold is 0.97. Uniform templates with standard deviation below 2 are skipped. At most eight candidate peaks per template and scale are considered. The runner preserves this station inference algorithm.

## Data and provenance

This initial snapshot contains completed, non-omitted reviews of credited public PURSUE videos. The training application also accepts other video sources; these provenance details describe this fixed snapshot. Sources are listed in `sources.json`; crop time positions, labels, and normalized source bounds are in `annotations.json`. Native exemplars are copied without smoothing or enlargement. No full source videos, private camera recordings, RF logs, local network addresses, or credentials are included. Dataset fingerprint: `e87a4acea5d149790eab57742cd8c10bff25781e47fad3e689868ff9b93519dc`.

## Evaluation

Independent held-out precision, recall, false-positive rate, and camera-transfer accuracy have not been measured. Tests verify portable inference parity with the source algorithm and template integrity; these are software checks, not real-world performance benchmarks. Same-source re-identification is not evidence of generalization. Review targets may share the same physical object or recording, so crop count is not a count of independent encounters.

## Intended use and limitations

Exploratory re-identification and reproducible experiments on visually similar footage. Appearance is sensitive to viewpoint, object scale, background, sensor modality, contrast, compression, and occlusion. Correlation can match overlays, reticles, sensor artifacts, or conventional objects. Multiple objects can be returned; this runner does not establish persistent identity through crossings or occlusion. A single positive-only class provides no calibrated discrimination against birds, aircraft, or clouds. The model carries human labels and makes no determination about physical identity or origin.

## Reproducibility

Use `python -m unittest -v test_inference` after installing requirements. `SHA256SUMS` records release file hashes. Tested with the software versions in `verification.json`. A standalone CPU runner requires no station services, Mac worker, GPU, or private filesystem layout.

## Attribution

Apache 2.0 applies to the project's original code, annotations, and compilation. Source media retain their separate status and terms described by official source pages. See LICENSE, NOTICE, and sources.json. Third-party software is installed separately and retains its own licenses.
