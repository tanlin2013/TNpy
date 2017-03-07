"""
This file contains several algorithms which are based on the Matrix Product State (MPS) ansatz.

* Infinite Size Density Matrix Renormalization Group (iDMRG)
* Infinte Time Evolution Bond Decimation (iTEBD)
* Finite Size Density Matrix Renormalization Group (fDMRG)
* Finte Time Evolution Bond Decimation (fTEBD)

"""

import time
import warnings
import numpy as np
import linalg
import tnstate as tn

class iDMRG:
    def __init__(self,MPO,Gs,SVMs,N,d,chi):
        self.MPO=MPO
        self.Gs=Gs
        self.SVMs=SVMs
        self.N=N
        self.d=d
        self.chi=chi
    
    def _initialize_Env(self):
        D=self.MPO(0).shape[1]
        vL=np.zeros(D)
        vL[0]=1.0
        L=np.kron(vL,np.identity(self.chi,dtype=float))      
        L=np.ndarray.reshape(L,(self.chi,D,self.chi))
        vR=np.zeros(D)
        vR[-1]=1.0
        R=np.kron(np.identity(self.chi,dtype=float),vR)
        R=np.ndarray.reshape(R,(self.chi,D,self.chi))
        return L,R
    
    def _effH(self,ML,MR):        
        H=np.tensordot(np.tensordot(L,ML,axes=(1,1)),np.tensordot(MR,R,axes=(3,1)),axes=(4,1))                                  
        H=np.swapaxes(H,1,4)
        H=np.swapaxes(H,3,6)
        H=np.swapaxes(H,1,2)
        H=np.swapaxes(H,5,6)
        H=np.ndarray.reshape(H,(self.chi**2*self.d**2,self.chi**2*self.d**2)) 
        return H
    """
    def _effHpsi(self,ML,MR):
        def H_matvec(X):
            
            return matvet
        psi=
        return H_matvec,psi
    """
    def warm_up_optimize(self):
        L,R=self.initialize_Env()
        for length in xrange(self.N/2):
            A=length%2
            B=(length+1)%2
            ML=self.MPO(A) ; MR=self.MPO(B)
            # optimize 2 new-added sites in the center
            H=self.effH(ML,MR)                      
            E,theta=linalg.eigensolver(H)
            E/=(2*self.N)
            # SVD
            theta=np.ndarray.reshape(theta,(self.chi*self.d,self.chi*self.d))
            X,S,Y=np.linalg.svd(theta,full_matrices=False)
            # truncation           
            X=X[:,0:self.chi] ; S=S[0:self.chi] ; Y=Y[0:self.chi,:]                         
            self.SVMs[A]=np.diagflat(S/np.linalg.norm(S))
            # form the new configuration
            X=np.ndarray.reshape(X,(self.chi,self.d,self.chi))
            Y=np.ndarray.reshape(Y,(self.chi,self.d,self.chi))
            if length==1:
                self.Gs[A]=X
                self.Gs[B]=Y
            else:
                SVM_inv=linalg.inverse_SVM(self.SVMs[B])
                self.Gs[A]=np.tensordot(SVM_inv,X,axes=(1,0))
                self.Gs[B]=np.tensordot(Y,SVM_inv,axes=(2,0))
            # update the environment
            if length==1:
                EnvL=np.tensordot(np.tensordot(self.Gs[A],ML,axes=(1,0)),np.conjugate(self.Gs[A]),axes=(3,1))
                L=np.tensordot(L,EnvL,axes=([0,1,2],[0,2,4]))
                EnvR=np.tensordot(np.tensordot(self.Gs[B],MR,axes=(1,0)),np.conjugate(self.Gs[B]),axes=(3,1))
                R=np.tensordot(EnvR,R,axes=([1,3,5],[0,1,2]))
            else:    
                EnvL=np.tensordot(np.tensordot(np.tensordot(self.SVMs[B],self.Gs[A],axes=(1,0)),ML,axes=(1,0)),np.tensordot(self.SVMs[B],np.conjugate(self.Gs[A]),axes=(1,0)),axes=(3,1))                        
                L=np.tensordot(L,EnvL,axes=([0,1,2],[0,2,4]))
                EnvR=np.tensordot(np.tensordot(np.tensordot(self.Gs[B],self.SVMs[B],axes=(2,0)),ML,axes=(1,0)),np.tensordot(np.conjugate(self.Gs[B]),self.SVMs[B],axes=(2,0)),axes=(3,1))
                R=np.tensordot(EnvR,R,axes=([1,3,5],[0,1,2]))
        return E

""" 
class iTEBD:
    def __init__(self):
    
    def time_evolution(self):  
"""        

