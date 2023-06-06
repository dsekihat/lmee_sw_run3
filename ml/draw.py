import datetime
import array
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from pylab import rcParams
import data_loader
import ROOT
from ROOT import TFile, TH1F, TH2F, THnSparseF, TString, TCanvas, TPad, TLegend, TPaveText
from ROOT import kWhite, kBlack, kRed, kGreen, kBlue, kYellow, kOrange, kCyan, kMagenta, kViolet

#____________________________________________________________________________________________
def make_common_style(g1,marker,size,color,width=1,fill=0):
    g1.SetMarkerStyle(marker);
    g1.SetMarkerColor(color);
    g1.SetMarkerSize(size);
    g1.SetLineColor(color);
    g1.SetLineWidth(width);
    g1.SetFillColor(color);
    g1.SetFillStyle(fill);
#____________________________________________________________________________________________
def apply_kinetic_cut_track(df, ptmin, etamax):
    df_new = df[
    ((df.pos_track_fPt > ptmin) & (df.neg_track_fPt > ptmin))
    & ((abs(df.pos_track_fEta) < etamax) & ( abs(df.neg_track_fEta) < etamax))
    ];
    return df_new;
#____________________________________________________________________________________________
def fill_sparse_hist(hs, df):
    hs_tmp = hs.Clone("{0}_clone".format(hs.GetName()));
    for index, row in df.iterrows():
        m =  row['fM'];
        pt = row['fPt'];
        pair_dca_xy = row['fPairDCAxy'];
        var = np.array([m, pt, pair_dca_xy], dtype=np.double);
        hs_tmp.Fill(var);
    return hs_tmp;
