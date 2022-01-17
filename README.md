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
python3 runTrees.py -i /home/alesauva/CMSSW_10_2_15/src/PhysicsTools/BParkingNano/test -o output -d samples/2018/2L_mc.yaml -c 'nSV>0' --friend -I PhysicsTools.BPH_DisplacedLeptons.producers.svTreeProducer svTree --year 2018

cd jobs_output_2018_2L/mc
./processor.py 0
```
