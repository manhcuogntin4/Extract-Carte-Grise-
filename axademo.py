#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Copyright (c) 2016 Haoming Wang
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
from ocr.clstm import clstm_ocr
from ocr.clstm import clstm_ocr_calib
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse
import werkzeug
import datetime
import math
import pytesseract
from PIL import Image
#Multiprocess
from multiprocessing import Pool   
import multiprocessing 
import subprocess
from multiprocessing import Manager
from functools import partial
import multiprocessing.pool


CLASSES = ('__background__', # always index 0
           'cni', 'person', 'mrz', 'nom', 'nomepouse', 'prenom', 'lieu')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel'),
        'inria': ('INRIA_Person',
                  'INRIA_Person_faster_rcnn_final.caffemodel'),
        'axa': ('axa_poc',
                  'axa_poc_faster_rcnn_final.caffemodel')}
UPLOAD_FOLDER = '/tmp/caffe_demos_uploads'

def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                  fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()

def extract_roi(class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    regions = []
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return regions

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        # a small regulation of detected zone, comment me if the lastest result is good enough
        hight = bbox[3] - bbox[1]
        if class_name == 'nom':
            bbox[0] += 1.5 * hight
            bbox[1] -= 0.25 * hight
            bbox[2] += 0.2 * (bbox[2] - bbox[0])
            bbox[3] += 0.15 * hight
        elif class_name == 'nomepouse':
            #bbox[0] += 2.5 * hight
            #bbox[2] += 0.1 * (bbox[2] - bbox[0])
	    bbox[0] += 2.5 * hight
            bbox[2] += 0.15 * (bbox[2] - bbox[0])
            bbox[3] += 0.2 * hight
        elif class_name == 'prenom':
            bbox[0] += 2.5 * hight
            bbox[2] += 0.15 * (bbox[2] - bbox[0])
            bbox[3] += 0.2 * hight
        elif class_name == 'lieu':
            bbox[0] += 0.8 * hight
            bbox[2] += 0.5 * hight
            #bbox[3] += 0.1 * hight
        elif class_name == 'mrz':
            bbox[2] += 0.5 * hight
        pts = [int(bx) for bx in bbox]
        regions.append(pts)
    return regions

def ocr_queue(im, bbx, cls, q):
	q.put(calib_roi(im,bbx,cls))


def demo(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    # im_file = os.path.join(UPLOAD_FOLDER, 'demo', image_name)
    im = cv2.imread(image_name)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    res = {}
    roi_file_name=[]
    #Parallel processing
    
    
    for cls_ind, cls in enumerate(CLASSES[3:]):
        cls_ind += 3 # because we skipped background, 'cni', 'person' and 'mrz'
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        tmp = extract_roi(cls, dets, thresh=CONF_THRESH)
        if len(tmp) > 0:
            #bbx = tmp[0]  # TODO: Find the zone with greatest probability
            #txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
            #res[cls] = (bbx, txt, prob)
        # vis_detections(im, cls, dets, thresh=CONF_THRESH)
            bbx = tmp[0]  # TODO: Find the zone with greatest probability
                # txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
                # if(prob<0.95):
                #     txt1,prob1=clstm_ocr(im[bbx[1]-3:bbx[3]+3, bbx[0]:bbx[2]], cls=='lieu')
                #     if(prob<prob1):
                #         txt=txt1
                #         prob=prob1
            if cls!="mrz":


                #Multiprocessing
                # p_cls = Pool(8)
                # rs[cls]=p_cls.map(calib_roi, im, bbx, cls)
                # p_cls.start()
                # p_cls.join()
                # txt,prob=rs[cls]
                #Queue
                # q = multiprocessing.Queue()
                # p = multiprocessing.Process(target=calib_roi, args=(im,bbx,cls,q,))
                # p.start()
                # p.join()
                # txt,prob=q.get()
                #Single processing
				txt, prob =calib_roi(im,bbx,cls)

                
            else :
                pts_msz = [int(bx) for bx in bbx]
                filename_ = werkzeug.secure_filename('output' + "mrz" + image_name + '.png')
                filename = os.path.join(UPLOAD_FOLDER, filename_)
                cv2.imwrite(filename, im[pts_msz[1]:pts_msz[3], pts_msz[0]:pts_msz[2]])
                txt, prob= pytesseract.image_to_string(Image.open(filename)), 1
                if(len(txt)>9):
                	txt= txt[-5:-3]+"-"+ txt[-7:-5]+"-"+ txt[-9:-7]

            #txt, prob =calib_roi(im,bbx,cls)
            res[cls] = (bbx, txt, prob)
            pts = [int(bx) for bx in bbx]   
            # filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            # werkzeug.secure_filename('output' + str(cls) + image_name+str(cls_ind) + '.png')
            filename_ = werkzeug.secure_filename('output' + str(cls) + image_name + '.png')
            filename = os.path.join(UPLOAD_FOLDER, filename_)
            cv2.imwrite(filename, im[pts[1]:pts[3], pts[0]:pts[2]])
            roi_file_name.append(filename)
            # filetext_=str(datetime.datetime.now()).replace(' ', '_') + \
            # werkzeug.secure_filename('output' + str(cls_ind) + '.txt')
            #filetext = os.path.join(UPLOAD_FOLDER, filetext_)
            filetext=filename+"txt"
            f=open(filetext, "w")
            f.write(txt.encode('utf8'))
            f.close()
    im = im[:, :, (2, 1, 0)]
    #return (im, res, timer.total_time, roi_file_name)
    return (im, res, timer.total_time), roi_file_name
    #return (im, res, timer.total_time)



def demo_parallel(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    # im_file = os.path.join(UPLOAD_FOLDER, 'demo', image_name)
    im = cv2.imread(image_name)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    res = {}
    roi_file_name=[]
    #Parallel processing
    
    list_bbx={}
    list_cls={}
    q={}
    p={}
    pts={}
    txt={}
    prob={}
    for cls_ind, cls in enumerate(CLASSES[3:]):
        cls_ind += 3 # because we skipped background, 'cni', 'person' and 'mrz'
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        tmp = extract_roi(cls, dets, thresh=CONF_THRESH)
        if len(tmp) > 0:
            #bbx = tmp[0]  # TODO: Find the zone with greatest probability
            #txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
            #res[cls] = (bbx, txt, prob)
        # vis_detections(im, cls, dets, thresh=CONF_THRESH)
            bbx = tmp[0]  # TODO: Find the zone with greatest probability
                # txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
                # if(prob<0.95):
                #     txt1,prob1=clstm_ocr(im[bbx[1]-3:bbx[3]+3, bbx[0]:bbx[2]], cls=='lieu')
                #     if(prob<prob1):
                #         txt=txt1
                #         prob=prob1
            list_bbx[cls]=bbx
            list_cls[cls]=cls
    #Multiprocessing
    for cls in list_cls:
    	if cls!="mrz":
    		#Queue
	    	q[cls] = multiprocessing.Queue()
	    	p[cls] = multiprocessing.Process(target=ocr_queue, args=(im,list_bbx[cls],cls,q[cls],))
	    	p[cls].start()
	    	p[cls].join()
	    	txt[cls],prob[cls]=q[cls].get()
    	

    	else:
	    	pts_msz = [int(bx) for bx in list_bbx["mrz"]]
	    	filename_ = werkzeug.secure_filename('output' + "mrz" + image_name + '.png')
	    	filename = os.path.join(UPLOAD_FOLDER, filename_)
	    	cv2.imwrite(filename, im[pts_msz[1]:pts_msz[3], pts_msz[0]:pts_msz[2]])
	    	txt["mrz"], prob["mrz"]= pytesseract.image_to_string(Image.open(filename)), 1
	    	if(len(txt["	mrz"])>9):
	    		txt["mrz"]= txt["mrz"][-5:-3]+"-"+ txt["mrz"][-7:-5]+"-"+ txt["mrz"][-9:-7]
        #txt, prob =calib_roi(im,bbx,cls)
        res[cls] = (list_bbx[cls], txt[cls], prob[cls])
        pts[cls] = [int(bx) for bx in list_bbx[cls]]   
        # filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
        # werkzeug.secure_filename('output' + str(cls) + image_name+str(cls_ind) + '.png')
        filename_ = werkzeug.secure_filename('output' + str(cls) + image_name + '.png')
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        cv2.imwrite(filename, im[pts[cls][1]:pts[cls][3], pts[cls][0]:pts[cls][2]])
        roi_file_name.append(filename)
        # filetext_=str(datetime.datetime.now()).replace(' ', '_') + \
        # werkzeug.secure_filename('output' + str(cls_ind) + '.txt')
        #filetext = os.path.join(UPLOAD_FOLDER, filetext_)
        filetext=filename+"txt"
        f=open(filetext, "w")
        f.write(txt[cls].encode('utf8'))
        f.close()

                #Queue
                # q = multiprocessing.Queue()
                # p = multiprocessing.Process(target=calib_roi, args=(im,bbx,cls,q,))
                # p.start()
                # p.join()
                # txt,prob=q.get()
                #Single processing

    
    im = im[:, :, (2, 1, 0)]
    #return (im, res, timer.total_time, roi_file_name)
    return (im, res, timer.total_time), roi_file_name




def check(boxes, scores, thresh=0.8, nms_thresh=0.3):
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, nms_thresh)
        dets = dets[keep, :]
        inds = np.where(dets[:, -1] >= thresh)[0]
        if cls_ind == 5:  #we skip 'nom epouse' check
            continue
        if len(inds) == 0:
            return False
    return False


"""demo2 is a complement for demo, in considering the multi-cni case 
    and if we should do faster-rcnn a second time"""
def demo2(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    # im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    im = cv2.imread(image_name)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    res = {}
    roi_file_name=[]
    if check(boxes, scores, CONF_THRESH, NMS_THRESH):
        for cls_ind, cls in enumerate(CLASSES[3:]):
            cls_ind += 3 # because we skipped background
            cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes,
                              cls_scores[:, np.newaxis])).astype(np.float32)
            keep = nms(dets, NMS_THRESH)
            dets = dets[keep, :]
            tmp = extract_roi(cls, dets, thresh=CONF_THRESH)
    
            if len(tmp) > 0:
                bbx = tmp[0]  # TODO: Find the zone with greatest probability
                # txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
                # if(prob<0.95):
                #     txt1,prob1=clstm_ocr(im[bbx[1]-3:bbx[3]+3, bbx[0]:bbx[2]], cls=='lieu')
                #     if(prob<prob1):
                #         txt=txt1
                #         prob=prob1
                if cls!="mrz":
                    txt, prob =calib_roi(im,bbx,cls)
                else :
                    pts_msz = [int(bx) for bx in bbx]
                    filename_ = werkzeug.secure_filename('output' + "mrz" + image_name + '.png')
                    filename = os.path.join(UPLOAD_FOLDER, filename_)
                    cv2.imwrite(filename, im[pts_msz[1]:pts_msz[3], pts_msz[0]:pts_msz[2]])
                    txt, prob= pytesseract.image_to_string(Image.open(filename)), 1
                    if(len(txt)>9):
                		txt= txt[-5:-3]+"-"+ txt[-7:-5]+"-"+ txt[-9:-7]

                res[cls] = (bbx, txt, prob)
                pts = [int(bx) for bx in bbx]   
                # filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
                # werkzeug.secure_filename('output' + str(cls) + image_name+str(cls_ind) + '.png')
                filename_ = werkzeug.secure_filename('output' + str(cls) + image_name + '.png')
                filename = os.path.join(UPLOAD_FOLDER, filename_)
                cv2.imwrite(filename, im[pts[1]:pts[3], pts[0]:pts[2]])
                roi_file_name.append(filename)
                # filetext_=str(datetime.datetime.now()).replace(' ', '_') + \
                # werkzeug.secure_filename('output' + str(cls_ind) + '.txt')
                #filetext = os.path.join(UPLOAD_FOLDER, filetext_)
                filetext=filename+"txt"
                f=open(filetext, "w")
                f.write(txt.encode('utf8'))
                f.close()
    else:  
        cls_ind = 1 # CNI
        cls = CLASSES[cls_ind]
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
        tot_info_cni = []
        for i in inds:
            bbox = dets[i, :4]
            score = dets[i, -1]
            coef = 1.05
            pmax = im.shape[:2][::-1]
            for ind in xrange(4):
                if ind < 2:
                    bbox[ind] = bbox[ind] / coef
                else:
                    bbox[ind] = min(bbox[ind] * coef, pmax[ind - 2])
            print 'Saving recognized cni...'
            pts = [int(bx) for bx in bbox]
            filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
                werkzeug.secure_filename('output' + str(i) + image_name +'.png')
            filename = os.path.join(UPLOAD_FOLDER, filename_)
            cv2.imwrite(filename, im[pts[1]:pts[3], pts[0]:pts[2]])
            info_cni, roi_file_name=demo_parallel(net, filename)
            tot_info_cni.append(info_cni)
            #tot_info_cni.append(demo(net, filename))
        #vis_detections(im, cls, dets, thresh=CONF_THRESH)
        return tot_info_cni, timer.total_time, roi_file_name
    im = im[:, :, (2, 1, 0)]
    return [(im, res, timer.total_time)], 0, roi_file_name  # equivalent to demo


"""demo2 is a complement for demo, in considering the multi-cni case 
    and if we should do faster-rcnn a second time"""

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        default=True,
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='axa')

    args = parser.parse_args()

    return args


def detect_cni(filename):
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.demo_net][0],
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS[args.demo_net][1])

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Demo for classified CNI image...'
    return demo2(net, filename)

def calib_roi(im,bbx,cls):
    txt, prob = clstm_ocr(im[bbx[1]:bbx[3], bbx[0]:bbx[2]], cls=='lieu')
    if(prob<0.95):
        for i in range(0,2):
            for j in range(0,2):
                txt_temp,prob_temp=clstm_ocr_calib(im[bbx[1]-5*i*math.pow( -1, j):bbx[3]+5*i*math.pow( -1, j), bbx[0]-3*i*math.pow( -1, j):bbx[2]+3*i*math.pow( -1, j)], cls=='lieu')
                if(prob<prob_temp):
                    txt=txt_temp
                    prob=prob_temp
    return txt, prob

def main():
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.demo_net][0],
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS[args.demo_net][1])

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    im_name = 'ID_FRA.jpg'
    # im_name = 'cni2.png'     
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Demo for data/demo/{}'.format(im_name)
    demo(net, im_name)

    plt.show()




if __name__ == '__main__':
    main()
