import caffe
import numpy as np
import yaml
import cv2
#import cv2.cv as cv
import random
import os
import re

class RoIDataLayer(caffe.Layer):

    def setup(self, bottom, top):
        """Setup the RoIDataLayer."""

        # parse the layer parameter string, which must be valid YAML
        if hasattr(self, 'param_str'):
            layer_params = yaml.load(self.param_str)
        else:
            layer_params = yaml.load(self.param_str_)

        self._batch_size = layer_params['batch_size']
        self._file = layer_params['file']
        self._width = layer_params['width']
        self._height = layer_params['height']
        self._channels = layer_params['channels']
        self._target_variance = layer_params['target_variance']
        self._num_classes = 1

        print "Batch size : ", self._batch_size

        self._name_to_top_map = {
            'data': 0,
            'rois': 1,
            'labels': 2,
            'bbox_targets': 3,
            'bbox_loss_weights': 4}

        self.images = []
        self.dir = os.path.dirname(self._file) + str("/")
        with open(self._file, 'r') as f:
            t = f.readlines()
            num = len(t)
            for l in t:
                self.images.append( l.split(',' , 10) )
                # path, x, y , w, h, ee = l.split(',' , 5)
                # im = cv2.imread('../' + path)
                # height, width, channel = im.shape
                # factor = height / 500
                # if factor > 1.5:
                #     factor = 1 / float(factor)
                #     im = cv2.resize(im,None, fx=factor, fy=factor, interpolation = cv2.INTER_AREA)
                #
                # demi_h = int(float(h)/2.0) ;
                # demi_w = int(float(w)/2.0) ;
                #
                # plt.imshow(im[ (int(y)-demi_h):(int(y)+demi_h), (int(x)-demi_w):(int(x)+demi_w) ])
                # plt.show()
                # print float(h)/float(w)
            print "Nombre de lignes:", num
        f.closed

        # data blob: holds a batch of N images, each with 3 channels
        # The height and width (100 x 100) are dummy values

        top[0].reshape(self._batch_size, self._channels, self._height, self._width)

        # rois blob: holds R regions of interest, each is a 5-tuple
        # (n, x1, y1, x2, y2) specifying an image batch index n and a
        # rectangle (x1, y1, x2, y2)

        # 2 labels
        top[1].reshape(self._batch_size)

        #labels blob: R categorical labels in [0, ..., K] for K foreground
        # classes plus background
        top[2].reshape(self._batch_size)

        # bbox_targets blob: R bounding-box regression targets with 4
        # targets per class
        top[3].reshape(self._batch_size, self._num_classes * 2)

        # bbox_loss_weights blob: At most 4 targets per roi are active;
        # thisbinary vector sepcifies the subset of active targets
        top[4].reshape(self._batch_size, self._num_classes * 2)

        self._cur = 0

        print "Dimensions : ", self._width, self._height
        print "File", self._file
        print "Batch size", self._batch_size
        print "Image directory", self.dir
        print "Target variance", self._target_variance
        #print "Num classes", self._num_classes


    def reshape(self, bottom, top):
        pass

    def forward(self, bottom, top):
        """Get blobs and copy them into this layer's top blob vector."""
        i = 0 ;


        #print "Batch from ",self._cur," to ",self._cur+self._batch_size


        while i < self._batch_size:
            #print "Sampling:",self.images[self._cur]
            r_im = int(random.uniform(0,len(self.images)))
            try:
                # print len(self.images[int(random.uniform(0,len(self.images)))])
                path, label, x, y, w, h, r, delta_x, delta_y, delta_r, delta_s = self.images[r_im]

                # print "label: ",label
                # label 0 pour positif
                # x = int(x)
                # y = int(y)
                label = int(label) -1

                # label = re.sub("[^a-z0-9\/]+","", label, flags=re.IGNORECASE)

                # if label:
                #     # print "OK"
                #     label = 0
                #     #int(x) *    4 + int(y)
                # else:
                #     # print "NEG"
                #     # continue
                #     label = 1
                # path, label = self.images[self._cur]
                # self._cur+=1
                # if self._cur == len(self.images):
                #     print "back begin"
                #     self._cur = 0

                im = cv2.imread( self.dir + path) #self.dir +
                im = cv2.resize(im, (self._width, self._height))
                height, width, channel = im.shape
                #print "Channel ", channel
                # gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) * 0.00390625

                # 1 channel => i,0
                # top[0].data[i,0] = gray[...]
                top[0].data[i,0] = im[...,2]
                top[0].data[i,1] = im[...,1]
                top[0].data[i,2] = im[...,0]
                # print label.rstrip()
                # top[1].data[i] = int(label.rstrip())
                top[1].data[i] = label

                # 1 classe => i
                # top[3].data[i] = [ x / self._target_variance, y / self._target_variance]

                # if label==0:
                #     top[4].data[i] = [ 1, 1]
                #     #print top[3].data[i]
                # else :
                #     top[4].data[i] = [ 0, 0]
                    #print top[3].data[i]

                #   top: "labels"
                #   top: "bbox_targets"
                #   top: "bbox_loss_weights"
                        # top[3].reshape(self._batch_size, self._num_classes * 2)
                        #
                        # # bbox_loss_weights blob: At most 4 targets per roi are active;
                        # # thisbinary vector sepcifies the subset of active targets
                        # top[4].reshape(self._batch_size, self._num_classes * 2)

                i+=1
            except (RuntimeError, TypeError, NameError, AttributeError) as e:
                print "Error"
                print e
                pass
            except ValueError as e :
                print self.images[r_im]
                print e
                pass

        # blobs = self._get_next_minibatch()
        #
        # for blob_name, blob in blobs.iteritems():
        #     top_ind = self._name_to_top_map[blob_name]
        #     # Reshape net's input blobs
        #     top[top_ind].reshape(*(blob.shape))
        #     # Copy data into net's input blobs
        #     top[top_ind].data[...] = blob.astype(np.float32, copy=False)
        print "End fo"


    def backward(self, top, propagate_down, bottom):
        pass
