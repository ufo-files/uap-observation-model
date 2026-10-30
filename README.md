# UAP Observation Model

An experimental, reusable appearance model built from manually labeled targets in credited source videos. This release includes **328 labeled crops from 17 source videos**, source credits, annotations, and a portable Python/OpenCV runner.

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

## Release

- Version: `model-f6a45756c1b54f3a9ef4cc2e055add85`
- Model ID: `f6a45756c1b54f3a9ef4cc2e055add85`
- Snapshot: `2026-10-30T18:48:17.688149+00:00`
- Label counts: `{"airplane": 1, "anomalous": 41, "bird": 51, "cloud": 235}`
- Usable templates after low-detail filtering: 327
- Independent held-out accuracy: not measured for this release

More templates increase CPU inference time. Start with still images before long videos. Threshold scores are correlations, not calibrated probabilities. This preview does not establish transfer accuracy on other cameras or environments.

## Sources and license

Original code, annotations, and compilation: **Apache License 2.0**, in [LICENSE](LICENSE). Source image crops retain their source-media status and terms; they are not relicensed as original imagery. [sources.json](sources.json) lists the official DVIDS page and source-video checksum for every contributing video. Source rights markings and attribution are recorded for each source; source media retain those separate terms. See [NOTICE](NOTICE) and [DVIDS source terms](https://www.dvidshub.net/about/copyright).

The appearance of U.S. Department of War (DoW) visual information does not imply or constitute DoW endorsement.
