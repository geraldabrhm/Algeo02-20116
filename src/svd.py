import numpy as np
import cv2 as cv
import math
import os
import timeit

def simultaneous_power_iteration(A, k):
    # fungsi untuk mencari nilai eigen dan eigen vector dengan metode QR Decomposition
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
 
    for i in range(200):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

    return np.diag(R), Q

def svd(A, k):
    A = A.astype('float64')
    m,n = A.shape
    At = np.transpose(A)

    Right = At @ A
    # Mengambil 200 nilai eigen yang paling besar
    EV, V = simultaneous_power_iteration(Right, min(k, 200))
    V = np.pad(V,((0,0),(0,n-V.shape[1])))
    # Membuat matriks Sigma
    singularValue = np.sqrt(abs(EV))
    Sigma = np.diag(singularValue)
    Sinv = np.linalg.inv(Sigma)
    Sigma = np.pad(Sigma, ((0,n-Sigma.shape[0]),(0,m-Sigma.shape[1])))
    Sinv = np.pad(Sinv, ((0,n-Sinv.shape[0]),(0,m-Sinv.shape[1])))

    # Mencari matriks U
    U = A @ V @ Sinv

    return U, Sigma, np.transpose(V)

def process(Mat, k):
    U,S,Vt = svd(Mat, k)
    if (min(Mat.shape) > 200):
        k *= 2
    else:
        k = k*min(Mat.shape)//100

    # proses pemotongan matriks 
    U = U[:,:k]
    S = S[:k,:k]
    Vt = Vt[:k,:]

    MatRes = U @ S @ Vt
    MatRes = np.clip(MatRes,0,255)
    MatRes = MatRes.astype(np.uint8)

    return MatRes

def main(img, persen):
    transparent = False
    # split tiap channel warna
    if (len(img[0][0]) == 4) :
        transparent = True
        b,g,r,a = cv.split(img)
    else:
        b,g,r = cv.split(img)

    # proses setiap channel secara terpisah
    afterB = process(b, persen)
    print("Channel Blue selesai")
    afterG = process(g, persen)
    print("Channel Green selesai")
    afterR = process(r, persen)
    print("Channel Red selesai")

    # menggabungkan kembali hasil pemrosesan tiap channel
    if (transparent):
        after = cv.merge([afterB, afterG, afterR, a])
    else :
        after = cv.merge([afterB, afterG, afterR])

    after = after.astype(np.uint8)
    return after

def compress(filename, persen):
    start = timeit.default_timer()
    pathfile = os.path.join(os.getcwd(), 'static', 'Image', filename)
    img = cv.imread(pathfile,-1)
    print("Compressing", filename)
    after = main(img, persen)

    if (min(img.shape[0], img.shape[1]) > 200):
        persen *= 2
    else:
        persen = persen*min(img.shape)//100
    
    pixel = pixelDiff(img, persen)

    stop = timeit.default_timer()
    total = round(stop - start)
    print('Running Time: ', total//60, 'm', total%60, 's')
    
    newFilename = filename.split(".")[0] +'_compressed.'+filename.split(".")[-1]
    newPathfile = os.path.join(os.getcwd(), 'static', 'Image', newFilename)
    cv.imwrite(newPathfile, after)
    return total, newFilename, pixel

def pixelDiff(Mat, k):
    m,n,_ = Mat.shape
    return ((m*k+k+k*n)*100/(m*n))
# time, compressedFilename = compress('logo_itb_128.png', 10)