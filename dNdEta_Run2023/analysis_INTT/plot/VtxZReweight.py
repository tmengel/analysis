#! /usr/bin/env python
from optparse import OptionParser
import sys
import os
import datetime
from array import *
from ROOT import TH1F, TH2F, TFile, TCanvas, TPad, TLegend, TColor, gROOT, kBlack
import numpy as np
import math
import glob
from plotUtil import GetHistogram

LeftMargin = 0.15
RightMargin = 0.08
TopMargin = 0.08
BottomMargin = 0.13
titlesize = 0.05
labelsize = 0.05
pad1scale = 1.05
pad2scale = 2.6

gROOT.SetBatch(True)

def draw_ratio(hdata, hsim, hweight, xtitle, plotname):
    c = TCanvas("c", "c", 800, 600)
    c.cd()
    pad1 = TPad( 'pad1', ' ', 0, 0.3, 1, 1)
    pad2 = TPad( 'pad2', ' ', 0, 0, 1, 0.3)
    pad1.SetBottomMargin(0.0)
    pad1.Draw()
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.35)
    pad2.Draw()
    pad1.cd()
    hdata.GetXaxis().SetTitle(xtitle)
    hdata.GetXaxis().SetTitleSize(titlesize*pad1scale)
    # hdata.GetXaxis().SetRangeUser(hdata.GetXaxis().GetXmin() - 1, hdata.GetXaxis().GetXmax() + 1)
    hdata.GetXaxis().SetRangeUser(hdata.GetXaxis().GetXmin(), hdata.GetXaxis().GetXmax())
    hdata.GetYaxis().SetTitle("Normalized counts")
    hdata.GetYaxis().SetTitleSize(titlesize*pad1scale)
    hdata.GetYaxis().SetTitleOffset(1.5)
    hdata.GetYaxis().SetLabelSize(labelsize*pad1scale)
    hdata.GetYaxis().SetRangeUser(0.0001, hdata.GetMaximum()*1.2 if hdata.GetMaximum() > hsim.GetMaximum() else hsim.GetMaximum() * 1.2)
    hdata.SetMarkerStyle(20)
    hdata.SetMarkerSize(0.8)
    hdata.SetMarkerColor(kBlack)
    hdata.SetLineColor(kBlack)
    hdata.Draw("PE1")
    hsim.SetLineColor(TColor.GetColor("#9A031E"))
    hsim.Draw("hist same")
    leg = TLegend(0.67, 0.77, 0.9, 0.9)
    leg.AddEntry(hdata, "Data", "lep")
    leg.AddEntry(hsim, "Simulation", "l")
    leg.SetTextSize(0.05*pad1scale)
    leg.SetFillStyle(0)
    leg.Draw("same")
    c.RedrawAxis()
    c.Update()
    # cd to the pad2
    pad2.cd()
    pad2.SetGridy()
    hweight.SetMarkerSize(0.8)
    hweight.GetXaxis().SetTitle(xtitle)
    hweight.GetXaxis().SetTitleSize(titlesize*pad2scale)
    hweight.GetXaxis().SetLabelSize(labelsize*pad2scale)
    hweight.GetXaxis().SetTitleOffset(1.3)
    hweight.GetYaxis().SetTitle("Data/Sim.")
    hweight.GetYaxis().SetNdivisions(505)
    hweight.GetYaxis().SetTitleSize(titlesize*pad2scale)
    hweight.GetYaxis().SetLabelSize(labelsize*pad2scale)
    hweight.GetYaxis().SetTitleOffset(0.6)
    hweight.GetXaxis().SetRangeUser(hdata.GetXaxis().GetXmin(), hdata.GetXaxis().GetXmax())
    hweight.GetYaxis().SetRangeUser(0, 2.1)
    hweight.SetMarkerColor(kBlack)
    hweight.SetLineColor(kBlack)
    hweight.Draw("PE1")
    c.SaveAs("{}.png".format(plotname))
    c.SaveAs("{}.pdf".format(plotname))

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog ver [options -h]")
    parser.add_option("--datafiledir", dest="datafiledir", default='/sphenix/user/hjheng/sPHENIXRepo/analysis/dNdEta_Run2023/analysis_INTT/plot/hists/Data_CombinedNtuple_Run20869_HotDead_BCO_ADC_Survey/RecoVtx', help="Data file directory")
    parser.add_option("--simfiledir", dest="simfiledir", default='/sphenix/user/hjheng/sPHENIXRepo/analysis/dNdEta_Run2023/analysis_INTT/plot/hists/Sim_Ntuple_HIJING_ana419_20240910/RecoVtx', help="Simulation file directory")
    parser.add_option("--plotappendix", dest="plotappendix", default='HIJING_ana419_20240910', help="Plot appendix")
    parser.add_option('--plotdir', dest='plotdir', type='string', default='RecoPV_ana', help='Plot directory')

    (opt, args) = parser.parse_args()
    print('opt: {}'.format(opt)) 
    
    datafiledir = opt.datafiledir
    simfiledir = opt.simfiledir
    plotappendix = opt.plotappendix
    plotdir = opt.plotdir
    os.makedirs('./{}/{}'.format(plotdir,plotappendix), exist_ok=True)
    
    if os.path.isfile("{}/hists_merged.root".format(datafiledir)):
        os.system("rm {}/hists_merged.root".format(datafiledir))
        os.system("hadd -j 20 {}/hists_merged.root {}/hists_0*.root".format(datafiledir, datafiledir))
    else:
        os.system("hadd -j 20 {}/hists_merged.root {}/hists_0*.root".format(datafiledir, datafiledir))
        
    if os.path.isfile("{}/hists_merged.root".format(simfiledir)):
        os.system("rm {}/hists_merged.root".format(simfiledir))
        os.system("hadd -j 20 {}/hists_merged.root {}/hists_0*.root".format(simfiledir, simfiledir))
    else:
        os.system("hadd -j 20 {}/hists_merged.root {}/hists_0*.root".format(simfiledir, simfiledir))
        
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data = GetHistogram("{}/hists_merged.root".format(datafiledir), "hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetName("hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim = GetHistogram("{}/hists_merged.root".format(simfiledir), "hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.SetName("hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Scale(1.0/hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Integral())
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Scale(1.0/hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Integral())
    VtxZ_reweight_VtxZm30to30 = hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Clone("VtxZ_reweight_VtxZm30to30")
    VtxZ_reweight_VtxZm30to30.Divide(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim)
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data = GetHistogram("{}/hists_merged.root".format(datafiledir), "hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetName("hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim = GetHistogram("{}/hists_merged.root".format(simfiledir), "hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.SetName("hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Scale(1.0/hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Integral())
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Scale(1.0/hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Integral())
    VtxZ_reweight_VtxZm30to30_MBD = hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Clone("VtxZ_reweight_VtxZm30to30_MBD")
    VtxZ_reweight_VtxZm30to30_MBD.Divide(hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim)
    
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data = GetHistogram("{}/hists_merged.root".format(datafiledir), "hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.SetName("hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim = GetHistogram("{}/hists_merged.root".format(simfiledir), "hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.SetName("hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Scale(1.0/hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Integral())
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Scale(1.0/hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Integral())
    VtxZ_reweight_VtxZm10to10 = hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Clone("VtxZ_reweight_VtxZm10to10")
    VtxZ_reweight_VtxZm10to10.Divide(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim)
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data = GetHistogram("{}/hists_merged.root".format(datafiledir), "hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.SetName("hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim = GetHistogram("{}/hists_merged.root".format(simfiledir), "hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.SetName("hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Scale(1.0/hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Integral())
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Scale(1.0/hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Integral())
    VtxZ_reweight_VtxZm10to10_MBD = hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Clone("VtxZ_reweight_VtxZm10to10_MBD")
    VtxZ_reweight_VtxZm10to10_MBD.Divide(hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim)
    
    draw_ratio(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data, hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim, VtxZ_reweight_VtxZm30to30, "INTT Z_{vtx} [cm]", "./{}/{}/VtxZ_reweight_VtxZm30to30_{}".format(plotdir, plotappendix, plotappendix))
    draw_ratio(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data, hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim, VtxZ_reweight_VtxZm10to10, "INTT Z_{vtx} [cm]", "./{}/{}/VtxZ_reweight_VtxZm10to10_{}".format(plotdir, plotappendix, plotappendix))
    draw_ratio(hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data, hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim, VtxZ_reweight_VtxZm30to30_MBD, "MBD Z_{vtx} [cm]", "./{}/{}/VtxZ_reweight_VtxZm30to30_MBD_{}".format(plotdir, plotappendix, plotappendix))
    draw_ratio(hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data, hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim, VtxZ_reweight_VtxZm10to10_MBD, "MBD Z_{vtx} [cm]", "./{}/{}/VtxZ_reweight_VtxZm10to10_MBD_{}".format(plotdir, plotappendix, plotappendix))
    
    # draw comparison of INTT and MBD vertex Z 
    c = TCanvas("c", "c", 800, 700)
    c.cd()
    pad1 = TPad( 'pad1', ' ', 0, 0.3, 1, 1)
    pad2 = TPad( 'pad2', ' ', 0, 0, 1, 0.3)
    pad1.SetBottomMargin(0.0)
    pad1.Draw()
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.35)
    pad2.Draw()
    pad1.cd()
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().SetTitle("vtx_{Z} [cm]")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().SetTitleSize(titlesize*pad1scale)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().SetRangeUser(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().GetXmin(), hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().GetXmax())
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetYaxis().SetTitle("Normalized counts")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetYaxis().SetTitleSize(titlesize*pad1scale)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetYaxis().SetTitleOffset(1.5)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetYaxis().SetLabelSize(labelsize*pad1scale)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetYaxis().SetRangeUser(0.0001, hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetMaximum()*1.2 if hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetMaximum() > hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetMaximum() else hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetMaximum() * 1.2)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerStyle(21)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerSize(0.8)
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerColor(TColor.GetColor("#0F4C75"))
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetLineColor(TColor.GetColor("#0F4C75"))
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Draw("PE1")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.SetLineColor(TColor.GetColor("#0F4C75"))
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Draw("hist same")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerStyle(20)
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerSize(0.8)
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetMarkerColor(TColor.GetColor("#9A031E"))
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.SetLineColor(TColor.GetColor("#9A031E"))
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Draw("PE1 same")
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.SetLineColor(TColor.GetColor("#9A031E"))
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Draw("hist same")
    leg = TLegend(0.67, 0.77, 0.9, 0.9)
    leg.AddEntry(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data, "INTT tracklet", "lep")
    leg.AddEntry(hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data, "MBD", "lep")
    leg.SetTextSize(0.05*pad1scale)
    leg.SetFillStyle(0)
    leg.Draw("same")
    c.RedrawAxis()
    c.Update()
    # cd to the pad2
    pad2.cd()
    pad2.SetGridy()
    VtxZ_reweight_VtxZm30to30.SetMarkerSize(0.8)
    VtxZ_reweight_VtxZm30to30.GetXaxis().SetTitle("vtx_{Z} [cm]")
    VtxZ_reweight_VtxZm30to30.GetXaxis().SetTitleSize(titlesize*pad2scale)
    VtxZ_reweight_VtxZm30to30.GetXaxis().SetLabelSize(labelsize*pad2scale)
    VtxZ_reweight_VtxZm30to30.GetXaxis().SetTitleOffset(1.3)
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetTitle("Data/Sim.")
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetNdivisions(505)
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetTitleSize(titlesize*pad2scale)
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetLabelSize(labelsize*pad2scale)
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetTitleOffset(0.6)
    VtxZ_reweight_VtxZm30to30.GetXaxis().SetRangeUser(hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().GetXmin(), hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.GetXaxis().GetXmax())
    VtxZ_reweight_VtxZm30to30.GetYaxis().SetRangeUser(0, 2.1)
    VtxZ_reweight_VtxZm30to30.SetMarkerSize(0.8)
    VtxZ_reweight_VtxZm30to30.SetMarkerStyle(21)
    VtxZ_reweight_VtxZm30to30.SetMarkerColor(TColor.GetColor("#0F4C75"))
    VtxZ_reweight_VtxZm30to30.SetLineColor(TColor.GetColor("#0F4C75"))
    VtxZ_reweight_VtxZm30to30.Draw("PE1")
    VtxZ_reweight_VtxZm30to30_MBD.SetMarkerSize(0.8)
    VtxZ_reweight_VtxZm30to30_MBD.SetMarkerStyle(20)
    VtxZ_reweight_VtxZm30to30_MBD.SetMarkerColor(TColor.GetColor("#9A031E"))
    VtxZ_reweight_VtxZm30to30_MBD.SetLineColor(TColor.GetColor("#9A031E"))
    VtxZ_reweight_VtxZm30to30_MBD.Draw("PE1 same")
    c.SaveAs("./{}/{}/INTTMBDVtxZ_VtxZm30to30_comparison_{}.png".format(plotdir, plotappendix, plotappendix))
    c.SaveAs("./{}/{}/INTTMBDVtxZ_VtxZm30to30_comparison_{}.pdf".format(plotdir, plotappendix, plotappendix))

    
    f = TFile("./{}/{}/VtxZ_reweight_{}.root".format(plotdir, plotappendix, plotappendix), "recreate")
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Write()
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Write()
    VtxZ_reweight_VtxZm30to30.Write()
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Write()
    hM_INTTVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Write()
    VtxZ_reweight_VtxZm10to10.Write()
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_data.Write()
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm30to30_coarse_sim.Write()
    VtxZ_reweight_VtxZm30to30_MBD.Write()
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_data.Write()
    hM_MBDVtxZ_Centrality0to70_MBDAsymLe1_VtxZm10to10_coarse_sim.Write()
    VtxZ_reweight_VtxZm10to10_MBD.Write()
    f.Close()
    