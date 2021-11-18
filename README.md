# BParkedDisplacedLeptons

#### Set up CMMSW and the official CMS NanoAOD-tools
```
cmsrel CMSSW_12_0_1
cd CMSSW_12_0_1
cmsenv

git clone git@github.com:cms-nanoaod/nanoaod-tools.git PhysicsTools/NanoAODTools
```
#### Clone custom BParked Displaced Leptons repo
```
cd PhysicsTools/
git clone git@github.com:marthaEstefany/BParkedDisplacedLeptons
```
#### Compile
```
cd ..
scram b -j8
```
#### Run a test interactively
```
cd PhysicsTools/BPH_DisplacedLeptons/run
python3 runPostProcessing.py -i /eos/uscms/store/user/manunezo/BParkingNANO_2021Oct06/ParkingBPH1/ -o output -d samples/2018/train.yaml -c 'nSV>0' --friend -I PhysicsTools.BPH_DisplacedLeptons.producers.svTreeProducer svTree -n 1

cd jobs
./processor.py 0
```
