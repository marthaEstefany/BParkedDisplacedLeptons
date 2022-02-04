#!/bin/bash


#unalias cp

stepsize=0.1
job=402
nstep=$(echo "$job" | bc)
echo nstep=$nstep
for (( i=0; i<$nstep; i++ ))
do
  
  shift=$(echo " $i" | bc)
  echo "./processor.py $shift"
  ./processor.py $shift
  xrdcp BParkNANO_mc_2022*.root root://cmseos.fnal.gov//store/user/alesauva/output
done


