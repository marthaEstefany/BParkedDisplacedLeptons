import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from ..helpers.utils import deltaPhi, deltaR, deltaR2, cosA, closest, polarP4, sumP4, get_subjets, transverseMass, minValue, configLogger
from ..helpers.triggerHelper import passTrigger


import logging
logger = logging.getLogger('nano')
configLogger('nano', loglevel=logging.INFO)

lumi_dict = {41.599}


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
        import json
        import re
        with open('metadata.json') as fp:
           md = json.load(fp)

        
        # NOTE: branch names must start with a lower case letter
        # check keep_and_drop_output.txt
        self.out = wrappedOutputTree
        # reco properties
        self.out.branch("Event", "F")
        self.out.branch("muon_N", "F")
        self.out.branch("DeltaR", "F")
        self.out.branch("cosA", "F")
        self.out.branch("Triggering_muon_isTriggering", "O")
        self.out.branch("Triggering_muon_px", "F")
        self.out.branch("Triggering_muon_pz", "F")
        self.out.branch("Triggering_muon_pt", "F")
        self.out.branch("Triggering_muon_dxy", "F")
        self.out.branch("Triggering_muon_dxyErr", "F")
        self.out.branch("Triggering_muon_eta", "F")
        self.out.branch("Triggering_muon_phi", "F")
        self.out.branch("Triggering_muon_mass", "F")
        self.out.branch("Triggering_muon_iso", "F")

        self.out.branch("nTriggering_iso_muon_isTriggering", "O")
        self.out.branch("nTriggering_iso_muon_px", "F")
        self.out.branch("nTriggering_iso_muon_pz", "F")
        self.out.branch("nTriggering_iso_muon_pt", "F")
        self.out.branch("nTriggering_iso_muon_dxy", "F")
        self.out.branch("nTriggering_iso_muon_dxyErr", "F")
        self.out.branch("nTriggering_iso_muon_eta", "F")
        self.out.branch("nTriggering_iso_muon_phi", "F")
        self.out.branch("nTriggering_iso_muon_mass", "F")
        self.out.branch("nTriggering_iso_muon_iso", "F")
        self.out.branch("nTriggering_iso_muon_cosA", "F")
        self.out.branch("nTriggering_iso_muon_deltaR", "F")         

        self.out.branch("nTriggering_IP_muon_isTriggering", "O")
        self.out.branch("nTriggering_IP_muon_px", "F")
        self.out.branch("nTriggering_IP_muon_pz", "F")
        self.out.branch("nTriggering_IP_muon_pt", "F")
        self.out.branch("nTriggering_IP_muon_dxy", "F")
        self.out.branch("nTriggering_IP_muon_dxyErr", "F")
        self.out.branch("nTriggering_IP_muon_eta", "F")
        self.out.branch("nTriggering_IP_muon_phi", "F")
        self.out.branch("nTriggering_IP_muon_mass", "F")
        self.out.branch("nTriggering_IP_muon_iso", "F")
        self.out.branch("nTriggering_IP_muon_cosA", "F")
        self.out.branch("nTriggering_IP_muon_deltaR", "F") 

        self.out.branch("nTriggering_dR_muon_isTriggering", "O")
        self.out.branch("nTriggering_dR_muon_px", "F")
        self.out.branch("nTriggering_dR_muon_pz", "F")
        self.out.branch("nTriggering_dR_muon_pt", "F")
        self.out.branch("nTriggering_dR_muon_dxy", "F")
        self.out.branch("nTriggering_dR_muon_dxyErr", "F")
        self.out.branch("nTriggering_dR_muon_eta", "F")
        self.out.branch("nTriggering_dR_muon_phi", "F")
        self.out.branch("nTriggering_dR_muon_mass", "F")
        self.out.branch("nTriggering_dR_muon_iso", "F")
        self.out.branch("nTriggering_dR_muon_cosA", "F")
        self.out.branch("nTriggering_dR_muon_deltaR", "F") 
  
        self.out.branch("nTriggering_cosA_muon_isTriggering", "O")
        self.out.branch("nTriggering_cosA_muon_px", "F")
        self.out.branch("nTriggering_cosA_muon_pz", "F")
        self.out.branch("nTriggering_cosA_muon_pt", "F")
        self.out.branch("nTriggering_cosA_muon_dxy", "F")
        self.out.branch("nTriggering_cosA_muon_dxyErr", "F")
        self.out.branch("nTriggering_cosA_muon_eta", "F")
        self.out.branch("nTriggering_cosA_muon_phi", "F")
        self.out.branch("nTriggering_cosA_muon_mass", "F")
        self.out.branch("nTriggering_cosA_muon_iso", "F")
        self.out.branch("nTriggering_cosA_muon_cosA", "F")
        self.out.branch("nTriggering_cosA_muon_deltaR", "F")   
        
        #If MC, importe the xs weight from the metadata json file
        self.isMC = bool(inputTree.GetBranch('genWeight'))
        if self.isMC==True:
           print("This is MC")
           # load xsec weight
           print(md['xsecWgt'])
           XSW=0
           converted_in = "{}".format(inputFile)
           #print(converted_in)
           input = re.search('/home/alesauva/CMSSW_10_2_15/src/PhysicsTools/BParkingNano/test/(.+?)/', converted_in).group(1)
           for i in range(len(md['xsecWgt'])):
              if md['xsecWgt'][i][0]==input:
                 XSW=md['xsecWgt'][i][1]
                 print('Loading cross section weight of %s for sample %s' % (XSW,md['xsecWgt'][i][0]))
           self.out.branch("muon_genWeight", "F")
         #  self.out.branch("muon_PUWeight", "F")
           self.out.branch("muon_xsWeight", "F")
           self.out.fillBranch("muon_xsWeight", XSW*41.599) 
          # self.out.branch("muon_SFWeight", "F")
          # self.out.branch("muon_totWeight", "F") 



    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
  

    def analyze(self, event):
        muon_general=[]
        muon_general_Triggering=[]
        muon_trigger=[]
        muon_Ntrigger=[]
   

        _all_muons  = Collection(event, 'Muon')
        #The first loop is for pre-selection
        if event.nMuon<2.0:
           return False
        for muon in _all_muons:
            #apply cuts here
            if (abs(muon.eta) < 2.4) & (muon.tightId == True) & (muon.isGlobal == True):
                muon_general.append(muon)
                if muon.isTriggering==True:
                   muon_general_Triggering.append(muon)
        if (len(muon_general)<2) or (len(muon_general_Triggering)<1):
           return False
        #The second loop is for setting the list of muon for each event
        _all_muons2  = Collection(event, 'Muon')
        for muons in _all_muons2:
            print("AL muon event:", event.event)
            print("AL muon event:", muons.eta, muons.tightId, muons.isGlobal)
            if (abs(muons.eta) < 2.4) & (muons.tightId == True) & (muons.isGlobal == True):
               print("AL istriggering: ", muons.isTriggering)
               if muons.isTriggering ==True:
                  muon_trigger.append(muons)
               else:
                  muon_Ntrigger.append(muons)
               print("Ntrigger muon iso, ip", muons.pfRelIso04_custom, muons.dxy)
        #Filling lead muon = triggering muon
        self.out.fillBranch("Triggering_muon_isTriggering", muon_trigger[0].isTriggering)
        self.out.fillBranch("Triggering_muon_px", muon_trigger[0].px)
        self.out.fillBranch("Triggering_muon_pz", muon_trigger[0].pz)
        self.out.fillBranch("Triggering_muon_pt", muon_trigger[0].pt)
        self.out.fillBranch("Triggering_muon_dxy", muon_trigger[0].dxy)
        self.out.fillBranch("Triggering_muon_dxyErr", muon_trigger[0].dxyErr)
        self.out.fillBranch("Triggering_muon_eta", muon_trigger[0].eta)
        self.out.fillBranch("Triggering_muon_phi", muon_trigger[0].phi)
        self.out.fillBranch("Triggering_muon_mass", muon_trigger[0].mass)
        self.out.fillBranch("Triggering_muon_iso", muon_trigger[0].pfRelIso04_custom)
        if len(muon_trigger)>1:
           print("Event have two triggering muons, will form a pair with both")
           self.out.fillBranch("nTriggering_iso_muon_isTriggering", muon_trigger[1].isTriggering)
           self.out.fillBranch("nTriggering_iso_muon_px", muon_trigger[1].px)
           self.out.fillBranch("nTriggering_iso_muon_pz", muon_trigger[1].pz)
           self.out.fillBranch("nTriggering_iso_muon_pt", muon_trigger[1].pt)
           self.out.fillBranch("nTriggering_iso_muon_dxy", muon_trigger[1].dxy)
           self.out.fillBranch("nTriggering_iso_muon_dxyErr", muon_trigger[1].dxyErr)
           self.out.fillBranch("nTriggering_iso_muon_eta", muon_trigger[1].eta)
           self.out.fillBranch("nTriggering_iso_muon_phi", muon_trigger[1].phi)
           self.out.fillBranch("nTriggering_iso_muon_mass", muon_trigger[1].mass)
           self.out.fillBranch("nTriggering_iso_muon_iso", muon_trigger[1].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_iso_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_trigger[1].px,muon_trigger[1].py,muon_trigger[1].pz))
           self.out.fillBranch("nTriggering_iso_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_trigger[1].phi,muon_trigger[1].eta))          

           self.out.fillBranch("nTriggering_IP_muon_isTriggering", muon_trigger[1].isTriggering)
           self.out.fillBranch("nTriggering_IP_muon_px", muon_trigger[1].px)
           self.out.fillBranch("nTriggering_IP_muon_pz", muon_trigger[1].pz)
           self.out.fillBranch("nTriggering_IP_muon_pt", muon_trigger[1].pt)
           self.out.fillBranch("nTriggering_IP_muon_dxy", muon_trigger[1].dxy)
           self.out.fillBranch("nTriggering_IP_muon_dxyErr", muon_trigger[1].dxyErr)
           self.out.fillBranch("nTriggering_IP_muon_eta", muon_trigger[1].eta)
           self.out.fillBranch("nTriggering_IP_muon_phi", muon_trigger[1].phi)
           self.out.fillBranch("nTriggering_IP_muon_mass", muon_trigger[1].mass)
           self.out.fillBranch("nTriggering_IP_muon_iso", muon_trigger[1].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_IP_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_trigger[1].px,muon_trigger[1].py,muon_trigger[1].pz))
           self.out.fillBranch("nTriggering_IP_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_trigger[1].phi,muon_trigger[1].eta))    

           self.out.fillBranch("nTriggering_dR_muon_isTriggering", muon_trigger[1].isTriggering)
           self.out.fillBranch("nTriggering_dR_muon_px", muon_trigger[1].px)
           self.out.fillBranch("nTriggering_dR_muon_pz", muon_trigger[1].pz)
           self.out.fillBranch("nTriggering_dR_muon_pt", muon_trigger[1].pt)
           self.out.fillBranch("nTriggering_dR_muon_dxy", muon_trigger[1].dxy)
           self.out.fillBranch("nTriggering_dR_muon_dxyErr", muon_trigger[1].dxyErr)
           self.out.fillBranch("nTriggering_dR_muon_eta", muon_trigger[1].eta)
           self.out.fillBranch("nTriggering_dR_muon_phi", muon_trigger[1].phi)
           self.out.fillBranch("nTriggering_dR_muon_mass", muon_trigger[1].mass)
           self.out.fillBranch("nTriggering_dR_muon_iso", muon_trigger[1].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_dR_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_trigger[1].px,muon_trigger[1].py,muon_trigger[1].pz))
           self.out.fillBranch("nTriggering_dR_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_trigger[1].phi,muon_trigger[1].eta))    
  
           self.out.fillBranch("nTriggering_cosA_muon_isTriggering", muon_trigger[1].isTriggering)
           self.out.fillBranch("nTriggering_cosA_muon_px", muon_trigger[1].px)
           self.out.fillBranch("nTriggering_cosA_muon_pz", muon_trigger[1].pz)
           self.out.fillBranch("nTriggering_cosA_muon_pt", muon_trigger[1].pt)
           self.out.fillBranch("nTriggering_cosA_muon_dxy", muon_trigger[1].dxy)
           self.out.fillBranch("nTriggering_cosA_muon_dxyErr", muon_trigger[1].dxyErr)
           self.out.fillBranch("nTriggering_cosA_muon_eta", muon_trigger[1].eta)
           self.out.fillBranch("nTriggering_cosA_muon_phi", muon_trigger[1].phi)
           self.out.fillBranch("nTriggering_cosA_muon_mass", muon_trigger[1].mass)
           self.out.fillBranch("nTriggering_cosA_muon_iso", muon_trigger[1].pfRelIso04_custom) 
           self.out.fillBranch("nTriggering_cosA_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_trigger[1].px,muon_trigger[1].py,muon_trigger[1].pz))
           self.out.fillBranch("nTriggering_cosA_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_trigger[1].phi,muon_trigger[1].eta))      
        else:
           #Filling non-triggering muon depending on variables
           muons_by_ip = sorted(muon_Ntrigger,key=lambda x: x.dxy, reverse=True)
           muons_by_iso = sorted(muon_Ntrigger,key=lambda x: x.pfRelIso04_custom, reverse=True)
           muons_by_cosA=sorted(muon_Ntrigger, key=lambda x: abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)))
           #print("cosA=", [abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)) for x in muon_Ntrigger])
           #print("muons_bycosa", muons_by_cosA)
           muons_by_dR=sorted(muon_Ntrigger, key=lambda x: deltaR(muon_trigger[0].phi,muon_trigger[0].eta,x.phi,x.eta), reverse=True)
           self.out.fillBranch("nTriggering_iso_muon_isTriggering", muons_by_iso[0].isTriggering)
           self.out.fillBranch("nTriggering_iso_muon_px", muons_by_iso[0].px)
           self.out.fillBranch("nTriggering_iso_muon_pz", muons_by_iso[0].pz)
           self.out.fillBranch("nTriggering_iso_muon_pt", muons_by_iso[0].pt)
           self.out.fillBranch("nTriggering_iso_muon_dxy", muons_by_iso[0].dxy)
           self.out.fillBranch("nTriggering_iso_muon_dxyErr", muons_by_iso[0].dxyErr)
           self.out.fillBranch("nTriggering_iso_muon_eta", muons_by_iso[0].eta)
           self.out.fillBranch("nTriggering_iso_muon_phi", muons_by_iso[0].phi)
           self.out.fillBranch("nTriggering_iso_muon_mass", muons_by_iso[0].mass)
           self.out.fillBranch("nTriggering_iso_muon_iso", muons_by_iso[0].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_iso_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muons_by_iso[0].px,muons_by_iso[0].py,muons_by_iso[0].pz))
           self.out.fillBranch("nTriggering_iso_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muons_by_iso[0].phi,muons_by_iso[0].eta))           

           self.out.fillBranch("nTriggering_IP_muon_isTriggering", muons_by_ip[0].isTriggering)
           self.out.fillBranch("nTriggering_IP_muon_px", muons_by_ip[0].px)
           self.out.fillBranch("nTriggering_IP_muon_pz", muons_by_ip[0].pz)
           self.out.fillBranch("nTriggering_IP_muon_pt", muons_by_ip[0].pt)
           self.out.fillBranch("nTriggering_IP_muon_dxy", muons_by_ip[0].dxy)
           self.out.fillBranch("nTriggering_IP_muon_dxyErr", muons_by_ip[0].dxyErr)
           self.out.fillBranch("nTriggering_IP_muon_eta", muons_by_ip[0].eta)
           self.out.fillBranch("nTriggering_IP_muon_phi", muons_by_ip[0].phi)
           self.out.fillBranch("nTriggering_IP_muon_mass", muons_by_ip[0].mass)
           self.out.fillBranch("nTriggering_IP_muon_iso", muons_by_ip[0].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_IP_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muons_by_ip[0].px,muons_by_ip[0].py,muons_by_ip[0].pz))
           self.out.fillBranch("nTriggering_IP_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muons_by_ip[0].phi,muons_by_ip[0].eta))    

           self.out.fillBranch("nTriggering_dR_muon_isTriggering", muons_by_dR[0].isTriggering)
           self.out.fillBranch("nTriggering_dR_muon_px", muons_by_dR[0].px)
           self.out.fillBranch("nTriggering_dR_muon_pz", muons_by_dR[0].pz)
           self.out.fillBranch("nTriggering_dR_muon_pt", muons_by_dR[0].pt)
           self.out.fillBranch("nTriggering_dR_muon_dxy", muons_by_dR[0].dxy)
           self.out.fillBranch("nTriggering_dR_muon_dxyErr", muons_by_dR[0].dxyErr)
           self.out.fillBranch("nTriggering_dR_muon_eta", muons_by_dR[0].eta)
           self.out.fillBranch("nTriggering_dR_muon_phi", muons_by_dR[0].phi)
           self.out.fillBranch("nTriggering_dR_muon_mass", muons_by_dR[0].mass)
           self.out.fillBranch("nTriggering_dR_muon_iso", muons_by_dR[0].pfRelIso04_custom)
           self.out.fillBranch("nTriggering_dR_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muons_by_dR[0].px,muons_by_dR[0].py,muons_by_dR[0].pz))
           self.out.fillBranch("nTriggering_dR_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muons_by_dR[0].phi,muons_by_dR[0].eta))    

  
           self.out.fillBranch("nTriggering_cosA_muon_isTriggering", muons_by_cosA[0].isTriggering)
           self.out.fillBranch("nTriggering_cosA_muon_px", muons_by_cosA[0].px)
           self.out.fillBranch("nTriggering_cosA_muon_pz", muons_by_cosA[0].pz)
           self.out.fillBranch("nTriggering_cosA_muon_pt", muons_by_cosA[0].pt)
           self.out.fillBranch("nTriggering_cosA_muon_dxy", muons_by_cosA[0].dxy)
           self.out.fillBranch("nTriggering_cosA_muon_dxyErr", muons_by_cosA[0].dxyErr)
           self.out.fillBranch("nTriggering_cosA_muon_eta", muons_by_cosA[0].eta)
           self.out.fillBranch("nTriggering_cosA_muon_phi", muons_by_cosA[0].phi)
           self.out.fillBranch("nTriggering_cosA_muon_mass", muons_by_cosA[0].mass)
           self.out.fillBranch("nTriggering_cosA_muon_iso", muons_by_cosA[0].pfRelIso04_custom)  
           self.out.fillBranch("nTriggering_cosA_muon_cosA", cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muons_by_cosA[0].px,muons_by_cosA[0].py,muons_by_cosA[0].pz))
           self.out.fillBranch("nTriggering_cosA_muon_deltaR", deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muons_by_cosA[0].phi,muons_by_cosA[0].eta))   
        print("AL event in analyse:", event.event)
        self.out.fillBranch("Event", event.event)
        self.out.fillBranch("muon_N", event.nMuon)
        self.out.fillBranch("muon_genWeight", event.genWeight)
               #self.out.fillBranch("muon_xsWeight", XSW) 
        #self.out.fill()
                  
                         

            
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def svTree():
    return SVTreeProducer()