#____________________________________________________________________________________________
def extract(filename_csv, ptmin, etamax):
    df = data_loader.load_data_pd(filename_csv)
    df = df[ (abs(df.pos_track_fDcaZ) < 1) & (abs(df.neg_track_fDcaZ) < 1) ];
    df = df[ (abs(df.pos_track_fDcaXY) < 1) & (abs(df.neg_track_fDcaXY) < 1) ];

    print("ptmin = {0:3.2f} GeV/c , etamax = {1:3.2f}".format(ptmin, etamax));
    df = apply_kinetic_cut_track(df, ptmin, etamax);

    outname = "output_lmee_pair_ptmin{0:3.2f}GeV_etamax{1:3.2f}.root".format(ptmin, etamax);
    outfile = TFile(outname, "RECREATE");
    ndim = 3;
    nbin = np.array([500, 100, 200], dtype=np.intc);
    xmin = np.array([  0,   0,   0], dtype=np.double);
    xmax = np.array([  5,  10,  20], dtype=np.double);
    hs = THnSparseF("hs", "hs", ndim, nbin, xmin, xmax);
    hs.Sumw2();
    hs.GetAxis(0).SetTitle("m_{ee} (GeV/c^{2})");
    hs.GetAxis(1).SetTitle("p_{T,ee} (GeV/c)");
    hs.GetAxis(2).SetTitle("DCA_{xy,ee} (#sigma)");

    #lf
    df_lf = df[ (df.fIsSM==1) & (abs(df.fPdgCode) < 399) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_lf);
    print("number of ee pairs from same mother", npair);
    hs_lf = fill_sparse_hist(hs, df_lf);
    hs_lf.SetName("hs_lf");
    hs_lf.SetTitle("LF -> ee");
    outfile.WriteTObject(hs_lf);
    #for index, row in df_lf.iterrows():
    #    if row.fPt < 0.1 and 0.25 < row.fM :
    #        print("lf->ee", row.fM, row.fPt, row['pos_track_fSign'], row['neg_track_fSign'], row['pos_track_fPdgCode'], row['neg_track_fPdgCode'], row['pos_track_fMotherPdgCode'], row['neg_track_fMotherPdgCode'], row['pos_track_fGrandMotherPdgCode'], row['neg_track_fGrandMotherPdgCode']);

    #prompt J/psi
    df_prompt_jpsi = df[ (df.fIsSM==1) & (abs(df.fPdgCode) == 443) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)
    & ~ ( ( (500 < abs(df.pos_track_fGrandMotherPdgCode)) & (abs(df.pos_track_fGrandMotherPdgCode) < 599) ) | ( (5000 < abs(df.pos_track_fGrandMotherPdgCode)) & (abs(df.pos_track_fGrandMotherPdgCode) < 5999) ) )
    & ~ ( ( (500 < abs(df.neg_track_fGrandMotherPdgCode)) & (abs(df.neg_track_fGrandMotherPdgCode) < 599) ) | ( (5000 < abs(df.neg_track_fGrandMotherPdgCode)) & (abs(df.neg_track_fGrandMotherPdgCode) < 5999) ) )
    ];
    npair = len(df_prompt_jpsi);
    print("number of ee pairs from prompt jpsi", npair);
    hs_prompt_jpsi = fill_sparse_hist(hs, df_prompt_jpsi);
    hs_prompt_jpsi.SetName("hs_prompt_jpsi");
    hs_prompt_jpsi.SetTitle("prompt J/#psi -> ee");
    outfile.WriteTObject(hs_prompt_jpsi);

    #nonprompt J/psi
    df_nonprompt_jpsi = df[ (df.fIsSM==1) & (abs(df.fPdgCode) == 443) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)
    & ( ( (500 < abs(df.pos_track_fGrandMotherPdgCode)) & (abs(df.pos_track_fGrandMotherPdgCode) < 599) ) | ( (5000 < abs(df.pos_track_fGrandMotherPdgCode)) & (abs(df.pos_track_fGrandMotherPdgCode) < 5999) ) )
    & ( ( (500 < abs(df.neg_track_fGrandMotherPdgCode)) & (abs(df.neg_track_fGrandMotherPdgCode) < 599) ) | ( (5000 < abs(df.neg_track_fGrandMotherPdgCode)) & (abs(df.neg_track_fGrandMotherPdgCode) < 5999) ) )
    ];
    npair = len(df_nonprompt_jpsi);
    print("number of ee pairs from nonprompt jpsi", npair);
    hs_nonprompt_jpsi = fill_sparse_hist(hs, df_nonprompt_jpsi);
    hs_nonprompt_jpsi.SetName("hs_nonprompt_jpsi");
    hs_nonprompt_jpsi.SetTitle("non-prompt J/#psi -> ee");
    outfile.WriteTObject(hs_nonprompt_jpsi);

    #uls hf cc->ee
    df_hf_c2e_c2e = df[ (df.fIsHF)==0 & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_hf_c2e_c2e);
    print("number of ee pairs from HF cc->ee", npair);
    hs_c2e_c2e = fill_sparse_hist(hs, df_hf_c2e_c2e);
    hs_c2e_c2e.SetName("hs_c2e_c2e");
    hs_c2e_c2e.SetTitle("HF ULS c->e + c->e");
    outfile.WriteTObject(hs_c2e_c2e);

    #uls hf bb->ee
    df_hf_b2e_b2e = df[ (df.fIsHF)==1 & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_hf_b2e_b2e);
    print("number of ee pairs from HF bb->ee", npair);
    hs_b2e_b2e = fill_sparse_hist(hs, df_hf_b2e_b2e);
    hs_b2e_b2e.SetName("hs_b2e_b2e");
    hs_b2e_b2e.SetTitle("HF ULS b->e + b->e");
    outfile.WriteTObject(hs_b2e_b2e);
    #for index, row in df_hf_b2e_b2e.iterrows():
    #    #print("b2e_b2e", row.fIsHF, row.fPairType);
    #    print("b2e_b2e",row['pos_track_fSign'], row['neg_track_fSign'], row['pos_track_fPdgCode'], row['neg_track_fPdgCode'], row['pos_track_fMotherPdgCode'], row['neg_track_fMotherPdgCode'], row['pos_track_fGrandMotherPdgCode'], row['neg_track_fGrandMotherPdgCode']);

    #uls hf b2c_b2c->ee
    df_hf_b2c2e_b2c2e = df[ (df.fIsHF==2) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_hf_b2c2e_b2c2e);
    print("number of ee pairs from HF b2c2e_b2c2e", npair);
    hs_b2c2e_b2c2e = fill_sparse_hist(hs, df_hf_b2c2e_b2c2e);
    hs_b2c2e_b2c2e.SetName("hs_b2c2e_b2c2e");
    hs_b2c2e_b2c2e.SetTitle("HF ULS b->c->e + b->c->e");
    outfile.WriteTObject(hs_b2c2e_b2c2e);

    #uls hf b2c2e_b2e_sameb
    df_hf_b2c2e_b2e_sameb = df[ (df.fIsHF==3) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_hf_b2c2e_b2e_sameb);
    print("number of ee pairs from HF b2c2e_b2e_sameb_b2c2e_b2e_sameb", npair);
    hs_b2c2e_b2e_sameb = fill_sparse_hist(hs, df_hf_b2c2e_b2e_sameb);
    hs_b2c2e_b2e_sameb.SetName("hs_b2c2e_b2e_sameb");
    hs_b2c2e_b2e_sameb.SetTitle("HF ULS b->c->e + b->e same b");
    outfile.WriteTObject(hs_b2c2e_b2e_sameb);

    #ls hf b2c2e_b2e_diffb
    df_hf_b2c2e_b2e_diffb = df[ (df.fIsHF==4) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1)];
    npair = len(df_hf_b2c2e_b2e_diffb);
    print("number of ee pairs from HF b2c2e_b2e_diffb_b2c2e_b2e_diffb", npair);
    hs_b2c2e_b2e_diffb = fill_sparse_hist(hs, df_hf_b2c2e_b2e_diffb);
    hs_b2c2e_b2e_diffb.SetName("hs_b2c2e_b2e_diffb");
    hs_b2c2e_b2e_diffb.SetTitle("HF LS b->c->e + b->e different b");
    outfile.WriteTObject(hs_b2c2e_b2e_diffb);

    #uls combinatorial bkg
    df_uls_bkg = df[ (df.fIsSM==0) & (df.fIsHF==-1) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1) & (df.fPairType==0)];
    npair = len(df_uls_bkg);
    print("number of ee pairs from uls bkg", npair);
    hs_uls_bkg = fill_sparse_hist(hs, df_uls_bkg);
    hs_uls_bkg.SetName("hs_uls_bkg");
    hs_uls_bkg.SetTitle("ULS bkg -> ee");
    outfile.WriteTObject(hs_uls_bkg);

    #ls++ combinatorial bkg
    df_lspp_bkg = df[ (df.fIsSM==0) & (df.fIsHF==-1) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1) & (df.fPairType==1)];
    npair = len(df_lspp_bkg);
    print("number of ee pairs from lspp bkg", npair);
    hs_lspp_bkg = fill_sparse_hist(hs, df_lspp_bkg);
    hs_lspp_bkg.SetName("hs_lspp_bkg");
    hs_lspp_bkg.SetTitle("LS++ -> ee");
    outfile.WriteTObject(hs_lspp_bkg);

    #ls-- combinatorial bkg
    df_lsnn_bkg = df[ (df.fIsSM==0) & (df.fIsHF==-1) & (df.pos_track_fIsPhysicalPrimary == 1) & (df.neg_track_fIsPhysicalPrimary == 1) & (df.fPairType==2)];
    npair = len(df_lsnn_bkg);
    print("number of ee pairs from lsnn bkg", npair);
    hs_lsnn_bkg = fill_sparse_hist(hs, df_lsnn_bkg);
    hs_lsnn_bkg.SetName("hs_lsnn_bkg");
    hs_lsnn_bkg.SetTitle("LS-- bkg -> ee");
    outfile.WriteTObject(hs_lsnn_bkg);

    #photon conversion
    df_pc = df[ (df.fIsSM==1) & (abs(df.fPdgCode)==22) & (df.pos_track_fIsPhysicalPrimary == 0) & (df.neg_track_fIsPhysicalPrimary == 0)];
    npair = len(df_pc);
    print("number of ee pairs from photon conversion", npair);
    hs_pc = fill_sparse_hist(hs, df_pc);
    hs_pc.SetName("hs_pc");
    hs_pc.SetTitle("#gamma -> ee");
    outfile.WriteTObject(hs_pc);

    outfile.Close();
