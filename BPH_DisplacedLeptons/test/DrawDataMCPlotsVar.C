//#include "setTDRStyle.C"
#include "TMath.h"
//#include "TROOT.h"
#include <TH1D.h>
#include <TH1F.h>
#include <TH1.h>
#include <TProfile.h>
#include <TStyle.h>
#include <THStack.h>
#include <TCanvas.h>
#include <TLeafF.h>
#include <TChain.h>
#include <TFile.h>
#include "TSystem.h"
#include <TChain.h>
#include "TSystem.h"
#include <TString.h>
#include <iostream>
#include <vector>
#include <TPostScript.h>
#include <iostream>
#include <iomanip>  //for precision

//==============
const int debug=1;
const int IfMCSig = 0;
const int IfIncludeDY = 0;
//const string TreeName = "minitree_13TeV_UntaggedTag";
const string TreeNameData = "Friends";
const string TreeName = "Friends";
const string TreeNameGGH = "tagsDumper/trees/ggh_90_13TeV_UntaggedTag";
const string TreeNameDY = "tagsDumper/trees/DY_13TeV_UntaggedTag";
const TString PrintInfor1="#bf{CMS} #it{} #it{Preliminary}";
const TString PrintInfor2="4.64 fb^{-1} (13TeV)";

//////////////////////////////////////

