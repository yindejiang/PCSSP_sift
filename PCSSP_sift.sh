#！/bin/bash
#################################################################
python PCSSP_sift.py     ###步骤5

dm=`cat ./Candidate/*ACCEL-DM.txt`
cand=`cat ./Candidate/*ACCEL-accelcand.txt`

DM=($dm)
Cand=($cand)

for i in $(seq ${#Cand[*]}); do prepfold  -noxwin  -nosearch  -accelcand   ""${Cand[i-1]}""   -accelfile  ""*${DM[i-1]}*.cand""  ""*${DM[i-1]}*.dat""  ;  done


for i in $(seq ${#Cand[*]}); do Fig1=`ls *${DM[i-1]}*_Cand_${Cand[i-1]}.pfd.png`;  Fig2=`ls ./Candidate/DmSigmaFig/*${DM[i-1]}*_Cand_${Cand[i-1]}.png`; convert +append ""${Fig1}"" ""${Fig2}""  ""${Fig1}.png""; done


echo ""The numbers of candidate: ${#Cand[*]}""
date

##################################################################                                           