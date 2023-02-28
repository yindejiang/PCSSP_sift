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
period_num_min = 3 
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


if os.path.exists("Candidate"):
    shutil.rmtree("Candidate")
os.makedirs("Candidate")
os.makedirs("./Candidate/DmSigmaFig")
os.makedirs("./Candidate/ACCEL_File")

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
            
    #ACCEL1 = ACCEL1.drop_duplicates(subset="p",keep='first')                                                 
    ACCEL1.to_csv("./Candidate/ACCEL_File/" + fire +  '_Max.csv',sep=',',index=0,header=1)                   
    
    
    

#path=path + "\\Candidate\\ACCEL_File"
path=path + "/Candidate/ACCEL_File"
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
        CAND.append(candidate_Name[i])
    else:
        Non_CAND.append(candidate_Name[i])


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
#"""

for i in range(len(CAND)):
    candidate_ = DF[DF["p"] == CAND[i]]
    #x = candidate_.Period
    AA = []
    for j in range(len(candidate_)):
        AAA = list(candidate_.Sigma)
        if AAA[j] == max(candidate_["Sigma"]):
            AA.append(j)

    fig,ax = plt.subplots(2,1,figsize=(6, 8.265))
    d = {'x': candidate_["DM"], 'y': candidate_["Sigma"]}
    df = pd.DataFrame(data=d)
    df = df.sort_values(by='x', ascending=True)
    ax[0].plot(df['x'], df['y'], color="#791E94")
    ax[0].scatter(df['x'], df['y'], color="#0080ff")
    ax[0].axvline(list(candidate_["DM"])[AA[0]],c="red",linestyle='--', linewidth=2,label=str(list(candidate_["DM"])[AA[0]])+ " (cm$^{-3}$ pc)")
    ax[0].set_xlabel("Trial DM" +" (cm$^{-3}$ pc)", fontsize=14)
    ax[0].set_ylabel("Sigma",fontsize=14)
    ax[0].legend(fontsize=14)
    ax[0].set_xlim(min(candidate_["DM"])-0.05 ,max(candidate_["DM"])+0.05)
    
    #ax[1].hist(x, bins = 50, color="#4c8dae")
    ax[1].scatter(candidate_["Period"], candidate_["Sigma"],s=30, color="#4c8dae")
    ax[1].scatter(list(candidate_["Period"])[AA[0]],list(candidate_["Sigma"])[AA[0]], s=30, c="red",marker='s', label = "Period = " + str(list(candidate_["Period"])[AA[0]])+ " ms")
    ax[1].scatter(list(candidate_["Period"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "Harm Num = " + str(list(candidate_["Num Harm"])[AA[0]]))
    ax[1].scatter(list(candidate_["Period"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "Accel = " + str(list(candidate_["Accel"])[AA[0]])+ " m/s^2")
    ax[1].scatter(list(candidate_["Period"])[AA[0]],list(candidate_["Sigma"])[AA[0]], c="red",alpha=0.0, label = "zmax = " + zmax)
    ax[1].set_xlabel("Period (ms)", fontsize=14)
    ax[1].set_ylabel("Sigma", fontsize=14)
    ax[1].get_yaxis().get_major_formatter().set_scientific(False)
    ax[1].legend(fontsize=10)
    plt.tight_layout(pad=1)
    plt.xticks(rotation = 45)
    plt.savefig("../DmSigmaFig/" +str(list(candidate_["DM1"])[AA[0]]) + "_" +"Cand"+"_" +str(list(candidate_["Cand"])[AA[0]])  +".png",bbox_inches="tight", dpi=200 )
    plt.cla()
    plt.clf()
    plt.close("all")
    
    
#"""