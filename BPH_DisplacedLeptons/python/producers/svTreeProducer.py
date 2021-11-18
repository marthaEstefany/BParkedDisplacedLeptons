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
        self.isMC = bool(inputTree.GetBranch('genWeight'))

        self.out = wrappedOutputTree

        # NOTE: branch names must start with a lower case letter
        # check keep_and_drop_output.txt

        # reco properties
        self.out.branch("sv_pt", "F")
        self.out.branch("muon_pt", "F")
        self.out.branch("muon_pt_triggering", "F")
        self.out.branch("muon_dxy", "F")
        self.out.branch("muon_dxyErr", "F")
        self.out.branch("muon_eta", "F")
        self.out.branch("muon_mass", "F")
        self.out.branch("muon_iso", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

        _all_svs    = Collection(event, 'SV')
        _all_muons  = Collection(event, 'Muon')
        _trig_muons = Collection(event, 'Muon')

        secondary_vertices     = []
        muons                  = []
        muons_triggering       = []
        muons_by_ip_           = []

        for sv in _all_svs:
            # do not consider SVs inside jets
            #if closest(sv, jets)[1] < 0.4:
            #    continue
            #sv.gen = _NullObject()
            #sv.hadron_flavor = 0
            #if sv.pt < 10.:
            #    continue
            secondary_vertices.append(sv)

        for muon in _all_muons:
            #apply cuts here
            muons.append(muon)
            muons_by_ip_.append(muon)
            self.out.fillBranch("muon_pt", muon.pt)
            self.out.fillBranch("muon_dxy", muon.dxy)
            self.out.fillBranch("muon_dxyErr", muon.dxyErr)
            self.out.fillBranch("muon_eta", muon.eta)
            self.out.fillBranch("muon_mass", muon.mass)
            self.out.fillBranch("muon_iso", muon.pfRelIso04_custom)

        mouns_by_ip = sorted(muons_by_ip_,key=lambda x: x.dxy, reverse=True)

        for muon in _trig_muons:
            if muon.isTriggering == False:
                continue
            muons_triggering.append(muon)
            self.out.fillBranch("muon_pt_triggering", muon.pt)

        # assign each b/c hadron uniquely to the "best-matched" SV
        # TODO: criteria for "best-match": deltaR? else?
        #self._selectHadrons(event)
        #sv_unmatched = set(secondary_vertices)
        #for gp in event.bHadrons + event.cHadrons:
        #    sv, dr = closest(gp, sv_unmatched)
        #    if dr < 0.4:
        #        # TODO: check the threshold
        #        sv.gen = gp
        #        sv.hadron_flavor = 5 if gp in event.bHadrons else 4
        #        sv.dr_gen = dr
        #        sv_unmatched.remove(sv)

        for sv in secondary_vertices:

            # TODO: reco sv properties
            self.out.fillBranch("sv_pt", sv.pt)

            # manually fill the tree here as we want to have one SV per row
            #self.out.fill()
        
        self.out.fill()
        # return False here as we have already filled the tree manually
        return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def svTree():
    return SVTreeProducer()