#____________________________________________________________________________________________
def draw_pair(period, list_parnames, ptmin, etamax, suffix):
    filename = "output_lmee_pair_ptmin{0:3.2f}GeV_etamax{1:3.2f}.root".format(ptmin, etamax);
    rootfile = TFile.Open(filename, "READ");
    npar = len(list_parnames);

    colors = [kRed+1, kGreen+2, kBlue+1, kYellow+1, kMagenta+1, kCyan+1, kOrange+1, kViolet+1];

    c1 = TCanvas("c1","c1",0,0, 1800, 600);
    c1.SetMargin(0,0,0,0);
    c1.Divide(3,1);

    p1 = c1.cd(1);
    p1.SetLogy(1);
    p1.SetTicks(1,1);
    p1.SetMargin(0.14,0.03,0.12,0.03);
    frame1 = p1.DrawFrame(0,1e-4, 5, 1e+1);
    frame1.GetXaxis().SetTitle("m_{ee} (GeV/c^{2})");
    frame1.GetYaxis().SetTitle("dN/dm_{ee} (a.u.)");
    frame1.GetXaxis().SetTitleSize(0.05);
    frame1.GetYaxis().SetTitleSize(0.05);
    frame1.GetXaxis().SetTitleOffset(1.0);
    frame1.GetYaxis().SetTitleOffset(1.2);
    frame1.GetXaxis().SetLabelSize(0.05);
    frame1.GetYaxis().SetLabelSize(0.05);
    ROOT.SetOwnership(frame1,False);
    ROOT.SetOwnership(p1,False);

    txt = TPaveText(0.2,0.77,0.4,0.92,"NDC");
    txt.SetFillColor(kWhite);
    txt.SetFillStyle(0);
    txt.SetBorderSize(0);
    txt.SetTextAlign(12);#middle,left
    txt.SetTextFont(42);#helvetica
    txt.SetTextSize(0.04);
    txt.AddText("pp at #sqrt{#it{s}} = 13.6 TeV");
    txt.AddText("ALICE simulation LHC23c2b");
    txt.AddText("#it{{p}}_{{T,e}} > {0:3.2f} GeV/#it{{c}}, |#it{{#eta}}_{{e}}| < {1:3.2f}".format(ptmin, etamax));
    txt.Draw();
    ROOT.SetOwnership(txt,False);

    p2 = c1.cd(2);
    p2.SetLogy(1);
    p2.SetTicks(1,1);
    p2.SetMargin(0.14,0.03,0.12,0.03);
    frame2 = p2.DrawFrame(0,1e-4, 10, 1e+1);
    frame2.GetXaxis().SetTitle("p_{T,ee} (GeV/c)");
    frame2.GetYaxis().SetTitle("dN/dp_{T,ee} (a.u.)");
    frame2.GetXaxis().SetTitleSize(0.05);
    frame2.GetYaxis().SetTitleSize(0.05);
    frame2.GetXaxis().SetTitleOffset(1.0);
    frame2.GetYaxis().SetTitleOffset(1.2);
    frame2.GetXaxis().SetLabelSize(0.05);
    frame2.GetYaxis().SetLabelSize(0.05);
    ROOT.SetOwnership(frame2,False);
    ROOT.SetOwnership(p2,False);

    leg = TLegend(0.55,0.7,0.75,0.92);
    leg.SetBorderSize(0);
    leg.SetFillColor(kWhite);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.04);
    ROOT.SetOwnership(leg,False);

    p3 = c1.cd(3);
    p3.SetLogy(1);
    p3.SetTicks(1,1);
    p3.SetMargin(0.14,0.03,0.12,0.03);
    frame3 = p3.DrawFrame(0,1e-4, 20, 1e+1);
    frame3.GetXaxis().SetTitle("DCA_{xy,ee} (#sigma)");
    frame3.GetYaxis().SetTitle("dN/dDCA_{xy,ee} (a.u.)");
    frame3.GetXaxis().SetTitleSize(0.05);
    frame3.GetYaxis().SetTitleSize(0.05);
    frame3.GetXaxis().SetTitleOffset(1.0);
    frame3.GetYaxis().SetTitleOffset(1.2);
    frame3.GetXaxis().SetLabelSize(0.05);
    frame3.GetYaxis().SetLabelSize(0.05);
    ROOT.SetOwnership(frame3,False);

    for ipar in range(0, npar):
        parname = list_parnames[ipar];
        hs = rootfile.Get("hs_{0}".format(parname));
        h1dndm = hs.Projection(0);
        h1dndpt = hs.Projection(1);
        h1dnddca = hs.Projection(2);
        ROOT.SetOwnership(h1dndm, False);
        ROOT.SetOwnership(h1dndpt, False);
        ROOT.SetOwnership(h1dnddca, False);
        h1dndm  .SetDirectory(0);
        h1dndpt .SetDirectory(0);
        h1dnddca.SetDirectory(0);
        h1dndm  .RebinX(10);
        h1dndpt .RebinX(5);
        h1dnddca.RebinX(10);
        h1dndm  .Scale(1, "width");
        h1dndpt .Scale(1, "width");
        h1dnddca.Scale(1, "width");
        h1dndm  .Scale(1/h1dndm  .Integral(1,h1dndm  .GetNbinsX() ));
        h1dndpt .Scale(1/h1dndpt .Integral(1,h1dndpt .GetNbinsX() ));
        h1dnddca.Scale(1/h1dnddca.Integral(1,h1dnddca.GetNbinsX() ));
        make_common_style(h1dndm, 20, 1.0, colors[ipar], 1, 0);
        make_common_style(h1dndpt, 20, 1.0, colors[ipar], 1, 0);
        make_common_style(h1dnddca, 20, 1.0, colors[ipar], 1, 0);
        if "diffb" in parname:
            h1dndm.SetMarkerStyle(24);
            h1dndpt.SetMarkerStyle(24);
            h1dnddca.SetMarkerStyle(24);

        leg.AddEntry(h1dndm, parname, "LP");

        p1 = c1.cd(1);
        h1dndm.Draw("E0same");

        p2 = c1.cd(2);
        h1dndpt.Draw("E0same");

        p3 = c1.cd(3);
        h1dnddca.Draw("E0same");


    p2 = c1.cd(2);
    leg.Draw("");


    date = datetime.date.today().strftime("%Y%m%d");
    c1.Modified();
    c1.Update();
    ROOT.SetOwnership(c1,False);
    c1.SaveAs("{0}_pp13.6TeV_{1}_ptmin{2:3.2f}GeV_etamax{3:3.2f}{4}.eps".format(date, period, ptmin, etamax, suffix));
    c1.SaveAs("{0}_pp13.6TeV_{1}_ptmin{2:3.2f}GeV_etamax{3:3.2f}{4}.pdf".format(date, period, ptmin, etamax, suffix));
    c1.SaveAs("{0}_pp13.6TeV_{1}_ptmin{2:3.2f}GeV_etamax{3:3.2f}{4}.png".format(date, period, ptmin, etamax, suffix));
    rootfile.Close();

