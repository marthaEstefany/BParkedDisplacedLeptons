from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True


class lepSFProducer(Module):
    def __init__(self):
        muonSelectionTag="LooseWP_2016"
        electronSelectionTag="GPMVA90_2016"
        if muonSelectionTag == "LooseWP_2016":
            mu_f = ["scaleFactor_results_cat_pt_eta_fit.root", "Mu_ID.root", "Mu_Iso.root"] #, "Mu_ID.root", "Mu_Iso.root"
            mu_h = [
                "hist_scale_factor",
                "MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio",
                "LooseISO_LooseID_pt_eta/pt_abseta_ratio"
            ]
        if electronSelectionTag == "GPMVA90_2016":
            el_f = ["EGM2D_eleGSF.root", "EGM2D_eleMVA90.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]
        mu_f = [
            "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in mu_f
        ]
        el_f = [
            "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in el_f
        ]

        self.mu_f = ROOT.std.vector(str)(len(mu_f))
        self.mu_h = ROOT.std.vector(str)(len(mu_f))
        for i in range(len(mu_f)):
            self.mu_f[i] = mu_f[i]
            self.mu_h[i] = mu_h[i]
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        for i in range(len(el_f)):
            self.el_f[i] = el_f[i]
            self.el_h[i] = el_h[i]
       # Try to load module via python dictionaries
        ROOT.gSystem.Load("/uscms/homes/a/alesauva/work/CMSSW_12_0_1/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector_cc.so")
        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries(
        ):
            print("aL Load C++ Worker")
            print("AL path", os.environ['CMSSW_BASE'], "/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+")
            ROOT.gROOT.ProcessLine(
                ".L %s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+"
                % os.environ['CMSSW_BASE'])
        ROOT.gSystem.Load("/uscms/homes/a/alesauva/work/CMSSW_12_0_1/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector_cc.so")
        ROOT.gSystem.Load("%s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector_cc.so" % os.environ['CMSSW_BASE'])

    def beginJob(self):
        self._worker_mu = ROOT.LeptonEfficiencyCorrector(self.mu_f, self.mu_h)
        self._worker_el = ROOT.LeptonEfficiencyCorrector(self.el_f, self.el_h)

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_effTrig_Trig", "F")
        for sort in ["iso","IP","pt","dz"]:
           self.out.branch("Muon_effTrig_nTrig_%s" % (sort), "F")
        #self.out.branch("Electron_effSF", "F", lenVar="nElectron")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muon_trigger=[]
        muon_Ntrigger=[]
        muons = Collection(event, "Muon")
       # electrons = Collection(event, "Electron")
      #  sf_el = [
      #      self._worker_el.getSF(el.pdgId, el.pt, el.eta) for el in electrons
      #  ]
        for muon in muons:
           if (abs(muon.eta) < 2.4) and (muon.tightId == True) and (muon.isGlobal == True) and not((0.3< muon.eta <1.2) & (0.4 < muon.phi <0.8) ):
               if muon.isTriggering ==True:
                  muon_trigger.append(muon)
               else:
                  muon_Ntrigger.append(muon)
        self.out.fillBranch("Muon_effTrig_Trig", self._worker_mu.getSF(muon_trigger[0].pdgId, muon_trigger[0].pt, muon_trigger[0].eta))
        #print("AL test:", self._worker_mu.getSF(muon_trigger[0].pdgId, muon_trigger[0].pt, muon_trigger[0].eta))
        if len(muon_trigger)>1:
           for var_subtrig in ["iso","IP","pt","dz"]:
              self.out.fillBranch("Muon_effTrig_nTrig_%s" % (var_subtrig), self._worker_mu.getSF(muon_trigger[1].pdgId, muon_trigger[1].pt, muon_trigger[1].eta))
        else:
           #Filling non-triggering muon depending on variables
           muons_by_IP = sorted(muon_Ntrigger,key=lambda x: x.dxy, reverse=True)
           muons_by_iso = sorted(muon_Ntrigger,key=lambda x: x.pfRelIso04_custom)
           #muons_by_cosA=sorted(muon_Ntrigger, key=lambda x: abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)))
           #print("cosA=", [abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)) for x in muon_Ntrigger])
           #print("muons_bycosa", muons_by_cosA)
           #muons_by_dR=sorted(muon_Ntrigger, key=lambda x: deltaR(muon_trigger[0].phi,muon_trigger[0].eta,x.phi,x.eta), reverse=True)
           muons_by_pt = sorted(muon_Ntrigger,key=lambda x: x.pt, reverse=True)
           muons_by_dz = sorted(muon_Ntrigger,key=lambda x: x.dz, reverse=True)
           self.out.fillBranch("nTriggering_iso_muon_isTriggering", muons_by_iso[0].isTriggering)
           for var_sub in ["iso","IP","pt","dz"]:
              str=("muons_by_%s" % (var_sub))
              muon_to_use=locals()[str][0]
              self.out.fillBranch("Muon_effTrig_nTrig_%s" % (var_sub), self._worker_mu.getSF(muon_to_use.pdgId, muon_to_use.pt, muon_to_use.eta))
       # self.out.fillBranch("Electron_effSF", sf_el)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid
# having them loaded when not needed

lepSF = lambda: lepSFProducer("LooseWP_2016", "GPMVA90_2016")
