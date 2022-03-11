import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from ..helpers.utils import deltaPhi, deltaR, deltaR2, cosA, closest, polarP4, sumP4, get_subjets, transverseMass, invariantMass, minValue, configLogger
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
        self.out.branch("nPV", "F")
        self.out.branch("nSV", "F")
        self.out.branch("nOtherPV", "F")

        self.out.branch("Triggering_muon_isTriggering", "O")
        for var in ["px","py","pz","pt","dxy","dxyErr","dz","dzErr","ip3d","charge","pdgId","eta","phi","mass","iso","genPartIdx","genPartFlav"]:
           self.out.branch("Triggering_muon_%s" % (var), "F")

        for sort in ["iso","IP","dR","cosA","pt","dz"]:
           self.out.branch("nTriggering_%s_muon_isTriggering" % (sort), "O")
           for var_s in ["px","py","pz","pt","dxy","dxyErr","dz","dzErr","ip3d","charge","pdgId","eta","phi","mass","iso","genPartIdx","genPartFlav","cosA","deltaR","di_mass"]:
              self.out.branch("nTriggering_%s_muon_%s" % (sort, var_s), "F")  
        
        #If MC, importe the xs weight from the metadata json file
        self.isMC = bool(inputTree.GetBranch('genWeight'))
        if self.isMC==True:
           self.out.branch("Gen_trigger_muon_iso", "F")
           self.out.branch("Gen_ntrigger_iso_muon_iso", "F")
           self.out.branch("Gen_ntrigger_IP_muon_iso", "F")
           self.out.branch("Gen_ntrigger_pt_muon_iso", "F")
           self.out.branch("Gen_trigger_muon_pt", "F")
           self.out.branch("Gen_ntrigger_iso_muon_pt", "F")
           self.out.branch("Gen_ntrigger_IP_muon_pt", "F")
           self.out.branch("Gen_ntrigger_pt_muon_pt", "F")
           print("This is MC")
           # load xsec weight
           print(md['xsecWgt'])
           XSW=0
           converted_in = "{}".format(inputFile)
           #print(converted_in)
           input = re.search('/eos/uscms/store/user/alesauva/BParkingNANO_signal_test/(.+?)/', converted_in).group(1) #To be replaced with the input file directory ParkingNANO_2022Feb15 BParkingNANO_Data_A
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
        dimuon_counter=0
        _all_muons  = Collection(event, 'Muon')
        #The first loop is for pre-selection
        if event.nMuon<2.0:
           return False
        for muon in _all_muons:
            #apply cuts here
            if (abs(muon.eta) < 2.4) and (muon.tightId == True) and (muon.isGlobal == True) and not((0.3< muon.eta <1.2) & (0.4 < muon.phi <0.8) ):
                muon_general.append(muon)
                if muon.isTriggering==True:
                   muon_general_Triggering.append(muon)
        if (len(muon_general)<2) or (len(muon_general_Triggering)<1):
           return False
        for i in range(len(muon_general)):
           for j in range(len(muon_general)):
              if i !=j:
                 if cosA(muon_general[i].px,muon_general[i].py,muon_general[i].pz,muon_general[j].px,muon_general[j].py,muon_general[j].pz)<-0.99:
                    return False
                 if deltaR( muon_general[i].phi, muon_general[i].eta,muon_general[j].phi,muon_general[j].eta)>0.2:
                    dimuon_counter=dimuon_counter+1
        if dimuon_counter==0:
           return False

        #The second loop is for setting the list of muon for each event
        Nmuons=0
        _all_muons2  = Collection(event, 'Muon')
        for muons in _all_muons2:
            #print("AL muon event:", event.event)
            #print("AL muon event:", muons.eta, muons.tightId, muons.isGlobal)
            if (abs(muons.eta) < 2.4) and (muons.tightId == True) and (muons.isGlobal == True) and not((0.3< muons.eta <1.2) & (0.4 < muons.phi <0.8) ):
               Nmuons=Nmuons+1
               if muons.isTriggering ==True:
                  muon_trigger.append(muons)
               else:
                  muon_Ntrigger.append(muons)
               #print("Ntrigger muon iso, ip", muons.pfRelIso04_custom, muons.dxy)
        #Filling lead muon = triggering muon
        #for var_trig in ["isTriggering","px","py","pz","pt","dxy","dxyErr","dz","dzErr","ip3d","charge","pdgId","eta","phi","mass","pfRelIso04_custom","genPartIdx","genPartFlav"]:

        self.out.fillBranch("Triggering_muon_isTriggering", muon_trigger[0].isTriggering)
        self.out.fillBranch("Triggering_muon_px", muon_trigger[0].px)
        self.out.fillBranch("Triggering_muon_py", muon_trigger[0].py)
        self.out.fillBranch("Triggering_muon_pz", muon_trigger[0].pz)
        self.out.fillBranch("Triggering_muon_pt", muon_trigger[0].pt)
        self.out.fillBranch("Triggering_muon_dxy", muon_trigger[0].dxy)
        self.out.fillBranch("Triggering_muon_dxyErr", muon_trigger[0].dxyErr)
        self.out.fillBranch("Triggering_muon_dz", muon_trigger[0].dz)
        self.out.fillBranch("Triggering_muon_ip3d", muon_trigger[0].ip3d)
        self.out.fillBranch("Triggering_muon_charge", muon_trigger[0].charge)
        self.out.fillBranch("Triggering_muon_pdgId", muon_trigger[0].pdgId)
        self.out.fillBranch("Triggering_muon_eta", muon_trigger[0].eta)
        self.out.fillBranch("Triggering_muon_phi", muon_trigger[0].phi)
        self.out.fillBranch("Triggering_muon_mass", muon_trigger[0].mass)
        self.out.fillBranch("Triggering_muon_iso", muon_trigger[0].pfRelIso04_custom)
       # self.out.fillBranch("Triggering_muon_genPartIdx", muon_trigger[0].genPartIdx)
       # self.out.fillBranch("Triggering_muon_genPartFlav", muon_trigger[0].genPartFlav)


        if len(muon_trigger)>1:
           #print("Event have two triggering muons, will form a pair with both")
           for var_subtrig in ["iso","IP","dR","cosA","pt","dz"]:
              self.out.fillBranch("nTriggering_%s_muon_isTriggering" % (var_subtrig), muon_trigger[1].isTriggering)
              self.out.fillBranch("nTriggering_%s_muon_px" % (var_subtrig), muon_trigger[1].px)
              self.out.fillBranch("nTriggering_%s_muon_pz" % (var_subtrig), muon_trigger[1].pz)
              self.out.fillBranch("nTriggering_%s_muon_pt" % (var_subtrig), muon_trigger[1].pt)
              self.out.fillBranch("nTriggering_%s_muon_dxy" % (var_subtrig), muon_trigger[1].dxy)
              self.out.fillBranch("nTriggering_%s_muon_dxyErr" % (var_subtrig), muon_trigger[1].dxyErr)
              self.out.fillBranch("nTriggering_%s_muon_eta" % (var_subtrig), muon_trigger[1].eta)
              self.out.fillBranch("nTriggering_%s_muon_phi" % (var_subtrig), muon_trigger[1].phi)
              self.out.fillBranch("nTriggering_%s_muon_mass" % (var_subtrig), muon_trigger[1].mass)
              self.out.fillBranch("nTriggering_%s_muon_iso" % (var_subtrig), muon_trigger[1].pfRelIso04_custom)
              self.out.fillBranch("nTriggering_%s_muon_cosA" % (var_subtrig), cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_trigger[1].px,muon_trigger[1].py,muon_trigger[1].pz))
              self.out.fillBranch("nTriggering_%s_muon_deltaR" % (var_subtrig), deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_trigger[1].phi,muon_trigger[1].eta))          
              self.out.fillBranch("nTriggering_%s_muon_py" % (var_subtrig), muon_trigger[1].py)
              self.out.fillBranch("nTriggering_%s_muon_dz" % (var_subtrig), muon_trigger[1].dz)
              self.out.fillBranch("nTriggering_%s_muon_dzErr" % (var_subtrig), muon_trigger[1].dzErr)
              self.out.fillBranch("nTriggering_%s_muon_ip3d" % (var_subtrig), muon_trigger[1].ip3d)
              self.out.fillBranch("nTriggering_%s_muon_charge" % (var_subtrig), muon_trigger[1].charge)
              self.out.fillBranch("nTriggering_%s_muon_pdgId" % (var_subtrig), muon_trigger[1].pdgId)
              #self.out.fillBranch("nTriggering_%s_muon_genPartIdx" % (var_subtrig), muon_trigger[1].genPartIdx)
              #self.out.fillBranch("nTriggering_%s_muon_genPartFlav" % (var_subtrig), muon_trigger[1].genPartFlav)
              #self.out.fillBranch("nTriggering_%s_muon_genPartIdx" % (var_subtrig), muon_trigger[1].genPartIdx)
              self.out.fillBranch("nTriggering_%s_muon_di_mass" % (var_subtrig), invariantMass(muon_trigger[0].mass,muon_trigger[1].mass,muon_trigger[0].px,muon_trigger[1].px,muon_trigger[0].py,muon_trigger[1].py,muon_trigger[0].pz,muon_trigger[1].pz))
        else:
           #Filling non-triggering muon depending on variables
           muons_by_IP = sorted(muon_Ntrigger,key=lambda x: x.dxy, reverse=True)
           muons_by_iso = sorted(muon_Ntrigger,key=lambda x: x.pfRelIso04_custom)
           muons_by_cosA=sorted(muon_Ntrigger, key=lambda x: abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)))
           #print("cosA=", [abs(cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,x.px,x.py,x.pz)) for x in muon_Ntrigger])
           #print("muons_bycosa", muons_by_cosA)
           muons_by_dR=sorted(muon_Ntrigger, key=lambda x: deltaR(muon_trigger[0].phi,muon_trigger[0].eta,x.phi,x.eta), reverse=True)
           muons_by_pt = sorted(muon_Ntrigger,key=lambda x: x.pt, reverse=True)
           muons_by_dz = sorted(muon_Ntrigger,key=lambda x: x.dz, reverse=True)
           self.out.fillBranch("nTriggering_iso_muon_isTriggering", muons_by_iso[0].isTriggering)
           for var_sub in ["iso","IP","dR","cosA","pt","dz"]:
              
              str=("muons_by_%s" % (var_sub))
              muon_to_use=locals()[str][0]
              #print("AL test:", muon_to_use)
              self.out.fillBranch("nTriggering_%s_muon_isTriggering" % (var_sub), muon_to_use.isTriggering)
              self.out.fillBranch("nTriggering_%s_muon_px" % (var_sub), muon_to_use.px)
              self.out.fillBranch("nTriggering_%s_muon_pz" % (var_sub), muon_to_use.pz)
              self.out.fillBranch("nTriggering_%s_muon_pt" % (var_sub), muon_to_use.pt)
              self.out.fillBranch("nTriggering_%s_muon_dxy" % (var_sub), muon_to_use.dxy)
              self.out.fillBranch("nTriggering_%s_muon_dxyErr" % (var_sub), muon_to_use.dxyErr)
              self.out.fillBranch("nTriggering_%s_muon_eta" % (var_sub), muon_to_use.eta)
              self.out.fillBranch("nTriggering_%s_muon_phi" % (var_sub), muon_to_use.phi)
              self.out.fillBranch("nTriggering_%s_muon_mass" % (var_sub), muon_to_use.mass)
              self.out.fillBranch("nTriggering_%s_muon_iso" % (var_sub), muon_to_use.pfRelIso04_custom)
              self.out.fillBranch("nTriggering_%s_muon_cosA" % (var_sub), cosA(muon_trigger[0].px,muon_trigger[0].py,muon_trigger[0].pz,muon_to_use.px,muon_to_use.py,muon_to_use.pz))
              self.out.fillBranch("nTriggering_%s_muon_deltaR" % (var_sub), deltaR( muon_trigger[0].phi, muon_trigger[0].eta,muon_to_use.phi,muon_to_use.eta))          
              self.out.fillBranch("nTriggering_%s_muon_py" % (var_sub), muon_to_use.py)
              self.out.fillBranch("nTriggering_%s_muon_dz" % (var_sub), muon_to_use.dz)
              self.out.fillBranch("nTriggering_%s_muon_dzErr" % (var_sub), muon_to_use.dzErr)
              self.out.fillBranch("nTriggering_%s_muon_ip3d" % (var_sub), muon_to_use.ip3d)
              self.out.fillBranch("nTriggering_%s_muon_charge" % (var_sub), muon_to_use.charge)
              self.out.fillBranch("nTriggering_%s_muon_pdgId" % (var_sub), muon_to_use.pdgId)
             # self.out.fillBranch("nTriggering_%s_muon_genPartIdx" % (var_sub), muon_to_use.genPartIdx)
             # self.out.fillBranch("nTriggering_%s_muon_genPartFlav" % (var_sub), muon_to_use.genPartFlav)
             # self.out.fillBranch("nTriggering_%s_muon_genPartIdx" % (var_sub), muon_to_use.genPartIdx)
              self.out.fillBranch("nTriggering_%s_muon_di_mass" % (var_sub), invariantMass(muon_trigger[0].mass,muon_to_use.mass,muon_trigger[0].px,muon_to_use.px,muon_trigger[0].py,muon_to_use.py,muon_trigger[0].pz,muon_to_use.pz))
        self.out.fillBranch("Event", event.event)
        self.out.fillBranch("muon_N", Nmuons)
        self.out.fillBranch("nSV", event.nSV)
        self.out.fillBranch("nPV", event.PV_npvs)
        self.out.fillBranch("nOtherPV", event.nOtherPV)
        if self.isMC==True:
           self.out.fillBranch("muon_genWeight", event.genWeight)
           gen_muon=[]
           dR_triggering_muon_match=100
           gen_triggering_muon=0
           gen_trigger_muon_iso=0
           dR_ntriggering_iso_muon_match=100
           gen_ntriggering_iso_muon=0
           gen_ntrigger_iso_muon_iso=0
           dR_ntriggering_IP_muon_match=100
           gen_ntriggering_IP_muon=0
           gen_ntrigger_IP_muon_iso=0
           dR_ntriggering_pt_muon_match=100
           gen_ntriggering_pt_muon=0
           gen_ntrigger_pt_muon_iso=0
           genparts = Collection(event, "GenPart")
           for gen in genparts:
              if abs(gen.pdgId)==13:
                 gen_muon.append(gen)
           if len(gen_muon)>1:
              for gmuon in gen_muon:
                 if deltaR( muon_trigger[0].phi, muon_trigger[0].eta,gmuon.phi,gmuon.eta)<dR_triggering_muon_match:
                    gen_triggering_muon=gmuon
                    dR_triggering_muon_match=deltaR( muon_trigger[0].phi, muon_trigger[0].eta,gmuon.phi,gmuon.eta)
                    if len(muon_trigger)<2:
                       if deltaR( muons_by_iso[0].phi, muons_by_iso[0].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_iso_muon_match:                    
                          gen_ntriggering_iso_muon=gmuon
                          dR_ntriggering_iso_muon_match=deltaR( muons_by_iso[0].phi, muons_by_iso[0].eta,gmuon.phi,gmuon.eta)     
                       if deltaR( muons_by_IP[0].phi, muons_by_IP[0].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_IP_muon_match:                    
                          gen_ntriggering_IP_muon=gmuon
                          dR_ntriggering_IP_muon_match=deltaR( muons_by_IP[0].phi, muons_by_IP[0].eta,gmuon.phi,gmuon.eta)  
                       if deltaR( muons_by_pt[0].phi, muons_by_pt[0].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_pt_muon_match:                    
                          gen_ntriggering_pt_muon=gmuon
                          dR_ntriggering_pt_muon_match=deltaR( muons_by_pt[0].phi, muons_by_pt[0].eta,gmuon.phi,gmuon.eta)  
                    else:
                       if deltaR( muon_trigger[1].phi, muon_trigger[1].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_iso_muon_match:                    
                          gen_ntriggering_iso_muon=gmuon
                          dR_ntriggering_iso_muon_match=deltaR( muon_trigger[1].phi,muon_trigger[1].eta,gmuon.phi,gmuon.eta)     
                       if deltaR( muon_trigger[1].phi, muon_trigger[1].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_IP_muon_match:                    
                          gen_ntriggering_IP_muon=gmuon
                          dR_ntriggering_IP_muon_match=deltaR( muon_trigger[1].phi, muon_trigger[1].eta,gmuon.phi,gmuon.eta)  
                       if deltaR( muon_trigger[1].phi, muon_trigger[1].eta,gmuon.phi,gmuon.eta)<dR_ntriggering_pt_muon_match:                    
                          gen_ntriggering_pt_muon=gmuon
                          dR_ntriggering_pt_muon_match=deltaR( muon_trigger[1].phi, muon_trigger[1].eta,gmuon.phi,gmuon.eta) 
 
              for genp in genparts:
                 if deltaR( gen_triggering_muon.phi, gen_triggering_muon.eta,genp.phi,genp.eta)<0.4:
                    gen_trigger_muon_iso=gen_trigger_muon_iso+genp.pt
                 if deltaR( gen_ntriggering_iso_muon.phi, gen_ntriggering_iso_muon.eta,genp.phi,genp.eta)<0.4:
                    gen_ntrigger_iso_muon_iso=gen_ntrigger_iso_muon_iso+genp.pt 
                 if deltaR( gen_ntriggering_IP_muon.phi, gen_ntriggering_IP_muon.eta,genp.phi,genp.eta)<0.4:
                    gen_ntrigger_IP_muon_iso=gen_ntrigger_IP_muon_iso+genp.pt 
                 if deltaR( gen_ntriggering_pt_muon.phi, gen_ntriggering_pt_muon.eta,genp.phi,genp.eta)<0.4:
                    gen_ntrigger_pt_muon_iso=gen_ntrigger_pt_muon_iso+genp.pt

              self.out.fillBranch("Gen_trigger_muon_pt", gen_triggering_muon.pt)   
              self.out.fillBranch("Gen_ntrigger_iso_muon_pt", gen_ntriggering_iso_muon.pt)
              self.out.fillBranch("Gen_ntrigger_IP_muon_pt", gen_ntriggering_IP_muon.pt)    
              self.out.fillBranch("Gen_ntrigger_pt_muon_pt", gen_ntriggering_pt_muon.pt)          
              self.out.fillBranch("Gen_trigger_muon_iso", gen_trigger_muon_iso)   
              self.out.fillBranch("Gen_ntrigger_iso_muon_iso", gen_ntrigger_iso_muon_iso)
              self.out.fillBranch("Gen_ntrigger_IP_muon_iso", gen_ntrigger_IP_muon_iso)    
              self.out.fillBranch("Gen_ntrigger_pt_muon_iso", gen_ntrigger_pt_muon_iso)
        #self.out.branch("GenPart_genPartIdxMother", "F")
               #self.out.fillBranch("muon_xsWeight", XSW) 
        #self.out.fill()
                  
                                   
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

def svTree():
    return SVTreeProducer()
