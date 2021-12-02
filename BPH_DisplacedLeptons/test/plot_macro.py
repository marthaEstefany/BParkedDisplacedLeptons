import ROOT
import sys
from ROOT import TChain, TFileCollection, TH1F, TCanvas, TFile, TH2F, TCut
ROOT.gROOT.SetBatch(True)

#################################################
### take in input and define output root file ###
#################################################

if len(sys.argv) != 3:
    print("USAGE: %s <input file> <output file>"%(sys.argv[0]))
    sys.exit(1)

inFileName  = sys.argv[1]
outFileName = sys.argv[2]
print("Reading from", inFileName, "and writing to", outFileName)

inFile = ROOT.TFile.Open(inFileName,"READ")
outFile = ROOT.TFile.Open(outFileName, "RECREATE")

## read name of input TTree
tree = inFile.Get("Friends")

### list of variables ###
labels = {"muon_pt":  ["muon_pt", 100, 0., 100.]}

########################################
### make 1D histograms for each leaf ###
########################################

def make1DHistogram(name, variable, bins, xmin, xmax):
    h = ROOT.TH1D(name, variable, bins, xmin, xmax)
    return h

##################
### start here ###
##################

def testarea(variable, bins):

    h = make1DHistogram(bins[0], variable, bins[1], bins[2], bins[3])
    h.Write()

if __name__ == "__main__":
    for variable in labels.keys():
        testarea(variable, labels[variable])

