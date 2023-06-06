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
#______________________________________________
#______________________________________________
