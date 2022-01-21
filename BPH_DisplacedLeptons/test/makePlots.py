import ROOT
import sys
from ROOT import TFile, TH1D, TCanvas

ROOT.ROOT.EnableImplicitMT()

ranges = {
        "Triggering_muon_pt":              (100, 0., 100.),
        "Triggering_muon_isTriggering":   (4, 0., 4.),
        "Triggering_muon_dxy":             (100, -100., 100.),
        "Triggering_muon_dxyErr":          (100, -100., 100.),
        "Triggering_muon_eta":             (100, -3., 3.),
        "Triggering_muon_mass":            (200, 0.,  200.),
        "Triggering_muon_iso":             (100, 0.,  25.),
        "nTriggering_iso_muon_pt":              (100, 0., 100.),
        "nTriggering_iso_muon_isTriggering":   (4, 0., 4.),
        "nTriggering_iso_muon_dxy":             (100, -100., 100.),
        "nTriggering_iso_muon_dxyErr":          (100, -100., 100.),
        "nTriggering_iso_muon_eta":             (100, -3., 3.),
        "nTriggering_iso_muon_mass":            (200, 0.,  200.),
        "nTriggering_iso_muon_iso":             (100, 0.,  25.),
        "nTriggering_iso_muon_cosA":             (100, -1.,  1.),
        "nTriggering_iso_muon_deltaR":             (100, 0., 10.),
        "nTriggering_IP_muon_pt":              (100, 0., 100.),
        "nTriggering_IP_muon_isTriggering":   (4, 0., 4.),
        "nTriggering_IP_muon_dxy":             (100, -100., 100.),
        "nTriggering_IP_muon_dxyErr":          (100, -100., 100.),
        "nTriggering_IP_muon_eta":             (100, -3., 3.),
        "nTriggering_IP_muon_mass":            (200, 0.,  200.),
        "nTriggering_IP_muon_iso":             (100, 0.,  25.),
        "nTriggering_IP_muon_cosA":             (100, -1.,  1.),
        "nTriggering_IP_muon_deltaR":             (100, 0., 10.),
        "nTriggering_dR_muon_pt":              (100, 0., 100.),
        "nTriggering_dR_muon_isTriggering":   (4, 0., 4.),
        "nTriggering_dR_muon_dxy":             (100, -100., 100.),
        "nTriggering_dR_muon_dxyErr":          (100, -100., 100.),
        "nTriggering_dR_muon_eta":             (100, -3., 3.),
        "nTriggering_dR_muon_mass":            (200, 0.,  200.),
        "nTriggering_dR_muon_iso":             (100, 0.,  25.),
        "nTriggering_dR_muon_cosA":             (100, -1.,  1.),
        "nTriggering_dR_muon_deltaR":             (100, 0., 10.),
        "nTriggering_cosA_muon_pt":              (100, 0., 100.),
        "nTriggering_cosA_muon_isTriggering":   (4, 0., 4.),
        "nTriggering_cosA_muon_dxy":             (100, -100., 100.),
        "nTriggering_cosA_muon_dxyErr":          (100, -100., 100.),
        "nTriggering_cosA_muon_eta":             (100, -3., 3.),
        "nTriggering_cosA_muon_mass":            (200, 0.,  200.),
        "nTriggering_cosA_muon_iso":             (100, 0.,  25.),
        "nTriggering_cosA_muon_cosA":             (100, -1.,  1.),
        "nTriggering_cosA_muon_deltaR":             (100, 0., 10.),
}

