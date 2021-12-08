import ROOT
import sys
from ROOT import TFile, TH1D, TCanvas

ROOT.ROOT.EnableImplicitMT()

ranges = {
        "muon_pt":              (100, 0., 100.),
        "muon_pt_triggering":   (100, 0., 100.),
        "muon_dxy":             (100, -100., 100.),
        "muon_dxyErr":          (100, -100., 100.),
        "muon_eta":             (100, -3., 3.),
        "muon_mass":            (200, 0.,  200.),
        "muon_iso":             (100, 0.,  25.),
        "Trig_muon_pt":              (100, 0., 100.),
        "Trig_muon_dxy":             (100, -100., 100.),
        "Trig_muon_dxyErr":          (100, -100., 100.),
        "Trig_muon_eta":             (100, -3., 3.),
        "Trig_muon_mass":            (200, 0.,  200.),
        "Trig_muon_iso":             (100, 0.,  25.),
        "noTrig_muon_pt":              (100, 0., 100.),
        "noTrig_muon_dxy":             (100, -100., 100.),
        "noTrig_muon_dxyErr":          (100, -100., 100.),
        "noTrig_muon_eta":             (100, -3., 3.),
        "noTrig_muon_mass":            (200, 0.,  200.),
        "noTrig_muon_iso":             (100, 0.,  25.),
}

axes = {
       "muon_pt":              ";mu_pT [GeV];N_{Events}",
       "muon_pt_triggering":   ";triggering mu_pT [GeV]; N_{Events}",
       "muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "muon_eta":             ";mu_eta; N_{Events}",
       "muon_mass":            ";mu_mass; N_{Events}",
       "muon_iso":             ";mu_iso; N_{Events}",
       "Trig_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "Trig_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "Trig_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "Trig_muon_eta":             ";mu_eta; N_{Events}",
       "Trig_muon_mass":            ";mu_mass; N_{Events}",
       "Trig_muon_iso":             ";mu_iso; N_{Events}",
       "noTrig_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "noTrig_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "noTrig_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "noTrig_muon_eta":             ";mu_eta; N_{Events}",
       "noTrig_muon_mass":            ";mu_mass; N_{Events}",
       "noTrig_muon_iso":             ";mu_iso; N_{Events}",
}

ranges2D = {
        "dxy_v_iso":              (100, 0., 25., 100, -0.1, .1),
        "dxy_v_dxy_trigVnoTrig":  (100, -0.1, .1, 100, -0.1, .1),
        "iso_v_iso_trigVnoTrig":  (100, 0., 25., 100, 0., 25.),
}

axes2D = {
        "dxy_v_iso":              (";mu_iso ;mu_dxy", "muon_iso", "muon_dxy"),
        "dxy_v_dxy_trigVnoTrig":  (";non triggering mu_dxy ;triggering mu_dxy", "Trig_muon_dxy", "noTrig_muon_dxy"),
        "iso_v_iso_trigVnoTrig":  (";non triggering mu_dxy ;triggering mu_dxy", "Trig_muon_iso", "noTrig_muon_iso"),
}


def make1Dhist(f, variable, xtitle, range_):
    h = f.Histo1D((variable, xtitle, range_[0], range_[1], range_[2]), variable)
    return h


def make2Dhist(f, name, axes_, range_):
    h = f.Histo2D((name, axes_[0], range_[0], range_[1], range_[2], range_[3], range_[4], range_[5]), axes_[1], axes_[2])
    return h

def writeHistogram(h, name):
    h.SetName(name)
    h.Write()

def main():

    outFile = ROOT.TFile("histograms.root", "RECREATE")
    inFile = ROOT.ROOT.RDataFrame("Friends", "/uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/BParkNANO_data_2021Oct06_1_Friend.root")
    
    variables = ranges.keys()
    variables2D = ranges2D.keys()
    hists = {}
    
    for variable in variables:
        hists[variable] = make1Dhist(inFile, variable, axes[variable], ranges[variable])
        writeHistogram(hists[variable], variable)

    for variable in variables2D:
        hists[variable] = make2Dhist(inFile, variable, axes2D[variable], ranges2D[variable])
        writeHistogram(hists[variable], variable)
        

if __name__ == "__main__":
    main()