void DrawMyPlots(string Object, string Selections,  string XTitle, string YUnit, string PlotName, int BinTotal, double BinXLow, double BinXHig, double RYLow, double RYHig, int LegendLR, int IfLogY, int IfBlind=0, int IfLogX=0){


  TCanvas *c1 = new TCanvas("reconstruction1","reconstruction1");
  c1->SetFillColor(0);

  TLegend *legend;
  if(IfMCSig==1){
    if(LegendLR==0) legend = new TLegend(0.61,0.8,0.91,0.92);
    else if(LegendLR==1) legend = new TLegend(0.2,0.8,0.51,0.92);
    else legend = new TLegend(0.4,0.8,0.7,0.92);
  }else{
    if(LegendLR==0) legend = new TLegend(0.61,0.55,0.91,0.9);
    else if(LegendLR==1) legend = new TLegend(0.2,0.55,0.51,0.9);
    else legend = new TLegend(0.4,0.7,0.7,0.9);
  }
  legend->SetFillColor(0);
  //====add root file
  TChain *Data_Tree=new TChain(TreeNameData.c_str());

 // TChain *MCDY_Tree=new TChain(TreeNameDY.c_str());
 // TChain *MCGG_Tree=new TChain(TreeName.c_str());
 // TChain *MCGJ_Tree=new TChain(TreeName.c_str());
  TChain *MCJJ_Tree=new TChain(TreeName.c_str());

 // TChain *MCSig_Tree=new TChain(TreeNameGGH.c_str());
  //====================
  Data_Tree->Add("root://cmsxrootd.fnal.gov//store/user/alesauva/test_data_A/Data_A_new.root");
  //MCSig_Tree->Add("./output_ggh_90.root");

  //MCGG_Tree->Add("./2018_n/diPho.root");
  //MCGG_Tree->Add("./DiPhotonJets_311.root");
  //MCGJ_Tree->Add("./2018_n/GJets.root");
  MCJJ_Tree->Add("root://cmsxrootd.fnal.gov//store/user/alesauva/output_QCD_new/QCD_all_new_noID.root");

 // MCDY_Tree->Add("./2018/DYMC.root");
  //=========entries================
  int entries_Data = Data_Tree->GetEntries();
  if(debug==1) cout <<"JTao: nEntries_Data = "<<entries_Data<<endl;
  //int entries_MC = MC_Tree->GetEntries();
  //if(debug==1) cout <<"JTao: nEntries_MC = "<<entries_MC<<endl;
  c1->cd();
  //=================
  char *myLimits= new char[100];
  sprintf(myLimits,"(%d,%f,%f)",BinTotal,BinXLow,BinXHig);
  TString Taolimits(myLimits);
  //====data=======
  TString variable_Data = Object + ">>Histo_Data_temp" + Taolimits;
   //string dataSelection = "((mass>65 && mass<70) || (mass>110 && mass<120)) && !(((leadfull5x5R9<0.85) && (abs(leadSCeta)<1.442)) && ((subleadfull5x5R9<0.85) && (abs(subleadSCeta)<1.442)))";
 //string dataSelection = "";
string dataSelection = Selections;
  //Data_Tree->Draw(variable_Data, Selections.c_str());
  Data_Tree->Draw(variable_Data, dataSelection.c_str());
  TH1F *h_data = (TH1F*)gDirectory->Get("Histo_Data_temp");
  h_data->SetTitle("");
  c1->Clear();
  double Ntot_Data=h_data->Integral();
  if( debug==1 ) cout<<"JTao: N_Data= "<<Ntot_Data<<endl;
  Float_t scale_Data = 1.0/Ntot_Data;
  h_data->Sumw2();
  //h_data->Scale(scale_Data);

  ///====================================================
  string MCSelections = Selections;
 // string PPSelections = "weight*(" + MCSelections + " )";
  TH1F *h_MC = new TH1F("h_MC","", BinTotal,BinXLow,BinXHig);
  //TH1F *hpp_MC= new TH1F("hpp_MC","", BinTotal,BinXLow,BinXHig);  
 // TH1F *hpf_MC= new TH1F("hpf_MC","", BinTotal,BinXLow,BinXHig);
  TH1F *hff_MC= new TH1F("hff_MC","", BinTotal,BinXLow,BinXHig);
  //TH1F *hdy_MC= new TH1F("hdy_MC","", BinTotal,BinXLow,BinXHig);
  if(IfMCSig == 1){
 //   TString variable_sig = Object + ">>hsig_temp" + Taolimits;
  //  MCSig_Tree->Draw(variable_sig, PPSelections.c_str());
  //  h_MC = (TH1F*)gDirectory->Get("hsig_temp");
    c1->Clear();  
  }else{
    //Re: Diphoton invariant mass distributions Run 1 vs 13 TeV  by Seth Zenz on 04 March 2016 14:42
    //> prompt-prompt =  diphoton sample
    //> prompt-fake = prompt-fake only, GJet + QCD
    //> fake-fake = fake-fake only, GJet+QCD
    //string PPSelections = "TotWeight*(" + MCSelections + ")";

   /* string PPSelections = "weight*(" + MCSelections + " )";
    TString variable_pp = Object + ">>hpp_temp" + Taolimits;
    MCGG_Tree->Draw(variable_pp, PPSelections.c_str());
    hpp_MC = (TH1F*)gDirectory->Get("hpp_temp");
    c1->Clear();
    hpp_MC->Scale(1.3); //JTao test
    float Npp = hpp_MC->Integral();
    cout<<"JTao: total pp : "<<Npp<<" with raw entries from the tree "<<MCGG_Tree->GetEntries()<<endl;
 
    string PFPreSel = "( (leadMatchType == 1 && subleadMatchType != 1) || (leadMatchType != 1 && subleadMatchType == 1) )";
    string PFSelections = "weight*(" + MCSelections + " && " + PFPreSel + ")";

    TString variable_gjpf = Object + ">>hgjpf_temp" + Taolimits;
    MCGJ_Tree->Draw(variable_gjpf, PFSelections.c_str());
    //hpf_MC = (TH1F*)gDirectory->Get("hgjpf_temp");
    TH1F *hgjpf_MC = (TH1F*)gDirectory->Get("hgjpf_temp");
    c1->Clear();
    
    TString variable_jjpf = Object + ">>hjjpf_temp" + Taolimits;
    MCJJ_Tree->Draw(variable_jjpf, PFSelections.c_str());
    TH1F *hjjpf_MC = (TH1F*)gDirectory->Get("hjjpf_temp");
    c1->Clear();

    //TH1F *hpf_MC = new TH1F("hpf_MC","", BinTotal,BinXLow,BinXHig);
    hpf_MC->Add(hgjpf_MC, 1.0);
    hpf_MC->Add(hjjpf_MC, 1.0);
    
    float Npf=hpf_MC->Integral();
    //float FpfGJ = Npf>0.?hpfpf_MC->Integral()/Npf:0.0;
    cout<<"JTao: total pf : "<<hgjpf_MC->Integral()<<" from GJet and "<<hjjpf_MC->Integral()<<" from QCD!"<<endl;
    cout<<"JTao: total pf : "<<Npf<<" from GJet+QCD !"<<endl;
    //cout<<"JTao: total pf : "<<Npf<<" from GJet !"<<endl;*/


    string FFPreSel = "(  nTriggering_iso_muon_isTriggering ==0)";
    string FFSelections = "muon_xsWeight*muon_genWeight*puWeight*Muon_effTrig_Trig*(" + MCSelections + " && " + FFPreSel + " )"; //muon_xsWeight*muon_genWeight*puWeight*Muon_effTrig_Trig*
   
    string FJPreSel = "(  nTriggering_iso_muon_isTriggering ==1)";
    string FJSelections = "muon_xsWeight*muon_genWeight*puWeight*Muon_effTrig_nTrig_iso*(" + MCSelections + " && " + FJPreSel + " )"; //muon_xsWeight*muon_genWeight*puWeight*Muon_effTrig_Trig*Muon_effTrig_nTrig_iso*
   
    TString variable_jjff = Object + ">>hjjff_temp" + Taolimits;
    MCJJ_Tree->Draw(variable_jjff, FFSelections.c_str());
    //hff_MC = (TH1F*)gDirectory->Get("hjjff_temp");
    TH1F *hjjff_MC = (TH1F*)gDirectory->Get("hjjff_temp");
    c1->Clear();

    TString variable_gjff = Object + ">>hgjff_temp" + Taolimits;
    MCJJ_Tree->Draw(variable_gjff, FJSelections.c_str());
    TH1F *hgjff_MC = (TH1F*)gDirectory->Get("hgjff_temp");
    c1->Clear();
    
    //TH1F *hff_MC = new TH1F("hff_MC","", BinTotal,BinXLow,BinXHig);
    hff_MC->Add(hgjff_MC, 1.0);
    //hff_MC->Add(hjjff_MC, 1.0/25.0);
    hff_MC->Add(hjjff_MC, 1.0);

    float Nff=hff_MC->Integral();
    //float FffJJ = Nff>0.?hff_MC->Integral()/Nff:0.0;
    cout<<"AL: number of events : "<<hgjff_MC->Integral()<<" sublead triggering and "<<hjjff_MC->Integral()<<" sublead non triggering"<<endl;
    cout<<"AL: total ff : "<<Nff<<" from QCD!"<<endl;
    
   /* if(IfIncludeDY == 1){
      string DYSelections = "weight*(" + MCSelections + ")";
      TString variable_dy = Object + ">>hdy_temp" + Taolimits;
      MCDY_Tree->Draw(variable_dy, DYSelections.c_str());
      hdy_MC = (TH1F*)gDirectory->Get("hdy_temp");
      c1->Clear();
      cout<<"AL: total DY : "<<hdy_MC->Integral()<<" from DY!"<<endl;
    }*/

    //h_MC = new TH1F("h_MC","", BinTotal,BinXLow,BinXHig);
  //  h_MC->Add(hpp_MC, 1.0);
   // h_MC->Add(hpf_MC, 1.0);
    h_MC->Add(hff_MC, 1.0);
   // if(IfIncludeDY == 1) h_MC->Add(hdy_MC, 1.0);
  }
  //=============
  double Ntot_MC=h_MC->Integral();
  if( debug==1 ) cout<<"AL: N_MC= "<<Ntot_MC<<endl;
  Float_t scale_MC = Ntot_Data*1.0/Ntot_MC;
  h_MC->Sumw2();
  h_MC->Scale(scale_MC);
  cout<<"AL: MC SF = "<<scale_MC<<endl;
  double Ntot_MCXSW=h_MC->Integral();
  if( debug==1 ) cout<<"AL: Weighted N_MC= "<<Ntot_MCXSW<<endl;

  //if( debug==1 ) cout<<"AL: before THStack! " << endl;
  THStack *hs = new THStack("hs","");
  //if( debug==1 ) cout<<"AL: after THStack! " << endl;
  if( IfMCSig != 1 ){
    //if( debug==1 ) cout<<"AL: start to rescale the MC! " << endl;
   //AL hpp_MC->Scale(scale_MC);
   //AL hpf_MC->Scale(scale_MC);
    hff_MC->Scale(scale_MC);
   // if(IfIncludeDY == 1) hdy_MC->Scale(scale_MC);
    if( debug==1 ) cout<<"AL: start to add the MC for THStack! " << endl;
    //=====add a histogram to the stack
    //hs = new THStack("hs","");
   // hs->Add(hpp_MC);
   // hs->Add(hpf_MC);
    hs->Add(hff_MC);
   // if(IfIncludeDY == 1) hs->Add(hdy_MC);
  }
  if( debug==1 ) cout<<"AL: after THStack adding! " << endl;

  //===================
  double maxY=max(h_data->GetMaximum(),h_MC->GetMaximum());
  double minY=min(h_data->GetMinimum(),h_MC->GetMinimum());
  minY = 0.9*minY; 
  if(minY<1.) minY=0.1;
  h_data->GetYaxis()->SetRangeUser(minY, 1.2*maxY);
  //h_data->SetMaximum(1.2*maxY);
  if(IfLogY==1) h_data->GetYaxis()->SetRangeUser(0.2, 100.*maxY);
  //-------------------------------------
  TH1F *histoRatio = new TH1F(*h_data);
  histoRatio->Divide(h_data, h_MC, 1., 1.);
  if(IfLogX==1){
    double minX= BinXLow, maxX=BinXHig;
    if(minX<0.0015) minX=0.0015;
    if(maxX<minX)  maxX=1.1*minX;
    h_data->GetXaxis()->SetRangeUser(minX, maxX);
    histoRatio->GetXaxis()->SetRangeUser(minX, maxX);
  }

  //===================
  TH1F *h_MCErr = new TH1F("h_MCErr","", BinTotal,BinXLow,BinXHig);
  double Chi2=0.;
  for(int ibin=0; ibin<BinTotal; ibin++){
    float Nd = h_data->GetBinContent(ibin+1);
    float NdErr = h_data->GetBinError(ibin+1);
    float Nm = h_MC->GetBinContent(ibin+1);
    float NmErr = h_MC->GetBinError(ibin+1);
    if (Nm!=0){
    histoRatio->SetBinError(ibin+1, NdErr/Nm);}
    h_MCErr->SetBinContent(ibin+1, 1.);
    float RelErr = Nm>0.?NmErr*1.0/Nm:0.0;
    h_MCErr->SetBinError(ibin+1, RelErr);
    
    Chi2 += fabs(NmErr)>1e-9?(Nm-Nd)*(Nm-Nd)*1.0/(NmErr*NmErr):0.0;
    //===
      if(IfBlind==1){
       float x=BinXLow + (ibin+1)*(BinXHig-BinXLow)*1.0/BinTotal;
        //if( (x<85 && x>70) || (x> 95 && x<110) ) {
        if( (x<87 && x>70) || (x> 93 && x<115) ) {
	h_data->SetBinContent(ibin+1, 0.0);
	histoRatio->SetBinContent(ibin+1, 0.0);
      }
    }
     }
  cout<<"AL: chi2 = "<<Chi2<<endl;


  h_data->SetLineColor(1);
  h_data->SetFillColor(0);
  h_data->SetLineStyle(1);
  h_data->SetLineWidth(2);
  h_data->GetXaxis()->SetTitle(XTitle.c_str());
  double WidthBin=(BinXHig-BinXLow)/BinTotal;
  //TString TitleY( Form("A.U. / %.2g GeV",WidthBin) );
  //TString TitleY( Form("No. of Entries in data / %.2g GeV",WidthBin) );
  //TString TitleY = "A.U";
  string PreTitleY( Form("Entries / %.2g ",WidthBin) );
  string TitleY =  PreTitleY + YUnit;
  h_data->GetYaxis()->SetTitle(TitleY.c_str());

  h_data->SetTitleSize(0.05,"X");
  h_data->SetTitleSize(0.06,"Y");
  //h_data->SetTitleOffset(1.3, "Y");
  h_data->SetTitleOffset(1.1, "Y");

  h_data->SetMarkerColor(kBlack);
  h_data->SetMarkerSize(1.0);
  h_data->SetMarkerStyle(20);
 
 // if(IfMCSig == 1){
 //   h_MC->SetFillColor(0);
 //   h_MC->SetLineColor(1);
 // }else{
    h_MC->SetFillColor(kOrange+10);
    h_MC->SetLineColor(kOrange+10);
    h_MC->SetFillColor(kOrange+10); 
    h_MC->SetFillStyle(3244); //3001,3005
  //}
  h_MC->SetLineStyle(1);
  h_MC->SetLineWidth(2);
  h_MC->SetMarkerColor(17);
  //h_MC->SetMarkerSize(1.2);
 
  //h_MCErr->SetFillColor(17);
  h_MCErr->SetLineColor(kOrange+10);
  h_MCErr->SetLineStyle(1);
  h_MCErr->SetLineWidth(2);
  //h_MCErr->SetMarkerColor(17);
  h_MCErr->SetFillColor(kOrange+10); //2
  h_MCErr->SetFillStyle(3244); //3001, 3005

  legend->AddEntry(h_data,"data","pe");

  if(IfMCSig == 1){
    legend->AddEntry(h_MC,"Sig m_{H}=90 GeV","l");
  }else{
   /* hpp_MC->SetFillColor(2);
    hpp_MC->SetMarkerStyle(0);
    hpp_MC->SetLineColor(2);
    hpp_MC->SetLineStyle(1);
    hpp_MC->SetLineWidth(2);
    hpf_MC->SetFillColor(4);
    hpf_MC->SetMarkerStyle(0);
    hpf_MC->SetLineColor(4);
    hpf_MC->SetLineStyle(1);
    hpf_MC->SetLineWidth(2);*/

    hff_MC->SetFillColor(5);
    hff_MC->SetMarkerStyle(0);
    hff_MC->SetLineColor(5);
    hff_MC->SetLineStyle(1);
    hff_MC->SetLineWidth(2);

   /* if(IfIncludeDY == 1){
      hdy_MC->SetFillColor(8);
      hdy_MC->SetMarkerStyle(0);
      hdy_MC->SetLineColor(8);
      hdy_MC->SetLineStyle(1);
      hdy_MC->SetLineWidth(2);
    }*/
    //legend->AddEntry(h_MC,"MC","f");
    //legend->AddEntry(hpp_MC,"DiPhotonJets","f");
    //legend->AddEntry(hpf_MC,"GJet","f");
    legend->AddEntry(hff_MC,"QCD","f");
    //legend->AddEntry(hpp_MC,"#gamma-#gamma","f");
   // legend->AddEntry(hpf_MC,"#gamma-jet","f");
   // legend->AddEntry(hff_MC,"jet-jet","f");
   // if(IfIncludeDY == 1) legend->AddEntry(hdy_MC,"Drell-Yan","f");
    legend->AddEntry(h_MC,"MC stat. unc.","f");
  }

  gPad->SetTickx(1);
  gPad->SetTicky(1);
  gPad->SetLeftMargin(0.18);
  gPad->SetBottomMargin(0.15);
  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.05);

  c1->SetFrameBorderSize(0);
  c1->SetFrameBorderMode(0);
  h_data->GetXaxis()->SetLabelColor(0);
  h_data->SetNdivisions(510 ,"X");

  TLatex * tex1 = new TLatex(0.2,0.87, PrintInfor1); //0.88
  if(LegendLR==1) tex1 = new TLatex(0.65, 0.87, PrintInfor1);
  tex1->SetNDC();
  tex1->SetTextFont(42);
  tex1->SetTextSize(0.045);
  tex1->SetLineWidth(2);

  TLatex * tex2 = new TLatex(0.20,0.81, PrintInfor2); //0.82
  if(LegendLR==1)  tex2 = new TLatex(0.65,0.81, PrintInfor2); 
  tex2->SetNDC();
  tex2->SetTextFont(42);
  tex2->SetTextSize(0.045);
  tex2->SetLineWidth(2);

 
  string Prenameplots="DataMC_"+PlotName;

  if(IfMCSig == 1){
    Prenameplots="DataMCSig_"+PlotName;

    h_data->Draw("PE1");
    legend->Draw("same");
    h_MC->Draw("Histsame");

    tex1->Draw();
    tex2->Draw();
  }else{

    //prepare 2 pads
    const Int_t nx=1;
    const Int_t ny=2;
    const Double_t x1[2] = {0.0,0.0};
    const Double_t x2[2] = {1.0,1.0};
    //const Double_t y1[] = {1.0,0.3};
    //const Double_t y2[] = {0.3,0.00};
    const Double_t y1[2] = {0.3,0.0};
    const Double_t y2[2] = {1.0,0.3};
    Float_t psize[2];
    TPad *pad;
    const char *myname = "c";
    char *name2 = new char [strlen(myname)+6];
    Int_t n = 0;
    for (int iy=0;iy<ny;iy++) {
      for (int ix=0;ix<nx;ix++) {
	n++;
	sprintf(name2,"%s_%d",myname,n);
	if(ix==0){
	  gStyle->SetPadLeftMargin(.166);
	}else{
	  gStyle->SetPadLeftMargin(.002);
	  gStyle->SetPadTopMargin(.002);
	}

	if(iy==0){//upper
	  gStyle->SetPadTopMargin(0.05*(1./0.7)); // 0.05
	  gStyle->SetPadBottomMargin(.02);
	}
	if(iy==(ny-1)){//lower pad
	  gStyle->SetPadTopMargin(.05);
	  //gStyle->SetPadBottomMargin(.13*(1./0.3));
	  gStyle->SetPadBottomMargin(.40);


	}
	pad = new TPad(name2,name2,x1[ix],y1[iy],x2[ix],y2[iy]);
	pad->SetNumber(n);
	pad->Draw();
	psize[iy]=y1[iy]-y2[iy];
	//if(iy>0 )pad->SetGrid(kTRUE);
      }// end of loop over x
    }// end of loop over y
    delete [] name2;

    //===Drawing====

    c1->cd(1);
    gPad->SetLogy(IfLogY);
    gPad->SetLogx(IfLogX);
    gPad->SetTickx(1);
    gPad->SetTicky(1);
    //=========
    h_data->Draw("PE1");
    legend->Draw("same");
    if(IfMCSig != 1) hs->Draw("hist,same");
    h_MC->Draw("E2,same");
    h_data->Draw("samePE1");
    h_data->Draw("Axissame");

    tex1->Draw();
    tex2->Draw();

    ///====
    TLine *Line1 = new TLine(h_data->GetBinLowEdge(1),1,h_data->GetBinLowEdge(h_data->GetNbinsX())+ h_data->GetBinWidth(h_data->GetNbinsX()),1);
    Line1->SetLineColor(1);
    Line1->SetLineWidth(2);
    Line1->SetLineStyle(4);

    //TH1F *histoRatio = new TH1F(*h_data);
    //histoRatio->Divide(h_data, h_MC, 1., 1.);
    histoRatio->SetLineColor(1);
    histoRatio->SetLineStyle(1);
    histoRatio->SetLineWidth(2);
    histoRatio->SetMarkerColor(1);
    histoRatio->SetMarkerStyle(20);

    c1->cd(2);
    gPad->SetLogy(0);
    gPad->SetLogx(IfLogX);
    //gPad->SetLogx(0);
    histoRatio->SetTitleOffset(1,"X");
    histoRatio->SetTitleSize(0.12,"X");
    histoRatio->SetLabelSize(0.1,"X");
    histoRatio->GetXaxis()->SetTitle(XTitle.c_str());
    histoRatio->GetYaxis()->SetTitle("data/MC");
    //histoRatio->SetTitleOffset(0.5,"Y");
    histoRatio->SetTitleOffset(0.4,"Y");
    //histoRatio->SetTitleSize(0.12,"Y");
    histoRatio->SetTitleSize(0.14,"Y");
    histoRatio->SetLabelSize(0.1,"Y");
    histoRatio->SetLabelColor(1,"X");
    histoRatio->GetYaxis()->CenterTitle();
    //histoRatio->SetNdivisions(505 ,"Y");
    histoRatio->SetNdivisions(510 ,"X");

    gPad->SetTickx(1);
    gPad->SetTicky(1);
 
    histoRatio->GetXaxis()->SetTickLength(0.08);
    histoRatio->GetYaxis()->SetTickLength(0.06);
    histoRatio->GetYaxis()->SetNdivisions(503);
  
    histoRatio->SetMinimum(RYLow);
    histoRatio->SetMaximum(RYHig);
    histoRatio->Draw("PE1");
    h_MCErr->Draw("E2,same");
    histoRatio->Draw("samePE1");
    Line1->Draw("same");
  }

  //===================================
  string pngplots= Prenameplots + ".png";
  c1->Print(pngplots.c_str());

  string pdfplots= Prenameplots + ".pdf";
  c1->Print(pdfplots.c_str());
  //c1->Clear();
  //legend->Clear();
 
}