axes = {
       "Triggering_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "Triggering_muon_isTriggering":   ";triggering mu; N_{Events}",
       "Triggering_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "Triggering_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "Triggering_muon_eta":             ";mu_eta; N_{Events}",
       "Triggering_muon_mass":            ";mu_mass; N_{Events}",
       "Triggering_muon_iso":             ";mu_iso; N_{Events}",
       "nTriggering_iso_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "nTriggering_iso_muon_isTriggering":   ";triggering mu; N_{Events}",
       "nTriggering_iso_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "nTriggering_iso_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "nTriggering_iso_muon_eta":             ";mu_eta; N_{Events}",
       "nTriggering_iso_muon_mass":            ";mu_mass; N_{Events}",
       "nTriggering_iso_muon_iso":             ";mu_iso; N_{Events}",
       "nTriggering_iso_muon_cosA":            ";cosA_{mu mu}; N_{Events}",
       "nTriggering_iso_muon_deltaR":             ";Delta R_{mu mu}; N_{Events}",
       "nTriggering_IP_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "nTriggering_IP_muon_isTriggering":   ";triggering mu; N_{Events}",
       "nTriggering_IP_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "nTriggering_IP_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "nTriggering_IP_muon_eta":             ";mu_eta; N_{Events}",
       "nTriggering_IP_muon_mass":            ";mu_mass; N_{Events}",
       "nTriggering_IP_muon_iso":             ";mu_iso; N_{Events}",
       "nTriggering_IP_muon_cosA":            ";cosA_{mu mu}; N_{Events}",
       "nTriggering_IP_muon_deltaR":             ";Delta R_{mu mu}; N_{Events}",
       "nTriggering_dR_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "nTriggering_dR_muon_isTriggering":   ";triggering mu; N_{Events}",
       "nTriggering_dR_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "nTriggering_dR_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "nTriggering_dR_muon_eta":             ";mu_eta; N_{Events}",
       "nTriggering_dR_muon_mass":            ";mu_mass; N_{Events}",
       "nTriggering_dR_muon_iso":             ";mu_iso; N_{Events}",
       "nTriggering_dR_muon_cosA":            ";cosA_{mu mu}; N_{Events}",
       "nTriggering_dR_muon_deltaR":             ";Delta R_{mu mu}; N_{Events}",
       "nTriggering_cosA_muon_pt":              ";mu_pT [GeV];N_{Events}",
       "nTriggering_cosA_muon_isTriggering":   ";triggering mu; N_{Events}",
       "nTriggering_cosA_muon_dxy":             ";m_d0 [mum]; N_{Events}",
       "nTriggering_cosA_muon_dxyErr":          ";mu_d0Err [mum]; N_{Events}",
       "nTriggering_cosA_muon_eta":             ";mu_eta; N_{Events}",
       "nTriggering_cosA_muon_mass":            ";mu_mass; N_{Events}",
       "nTriggering_cosA_muon_iso":             ";mu_iso; N_{Events}",
       "nTriggering_cosA_muon_cosA":            ";cosA_{mu mu}; N_{Events}",
       "nTriggering_cosA_muon_deltaR":             ";Delta R_{mu mu}; N_{Events}",
}

ranges2D = {
        "dxy_v_dxy_trigVnoTrig":  (100, -0.1, .1, 100, -0.1, .1),
        "iso_v_iso_trigVnoTrig":  (100, 0., 25., 100, 0., 25.),
        "cosA_v_cosA_trigVnoTrig":  (100, 0., 25., 100, 0., 25.),
        "dR_v_dR_trigVnoTrig":  (100, 0., 25., 100, 0., 25.),

}

axes2D = {
        "dxy_v_dxy_trigVnoTrig":  (";non triggering mu_dxy ;triggering mu_dxy", "Triggering_muon_dxy", "nTriggering_IP_muon_dxy"),
        "iso_v_iso_trigVnoTrig":  (";non triggering mu_iso ;triggering mu_iso", "Triggering_muon_iso", "nTriggering_iso_muon_iso"),
        "cosA_v_cosA_trigVnoTrig":  (";non triggering cosA mu_iso ;triggering mu_iso", "Triggering_muon_iso", "nTriggering_cosA_muon_iso"),
        "dR_v_dR_trigVnoTrig":  (";non triggering dR mu_iso ;triggering mu_iso", "Triggering_muon_iso", "nTriggering_dR_muon_iso"),
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
    inFile = ROOT.ROOT.RDataFrame("Friends", "/uscms/homes/a/alesauva/work/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs_output_2018_2L/data/Bs_tree.root")
    
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
