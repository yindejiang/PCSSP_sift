#!/usr/bin/env python
# @ Dejiang Yin
import pandas as pd
import os
import shutil
import re
import numpy as np
import glob
import matplotlib.pyplot as plt


# Note: the following are global variables that can
#       (and should) be set in whatever module
#       imports this file.  The following values are
#       "OK" defaults for some searches....

# the precise decimal point of the dfferent periods divided into one group, default is 6.
Period_digital = 6
# Minimum period of candidate (ms), the default is 0.5 ms.
Min_period = 0.5
# Maximum period of candidate (ms), the default is 15000 ms or 15 s.
Max_period = 15000
# The number of  each candidate appears in different trial DM, at least!, the default is  3 times.
period_num_min = 2
# The range of trial DM for each candidate, the default is 100. 
# If you want to search for faint high dispersion measure millisecond pulsars, 
# this value can be set very small, such as 2 or 1 (especially for globular clusters with several known pulsars).
DM_range = 100
# Ignore candidates with a sigma (from incoherent power summation) less than this
sigma_threshold = 2.0
# Perhaps you can continue to add the conditions for screening candidates here,
# and add the corresponding conditions in the following procedure.


path = os.getcwd()
#path=r'D:\FAST_document\data_process\NGC6517\ACCEL.cand\20200426_zmax1200'
os.chdir(path)
# The suffix of accelsearch results files from PRESTO, e.g., NGC6517_DM180.0_ACCEL_1200, the default is 0 (-zmax 0, 10, 20, ...)
globaccel = "*ACCEL_*0"
candfiles = glob.glob(globaccel)


if os.path.exists("PCSSP"):
    shutil.rmtree("PCSSP")
os.makedirs("PCSSP")
os.makedirs("./PCSSP/DmSigmaFig")
os.makedirs("./PCSSP/ACCEL_File")

for fire in candfiles:
    firelist=fire.split('_') 
    zmax=firelist[-1]
    linelist = []                                                                                            
    with open(fire, "r") as f:                                                                               
        for line in f.readlines():                                                                           
            line = line.strip('\n')                                                                          
            linelist.append(line)                                                                            
                                                                                                             
    Linelist = []                                                                                            
    i = 0                                                                                                    
    while i < len(linelist):                                                                                 
        if linelist[i] == '':                                                                                
            break                                                                                            
        Linelist.append(linelist[i])                                                                         
        i+=1                                                                                                 
    Linelist = Linelist[3:]                                                                                  
                                                                                                             
    ACCEL=[]                                                                                                 
    for i in range(len(Linelist)):                                                                           
        ACCEL.append(Linelist[i].strip().split(" "))                                                         
    for i in range(len(ACCEL)):                                                                              
        while "" in ACCEL[i]:                                                                                
            ACCEL[i].remove("")                                                                              
                                                                                                             
    ACCEL1 = []                                                                                              
    for i in range(len(ACCEL)):                                                                              
        ACCEL1.append(ACCEL[i][0:11])                                                                        
                                                                                                             
    ACCEL1 = pd.DataFrame(ACCEL1)                                                                            
    ACCEL1.columns = ['Cand', 'Sigma', 'Summed Power', 'Coherent Power', 'Num Harm','Period',\
                      'Frequency','FFT"r"', 'Freq Deriv', 'FFT "z"', 'Accel' ]                               
                                                                                                             
    dm_string = fire.split("DM")[-1].split("_")[0]                                                           
    dm_string1 = "DM" + fire.split("DM")[-1].split("_")[0]                                                   
    ACCEL1.insert(loc=6, column='DM', value=dm_string)                                                       
    ACCEL1.insert(loc=7, column='DM1', value=dm_string1)                                                     
                                                                                                             
    P = ACCEL1['Period'].str.replace(r"\(.*\)","",regex=True)                                               
    ACCEL1.insert(loc=6, column='P', value=P)    
    
    pattern = r'\d+\.\d+x10\^\d+'
    mask = ACCEL1['P'].str.contains(pattern, regex=True)
    ACCEL1.loc[mask, 'P'] = ACCEL1.loc[mask, 'P'].apply(lambda x: float(re.sub(r'x10\^', 'e', x)))
    p= []                                                                                                    
    for i in range(len(ACCEL1)):                                                                             
        A= str(ACCEL1['P'][i])                                                                                    
        B=A[0:Period_digital]                                                                                             
        p.append(B)                                                                                          
    ACCEL1.insert(loc=7, column='p', value=p)  
            
    ACCEL1 = ACCEL1.drop_duplicates(subset="p",keep='first')                                                 
    ACCEL1.to_csv("./PCSSP/ACCEL_File/" + fire +  '_Max.csv',sep=',',index=0,header=1)                   
    
    
    

