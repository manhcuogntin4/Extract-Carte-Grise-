import numpy as np

 

import sys,os

 

caffe_root = '/home/cuong-nguyen/2016/Workspace/brexia/Septembre/Codesource/caffe-master'

sys.path.insert(0, caffe_root + 'python')

import caffe

os.chdir(caffe_root)

 

net_file='/home/cuong-nguyen/2017/Workspace/Fevrier/CodeSource/AnnotationTool/AnnotationTool/python/document_category_googlenet/deploy.prototxt'

caffe_model='/home/cuong-nguyen/2017/Workspace/Fevrier/CodeSource/AnnotationTool/AnnotationTool/python/document_category_googlenet/train_val.caffemodel'

mean_file='/home/cuong-nguyen/2016/Workspace/brexia/Decembre/CodeSource/codeHaoming/web-demo-version4.0/caffe-fast-rcnn/python/caffe/imagenet'

 

net = caffe.Net(net_file,caffe_model,caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))

#transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))

transformer.set_raw_scale('data', 255)

transformer.set_channel_swap('data', (2,1,0)) # if using RGB instead if BGR

 

#im=caffe.io.load_image(caffe_root+'examples/images/cat.jpg')

#im=caffe.io.load_image(caffe_root+'examples/images/cross-eyed-cat.jpg')

img=caffe.io.load_image('/home/cuong-nguyen/2017/Workspace/Fevrier/Documents/prefix-1.png')

net.blobs['data'].data[...] = transformer.preprocess('data',img)

out = net.forward()
print out 
#proba = out['prob'][0]
 

imagenet_labels_filename ='/home/cuong-nguyen/2017/Workspace/Fevrier/CodeSource/AnnotationTool/AnnotationTool/python/document_category_googlenet/synset_words.txt'

labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

print labels 

#top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
top_k = net.blobs['fc8'].data[0].flatten().argsort()[-1:-6:-1]
#indices = (-proba).argsort()[:3]
#print indices
print top_k


# for i in np.arange(top_k.size):

#     print top_k[i], labels[top_k[i]]