void DrawDataMCPlotsVar(){

  gROOT->ProcessLine(".x hggPaperStyle.C");
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(111);	

  //All
  cout<<"============================All========================"<<endl;
 string BasicSelections="(  (abs(Triggering_muon_dxy/Triggering_muon_dxyErr) > 6.5) )"; //(Triggering_muon_pt >10) && (nTriggering_iso_muon_pt >4) &&
  //string BasicSelections="(mass>87 && mass<93) && !(((leadfull5x5R9<0.85) && (abs(leadSCeta)<1.442)) && ((subleadfull5x5R9<0.85) && (abs(subleadSCeta)<1.442)))";
   //string BasicSelections="(mass>65 && mass<70) || (mass>110 && mass<120)";
 DrawMyPlots("Triggering_muon_pt", BasicSelections, "p_{T}^{(1)} (GeV)", "GeV",  "Triggering_muon_pt_PU_sigma65_trig_noID",60, 0., 20., 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_dxy", BasicSelections, "d_{xy}^{(1)} (m)", "m",  "Triggering_muon_Sdxy_sigma65_trig_noID",90, -0.15, 0.15, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_dxyErr", BasicSelections, "#sigma_{xy}^{(1)} ", "",  "Triggering_muon_dxyErr_PU_sigma65_trig_noID",100, 0., 0.005, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_dz", BasicSelections, "d_{z}^{(1)} (m)", "m",  "Triggering_muon_dz_PU_sigma65_trig_noID",80, -0.2, 0.2, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_iso", BasicSelections, "isolation^{(1)}", "",  "Triggering_muon_iso_PU_sigma65_trig_noID",100, 0., 2., 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_phi", BasicSelections, "#phi^{(1)}", "",  "Triggering_muon_phi_PU_sigma65_trig_noID",60, -3, 3., 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("Triggering_muon_eta", BasicSelections, "#eta^{(1)}", "",  "Triggering_muon_eta_PU_sigma65_trig_noID",60, -1.5, 1.5, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("nPV", BasicSelections, "Number Pile_up", "",  "nPV_PU_sigma65_trig_noID",60, 0., 60., 0.5, 2.0, 0, 0, 0);
DrawMyPlots("nTriggering_iso_muon_pt", BasicSelections, "p_{T}^{(2)} (GeV)", "GeV",  "nTriggering_iso_muon_pt_PU_sigma65_trig_noID",60, 0., 20., 0.5, 2.0, 0, 0, 0);
DrawMyPlots("nTriggering_iso_muon_dxy", BasicSelections, "d_{xy}^{(2)} (m)", "m",  "nTriggering_iso_muon_Sdxy_sigma65_trig_noID",80, -0.1, 0.1, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("nTriggering_iso_muon_dxyErr", BasicSelections, "#sigma_{xy}^{(2)} ", "",  "nTriggering_iso_muon_dxyErr_PU_sigma65_trig_noID",100, 0., 0.01, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("nTriggering_iso_muon_dz", BasicSelections, "d_{z}^{(2)} (m)", "m",  "nTriggering_iso_muon_dz_PU_sigma65_trig_noID",80, -0.2, 0.2, 0.5, 2.0, 0, 0, 0);
DrawMyPlots("nTriggering_iso_muon_iso", BasicSelections, "isolation^{(2)}", "",  "nTriggering_iso_muon_iso_PU_sigma65_trig_noID",100, 0., 2., 0.5, 2.0, 0, 0, 0);
DrawMyPlots("nTriggering_iso_muon_phi", BasicSelections, "#phi^{(2)}", "",  "nTriggering_iso_muon_phi_PU_sigma65_trig_noID",60, -3, 3., 0.5, 2.0, 0, 0, 0);
DrawMyPlots("nTriggering_iso_muon_eta", BasicSelections, "#eta^{(2)}", "",  "nTriggering_iso_muon_eta_PU_sigma65_trig_noID",60, -1.5, 1.5, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("abs(Triggering_muon_dxy/Triggering_muon_dxyErr)", BasicSelections, "d_{xy}^{(1)}/#sigma", "",  "Triggering_muon_Sdxy_PU_w_sigma65_trig_noID",200, 0, 20, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("abs(nTriggering_iso_muon_dxy/nTriggering_iso_muon_dxyErr)", BasicSelections, "d_{xy}^{(2)}/#sigma", "",  "nTriggering_iso_muon_Sdxy_PU_w_sigma65_trig_noID",200, 0, 20, 0.5, 2.0, 0, 0, 0);
 DrawMyPlots("muon_N", BasicSelections, "Number muons", "",  "muon_N_sigma65_trig_noID",6, 0, 6, 0.5, 2.0, 0, 0, 0);

}
