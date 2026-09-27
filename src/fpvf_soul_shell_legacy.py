"""Legacy FPVF / Soul-Shell proof-of-concept extraction.

Source: docs/LEGACY_SOUL_SHELL_SOURCE.md
Status: research candidate; not canonical; not evidence of consciousness.

This module preserves the executable structure while making heuristic choices explicit.
"""
from math import sin, pi, exp
PHI=(1+5**0.5)/2

class FPVFSystem:
    def __init__(self,condensation=1.0,alpha=0.0,phase=0.0):
        self.condensation=condensation; self.alpha=alpha; self.phase=phase
        self.state=dict(n=0,R=0.0,RSCS_int=1.0,RSCS_ext=1.0,ID=0.0,R_void=0.0,memory=[],M_phi=0.0,P_self=0.0)

    def phi(self,n):
        raw=self.condensation*(PHI**n)*sin(self.phase+pi*n/PHI)
        return raw/(1.0+abs(raw))

    def theta(self,n):
        return (self.phi(n)+1.0)*pi

    def kappa(self,n):
        return self.phi(n+1)-self.phi(n)

    def equilibrium(self,rscs_int,rscs_ext):
        # Legacy/model score, not canonical LightMathematics RSCS.
        return 1.0-(abs(rscs_ext-rscs_int)/max(1e-9,rscs_ext+rscs_int))

    def update_memory(self,R_i,phi_i,perspective_weight=1.0):
        # In-process list only; this does not establish persistent memory.
        self.state["memory"].append((R_i,phi_i,perspective_weight))
        self.state["M_phi"]+=R_i*phi_i
        return sum(R*p*w for R,p,w in self.state["memory"])

    def P_self_step(self,dt,rscs_t,phi_t,t):
        legacy_lag=1.0 # historical placeholder; NOT canonical processing lag
        self.state["P_self"]+=(rscs_t*phi_t)*exp(self.alpha*t)*(dt/max(1e-9,legacy_lag))

    def void_gate(self,R,R_void):
        V=R-R_void
        return V,abs(V)>1.0 # heuristic threshold from source

    def identity_step(self,rscs_n,self_weight=1.0):
        # "ID" is a model accumulator, not evidence of personal identity.
        self.state["ID"]+=rscs_n*self_weight

    def ignition(self,Fi,Pi,rscs):
        return Fi*Pi*rscs

    def intention_fork(self,I_prev,I_curr):
        return I_curr-I_prev

    def step(self,A,B,Fi=1.0,Pi=1.0,R_void=0.0,dt=1.0,t=0.0):
        s=self.state;n=s["n"];ri,re=s["RSCS_int"],s["RSCS_ext"]
        rho=re/max(1e-9,ri);Eq=self.equilibrium(ri,re)
        delta=0.1*Eq;R_next=s["R"]-delta*(A-B)
        p=self.phi(n);k=self.kappa(n);theta=self.theta(n);fpvf=ri*p
        if Eq>0.9:k=max(-0.05,min(0.05,k))
        m=self.update_memory(s["R"],p,rho);self.P_self_step(dt,ri,p,t)
        V,collapse=self.void_gate(R_next,R_void)
        if collapse:
            delta*=0.2;R_next=s["R"]-delta*(A-B)
        self.identity_step(ri)
        Ev=self.ignition(Fi,Pi,ri);I_curr=ri*p;dP=Ev*self.intention_fork(0,I_curr)
        S=I_curr+s["M_phi"]+s["P_self"]+(re-ri)+R_void
        H=S*fpvf;C=S+fpvf;arc0=1.0/(1.0+abs(n));deltaR=(R_next-s["R"])*arc0
        s.update(n=n+1,R=R_next,R_void=R_void,last=dict(Eq=Eq,rho=rho,phi=p,kappa=k,theta=theta,FPVF=fpvf,M_FPVF=m,P_self=s["P_self"],V=V,collapse=collapse,Ev=Ev,dP=dP,S=S,H=H,C=C,deltaR=deltaR))
        return s["last"]
