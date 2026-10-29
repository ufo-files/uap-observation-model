# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 ufo-files contributors
"""Portable inference for the UAP appearance model. No station services required."""
import argparse, hashlib, json, sys
from pathlib import Path
import cv2
import numpy as np
cv2.setNumThreads(1)

def detect(image,templates,threshold,labels,verify_detail=True):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);h,w=gray.shape;matches=[]
    # Native pixels are used for both the saved examples and full-frame inference.
    for label,template in templates:
        th,tw=template.shape
        for scale in (.65,.8,1.,1.25,1.6):
            sw,sh=round(tw*scale),round(th*scale)
            if min(sw,sh)<3 or sw>w or sh>h:continue
            target=cv2.resize(template,(sw,sh),interpolation=cv2.INTER_AREA if scale<1 else cv2.INTER_CUBIC)
            if target.std()<2:continue
            scores=cv2.matchTemplate(gray,target,cv2.TM_CCOEFF_NORMED)
            # Raw NCC can be almost perfect for two unrelated smooth gradients.
            # Verify fine spatial structure independently before calling it an object.
            target_detail=None
            if verify_detail and label!='cloud':
                target_float=target.astype(np.float32)
                # A linear sky gradient has no localized subject; blur boundaries
                # and 8-bit quantization must not manufacture apparent detail.
                xx=np.arange(sw,dtype=np.float32)-(sw-1)/2
                yy=np.arange(sh,dtype=np.float32)-(sh-1)/2
                ax=float(np.sum(target_float*xx[None,:]))/max(1,float(sh*np.sum(xx*xx)))
                ay=float(np.sum(target_float*yy[:,None]))/max(1,float(sw*np.sum(yy*yy)))
                structure=target_float-target_float.mean()-ax*xx[None,:]-ay*yy[:,None]
                if structure.std()<.5:continue
                target_detail=target_float-cv2.GaussianBlur(target_float,(0,0),1.2)
                if target_detail.std()<.2:continue
            # Nonmaximum suppression allows multiple objects from a learned class.
            for _ in range(8):
                _,score,_,location=cv2.minMaxLoc(scores)
                if score<threshold:break
                x,y=location
                detail_score=None
                if target_detail is not None:
                    patch=gray[y:y+sh,x:x+sw].astype(np.float32)
                    detail=patch-cv2.GaussianBlur(patch,(0,0),1.2)
                    if detail.std()>=.2:detail_score=float(cv2.matchTemplate(detail,target_detail,cv2.TM_CCOEFF_NORMED)[0,0])
                if target_detail is None or (detail_score is not None and np.isfinite(detail_score) and detail_score>=.55):
                    match=dict(label=label,score=float(score),box=[x,y,sw,sh])
                    if detail_score is not None:match['detail_score']=detail_score
                    matches.append(match)
                scores[max(0,y-sh//2):min(scores.shape[0],y+sh//2+1),max(0,x-sw//2):min(scores.shape[1],x+sw//2+1)]=-1
    result=[]
    for m in sorted(matches,key=lambda v:-v['score']):
        x,y,bw,bh=m['box']
        def overlap(n):
            xx,yy,ww,hh=n['box'];inter=max(0,min(x+bw,xx+ww)-max(x,xx))*max(0,min(y+bh,yy+hh)-max(y,yy))
            return inter/max(1,min(bw*bh,ww*hh))
        if not any(overlap(n)>.35 for n in result):result.append(m)
    # Reviewed known objects compete with anomalous examples, so stronger known
    # matches can suppress a weaker target match at the same location.
    return [m for m in result if m['label'] in labels]

class Matcher:
    def __init__(self, model_dir=None):
        self.root=Path(model_dir or Path(__file__).resolve().parent).resolve()
        self.model=json.loads((self.root/'model.json').read_text())
        self.templates=[]
        for example in self.model['examples']:
            path=(self.root/example['image']).resolve()
            if not path.is_relative_to(self.root):raise ValueError('Invalid template path')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=example['sha256']:raise ValueError('Template checksum mismatch: '+example['image'])
            image=cv2.imread(str(path),cv2.IMREAD_GRAYSCALE)
            if image is None:raise ValueError('Invalid template: '+example['image'])
            if image.std()>=2:self.templates.append((example['label'],image))
        if not self.templates:raise ValueError('No usable templates')
    def predict(self, image, threshold=.97, labels=None):
        if not .5<=threshold<=1:raise ValueError('Threshold must be between 0.5 and 1')
        return detect(image,self.templates,threshold,labels or self.model['classes'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('--model',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--threshold',type=float,default=.97);parser.add_argument('--labels',help='Comma-separated output labels')
    parser.add_argument('--output',type=Path,help='JSONL detections; defaults to stdout')
    args=parser.parse_args();matcher=Matcher(args.model);labels=args.labels.split(',') if args.labels else None
    out=args.output.open('w') if args.output else sys.stdout
    try:
        image=cv2.imread(str(args.input),cv2.IMREAD_COLOR) if args.input.suffix.lower() in ('.png','.jpg','.jpeg','.bmp','.tif','.tiff','.webp') else None
        if image is not None:
            print(json.dumps(dict(model_id=matcher.model['id'],frame=0,objects=matcher.predict(image,args.threshold,labels))),file=out)
        else:
            video=cv2.VideoCapture(str(args.input))
            if not video.isOpened():raise ValueError('Cannot open input video')
            frame=0
            try:
                while True:
                    ok,image=video.read()
                    if not ok:break
                    print(json.dumps(dict(model_id=matcher.model['id'],frame=frame,objects=matcher.predict(image,args.threshold,labels))),file=out)
                    frame+=1
            finally:video.release()
    finally:
        if out is not sys.stdout:out.close()
if __name__=='__main__':main()