#path=path + "\\Candidate\\ACCEL_File"
path=path + "/PCSSP/ACCEL_File"
os.chdir(path)
DF = pd.DataFrame(columns=['Cand', 'Sigma', 'Summed Power', 'Coherent Power', 'Num Harm','Period',\
                      'P','p','DM','DM1','Frequency','FFT"r"', 'Freq Deriv', 'FFT "z"', 'Accel' ])

i =0
fire_Num = []
for fire in os.listdir():
    if fire.endswith('_Max.csv'):
        firelist=fire.split('_')
        fire_Num.append(firelist[0][0:])

        while i < len(fire_Num):
            DF2 =  pd.read_csv(fire)
            DF = pd.concat([DF, DF2], ignore_index=True)
            i+=1

DF.to_csv("../"+'All_Candidate.csv',sep=',', index=0, header=1)
DF_ = DF.drop_duplicates(subset="p",keep='first')
DF_.to_csv("../" + 'One_Candidate.csv',sep=',',index=0,header=1)


candidate_p = list(DF_["p"])
CAND = []
Non_CAND = []

# Setting of candidate conditions!

for i in range(len(DF_)):
    if ( len(DF[DF["p"] == candidate_p[i]].p) >= period_num_min ) \
    and ( (max(DF[DF["p"] == candidate_p[i]].DM) - min(DF[DF["p"] == candidate_p[i]].DM))  <= DM_range )\
    and ( candidate_p[i] >= Min_period )\
    and ( candidate_p[i] <= Max_period )\
    and ( max(DF[DF["p"] == candidate_p[i]].Sigma)  >= sigma_threshold ):
    # You can add other conditions here.
        CAND.append(candidate_p[i])
    else:
        Non_CAND.append(candidate_p[i])


pp = []
dmdm = []
sigma = []
Cand = []
Num_Harm = []
Accel = []

for i in range(len(CAND)):
    candidate_ = DF[DF["p"] == CAND[i]]
    AA = []
    for j in range(len(candidate_)):
        AAA = list(candidate_.Sigma)
        if AAA[j] == max(candidate_["Sigma"]):
            AA.append(j)
    pp.append(str(list(candidate_["p"])[0]))
    dmdm.append(str(list(candidate_["DM1"])[AA[0]]))
    sigma.append(str(list(candidate_["Sigma"])[AA[0]]))
    Cand.append(str(list(candidate_["Cand"])[AA[0]]))
    Num_Harm.append(str(list(candidate_["Num Harm"])[AA[0]]))
    Accel.append(str(list(candidate_["Accel"])[AA[0]]))
    
    
c ={"CAND":Cand,
   "DM":dmdm,
   "p":pp,
   "Sigma":sigma,
   "Num_Harm":Num_Harm,
   "Accel":Accel}
best_cand = pd.DataFrame(c)
best_cand.to_csv("../"+'best_Candidate.csv',sep=',',index=0,header=1)

dm = best_cand["DM"]
DM={"DM" : dm}
DM = pd.DataFrame(DM)
DM_T = DM.T
DM_T.to_csv('../'+str(len(CAND)) +'ACCEL-DM.txt',sep=' ',index=0,header=0)

