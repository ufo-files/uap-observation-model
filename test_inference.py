# SPDX-License-Identifier: Apache-2.0
import hashlib,json,tempfile,unittest
from pathlib import Path
import cv2
import numpy as np
from inference import Matcher

class MatcherTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.target=np.random.default_rng(17).integers(20,240,(16,16,3),dtype=np.uint8)
        cv2.imwrite(str(self.root/'target.png'),self.target)
        self.manifest=dict(id='test',classes=['anomalous'],examples=[dict(image='target.png',label='anomalous',sha256=hashlib.sha256((self.root/'target.png').read_bytes()).hexdigest())])
        (self.root/'model.json').write_text(json.dumps(self.manifest))
    def tearDown(self):self.tmp.cleanup()
    def test_multiple_native_pixel_boxes_and_label_filter(self):
        image=np.zeros((128,192,3),np.uint8);image[20:36,30:46]=self.target;image[80:96,130:146]=self.target
        model=Matcher(self.root);matches=model.predict(image,.99)
        self.assertEqual(sorted(m['box'] for m in matches),[[30,20,16,16],[130,80,16,16]])
        self.assertEqual(model.predict(image,.99,['bird']),[])
    def test_modified_templates_are_rejected(self):
        (self.root/'target.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):Matcher(self.root)
    def test_paths_outside_model_are_rejected(self):
        self.manifest['examples'][0]['image']='../outside.png';(self.root/'model.json').write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError,'Invalid template path'):Matcher(self.root)
    def test_released_model_integrity(self):
        model=Matcher();summary=json.loads((Path(__file__).parent/'release-summary.json').read_text())
        self.assertEqual(len(model.model['examples']),summary['examples']);self.assertEqual(len(model.templates),summary['usable_templates'])
if __name__=='__main__':unittest.main()
