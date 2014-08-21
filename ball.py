import math
import cv2 as cv
import numpy as np
from scipy.spatial.distance import cdist
from scipy.cluster.vq import kmeans2

A_BUCKET = 4
MAX_A = 360/A_BUCKET
PAIR_PHASE = 180/A_BUCKET

def FCD( src, filter ):
	max_d = np.sum( src.shape )/4

        sobel_x = cv.Sobel( src, cv.CV_32F, 1, 0, ksize = 5 )
        sobel_y = cv.Sobel( src, cv.CV_32F, 0, 1, ksize = 5 )

	magnitude = np.hypot( sobel_x, sobel_y )

	gradient = np.degrees( np.arctan2(sobel_y,sobel_x) ) / A_BUCKET
	m_angle = np.ma.array( gradient.round(0)%MAX_A, mask=magnitude<filter )

	obs = []
	for i in range(PAIR_PHASE):
		A = np.nonzero( m_angle == i ).transpose() 
		B = np.nonzero( m_angle == i+PAIR_PHASE ).transpose()

		dts = cdist( A, B )
		cts = ( B + A[:,np.newaxis] )/2
		vts = B - A[:,np.newaxis]
		agls = np.degrees(np.arctan2(vts[...,1],vts[...,0]))/A_BUCKET

		pts = ( dist < max_d ) & ( ( agls.round(0) % MAX_A ) == i )
		obs.extend( np.insert( cts[pts], 2, dts[pts]/2, axis=1 ) )

	circles, labels = kmeans2( np.array( obs ), 3, 10, minit='points' )

	print np.array(obs)
	print circles
	print labels

	return

# cmath.rect(r,t)

#cv.namedWindow( "i" )
#cv.namedWindow( "j" )

src = cv.imread('test.jpg')
src_hsv = cv.cvtColor( src[200:1450,650:1880], cv.COLOR_BGR2HSV )
#src_v = src_hsv[...,2]
src_v = cv.resize( cv.split(src_hsv)[2], None, fx=0.1, fy=0.1 )
blurred = cv.GaussianBlur( src_v, (7,7), 5 )

FCD( blurred, 1500 )
#cv.imshow( "i", blurred )
#cv.waitKey(0)
#cv.destroyAllWindows()