class fDMRG:
    def __init__(self,MPO,Gs,N,d,chi,tolerance=1e-12,maxsweep=200):
        self.MPO=MPO
        self.Gs=Gs
        self.N=N
        self.d=d
        self.chi=chi
        self.tolerance=tolerance
        self.maxsweep=maxsweep
        
    def _initialize_Env(self):
        L=[None]*(self.N-1) ; R=[None]*(self.N-1)
        for site in xrange(self.N-1):
            if site==0:
                EnvL=tn.transfer_operator(self.Gs[site],self.MPO(site))             
            else:    
                EnvL=self._update_EnvL(EnvL,site)            
            L[site]=EnvL                       
        for site in xrange(self.N-1,0,-1):
            if site==self.N-1:
                EnvR=tn.transfer_operator(self.Gs[site],self.MPO(site))
            else:
                EnvR=self._update_EnvR(EnvR,site)            
            R[site]=EnvR      
        return L,R
        
    def _update_EnvL(self,EnvL,site):
        M=self.MPO(site)
        if site==self.N-1:
            EnvL=np.tensordot(np.tensordot(np.tensordot(EnvL,self.Gs[site],axes=(0,1)),M,axes=([0,2],[1,0])),np.conjugate(self.Gs[site]),axes=([0,1],[1,0]))
        else:
            EnvL=np.tensordot(np.tensordot(np.tensordot(EnvL,self.Gs[site],axes=(0,0)),M,axes=([0,2],[1,0])),np.conjugate(self.Gs[site]),axes=([0,2],[0,1]))
        return EnvL

    def _update_EnvR(self,EnvR,site):
        M=self.MPO(site)
        if site==0: 
            EnvR=np.tensordot(np.tensordot(np.tensordot(EnvR,self.Gs[site],axes=(0,1)),M,axes=([0,2],[1,0])),np.conjugate(self.Gs[site]),axes=([0,1],[1,0]))   
        else:
            EnvR=np.tensordot(np.tensordot(np.tensordot(EnvR,self.Gs[site],axes=(0,2)),M,axes=([0,3],[3,0])),np.conjugate(self.Gs[site]),axes=([0,3],[2,1]))
        return EnvR    

    def _effH(self,L,R,site):
        M=self.MPO(site)
        if site==0:
            dimH=self.d*self.Gs[site].shape[1]
            H=np.tensordot(M,R[self.N-2-site],axes=(1,1))
            H=np.swapaxes(H,1,2)
        elif site==self.N-1:
            dimH=self.d*self.Gs[site].shape[1]
            H=np.tensordot(L[site-1],M,axes=(1,1))
            H=np.swapaxes(H,1,2)              
        else:
            dimH=self.d*self.Gs[site].shape[0]*self.Gs[site].shape[2]
            H=np.tensordot(L[site-1],np.tensordot(M,R[self.N-2-site],axes=(3,1)),axes=(1,1))
            H=np.swapaxes(H,1,3)
            H=np.swapaxes(H,2,4)
            H=np.swapaxes(H,1,4)
        H=np.ndarray.reshape(H,(dimH,dimH))
        psi=np.ndarray.reshape(self.Gs[site],(dimH,1))
        return H,psi
    
    def _effHpsi(self,L,R,site):
        M=self.MPO(site)     
        def H_matvec(X):
            G=np.ndarray.reshape(X,self.Gs[site].shape)
            if site==0:
                matvec=np.tensordot(np.tensordot(R[self.N-2-site],G,axes=(0,1)),M,axes=([2,0],[0,1]))
                matvec=np.swapaxes(matvec,0,1)
            elif site==self.N-1:
                matvec=np.tensordot(np.tensordot(L[site-1],G,axes=(0,1)),M,axes=([2,0],[0,1]))
                matvec=np.swapaxes(matvec,0,1)
            else:
                matvec=np.tensordot(np.tensordot(np.tensordot(L[site-1],G,axes=(0,0)),M,axes=([0,2],[1,0])),R[self.N-2-site],axes=([1,3],[0,1]))
            matvec=np.ndarray.reshape(matvec,X.shape)
            return matvec
        psi=np.ndarray.reshape(self.Gs[site],(self.Gs[site].size,1))
        return H_matvec,psi
        
    def variational_optimize(self,show_stats=True,return_stats=True):
        L,R=self._initialize_Env()
        E0=0.0 ; t0=time.clock()
        for sweep in xrange(1,self.maxsweep):
            #--------------------------------------------------------------------------------------------
            # Right Sweep         
            for site in xrange(self.N-1):
                # construct effH & diagonalize it; psi is an initial guess of eigenvector    
                E,theta=linalg.eigshmv(*self._effHpsi(L,R,site))
                E/=self.N
                if show_stats:
                    print "site%d," % site,"E/N= %.12f" % E
                # SVD
                if site==0:
                    theta=np.ndarray.reshape(theta,(self.d,self.Gs[site].shape[1])) 
                else:    
                    theta=np.ndarray.reshape(theta,(self.d*self.Gs[site].shape[0],self.Gs[site].shape[2]))                       
                X,S,Y=np.linalg.svd(theta,full_matrices=False)
                # truncation
                dim=min(len(S),self.chi)
                X=X[:,0:dim] ; S=S[0:dim] ; Y=Y[0:dim,:]
                S=np.diagflat(S/np.linalg.norm(S))
                # form the new configuration               
                if site==self.N-2:
                    self.Gs[site+1]=np.tensordot(self.Gs[site+1],np.dot(S,Y),axes=(1,1))
                else:
                    self.Gs[site+1]=np.tensordot(np.dot(S,Y),self.Gs[site+1],axes=(1,0))                           
                if site==0:                    
                    self.Gs[site]=np.ndarray.reshape(X,(self.d,dim))
                    EnvL=tn.transfer_operator(self.Gs[site],self.MPO(site))
                else:
                    self.Gs[site]=np.ndarray.reshape(X,(self.Gs[site].shape[0],self.d,dim))                                       
                    EnvL=self.update_EnvL(EnvL,site)                   
                L[site]=EnvL                                                     
            # check convergence of right-sweep   
            dE=E0-E ; E0=E
            if show_stats:
                print "sweep %.1f," % (sweep-0.5),"E/N= %.12f," % E,"dE= %.4e" % dE                               
            if self._convergence(sweep-0.5,E,dE):
                sweep=sweep-0.5
                t=(time.clock()-t0)/(sweep*60.0)
                break                       
            #--------------------------------------------------------------------------------------------               
            # Left Sweep
            for site in xrange(self.N-1,0,-1):
                # construct H & diagonalize it; psi is an initial guess of eigenvector                  
                E,theta=linalg.eigshmv(*self._effHpsi(L,R,site))
                E/=self.N
                if show_stats:
                    print "site%d," % site,"E/N= %.12f" % E
                # SVD
                if site==self.N-1:
                    theta=np.ndarray.reshape(theta,(self.Gs[site].shape[1],self.d))    
                else:    
                    theta=np.ndarray.reshape(theta,(self.Gs[site].shape[0],self.d*self.Gs[site].shape[2]))            
                X,S,Y=np.linalg.svd(theta,full_matrices=False)
                # truncation
                dim=min(len(S),self.chi)
                X=X[:,0:dim] ; S=S[0:dim] ; Y=Y[0:dim,:]
                S=np.diagflat(S/np.linalg.norm(S))
                # form the new configuration              
                if site==1:
                    self.Gs[site-1]=np.tensordot(self.Gs[site-1],np.dot(X,S),axes=(1,0))
                else:
                    self.Gs[site-1]=np.tensordot(self.Gs[site-1],np.dot(X,S),axes=(2,0))
                if site==self.N-1:                    
                    self.Gs[site]=np.ndarray.reshape(Y,(self.d,self.Gs[site].shape[1]))
                    EnvR=tn.transfer_operator(self.Gs[site],self.MPO(site))
                else:
                    self.Gs[site]=np.ndarray.reshape(Y,(self.Gs[site].shape[0],self.d,self.Gs[site].shape[2]))                      
                    EnvR=self._update_EnvR(EnvR,site)                                                
                R[self.N-1-site]=EnvR           
            # check convergence of left-sweep
            dE=E0-E ; E0=E
            if show_stats:
                print "sweep %d," % sweep,"E/N= %.12f," % E,"dE= %.4e" % dE                   
            if self._convergence(sweep,E,dE):
                t=(time.clock()-t0)/(sweep*60.0)
                break
            #--------------------------------------------------------------------------------------------
        if return_stats:
            stats=[dE,self.maxsweep,t]
            return E,stats
        else:
            return E
        
    def _convergence(self,sweep,E,dE): # print warning messages and check the convergence of main routine
        warnings.simplefilter("always")        
        if dE < 0.0:
            warnings.warn("ValueWarning: Encounter negative dE=E(sweep-0.5)-E(sweep).")            
        if sweep==self.maxsweep-1 and dE > self.tolerance: 
            warnings.warn("ConvergenceWarning: Convergence is not yet achieved before the maxsweep has reached.")
            return True       
        if 0.0 < dE < self.tolerance:
            self.maxsweep=sweep
            return True
        else:
            return False
"""
class fTEBD:
    def __init__(self):
        
    def time_evolution(self):
"""        
        
