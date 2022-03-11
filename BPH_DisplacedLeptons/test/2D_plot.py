import uproot
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import numpy as np

file = uproot.open("root://cmsxrootd.fnal.gov//store/user/alesauva/test_data_A/Data_A_new.root")

#file = uproot.open("root://cmsxrootd.fnal.gov//store/user/alesauva/output_jobs/DYToLL.root")



events= file["Friends"]




iso_variables=[]
for var_trig in ["isTriggering","dxy","iso","pt","dxyErr"]:
   iso_variables.append("Triggering_muon_%s" % (var_trig))
for var_ntrig in ["isTriggering","dxy","iso","pt","dxyErr"]:
   for sort in ["iso","IP","dR","cosA","pt","dz"]:
      iso_variables.append("nTriggering_%s_muon_%s" % (sort,var_ntrig))
for x in ["muon_N","nSV","nOtherPV"] :
   iso_variables.append(x)  
isocut=0.2
lead_pt_cut=7
sublead_pt_cut=5
IPscut=3

variables_i = events.arrays(iso_variables, outputtype=pandas.DataFrame)
#variables_o=variables_i[(variables_i["nTriggering_iso_muon_iso"]<isocut) & (variables_i["Triggering_muon_pt"]>lead_pt_cut) & (variables_i["nTriggering_iso_muon_pt"]>sublead_pt_cut) & (variables_i["nTriggering_iso_muon_dxy"]/variables_i["nTriggering_iso_muon_dxyErr"]>IPscut) & (variables_i["Triggering_muon_dxy"]/variables_i["Triggering_muon_dxyErr"]>IPscut)]
y_space =np.logspace(0, np.log10(200.0), 200)

x_space = np.linspace(0, 10, 100)

#variables_i.plot.scatter(x="Triggering_muon_iso", y="nTriggering_iso_muon_dxy");
plt.hist2d(abs(variables_i["Triggering_muon_dxy"]/variables_i["Triggering_muon_dxyErr"]),abs(variables_i["Triggering_muon_dxy"])*1000,bins=(x_space, y_space), norm=mpl.colors.LogNorm()) #bins=50,range=[[0.0,200],[0,30]]
plt.ylabel("'lead' muon IP xy (mm)")
plt.xlabel("'lead' muon sigma IP xy")
plt.yscale('log')
plt.savefig("data_dxy_Deltadxy_lead.pdf")
