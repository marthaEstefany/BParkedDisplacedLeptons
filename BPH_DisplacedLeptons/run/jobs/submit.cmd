universe              = vanilla
requirements          = (Arch == "X86_64") && (OpSys == "LINUX")
request_memory        = 2000
request_disk          = 10000000
executable            = /uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/run_postproc_condor.sh
arguments             = $(jobid)
transfer_input_files  = /uscms_data/d3/manunezo/BPHDisplaced/CMSSW.tar.gz,/uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/processor.py,/uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/metadata.json,/uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/keep_and_drop_input.txt,/uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/keep_and_drop_output.txt
output                = /uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/$(jobid).out
error                 = /uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/$(jobid).err
log                   = /uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/$(jobid).log
use_x509userproxy     = true
Should_Transfer_Files = YES
initialdir            = output/pieces
WhenToTransferOutput  = ON_EXIT
want_graceful_removal = true
on_exit_remove        = (ExitBySignal == False) && (ExitCode == 0)
on_exit_hold          = ( (ExitBySignal == True) || (ExitCode != 0) )
on_exit_hold_reason   = strcat("Job held by ON_EXIT_HOLD due to ", ifThenElse((ExitBySignal == True), "exit by signal", strcat("exit code ",ExitCode)), ".")
periodic_release      = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 10*60)


+MaxRuntime = 24*60*60


queue jobid from /uscms_data/d3/manunezo/BPHDisplaced/CMSSW_12_0_1/src/PhysicsTools/BPH_DisplacedLeptons/run/jobs/submit.txt
