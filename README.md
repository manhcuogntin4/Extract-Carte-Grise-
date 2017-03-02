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
