import uproot
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import numpy as np

file = uproot.open("root://cmsxrootd.fnal.gov//store/user/alesauva/output_QCD/QCD_all_w.root")

#file = uproot.open("root://cmsxrootd.fnal.gov//store/user/alesauva/output_jobs/DYToLL.root")



events= file["Friends"]




iso_variables=[]
for var_trig in ["isTriggering","dxy","iso","pt","dxyErr","dz"]:
   iso_variables.append("Triggering_muon_%s" % (var_trig))
for var_ntrig in ["isTriggering","dxy","iso","pt","dxyErr","dz"]:
   for sort in ["iso","IP","dR","cosA","pt","dz"]:
      iso_variables.append("nTriggering_%s_muon_%s" % (sort,var_ntrig))
for x in ["muon_N","nSV","nOtherPV","muon_xsWeight"] :
   iso_variables.append(x)  
isocut=0.2
lead_pt_cut=7
sublead_pt_cut=5
IPscut=3
dzcut=0.0005
variables_i = events.arrays(iso_variables, outputtype=pandas.DataFrame)
variables_o=variables_i[(variables_i["nTriggering_iso_muon_iso"]<isocut) & (variables_i["Triggering_muon_pt"]>lead_pt_cut) & (variables_i["nTriggering_iso_muon_pt"]>sublead_pt_cut) & (variables_i["nTriggering_iso_muon_dxy"]/variables_i["nTriggering_iso_muon_dxyErr"]>IPscut) & (variables_i["Triggering_muon_dxy"]/variables_i["Triggering_muon_dxyErr"]>IPscut) & (variables_i["Triggering_muon_dz"]>dzcut) & (variables_i["nTriggering_iso_muon_dz"]>dzcut)]
y_space = np.linspace(0, 30, 60)

x_space = np.logspace(0, np.log10(200.0), 200)

#variables_i.plot.scatter(x="Triggering_muon_iso", y="nTriggering_iso_muon_dxy");
plt.hist2d(abs(variables_o["nTriggering_iso_muon_dxy"])*1000,1/variables_o["Triggering_muon_iso"],bins=(x_space, y_space), norm=mpl.colors.LogNorm()) #bins=50,range=[[0.0,200],[0,30]]
plt.ylabel("Triggering muon 1/isolation")
plt.xlabel("'Sublead' muon IP (mm)")
plt.xscale('log')
plt.savefig("QCD_1isoIP_iso02_pt75_IPs3_dz0005.pdf")
