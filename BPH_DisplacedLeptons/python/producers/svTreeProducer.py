import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from ..helpers.utils import deltaPhi, deltaR, deltaR2, closest, polarP4, sumP4, get_subjets, transverseMass, minValue, configLogger
from ..helpers.triggerHelper import passTrigger

import logging
logger = logging.getLogger('nano')
configLogger('nano', loglevel=logging.INFO)

lumi_dict = {2016: 35.92, 2017: 41.53, 2018: 59.74}


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


class SVTreeProducer(Module):

    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #self.isMC = bool(inputTree.GetBranch('genWeight'))

        self.out = wrappedOutputTree

        # NOTE: branch names must start with a lower case letter
        # check keep_and_drop_output.txt

        self.out.branch("counter","I")
        self.out.branch("double_counter", "I")

        # reco properties
        self.out.branch("sv_pt", "F")
        self.out.branch("muon_pt", "F")
        self.out.branch("muon_pt_triggering", "F")
        self.out.branch("muon_dxy", "F")
        self.out.branch("muon_dxyErr", "F")
        self.out.branch("muon_eta", "F")
        self.out.branch("muon_mass", "F")
        self.out.branch("muon_iso", "F")

        self.out.branch("Trig_muon_pt", "F")
        self.out.branch("Trig_muon_dxy", "F")
        self.out.branch("Trig_muon_dxyErr", "F")
        self.out.branch("Trig_muon_eta", "F")
        self.out.branch("Trig_muon_mass", "F")
        self.out.branch("Trig_muon_iso", "F")

        self.out.branch("noTrig_muon_pt", "F")
        self.out.branch("noTrig_muon_dxy", "F")
        self.out.branch("noTrig_muon_dxyErr", "F")
        self.out.branch("noTrig_muon_eta", "F")
        self.out.branch("noTrig_muon_mass", "F")
        self.out.branch("noTrig_muon_iso", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

        self.out.fillBranch("counter", 10)
        self.out.fillBranch("double_counter", 30)
        self.out.fillBranch("double_counter", 10)

        _all_svs    = Collection(event, 'SV')
        _all_muons  = Collection(event, 'Muon')
        _trig_muons = Collection(event, 'Muon')
        _lead_muons = Collection(event, 'Muon')

        secondary_vertices     = []
        muons                  = []
        muons_triggering       = []
        muons_by_ip_           = []
        muons_noTrig           = []
        muon_noTrig_ptLead     = []

        for sv in _all_svs:
            secondary_vertices.append(sv)

        for muon in _all_muons:
            #apply cuts here
            if muon.eta > 2.4:
                continue
            if muon.tightId == False:
                continue
            if muon.isGlobal == False:
                continue
            # add deltaR
            # add cosA
 
            muons.append(muon)
            muons_by_ip_.append(muon)
            self.out.fillBranch("muon_pt", muon.pt)
            self.out.fillBranch("muon_dxy", muon.dxy)
            self.out.fillBranch("muon_dxyErr", muon.dxyErr)
            self.out.fillBranch("muon_eta", muon.eta)
            self.out.fillBranch("muon_mass", muon.mass)
            self.out.fillBranch("muon_iso", muon.pfRelIso04_custom)

        print("nMuons:", len(muons))
        mouns_by_ip = sorted(muons_by_ip_,key=lambda x: x.dxy, reverse=True)

        for muon in _trig_muons:
            if muon.isTriggering == False:
                continue
            if muon.eta > 2.4:
                continue
            if muon.tightId == False:
                continue
            if muon.isGlobal == False:
                continue
            muons_triggering.append(muon)
            self.out.fillBranch("muon_pt_triggering", muon.pt)
            self.out.fillBranch("Trig_muon_pt", muon.pt)
            self.out.fillBranch("Trig_muon_dxy", muon.dxy)
            self.out.fillBranch("Trig_muon_dxyErr", muon.dxyErr)
            self.out.fillBranch("Trig_muon_eta", muon.eta)
            self.out.fillBranch("Trig_muon_mass", muon.mass)
            self.out.fillBranch("Trig_muon_iso", muon.pfRelIso04_custom)

        print("TrigMuons:", len(muons_triggering))

        for muon in _all_muons:
            if muon.isTriggering == True:
                continue
            if muon.eta > 2.4:
                continue
            if muon.tightId == False:
                continue
            if muon.isGlobal == False:
                continue
            muons_noTrig.append(muon)
            self.out.fillBranch("noTrig_muon_pt", muon.pt)
            self.out.fillBranch("noTrig_muon_dxy", muon.dxy)
            self.out.fillBranch("noTrig_muon_dxyErr", muon.dxyErr)
            self.out.fillBranch("noTrig_muon_eta", muon.eta)
            self.out.fillBranch("noTrig_muon_mass", muon.mass)
            self.out.fillBranch("noTrig_muon_iso", muon.pfRelIso04_custom)

        muons_noTrig_by_pt = sorted(muons_noTrig,key=lambda x: x.pt, reverse=True)
        muons_noTrig_by_d0 = sorted(muons_noTrig,key=lambda x: x.dxy, reverse=True)

        for sv in secondary_vertices:

            # TODO: reco sv properties
            self.out.fillBranch("sv_pt", sv.pt)
        
        self.out.fill()
        # return False here as we have already filled the tree manually
        return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def svTree():
    return SVTreeProducer()
