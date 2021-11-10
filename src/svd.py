import numpy as np
import cv2 as cv
import math
import os
import timeit

def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q
 
    for i in range(200):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        err = ((Q - Q_prev) ** 2).sum()

        Q_prev = Q
        if err < 1e-3:
            break

    return np.diag(R), Q

def svd(A):
    A = A.astype('float64')
    m,n = A.shape
    At = np.transpose(A)

    if (m<n):
        ALeft  = np.matmul(A,At)
        # Mencari Eigen Value dan Matriks singular kiri
        EV, U = simultaneous_power_iteration(ALeft, m)
        singularValue = [math.sqrt(i) for i in EV if i>0]
        k = len(singularValue)
        # Menyusun matriks Sigma
        Sigma = np.diag(singularValue)

        # normalisasi tiap vector di U
        for i in range(m):
            norm = np.linalg.norm(U[i])
            U[i] = U[i]/norm

        # Mencari Vt
        Sinv = np.linalg.inv(Sigma)
        temp = np.zeros((n,m))
        if (k != m and k != n):
            temp[:(k-n),:(k-m)] = Sinv
            Sinv = temp
        elif (k == m and k == n):
            temp[:,:] = Sinv
            Sinv = temp
        elif (k == m):
            temp[:(k-n),:] = Sinv
            Sinv = temp
        elif (k == n):
            temp[:,:(k-m)] = Sinv
            Sinv = temp

        Ut = np.transpose(U)
        Vt = np.matmul(Sinv, Ut)
        Vt = np.matmul(Vt, A)

    else :
        ARight = np.matmul(At,A)
        # Mencari Eigen Value dan Matriks singular kanan
        EV, V = simultaneous_power_iteration(ARight, n)
        singularValue = [math.sqrt(i) for i in EV if i>0]
        k = len(singularValue)
        # Menyusun matriks Sigma
        Sigma = np.diag(singularValue)

        # normalisasi mtiap vector di V
        for i in range(n):
            norm = np.linalg.norm(V[i])
            V[i] = V[i]/norm

        # Mencari matriks U
        Sinv = np.linalg.inv(Sigma)
        temp = np.zeros((n,m))
        if (k != m and k != n):
            temp[:(k-n),:(k-m)] = Sinv
            Sinv = temp
        elif (k == m and k == n):
            temp[:,:] = Sinv
            Sinv = temp
        elif (k == m):
            temp[:(k-n),:] = Sinv
            Sinv = temp
        elif (k == n):
            temp[:,:(k-m)] = Sinv
            Sinv = temp

        Vt = np.transpose(V)
        U = np.matmul(A,V)
        U = np.matmul(U,Sinv)

    return U, Sigma, Vt

def process(Mat, k):
    U,S,Vt = svd(Mat)

    k = k*len(S[0])//100

    # proses pemotongan matriks 
    U = U[:,:k]
    S = S[:k,:k]
    Vt = Vt[:k,:]

    MatRes = np.matmul(U,S)
    MatRes = np.matmul(MatRes,Vt)
    MatRes = MatRes.astype(np.uint8)

    return MatRes

def main(img, persen):
  transparent = False
  if (len(img[0][0]) == 4) :
    transparent = True
    b,g,r,a = cv.split(img)
  else:
    b,g,r = cv.split(img)

  afterB = process(b, persen)
  afterG = process(g, persen)
  afterR = process(r, persen)

  if (transparent):
    after = cv.merge([afterB, afterG, afterR, a])
  else :
    after = cv.merge([afterB, afterG, afterR])

  after = after.astype(np.uint8)

  return after

def compress(filename, persen):
  start = timeit.default_timer()
  pathfile = os.path.join(os.getcwd(), 'src', 'static', 'Image', filename)
  img = cv.imread(pathfile,-1)
  after = main(img, persen)

  stop = timeit.default_timer()
  total = round(stop - start)
  print('Running Time: ', total//60, 'm', total%60, 's')
  
  newFilename = filename.split(".")[0] +'_'+str(persen)+'.'+filename.split(".")[-1]
  newPathfile = os.path.join(os.getcwd(), 'src', 'static', 'Image', newFilename)
  cv.imwrite(newPathfile, after)


compress('lena.png', 50)