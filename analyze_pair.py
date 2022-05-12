import os, sys, shutil
import math
import numpy as np
import ctypes
import ROOT
from ROOT import TH1D, TH2D, TH3D, TList
from ROOT import gROOT, gSystem, gStyle, gPad
from ROOT import kWhite, kBlack, kRed, kGreen, kBlue, kYellow, kOrange
from histo_analyzer import slice_histogram, rebin_histogram, get_R_factor, get_corrected_bkg, get_bkg_subtracted, get_SBratio

#____________________________________________________________________________________________
def analyze_mee_pTee(arr_mee, arr_ptee):
    print(arr_mee);
    print(arr_ptee);
#____________________________________________________________________________________________
def analyze_mee_pTee_dcaee(arr_mee, arr_ptee, arr_dcaee):
    print(arr_mee);
    print(arr_ptee);
    print(arr_dcaee);
#____________________________________________________________________________________________
