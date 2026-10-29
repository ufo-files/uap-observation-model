# UAP Appearance Model

An experimental, reusable appearance model built from manually reviewed video targets. The project supports source videos beyond PURSUE; the initial preview uses public PURSUE footage as its seed dataset. This release includes **440 labeled crops from 67 source videos**, source credits, annotations, and a portable Python/OpenCV runner.

## Use it

Requires Python 3.11+ and a CPU. Clone this repository or extract the release ZIP, then:

```bash
python -m venv .venv
# Linux/macOS; on Windows use .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python inference.py your-image.jpg --output detections.jsonl
python inference.py your-video.mp4 --threshold 0.97 --output detections.jsonl
```

Or use it from Python:

```python
import cv2
from inference import Matcher
model = Matcher()
objects = model.predict(cv2.imread("your-image.jpg"))
```

Each detection has a label, correlation score, and `[x, y, width, height]` box in native image pixels. Video output contains one JSON line per decoded frame, indexed from zero. The lightweight runner emits detections; recording, RF capture, event trimming, and cropped video export belong to the station application and are not bundled here.

## What is saved

`model.json` selects labeled native PNG templates in `templates/`. Inference searches five scales using normalized correlation and suppresses overlapping matches. Known-class examples compete with target examples when present. See [MODEL_CARD.md](MODEL_CARD.md) for coverage and limitations.

This is a template-based appearance model. No neural network weights or gradient-trained detector are claimed. The label `anomalous` records a human review choice. The model predicts a resemblance to those selections; it does not determine an object's identity or cause.

## New training videos and review history

The companion training app accepts arbitrary videos dropped into its `training-data` folder or uploaded through the browser. Completed and omitted reviews are durable and keyed by file-content SHA-256, so renaming or copying an identical file does not make it appear for review again. Different content reusing a filename is a new video. New reviewed examples are included when the next model is saved with Done.

This repository publishes fixed release snapshots. The first snapshot is credited PURSUE footage; other documented sources can contribute to future snapshots. New private inputs are not automatically uploaded to GitHub.

## Release

- Version: `v0.1.0-preview`
- Model ID: `e87a4acea5d149790eab57742cd8c10b`
- Snapshot: `2026-10-29T00:44:26.647532+00:00`
- Label counts: `{"anomalous": 440}`
- Usable templates after low-detail filtering: 437
- Independent held-out accuracy: not measured for this release

More templates increase CPU inference time. Start with still images before long videos. Threshold scores are correlations, not calibrated probabilities. This preview does not establish transfer accuracy on other cameras or environments.

## Sources and license

Original code, annotations, and compilation: **Apache License 2.0**, in [LICENSE](LICENSE). Source image crops retain their source-media status and terms; they are not relicensed as original imagery. [sources.json](sources.json) lists the official DVIDS page and source-video checksum for every contributing video. Included source pages were labeled PUBLIC DOMAIN at preparation time. See [NOTICE](NOTICE) and [DVIDS source terms](https://www.dvidshub.net/about/copyright).

The appearance of U.S. Department of War (DoW) visual information does not imply or constitute DoW endorsement.
