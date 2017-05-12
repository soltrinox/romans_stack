import numpy as np
import matplotlib.pyplot as plt
import caffe

caffe.set_mode_gpu()

# Load the original network and extract the fully connected layers' parameters.
net1 = caffe.Net('/home/kevin/models/caffe_net/deploy.prototxt', 
                '/home/kevin/models/caffe_net/bvlc_reference_caffenet.caffemodel', 
                caffe.TEST)
params1 = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5']
#fc_params = {name: (weights, biases)}
params_net1 = {pr: (net1.params[pr][0].data, net1.params[pr][1].data) for pr in params1}

print "====================================================================================="
print "finish loading the source model"
print "====================================================================================="

for pr in params1:
	print 'fc: {} weights are {} dimensional and biases are {} dimensional'.format(pr, params_net1[pr][0].shape, params_net1[pr][1].shape)
	

net2 = caffe.Net('/home/kevin/catkin_release/src/romans_stack/dcnns/romans_fast/stage1/train.prototxt', 
                '/home/kevin/models/caffe_net/bvlc_reference_caffenet.caffemodel', 
                caffe.TEST)
params2 = ['rgb_conv1', 'rgb_conv2', 'rgb_conv3', 'rgb_conv4', 'rgb_conv5']
#conv_params = {name: (weights, biases)}
params_net2 = {pr: (net2.params[pr][0].data, net2.params[pr][1].data) for pr in params2}

print "====================================================================================="
print "finish loading the target model"
print "====================================================================================="

for pr in params2:
    print 'net2: {} weights are {} dimensional and biases are {} dimensional'.format(pr, params_net2[pr][0].shape, params_net2[pr][1].shape)


# transplant the weights
for pr1, pr2 in zip(params1, params2):
    print "------------------------->"
    print "------------------------->"
    print "------------------------->"
    print "copy " 
    print params_net1[pr1][0].shape
    print "to "
    print params_net2[pr2][0].shape
    print "------------------------->"
    print "------------------------->"
    print "------------------------->"
    print "copy " 
    print params_net1[pr1][1].shape
    print "to "
    print params_net2[pr2][1].shape

    params_net2[pr2][0][...] = params_net1[pr1][0] 
    params_net2[pr2][1][...] = params_net1[pr1][1]

print "save new caffemodel"
net2.save('/home/kevin/models/rgbd_net_fast/rgb_model.caffemodel')

print "====================================================================================="
