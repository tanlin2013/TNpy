"""
This file contains the fundamental functions for the Matrix Product State (MPS) operations. 
"""

import numpy as np
from scipy import sparse
import Primme

class MPS:   
    def __init__(self,d,chi):
        """
        * Parameters:
            * d: int
                The physical bond dimension which is associated to the dimension of single-particle Hilbert space.
            * chi: int
                The visual bond dimension to be keep after the Singular Value Decomposition (SVD).               
        """
        self.d=d
        self.chi=chi
        
    def initialize_MPS(self,whichMPS,canonical_form=None,size=None):
        """
        Randomly initialize the MPS.
    
        * Parameters:
            * whichMPS: string, {'i','f'} 
                If whichMPS='i', an infinite MPS is initialized. Otherwise if whichMPS='f', a finite MPS is created.            
            * canonical_form: string, {'L','R','GL'}, optional
                If whichMPS='f', fMPS can be represented as left-normalized, right-normalized or the standard (Gamma-Lambda representation) MPS.
            * size: int, optional
                If whichMPS='f', the size of system is needed. 
        
        * Returns: 
            * Gs: list of ndarray
                A list of rank-3 tensors which represents the MPS. The order of tensor is (chi,d,chi) or (d,chi) for the boundaries if fMPS is considered.  
            * SVMs: list of ndarray
                A list of singular value matrices. SVMs is always return for iMPS. But, for the fMPS SVMs only return when canonical_form='GL'.
        """
        
        """ Check the input variables"""
        if whichMPS=='f': 
            if cononical_form is None or size is None:
                raise ValueError('canonical_form and size must be specified when whichMPS='f'.')        
        
        Gs=[] ; SVMs=[]
        if whichMPS=='i':
            """ Create the iMPS """
            for site in range(2):
                Gs.append(np.random.rand(self.chi,self.d,self.chi))
                SVMs.append(np.diagflat(np.random.rand(self.chi)))
            return Gs,SVMs    
        elif whichMPS=='f':
            """ Create the fMPS in the standard (GL) representation """
            size_parity=size%2
            for site in range(size):        
                if size_parity==0:
                    if site==0 or site==size-1:
                        Gs.append(np.random.rand(self.d,min(self.d,self.chi)))
                    elif site<=size/2-1 and site!=0:
                        Gs.append(np.random.rand(min(self.d**site,self.chi),self.d,min(self.d**(site+1),self.chi)))
                    elif site>size/2-1 and site!=size-1:
                        Gs.append(np.random.rand(min(self.d**(size-site),self.chi),self.d,min(self.d**(size-1-site),self.chi)))
                elif size_parity==1:
                    if site==0 or site==size-1:
                        Gs.append(np.random.rand(self.d,min(self.d,self.chi)))
                    elif site<size/2 and site!=0:
                        Gs.append(np.random.rand(min(self.d**site,self.chi),self.d,min(self.d**(site+1),self.chi)))
                    elif site==size/2:
                        Gs.append(np.random.rand(min(self.d**site,self.chi),self.d,min(self.d**site,self.chi)))
                    elif site>size/2 and site!=size-1:
                        Gs.append(np.random.rand(min(self.d**(size-site),self.chi),self.d,min(self.d**(size-1-site),self.chi)))
            """ Left- or right-normalized the MPS """
            if canonical_form=='L':
                
                return Gs
            elif canonical_form=='R':
                
                return Gs
            elif canonical_form=='GL':                
                return Gs,SVMs
            else:
                raise ValueError('Only the standard (GL), Left- and Right-normalized canonical form are supported.')    
        else:
            raise ValueError('Only iMPS and fMPS are supported.')        
    
    def normalize_MPS(self,Gs,SVMs,order):
        """
        An helper function of initialize_MPS(). Left or Right normalize the MPS.
        
        * Parameters:
        * Returns:
        """
        return
    
    def initialize_EnvLs(self,whichMPS):
        """
        Create an initial left enviroment for either iDMRG or fDMRG algorithm.
        """
        return
    
    def initialize_EnvRs(self,whichMPS):
        """
        Create an initial right enviroment for either iDMRG or fDMRG algorithm.
        """
        return    

class contraction: 
    def __int__(self):
        
    def transfer_operator(self):    
        return
    
    def update_EnvLs(self):
        return

    def update_EnvRs(self):
        return
        
def eigensolver(H,psi):
    """
    This function is a warpper of PRIMME function eigsh().
    
    * Parameters:
        * H: ndarray
        * psi: array
    * Returns:
        * evals:
        * evecs:
    """
    A=sparse.csr_matrix(H)
    evals,evecs,stats=Primme.eigsh(A,k=1,which='SA',v0=psi,tol=self.tolerance,return_stats=True)                                    
    return evals[0],evecs

def Trotter_Suzuki_Decomposition():
    """
    """
    return

def inverse_SVM(A):
    """
    Compute the inverse of singular value matrix.
    
    * Parameters:
        A: ndarray
            The singular value matrix wants to be convert.
    * Returns:
        A_inv: ndarray
            The inverse of singular value matrix.
    """
    
    return A_inv
