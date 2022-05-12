import os, sys, shutil
import math
import numpy as np
import ctypes
import ROOT
from ROOT import TH1D, TH2D, TH3D, TList
from ROOT import gROOT, gSystem, gStyle, gPad
from ROOT import kWhite, kBlack, kRed, kGreen, kBlue, kYellow, kOrange
from histo_manager import slice_histogram, rebin_histogram, get_R_factor, get_corrected_bkg, get_bkg_subtracted, get_SBratio

#_________________________________________________________________________________________
def analyze_mee_ptee(rootfile,cutname,arr_mee, arr_ptee):
    print(sys._getframe().f_code.co_name);
    outlist = TList();
    outlist.SetName(cutname);
    return outlist;
#_________________________________________________________________________________________
def analyze_mee_ptee_dcaee(rootfile,cutname,arr_mee, arr_ptee, arr_dcaee):
    print(sys._getframe().f_code.co_name);
    outlist = TList();
    outlist.SetName(cutname);
    return outlist;
#_________________________________________________________________________________________
def analyze_mee_ptee_efficiency(rootfile,cutname,arr_mee, arr_ptee):
    print(sys._getframe().f_code.co_name);
    outlist = TList();
    outlist.SetName(cutname);
    return outlist;
#_________________________________________________________________________________________
