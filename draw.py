import numpy as np
import datetime
import ROOT
from  file_manager import FileManager
from ROOT import TFile, TDirectory, THashList, TH1F, TH2F, TCanvas, TLegend, TPaveText, TPython, TMath
from ROOT import gStyle, gROOT, gSystem
from ROOT import kWhite, kBlack, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan
gStyle.SetOptStat(0);
gStyle.SetOptTitle(0);

#_____________________________________________________________________
def draw_dedx_pin(cutnames):

    list_hierarchies = [
        "AnalysisResults_table_maker.root"
        ,"table-maker"
        ,"output"
    ];
    fm = FileManager(list_hierarchies);

    list_ev = fm.get("Event_AfterCuts");
    h1vtx = list_ev.FindObject("VtxZ");
    nev = h1vtx.GetEntries();
    print("nev = {0} M events".format(nev/1e+6));
    gStyle.SetPalette(55);
    ncuts = len(cutnames);

    date = datetime.date.today().strftime("%Y%m%d");

    for i in range(0,ncuts):
        c1 = TCanvas("c{0}".format(i),"cv_{0}".format(cutnames[i]),0,0,800,800);
        c1.SetLogx(1);
        c1.SetLogz(1);
        c1.SetTicks(1,1);
        c1.SetMargin(0.12,0.12,0.12,0.03);

        frame = c1.DrawFrame(0.01,0,10,200);
        list_track_barrel = fm.get("TrackBarrel_{0}".format(cutnames[i]));
        h2 = list_track_barrel.FindObject("TPCdedx_pIN");
        h2.SetDirectory(0);
        h2.SetContour(100);
        h2.GetXaxis().SetRangeUser(0.01,10);
        h2.GetYaxis().SetRangeUser(0,200);
        h2.GetXaxis().SetTitleOffset(1.5);
        h2.GetYaxis().SetTitleOffset(1.5);
        h2.GetXaxis().SetTitleSize(0.035);
        h2.GetYaxis().SetTitleSize(0.035);
        h2.GetXaxis().SetLabelSize(0.035);
        h2.GetYaxis().SetLabelSize(0.035);
        h2.GetXaxis().SetMoreLogLabels(1);
        h2.Draw("colz");
        ROOT.SetOwnership(h2,False);

        c1.Modified();
        c1.Update();
        c1.SaveAs("{0}_pilotbeam_pp_900GeV_TPCdedx_{1}.eps".format(date,cutnames[i]));
        c1.SaveAs("{0}_pilotbeam_pp_900GeV_TPCdedx_{1}.pdf".format(date,cutnames[i]));
        ROOT.SetOwnership(c1,False);

    fm.close();
#_____________________________________________________________________
if __name__ == "__main__":
    cutnames = ["BeforeCuts","jpsiO2MCdebugCuts"];
    draw_dedx_pin(cutnames);

