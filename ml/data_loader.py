import numpy as np
import pandas as pd

#______________________________________________
def load_data_np(filename):
    data = np.load(filename,'r');
    return data;
#______________________________________________
def load_data_pd(filename):
    data = pd.read_csv(filename,index_col=0);
    return data;
#______________________________________________
def create_df_ml_pair_separation(org_df):
    df = org_df.loc[:, [
        'fMultNTracksPV'

        ,'fM'
        ,'fPt'
        ,'fEta'
        ,'fPhi'
        ,'fPhiV'
        ,'fPairDCAxy'
        ,'fPairDCAz'
        ,'fIsSM'    #this is correct answer for classification
        ,'fIsHF'    #this is correct answer for classification
        ,'fPdgCode' #this is correct answer for classification

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
        ,'pos_track_fITSNcls'
        ,'pos_track_fITSChi2NCl'
        ,'pos_track_hit_on_ITS1'
        ,'pos_track_hit_on_ITS2'
        ,'pos_track_hit_on_ITS3'
        ,'pos_track_hit_on_ITS4'
        ,'pos_track_hit_on_ITS5'
        ,'pos_track_hit_on_ITS6'
        ,'pos_track_hit_on_ITS7'

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
        ,'neg_track_fITSNcls'
        ,'neg_track_fITSChi2NCl'
        ,'neg_track_hit_on_ITS1'
        ,'neg_track_hit_on_ITS2'
        ,'neg_track_hit_on_ITS3'
        ,'neg_track_hit_on_ITS4'
        ,'neg_track_hit_on_ITS5'
        ,'neg_track_hit_on_ITS6'
        ,'neg_track_hit_on_ITS7'
    ] ];
    return df;
#______________________________________________
def create_df_ml_photon_conversion_rejection(org_df):
    df = org_df.loc[:, [
        'fMultNTracksPV'

        ,'fM'
        ,'fPt'
        ,'fEta'
        ,'fPhi'
        ,'fPhiV'
        ,'fIsSM'    #this is correct answer for classification
        ,'fPdgCode' #this is correct answer for classification

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
        ,'pos_track_fITSNcls'
        ,'pos_track_fITSChi2NCl'
        ,'pos_track_hit_on_ITS1'
        ,'pos_track_hit_on_ITS2'
        ,'pos_track_hit_on_ITS3'
        ,'pos_track_hit_on_ITS4'
        ,'pos_track_hit_on_ITS5'
        ,'pos_track_hit_on_ITS6'
        ,'pos_track_hit_on_ITS7'

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
        ,'neg_track_fITSNcls'
        ,'neg_track_fITSChi2NCl'
        ,'neg_track_hit_on_ITS1'
        ,'neg_track_hit_on_ITS2'
        ,'neg_track_hit_on_ITS3'
        ,'neg_track_hit_on_ITS4'
        ,'neg_track_hit_on_ITS5'
        ,'neg_track_hit_on_ITS6'
        ,'neg_track_hit_on_ITS7'
    ] ];
    return df;
#______________________________________________
#______________________________________________
#______________________________________________
#______________________________________________
