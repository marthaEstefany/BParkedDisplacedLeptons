import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from ..helpers.utils import deltaPhi, deltaR, deltaR2, closest, polarP4, sumP4, get_subjets, transverseMass, minValue, configLogger
from ..helpers.triggerHelper import passTrigger

import logging
logger = logging.getLogger('nano')
configLogger('nano', loglevel=logging.INFO)

lumi_dict = { 2018: 41.599}


class _NullObject:
    '''An null object which does not store anything, and does not raise exception.'''

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __getattr__(self, name):
        return 0

    def __setattr__(self, name, value):
        pass


class METObject(Object):

    def p4(self):
        return polarP4(self, eta=None, mass=None)


class GMTreeProducer(Module):

    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.isMC = bool(inputTree.GetBranch('genWeight'))

        self.out = wrappedOutputTree

        # NOTE: branch names must start with a lower case letter
        # check keep_and_drop_output.txt

        # reco properties
       
        self.out.branch("muon_pt", "F")
        self.out.branch("isTriggering", "O")
        self.out.branch("muon_dxy", "F")
        self.out.branch("muon_dxyErr", "F")
        self.out.branch("muon_eta", "F")
        self.out.branch("muon_phi", "F")
        self.out.branch("muon_mass", "F")
        #self.out.branch("muon_iso", "F")
        # need px, py, pz to compute cos3D

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

        _all_muons  = Collection(event, 'Muon')
 

        if len(_all_muons)<0:
           return False #Go to next next event, useful as a conditon - Antoine
    
        for muon in _all_muons:

            if muon.eta > 2.4:
                continue
            if muon.tightId == False:
                continue
            if muon.isGlobal == False:
                continue
                 
            self.out.fillBranch("muon_pt", muon.pt)
            self.out.fillBranch("isTriggering", muon.isTriggering)
            self.out.fillBranch("muon_dxy", muon.dxy)
            self.out.fillBranch("muon_dxyErr", muon.dxyErr)
            self.out.fillBranch("muon_eta", muon.eta)
            self.out.fillBranch("muon_phi", muon.phi)
            self.out.fillBranch("muon_mass", muon.mass)
            #self.out.fillBranch("muon_iso", muon.iso)
            self.out.fill()
                  
                         

            
        return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def gmTree():
    return GMTreeProducer()