cand = best_cand["CAND"]
accelcand = {"accelcand" : cand}
accelcand = pd.DataFrame(accelcand)
accelcand_T = accelcand.T
accelcand_T.to_csv('../'+str(len(CAND)) +'ACCEL-accelcand.txt',sep=' ',index=0,header=0)
print("Accel_sifting candidate numbers:",len(CAND))
print("Accel_sifing results are in folder, Candidate")
print("OK!")



###  DM - Sigma relation figure
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as ticker

for i in range(len(CAND)):
    candidate_ = DF[DF["p"] == CAND[i]]
    AA = []
    for j in range(len(candidate_)):
        AAA = list(candidate_.Sigma)
        if AAA[j] == max(candidate_["Sigma"]):
            AA.append(j)

    fig,ax = plt.subplots(1,1,figsize=(10, 4))
    d = {'DM': candidate_["DM"], 'Sigma': candidate_["Sigma"], 'P':candidate_["P"]}
    df = pd.DataFrame(data=d)
    df = df.sort_values(by='DM', ascending=True)
    # Create scatter plot
    ax0 = ax.scatter(df['DM'], df['Sigma'], c=df['P'], cmap='Greys')
    # Add circles to scatter plot
    ax.scatter(df['DM'], df['Sigma'], marker='o', facecolors='none', edgecolors='#000000', s=50,linewidths=1.5)
    # Add line to scatter plot
    ax.plot(df['DM'], df['Sigma'], color="#791E94")
    nums = np.array(candidate_["P"])
    max_decimals = 0
    for num in nums:
        num_str = str(num)
        if "." in num_str:
            decimal_part = num_str.split('.')[-1]
        else:
            decimal_part = ""
        decimal_len = len(decimal_part)
        if decimal_len > max_decimals:
            max_decimals = decimal_len
    
    num_ticks = len(df['P']) + 1
    num_decimals = max_decimals
    format_str = f'%.{num_decimals}f'
    ax.axvline(list(candidate_["DM"])[AA[0]],c="#791E94",linestyle='--', linewidth=2,label=str(list(candidate_["DM"])[AA[0]])+ " (cm$^{-3}$ pc)")
    ax.scatter(list(candidate_["DM"])[AA[0]],list(candidate_["Sigma"])[AA[0]], s=30, c="red",alpha=0.0, marker='s', label = "Period: " + str(list(candidate_["Period"])[AA[0]])+ " ms")
    ax.scatter(list(candidate_["DM"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "zmax: " + zmax+"; "+"Candnum"+": " +str(list(candidate_["Cand"])[AA[0]]))
    ax.scatter(list(candidate_["DM"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "Accel: " + str(list(candidate_["Accel"])[AA[0]])+ " m/s^2")
    ax.scatter(list(candidate_["DM"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "Harm Num: " + str(list(candidate_["Num Harm"])[AA[0]]))
    ax.set_xlabel("Trial DM" +" (cm$^{-3}$ pc)", fontsize=9)
    ax.set_ylabel("Sigma",fontsize=9)
    ax.legend(fontsize=9)
    # Set colorbar limits to data limits
    cbar = fig.colorbar(ax0, ax=ax, format=format_str, label="Period (ms)",pad = 0.01, fraction=0.035)  
    vmin = df['P'].min()
    vmax = df['P'].max()
    cbar.set_ticks([vmin, vmax])
    cbar.set_label(label="Period (ms)", size=9)
    df1 = df.drop_duplicates(subset="P",keep='first')      
    num_ticks = len(df1['P'])
    cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
    plt.savefig("../DmSigmaFig/" +str(list(candidate_["DM1"])[AA[0]]) + "_" +"Cand"+"_" +str(list(candidate_["Cand"])[AA[0]])  +".png",bbox_inches="tight", dpi=200 )
    plt.cla()
    plt.clf()
    plt.close("all")


