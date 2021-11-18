# BParkedDisplacedLeptons

#### Set up CMMSW and the official CMS NanoAOD-tools
```
cmsrel CMSSW_12_0_1
cd CMSSW_12_0_1
cmsenv

git clone git@github.com:cms-nanoaod/nanoaod-tools.git PhysicsTools/NanoAODTools
```
#### Clone this custom repo for BParked Displaced Leptons
```
cd PhysicsTools/
git clone git@github.com:marthaEstefany/BParkedDisplacedLeptons
```
#### Compile
```
scram b -j8
```
