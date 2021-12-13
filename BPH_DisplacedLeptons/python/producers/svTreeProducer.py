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
        #self.out.branch("sv_pt", "F")

        self.out.branch("muon_trig_by_ip_pt", "F")
        self.out.branch("muon_trig_by_ip_eta", "F")
        self.out.branch("muon_trig_by_ip_phi", "F")
        self.out.branch("muon_trig_by_ip_iso", "F")
        self.out.branch("muon_trig_by_ip_dxy", "F")
        self.out.branch("muon_trig_by_ip_dxyErr", "F")

        self.out.branch("muon_trig_by_pt_pt", "F")
        self.out.branch("muon_trig_by_pt_eta", "F")
        self.out.branch("muon_trig_by_pt_phi", "F")
        self.out.branch("muon_trig_by_pt_iso", "F")
        self.out.branch("muon_trig_by_pt_dxy", "F")
        self.out.branch("muon_trig_by_pt_dxyErr", "F")

        self.out.branch("muon_ntrig_ip_1_pt", "F")
        self.out.branch("muon_ntrig_ip_1_eta", "F")
        self.out.branch("muon_ntrig_ip_1_phi", "F")
        self.out.branch("muon_ntrig_ip_1_iso", "F")
        self.out.branch("muon_ntrig_ip_1_dxy", "F")
        self.out.branch("muon_ntrig_ip_1_dxyErr", "F")

        self.out.branch("muon_ntrig_ip_2_pt", "F")
        self.out.branch("muon_ntrig_ip_2_eta", "F")
        self.out.branch("muon_ntrig_ip_2_phi", "F")
        self.out.branch("muon_ntrig_ip_2_iso", "F")
        self.out.branch("muon_ntrig_ip_2_dxy", "F")
        self.out.branch("muon_ntrig_ip_2_dxyErr", "F")

        self.out.branch("muon_ntrig_pt_1_pt", "F")
        self.out.branch("muon_ntrig_pt_1_eta", "F")
        self.out.branch("muon_ntrig_pt_1_phi", "F")
        self.out.branch("muon_ntrig_pt_1_iso", "F")
        self.out.branch("muon_ntrig_pt_1_dxy", "F")
        self.out.branch("muon_ntrig_pt_1_dxyErr", "F")

        self.out.branch("muon_ntrig_pt_2_pt", "F")
        self.out.branch("muon_ntrig_pt_2_eta", "F")
        self.out.branch("muon_ntrig_pt_2_phi", "F")
        self.out.branch("muon_ntrig_pt_2_iso", "F")
        self.out.branch("muon_ntrig_pt_2_dxy", "F")
        self.out.branch("muon_ntrig_pt_2_dxyErr", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

        #n = 10

        #self.out.fillBranch("counter", n)
        #self.out.fillBranch("double_counter", 30)
        #self.out.fillBranch("double_counter", 10)

        #_all_svs    = Collection(event, 'SV')
        _all_muons  = Collection(event, 'Muon')
        _trig_muons = Collection(event, 'Muon')
        _lead_muons = Collection(event, 'Muon')

        secondary_vertices     = []
        muons                  = []
        muons_by_ip_           = []
        muons_by_pt_           = []
        muons_noTrig_by_ip_    = []
        muons_noTrig_by_pt_    = []

        #for sv in _all_svs:
        #    secondary_vertices.append(sv)

        for muon in _all_muons:
            #apply cuts here
            if muon.eta > 2.4:
                continue
            if muon.tightId == False:
                continue
            if muon.isGlobal == False:
                continue
 
            muons.append(muon)
            muons_by_ip_.append(muon)
            muons_by_pt_.append(muon)
            
        muons_by_ip = sorted(muons_by_ip_,key=lambda x: x.dxy, reverse=True)
        muons_by_pt = sorted(muons_by_pt_,key=lambda x: x.pt, reverse=True)

        count_ip = 0 
        ind_trig_mu_ip = -1

        # fills branches of leading, trig muons by IP
        for muon in muons_by_ip:
            if muon.isTriggering == True:
                ind_trig_mu_ip = count_ip
                print("inside if true")
            else:
                muons_noTrig_by_ip_.append(muon)
            count_ip = count_ip+1
            print(count_ip, ind_trig_mu_ip)
        if ind_trig_mu_ip != -1:
            self.out.fillBranch("muon_trig_by_ip_pt", muons_by_ip[ind_trig_mu_ip].pt)
            self.out.fillBranch("muon_trig_by_ip_eta", muons_by_ip[ind_trig_mu_ip].eta)
            self.out.fillBranch("muon_trig_by_ip_phi", muons_by_ip[ind_trig_mu_ip].phi)
            self.out.fillBranch("muon_trig_by_ip_iso", muons_by_ip[ind_trig_mu_ip].pfRelIso04_custom)
            self.out.fillBranch("muon_trig_by_ip_dxy", muons_by_ip[ind_trig_mu_ip].dxy)
            self.out.fillBranch("muon_trig_by_ip_dxyErr", muons_by_ip[ind_trig_mu_ip].dxyErr)

        count_pt = 0
        ind_trig_mu_pt = -1

        # fills branches of leading, trig muons by pT
        for muon in muons_by_pt:
            if muon.isTriggering == True:
                ind_trig_mu_pt = count_pt
                print("inside by pT, if true")
            else:
                muons_noTrig_by_pt_.append(muon)
            count_pt = count_pt+1
            print(count_pt, ind_trig_mu_pt)
        if ind_trig_mu_pt != -1:
            self.out.fillBranch("muon_trig_by_pt_pt", muons_by_pt[ind_trig_mu_pt].pt)
            self.out.fillBranch("muon_trig_by_pt_eta", muons_by_pt[ind_trig_mu_pt].eta)
            self.out.fillBranch("muon_trig_by_pt_phi", muons_by_pt[ind_trig_mu_pt].phi)
            self.out.fillBranch("muon_trig_by_pt_iso", muons_by_pt[ind_trig_mu_pt].pfRelIso04_custom)
            self.out.fillBranch("muon_trig_by_pt_dxy", muons_by_pt[ind_trig_mu_pt].dxy)
            self.out.fillBranch("muon_trig_by_pt_dxyErr", muons_by_pt[ind_trig_mu_pt].dxyErr)

        # fills branches of leading and subleading, ntrig muons by IP
        for muon in muons_noTrig_by_ip_:
            self.out.fillBranch("muon_ntrig_ip_1_pt", muons_noTrig_by_ip_[0].pt)
            self.out.fillBranch("muon_ntrig_ip_1_eta", muons_noTrig_by_ip_[0].eta)
            self.out.fillBranch("muon_ntrig_ip_1_phi", muons_noTrig_by_ip_[0].phi)
            self.out.fillBranch("muon_ntrig_ip_1_iso", muons_noTrig_by_ip_[0].pfRelIso04_custom)
            self.out.fillBranch("muon_ntrig_ip_1_dxy", muons_noTrig_by_ip_[0].dxy)
            self.out.fillBranch("muon_ntrig_ip_1_dxyErr", muons_noTrig_by_ip_[0].dxyErr)

            if len(muons_noTrig_by_ip_) > 1:
                self.out.fillBranch("muon_ntrig_ip_2_pt", muons_noTrig_by_ip_[1].pt)
                self.out.fillBranch("muon_ntrig_ip_2_eta", muons_noTrig_by_ip_[1].eta)
                self.out.fillBranch("muon_ntrig_ip_2_phi", muons_noTrig_by_ip_[1].phi)
                self.out.fillBranch("muon_ntrig_ip_2_iso", muons_noTrig_by_ip_[1].pfRelIso04_custom)
                self.out.fillBranch("muon_ntrig_ip_2_dxy", muons_noTrig_by_ip_[1].dxy)
                self.out.fillBranch("muon_ntrig_ip_2_dxyErr", muons_noTrig_by_ip_[1].dxyErr)

        # fills branches of leading and subleading, ntrig muons by pT
        for muon in muons_noTrig_by_pt_:
            self.out.fillBranch("muon_ntrig_pt_1_pt", muons_noTrig_by_pt_[0].pt)
            self.out.fillBranch("muon_ntrig_pt_1_eta", muons_noTrig_by_pt_[0].eta)
            self.out.fillBranch("muon_ntrig_pt_1_phi", muons_noTrig_by_pt_[0].phi)
            self.out.fillBranch("muon_ntrig_pt_1_iso", muons_noTrig_by_pt_[0].pfRelIso04_custom)
            self.out.fillBranch("muon_ntrig_pt_1_dxy", muons_noTrig_by_pt_[0].dxy)
            self.out.fillBranch("muon_ntrig_pt_1_dxyErr", muons_noTrig_by_pt_[0].dxyErr)

            if len(muons_noTrig_by_pt_) > 1:
                self.out.fillBranch("muon_ntrig_pt_2_pt", muons_noTrig_by_pt_[1].pt)
                self.out.fillBranch("muon_ntrig_pt_2_eta", muons_noTrig_by_pt_[1].eta)
                self.out.fillBranch("muon_ntrig_pt_2_phi", muons_noTrig_by_pt_[1].phi)
                self.out.fillBranch("muon_ntrig_pt_2_iso", muons_noTrig_by_pt_[1].pfRelIso04_custom)
                self.out.fillBranch("muon_ntrig_pt_2_dxy", muons_noTrig_by_pt_[1].dxy)
                self.out.fillBranch("muon_ntrig_pt_2_dxyErr", muons_noTrig_by_pt_[1].dxyErr)


        #for sv in secondary_vertices:

        #    # TODO: reco sv properties
        #    self.out.fillBranch("sv_pt", sv.pt)
        
        self.out.fill()
        # return False here as we have already filled the tree manually
        return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def svTree():
    return SVTreeProducer()
