#！/bin/bash
#################################################################
python PCSSP_sift.py     

dm=`cat ./PCSSP/*ACCEL-DM.txt`
cand=`cat ./PCSSP/*ACCEL-accelcand.txt`

DM=($dm)
Cand=($cand)

for i in $(seq ${#Cand[*]}); do prepfold  -noxwin  -nosearch  -n 64 -npart 128 -accelcand   ""${Cand[i-1]}""   -accelfile  ""*${DM[i-1]}*.cand""  ""*${DM[i-1]}*.dat""  ;  done
ls *DM*Cand*.png | xargs -n 1 --replace convert {} -gravity east -chop 12%x0 -gravity west -chop 3.5%x0 -gravity north -chop 0x8% {}


for i in $(seq ${#Cand[*]}); do Fig1=`ls *${DM[i-1]}*_Cand_${Cand[i-1]}.pfd.png`;  Fig2=`ls ./PCSSP/DmSigmaFig/*${DM[i-1]}*_Cand_${Cand[i-1]}.png`; convert ${Fig2} -gravity west -chop 1%x0 -gravity north -chop 0x1% -gravity south -chop 0x1%  ${Fig2}; convert ${Fig2} -resize 1986x  ${Fig2}; convert -append ""${Fig1}"" ""${Fig2}""  ""${Fig1}.png""; done

mkdir ./PCSSP/PCSSP_fig

mv *pfd* ./PCSSP/PCSSP_fig

echo ""The numbers of candidate: ${#Cand[*]}""
date
##################################################################                                           
