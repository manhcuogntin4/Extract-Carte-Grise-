# Extract-Carte-Grise-

First solution

Step 1 : Convert file image carte grise pdf to png file using pdftoppm outil
http://askubuntu.com/questions/50170/how-to-convert-pdf-to-image/50180

Step 2 : Classify the cni, passeport, carte grise with the other type by the convolutional neurone network

Second solution 

Using the solution presented in README.MD in AnnnotationTool. Some changes need to be added in the shell file for suitable the number of class. Remove line #import cv2.cv as cv if you use the OpenCV3

Attention : Change the number of output : num_output in the deploy.prototxt and train_val.prototxt to the real number types of docs.

Step 3: Prepare DataSet for Faster RCNN with the cpdata.sh shell

Step 4: Upload the file DataSet on S3

Step 5: Download file from S3 to EC2
$> aws configure

 

Access key id : <acces key>

Secret Access Key : <secret access key>

Zone : eu-west-1

Format : json

$> aws s3 cp link s3 --recursive

Step 6 : Prepare for trainning Faster RCNN.
Change the number of classe in the axa.py, train.proto and test.proto files.
Start trainning with command line :
./tools/train_net.py --gpu 0 --solver models/axa_poc/VGG_CNN_M_1024/faster_rcnn_end2end/solver.prototxt --weights data/imagenet_models/VGG_CNN_M_1024.v2.caffemodel --imdb axa_train --iters 80000 --cfg experiments/cfgs/faster_rcnn_end2end.yml

Step 7 : Prepare data for CLSTM with gendataset.py