#____________________________________________________________________________________________
if __name__ == "__main__":
    filename_csv = "data_ele_ml.csv";
    #ptmin = 0.;
    #etamax = 0.9;
    #extract(filename_csv, 0.0 , 0.9);
    #extract(filename_csv, 0.05, 0.8);
    #extract(filename_csv, 0.1 , 0.8);
    #extract(filename_csv, 0.2 , 0.8);
    #extract(filename_csv, 0.4 , 0.8);
    period = "LHC23c2b";
    #list_parnames = ['lf','prompt_jpsi','nonprompt_jpsi', 'c2e_c2e','b2e_b2e','b2c2e_b2c2e', 'b2c2e_b2e_sameb', 'b2c2e_b2e_diffb', 'pc'];

    #list_parnames_sm = ['lf', 'prompt_jpsi','nonprompt_jpsi'];
    #list_parnames_hf = ['c2e_c2e','b2e_b2e','b2c2e_b2c2e', 'b2c2e_b2e_sameb', 'b2c2e_b2e_diffb'];
    #draw_pair(period, list_parnames_sm, 0.4 , 0.8, "_sm");
    #draw_pair(period, list_parnames_hf, 0.4 , 0.8, "_hf");
    #draw_pair(period, list_parnames_sm, 0.2 , 0.8, "_sm");
    #draw_pair(period, list_parnames_hf, 0.2 , 0.8, "_hf");
    #draw_pair(period, list_parnames_sm, 0.1 , 0.8, "_sm");
    #draw_pair(period, list_parnames_hf, 0.1 , 0.8, "_hf");
    #draw_pair(period, list_parnames_sm, 0.05, 0.8, "_sm");
    #draw_pair(period, list_parnames_hf, 0.05, 0.8, "_hf");
    #draw_pair(period, list_parnames_sm, 0.0 , 0.9, "_sm");
    #draw_pair(period, list_parnames_hf, 0.0 , 0.9, "_hf");

    list_parnames_jpsi_hf = ['prompt_jpsi','nonprompt_jpsi', 'c2e_c2e','b2e_b2e','b2c2e_b2c2e', 'b2c2e_b2e_sameb', 'b2c2e_b2e_diffb'];
    draw_pair(period, list_parnames_jpsi_hf, 0.4 , 0.8, "_jpsi_hf");
    draw_pair(period, list_parnames_jpsi_hf, 0.2 , 0.8, "_jpsi_hf");
