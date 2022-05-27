import ROOT
from ROOT import TH1D, TF1

class VirutalPhotonFitter:
    def __init__(self, h1data, h1LF, h1HF, h1vph):
        self.h1data  = h1data.Clone("h1data_tmp");
        self.h1LF    = h1LF.Clone("h1LF_tmp");
        self.h1HF    = h1HF.Clone("h1HF_tmp");
        self.h1vph   = h1vph.Clone("h1vph_tmp");
        self.f1vph = TF1("f1vph",self.vph_function,0,5,1);
        self.f1vph.SetNpx(5000);
        self.f1vph.SetParLimits(0,-1,+1);
        self.f1vph.SetParameter(0,0.1);
        self.f1vph.SetParError(0,0.01);
        self.f1vph.SetParName(0,"r");
        #print(self.h1data.GetNbinsX());
        #print(self.h1LF.GetNbinsX());
        #print(self.h1HF.GetNbinsX());
        #print(self.h1vph.GetNbinsX());

    def vph_function(self,x,par):
        r = par[0];#direct photon fraction
        mbinLF  = self.h1LF .FindBin(x[0]);
        mbinHF  = self.h1HF .FindBin(x[0]);
        mbinVPH = self.h1vph.FindBin(x[0]);
        dNdm = r * self.h1vph.GetBinContent(mbinVPH) + (1 - r) * self.h1LF.GetBinContent(mbinLF) + self.h1HF.GetBinContent(mbinHF);
        return dNdm;

    def get_function(self):
        return self.f1vph;

    def fit(opt1, opt2, xmin, xmax):
        return self.h1data.Fit(self.f1vph,opt1,opt2,xmin,xmax);