### selections
##MuMu_selections = "nMuon >= 2 && abs(Muon_eta) < 2.4 && Muon_tightId  && Muon_pfRelIso03_all < 0.10 && Muon_isGlobal && !(Muon_eta >= 0.3 && Muon_eta <= 1.2 && Muon_phi >= 0.4 && Muon_phi <= 0.8) && ((Muon_eta[0]-Muon_eta[1])*(Muon_eta[0]-Muon_eta[1]) + (Muon_phi[0]-Muon_phi[1])*(Muon_phi[0]-Muon_phi[1])) > 0.2 && ( Muon_pt[0]*cos(Muon_phi[0])*Muon_pt[1]*cos(Muon_phi[1]) +  Muon_pt[0]*sin(Muon_phi[0])*Muon_pt[1]*sin(Muon_phi[1]) + Muon_pt[0]/tan(Muon_phi[0])*Muon_pt[1]/tan(Muon_phi[1]) ) / ( sqrt(   Muon_pt[0]*cos(Muon_phi[0])*Muon_pt[0]*cos(Muon_phi[0]) + Muon_pt[1]*cos(Muon_phi[1])*Muon_pt[1]*cos(Muon_phi[1]) + Muon_pt[0]/tan(Muon_phi[0])*Muon_pt[0]/tan(Muon_phi[0]) ) * sqrt( Muon_pt[1]*cos(Muon_phi[1])*Muon_pt[1]*cos(Muon_phi[1]) + Muon_pt[1]*sin(Muon_phi[1])*Muon_pt[1]*sin(Muon_phi[1]) + Muon_pt[1]/tan(Muon_phi[1])*Muon_pt[1]/tan(Muon_phi[1])  )) > -0.99"
##
##onePrompt_oneDisplaced = "(10000*abs(Muon_dxy[0]) < 100 && 10000*abs(Muon_dxy[1]) > 100)  || (10000*abs(Muon_dxy[0]) > 100 &&  10000*abs(Muon_dxy[1]) < 100)"
##prompt_leading = "10000*abs(Muon_dxy[0]) < 100 && 10000*abs(Muon_dxy[1]) > 100"
##prompt_subleading = "10000*abs(Muon_dxy[1]) < 100)  && (10000*abs(Muon_dxy[0]) > 100"
##prompt = "10000*abs(Muon_dxy[0]) < 50 && 10000*abs(Muon_dxy[1]) < 50"
##prompt30To100_displaced100to500 = "((10000*abs(Muon_dxy[0]) > 30 && 10000*abs(Muon_dxy[0]) < 100) && \
##                                   (10000*abs(Muon_dxy[1]) > 100 && 10000*abs(Muon_dxy[1]) < 500)) || \
##                                   ((10000*abs(Muon_dxy[1]) > 30 && 10000*abs(Muon_dxy[1]) < 100) && \
##                                   (10000*abs(Muon_dxy[0]) > 100 && 10000*abs(Muon_dxy[0]) < 500))"
##
##controlRegion1 = MuMu_selections + " && " + onePrompt_oneDisplaced
##controlRegion2 = MuMu_selections + " && " + prompt
##controlRegion3 = MuMu_selections + " && " + prompt30To100_displaced100to500
#
## iso = 1/(lepton pT) * max[0, (all charged hadron pT in dR cone) + (all neutral hadron Et in dR cone) + (all photon Et in dR cone) - rho*pi*dR^2 ]
## where rho = (total Et of all PF candidates up to some eta)/(total detector area up to some eta)
#
## displaced lep
##"1/muon.pt * max(muon.pfIsolationR04_.sumChargedHadronPt + muon.pfIsolationR04_.sumPUPt + muon.pfIsolationR04_.sumNeutralHadronEt + muon.pfIsolationR04_.sumPhotonEt - muon.rho*0.503, 0)" # 0.503 = pi*0.4**2
#
## parking
##"(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt",float,doc="PF relative isolation dR=0.4, total (deltaBeta corrections)"
#
## old displaced lep
##" ((pT of charged hadrons from PV[0]) + max(0, (ET of neutral hadrons)+(ET of photons)-0.5*(pT of charged hadrons from PV[n>0])))/(pT of muon)"
#
### plot maker
#out = ROOT.TFile("output_histograms.root", "new")    
#labels = {
#         "muon_pt": [1, "muon_pt", 50, 0, 100],
##	 "BToKMuMu_fit_mass":   [1, "m(B #rightarrow KK_{#mu#mu}) [GeV]", 50, 4, 8],
##        "Muon_dxy":            [1, "#mu |d0| [cm]", 10, 0, 2],
##        "nMuon":               [1, "n. #mu", 10,0,10],
##        "Muon_tightId":        [1, "tight id", 2,0,2],
##        "Muon_eta":            [1, "#mu #eta", 100, -2.5, 2.5],
##        "Muon_phi":            [1, "#mu #phi", 100, -3.5, 3.5],
##        "Muon_pt":             [1, "#mu pT [GeV]", 300, 0, 100],
##        "Muon_pfRelIso03_all": [1, "#mu relative Iso with dR < 0.3", 30,0,30],
##        "Muon_isGlobal":       [1, "global #mu", 2,0,2],
##        "(Muon_eta[0]-Muon_eta[1])*(Muon_eta[0]-Muon_eta[1]) + (Muon_phi[0]-Muon_phi[1])*(Muon_phi[0]-Muon_phi[1])":   [1, "delta R", 50, 0, 1],
##        "(Muon_pt[0]*cos(Muon_phi[0])*Muon_pt[1]*cos(Muon_phi[1]) + Muon_pt[0]*sin(Muon_phi[0])*Muon_pt[1]*sin(Muon_phi[1]) + Muon_pt[0]/tan(Muon_phi[0])*Muon_pt[1]/tan(Muon_phi[1]) ) / ( sqrt(Muon_pt[0]*cos(Muon_phi[0])*Muon_pt[0]*cos(Muon_phi[0]) + Muon_pt[1]*cos(Muon_phi[1])*Muon_pt[1]*cos(Muon_phi[1]) + Muon_pt[0]/tan(Muon_phi[0])*Muon_pt[0]/tan(Muon_phi[0])) * sqrt( Muon_pt[1]*cos(Muon_phi[1])*Muon_pt[1]*cos(Muon_phi[1]) + Muon_pt[1]*sin(Muon_phi[1])*Muon_pt[1]*sin(Muon_phi[1]) + Muon_pt[1]/tan(Muon_phi[1])*Muon_pt[1]/tan(Muon_phi[1])))":   [1, "cos(#alpha)", 50, -1, 1],
##
##        "10000*abs(Muon_dxy[0]):10000*abs(Muon_dxy[1])":  [2, "leading #mu vs subleading #mu |d0|", 100, 0, 50, 100, 0, 50]
#}
#
#def make1DHistogram(f, name, variable, nbins, xmin, xmax):
#    h = TH1F(name, variable, nbins, xmin, xmax)
#    #tfile.Project(name, variable, selections)
#    return h
#
##def make2DHistogram(tfile, name, variable, nxbins, xmin, xmax, nybins, ymin, ymax, selections):
##    h = TH2F(name, name, nxbins, xmin, xmax, nybins, ymin, ymax)
##    tfile.Project(name, variable, selections)
##    return h
#
#def testarea(variable, bins):
#    #chain = TChain("Events")
#    #fc = TFileCollection("file", "", "data.txt")
#    #chain.AddFileInfoList(fc.GetList())
#
#    f = ROOT.TFile("BParkNANO_data_2021Oct06_1_Friend.root", "RECREATE")
#
#    if bins[0] == 1:
#        h = make1DHistogram(f, bins[1], variable, bins[2], bins[3], bins[4])
#        h.Write()
#    #elif bins[0] == 2:
#    #    h = make2DHistogram(chain, bins[1], variable, bins[2], bins[3], bins[4], bins[5], bins[6], bins[7], selections)
#    #    h.Write()
#
#if __name__ == "__main__":
#
#    for variable in labels.keys():
#	testarea(variable, labels[variable])
