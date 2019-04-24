import numpy as np

"""
class Robust_pca takes the input matrix M, and do the Robust PCA on M
Return: two matrix L,S which stand for foreground and background seperately.
Reference:https://github.com/dlaptev/RobustPCA/blob/master/RobustPCA.m
"""
class Robust_pca:

    #initialize S0=Y0=L0=0
    #initialize lambda, mu , mu(inverse) , tolerance,
    def __init__(self,M):
        self.M=M
        self.S=np.zeros(self.M.shape)
        self.Y=np.zeros(self.M.shape)
        self.L=np.zeros(self.M.shape)
        self.lam=1/np.sqrt(np.max(self.M.shape))
        self.mu=10*self.lam
        self.mu_inv=1/(self.mu)
        self.tolerance=1e-6
        self.max_iter=1000

    #function used to compute Sk+1 = Sλ/μ(M − Lk+1 + μ−1Yk)
    def S_function(self,M,tau):
        result=np.sign(M)*np.maximum(np.abs(M)-tau,0)
        return result

    #function used to compute Lk+1 = D1/μ(M− Sk + Yk/μ)
    def D_function(self,M,tau):
        U,S,V=np.linalg.svd(M,full_matrices=False)
        result_s=self.S_function(S,tau)
        US=np.dot(U,np.diag(result_s))
        result=np.dot(US,V)
        return result

    #function : generate Robust PCA
    def generate_pca(self):
        #initialize Sk, Yk, Lk and error
        Sk=self.S
        Yk=self.Y
        Lk=self.L
        err=np.Inf

        #run loop until reach max iteration or converged
        for i in range (0,self.max_iter):
            #compute Lk+1 = D1/μ(M− Sk + Yk/μ)
            Lk=self.D_function(self.M-Sk+self.mu_inv*Yk,self.mu_inv)
            #compute Sk+1 = Sλ/μ(M − Lk+1 + Yk/μ−1)
            Sk=self.S_function(self.M-Lk+self.mu_inv*Yk,self.mu_inv*self.lam)
            #compute Yk+1 = Yk + μ(M − Lk+1 − Sk+1)
            Yk=Yk+self.mu*(self.M-Lk-Sk)
            #compute the error using Frobenius norm
            err=np.linalg.norm(self.M-Lk-Sk,'fro')/np.linalg.norm(self.M,'fro')
            #print information iteratively
            if i==1 or (i%10)==0 or err<self.tolerance:
                print_info=' iteration : {0} ; error : {1}'.format(i, err)
                print(print_info)
            #check convergence
            if err<self.tolerance:
                break

        self.L=Lk
        self.S=Sk
        return Lk,Sk