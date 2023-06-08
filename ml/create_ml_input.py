import os
import sys
import math
import numpy as np
import pandas as pd
import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import gROOT, TBranch
from ROOT import TFile, TDirectory, TTree, TH1F, TH2F, THnSparseF, TEventList, TMath

#_________________________________________________________________________________
def create_ml_input(filename, criteria_v0="", suffix=""):
    print(sys._getframe().f_code.co_name);
    print("reading...", filename);
    rootfile = TFile.Open(filename,"READ");

    outfile = TFile("tmp_output_pair_ee{0}.root".format(suffix), "RECREATE");
    h2VxyMC = TH2F("h2VxyMC","seconday vertex of e^{#pm} from #gamma in XY MC;V_{x} (cm); V_{y} (cm)", 2000,-100,+100, 2000,-100,+100);
    h2DCA = TH2F("h2DCA","DCA xy vs z;DCA_{xy} (cm); DCA_{z} (cm)", 1000,-5,+5, 1000,-5,+5);

    h2MvsPt = TH2F("h2MvsPt","h2MvsPt", 500,0,5, 100,0,10);
    h2MvsPt.Sumw2();

    list_data = [];
    list_var_coll = [];
    list_var_pair = [];
    list_var_pos_track = [];
    list_var_neg_track = [];

    nall = 0;

    dirnames = rootfile.GetListOfKeys();
    for il in range(0, dirnames.GetEntries()):
        key = dirnames.At(il).GetName();
        #print(key);
        if "DF_" not in key:
            continue;
        if il % 10 == 0:
            print("reading DF at", il);

        df = rootfile.Get(key);
        tree_coll = df.Get("Collisions");
        tree_pair = df.Get("Pairs");
        tree_track = df.Get("Tracks");

        tree_pair.Draw(">>selected_tree_pair",criteria);
        selected_tree_pair = gROOT.FindObject("selected_tree_pair"); #this is TEventList object
        npair = selected_tree_pair.GetN();
        #print(key, npair);

        for ipair in range(0, npair):
            tree_pair.GetEntry(selected_tree_pair.GetEntry(ipair), 0);
            #get event multiplicity
            tree_coll.GetEntry(tree_pair.fIndexMyCollisions,0);

            #if tree_coll.fSel8 < 0.5:
            #    continue;

            #if abs(tree_coll.fPosZ) > 10.0:
            #    continue;

            nall += npair;
            list_var_coll.append([
                # tree_coll.fPosX
                #,tree_coll.fPosY
                tree_coll.fPosZ
                #,tree_coll.fNumContrib
                #,tree_coll.fSel8
                #,tree_coll.fBz
                #,tree_coll.fGeneratorsID
                #,tree_coll.fMCPosX
                #,tree_coll.fMCPosY
                #,tree_coll.fMCPosZ
                #,tree_coll.fMultTPC
                #,tree_coll.fMultFV0A
                #,tree_coll.fMultFV0C
                #,tree_coll.fMultFT0A
                #,tree_coll.fMultFT0C
                #,tree_coll.fMultFDDA
                #,tree_coll.fMultFDDC
                #,tree_coll.fMultZNA
                #,tree_coll.fMultZNC
                #,tree_coll.fMultTracklets
                ,tree_coll.fMultNTracksPV
                #,tree_coll.fMultNTracksPVeta1
            ]);
            h2MvsPt.Fill(tree_pair.fM, tree_pair.fPt);
            list_var_pair.append([
                tree_pair.fM
                ,tree_pair.fPt
                ,tree_pair.fEta
                ,tree_pair.fPhi
                ,tree_pair.fPhiV
                ,tree_pair.fPairDCAxy
                ,tree_pair.fPairDCAz
                ,tree_pair.fIsSM
                ,tree_pair.fIsHF
                ,tree_pair.fPairType
                ,tree_pair.fIsPrompt
                ,tree_pair.fPdgCode
                #,tree_pair.fStatusCode
                #,tree_pair.fFlags
                #,tree_pair.fVx
                #,tree_pair.fVy
                #,tree_pair.fVz
            ]);

            #first positive track
            pos_track_id = tree_pair.fIndexMyTracks_Pos;
            tree_track.GetEntry(pos_track_id, 0);
            ncls_its = 0;
            for il in range(0,7):
               if bool(ord(tree_track.fITSClusterMap) & (1 << il)):
                    ncls_its += 1;
            list_var_pos_track.append([
                 tree_track.fSign    
                ,tree_track.fPt      
                ,tree_track.fEta     
                ,tree_track.fPhi     
                ,tree_track.fDcaXY   
                ,tree_track.fDcaZ    
                ,tree_track.fDCAresXY
                ,tree_track.fDCAresZ 
                ,tree_track.fTPCNClsFindable
                ,tree_track.fTPCNClsFound
                ,tree_track.fTPCNClsCrossedRows
                ,tree_track.fTPCChi2NCl
                ,tree_track.fTPCInnerParam
                ,tree_track.fTPCSignal
                ,tree_track.fTPCNSigmaEl
                ,tree_track.fTPCNSigmaMu
                ,tree_track.fTPCNSigmaPi
                ,tree_track.fTPCNSigmaKa
                ,tree_track.fTPCNSigmaPr
                ,tree_track.fBeta
                ,tree_track.fTOFNSigmaEl
                ,tree_track.fTOFNSigmaMu
                ,tree_track.fTOFNSigmaPi
                ,tree_track.fTOFNSigmaKa
                ,tree_track.fTOFNSigmaPr
                ,ncls_its
                ,tree_track.fITSChi2NCl
                ,bool(ord(tree_track.fITSClusterMap) &  1)
                ,bool(ord(tree_track.fITSClusterMap) &  2)
                ,bool(ord(tree_track.fITSClusterMap) &  4)
                ,bool(ord(tree_track.fITSClusterMap) &  8)
                ,bool(ord(tree_track.fITSClusterMap) & 16)
                ,bool(ord(tree_track.fITSClusterMap) & 32)
                ,bool(ord(tree_track.fITSClusterMap) & 64)
                #,tree_track.fMCPt   
                #,tree_track.fMCEta  
                #,tree_track.fMCPhi  
                #,tree_track.fMCVx   
                #,tree_track.fMCVy   
                #,tree_track.fMCVz   
                ,tree_track.fPdgCode
                ,tree_track.fIsPhysicalPrimary
                #,tree_track.fMotherPdgCode
                #,tree_track.fGrandMotherPdgCode
            ]);

            #second negative track
            neg_track_id = tree_pair.fIndexMyTracks_Neg;
            tree_track.GetEntry(neg_track_id, 0);
            ncls_its = 0;
            for il in range(0,7):
               if bool(ord(tree_track.fITSClusterMap) & (1 << il)):
                    ncls_its += 1;
            list_var_neg_track.append([
                tree_track.fSign    
                ,tree_track.fPt      
                ,tree_track.fEta     
                ,tree_track.fPhi     
                ,tree_track.fDcaXY   
                ,tree_track.fDcaZ    
                ,tree_track.fDCAresXY
                ,tree_track.fDCAresZ 
                ,tree_track.fTPCNClsFindable
                ,tree_track.fTPCNClsFound
                ,tree_track.fTPCNClsCrossedRows
                ,tree_track.fTPCChi2NCl
                ,tree_track.fTPCInnerParam
                ,tree_track.fTPCSignal
                ,tree_track.fTPCNSigmaEl
                ,tree_track.fTPCNSigmaMu
                ,tree_track.fTPCNSigmaPi
                ,tree_track.fTPCNSigmaKa
                ,tree_track.fTPCNSigmaPr
                ,tree_track.fBeta
                ,tree_track.fTOFNSigmaEl
                ,tree_track.fTOFNSigmaMu
                ,tree_track.fTOFNSigmaPi
                ,tree_track.fTOFNSigmaKa
                ,tree_track.fTOFNSigmaPr
                ,ncls_its
                ,tree_track.fITSChi2NCl
                ,bool(ord(tree_track.fITSClusterMap) &  1)
                ,bool(ord(tree_track.fITSClusterMap) &  2)
                ,bool(ord(tree_track.fITSClusterMap) &  4)
                ,bool(ord(tree_track.fITSClusterMap) &  8)
                ,bool(ord(tree_track.fITSClusterMap) & 16)
                ,bool(ord(tree_track.fITSClusterMap) & 32)
                ,bool(ord(tree_track.fITSClusterMap) & 64)
                #,tree_track.fMCPt   
                #,tree_track.fMCEta  
                #,tree_track.fMCPhi  
                #,tree_track.fMCVx   
                #,tree_track.fMCVy   
                #,tree_track.fMCVz   
                ,tree_track.fPdgCode
                ,tree_track.fIsPhysicalPrimary
                #,tree_track.fMotherPdgCode
                #,tree_track.fGrandMotherPdgCode
            ]);

    print("nall = ", nall);
    print("len(list_var_coll) = ", len(list_var_coll));
    print("len(list_var_pair) = ", len(list_var_pair));

    data_coll = np.array(list_var_coll);
    data_pair = np.array(list_var_pair);
    data_pos  = np.array(list_var_pos_track);
    data_neg  = np.array(list_var_neg_track);

    data = np.concatenate([data_coll, data_pair, data_pos, data_neg], axis=1);
    #print(data);
    np.save('data_ele_ml.npy', data);

    columns = [
        # 'fPosX'
        #,'fPosY'
        'fPosZ'
        #,'fNumContrib'
        #,'fSel8'
        #,'fBz'
        #,'fGeneratorsID'
        #,'fMCPosX'
        #,'fMCPosY'
        #,'fMCPosZ'
        #,'fMultTPC'
        #,'fMultFV0A'
        #,'fMultFV0C'
        #,'fMultFT0A'
        #,'fMultFT0C'
        #,'fMultFDDA'
        #,'fMultFDDC'
        #,'fMultZNA'
        #,'fMultZNC'
        #,'fMultTracklets'
        ,'fMultNTracksPV'
        #,'fMultNTracksPVeta1'

        ,'fM'
        ,'fPt'
        ,'fEta'
        ,'fPhi'
        ,'fPhiV'
        ,'fPairDCAxy'
        ,'fPairDCAz'
        ,'fIsSM'
        ,'fIsHF'
        ,'fPairType'
        ,'fIsPrompt'
        ,'fPdgCode'
        #,'fStatusCode'
        #,'fFlags'
        #,'fVx'
        #,'fVy'
        #,'fVz'

        ,'pos_track_fSign'
        ,'pos_track_fPt'
        ,'pos_track_fEta'
        ,'pos_track_fPhi'
        ,'pos_track_fDcaXY'
        ,'pos_track_fDcaZ'
        ,'pos_track_fDCAresXY'
        ,'pos_track_fDCAresZ'
        ,'pos_track_fTPCNClsFindable'
        ,'pos_track_fTPCNClsFound'
        ,'pos_track_fTPCNClsCrossedRows'
        ,'pos_track_fTPCChi2NCl'
        ,'pos_track_fTPCInnerParam'
        ,'pos_track_fTPCSignal'
        ,'pos_track_fTPCNSigmaEl'
        ,'pos_track_fTPCNSigmaMu'
        ,'pos_track_fTPCNSigmaPi'
        ,'pos_track_fTPCNSigmaKa'
        ,'pos_track_fTPCNSigmaPr'
        ,'pos_track_fBeta'
        ,'pos_track_fTOFNSigmaEl'
        ,'pos_track_fTOFNSigmaMu'
        ,'pos_track_fTOFNSigmaPi'
        ,'pos_track_fTOFNSigmaKa'
        ,'pos_track_fTOFNSigmaPr'
        ,'pos_track_fITSNcls'
        ,'pos_track_fITSChi2NCl'
        ,'pos_track_hit_on_ITS1'
        ,'pos_track_hit_on_ITS2'
        ,'pos_track_hit_on_ITS3'
        ,'pos_track_hit_on_ITS4'
        ,'pos_track_hit_on_ITS5'
        ,'pos_track_hit_on_ITS6'
        ,'pos_track_hit_on_ITS7'
        #,'pos_track_fMCPt'
        #,'pos_track_fMCEta'
        #,'pos_track_fMCPhi'
        #,'pos_track_fMCVx'
        #,'pos_track_fMCVy'
        #,'pos_track_fMCVz'
        ,'pos_track_fPdgCode'
        ,'pos_track_fIsPhysicalPrimary'
        #,'pos_track_fMotherPdgCode'
        #,'pos_track_fGrandMotherPdgCode'

        ,'neg_track_fSign'
        ,'neg_track_fPt'
        ,'neg_track_fEta'
        ,'neg_track_fPhi'
        ,'neg_track_fDcaXY'
        ,'neg_track_fDcaZ'
        ,'neg_track_fDCAresXY'
        ,'neg_track_fDCAresZ'
        ,'neg_track_fTPCNClsFindable'
        ,'neg_track_fTPCNClsFound'
        ,'neg_track_fTPCNClsCrossedRows'
        ,'neg_track_fTPCChi2NCl'
        ,'neg_track_fTPCInnerParam'
        ,'neg_track_fTPCSignal'
        ,'neg_track_fTPCNSigmaEl'
        ,'neg_track_fTPCNSigmaMu'
        ,'neg_track_fTPCNSigmaPi'
        ,'neg_track_fTPCNSigmaKa'
        ,'neg_track_fTPCNSigmaPr'
        ,'neg_track_fBeta'
        ,'neg_track_fTOFNSigmaEl'
        ,'neg_track_fTOFNSigmaMu'
        ,'neg_track_fTOFNSigmaPi'
        ,'neg_track_fTOFNSigmaKa'
        ,'neg_track_fTOFNSigmaPr'
        ,'neg_track_fITSNcls'
        ,'neg_track_fITSChi2NCl'
        ,'neg_track_hit_on_ITS1'
        ,'neg_track_hit_on_ITS2'
        ,'neg_track_hit_on_ITS3'
        ,'neg_track_hit_on_ITS4'
        ,'neg_track_hit_on_ITS5'
        ,'neg_track_hit_on_ITS6'
        ,'neg_track_hit_on_ITS7'
        #,'neg_track_fMCPt'
        #,'neg_track_fMCEta'
        #,'neg_track_fMCPhi'
        #,'neg_track_fMCVx'
        #,'neg_track_fMCVy'
        #,'neg_track_fMCVz'
        ,'neg_track_fPdgCode'
        ,'neg_track_fIsPhysicalPrimary'
        #,'neg_track_fMotherPdgCode'
        #,'neg_track_fGrandMotherPdgCode'
    ];

    df = pd.DataFrame(data=data, columns=columns);
    df.to_csv('data_ele_ml.csv');

    outfile.WriteTObject(h2VxyMC);
    outfile.WriteTObject(h2MvsPt);
    outfile.Close();
    rootfile.Close();
#_________________________________________________________________________________
if __name__ == "__main__":
    filename = "emAO2D.root";
    criteria = "";
    suffix = "";
    create_ml_input(filename, criteria, suffix);
#_________________________________________________________________________________
