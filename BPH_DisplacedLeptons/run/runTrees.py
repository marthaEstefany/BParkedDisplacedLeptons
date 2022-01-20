#!/usr/bin/env python3
from __future__ import print_function

import os
import copy
import json

from runPostProcessing import get_arg_parser, run, tar_cmssw
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

run_cfgname = 'svtree_cfg.json'
default_config = {'channel': None,
                  'jec': False, 'jes': None, 'jes_source': '', 'jes_uncertainty_file_prefix': 'RegroupedV2_',
                  # 'jer': 'nominal',
                  'jer': None,
                  'jmr': None, 'met_unclustered': None, 'applyHEMUnc': False,
                  'smearMET': False, 'useMETFixEE2017': True}

# _jes_uncertainty_sources = [
#     'AbsoluteMPFBias', 'AbsoluteScale', 'AbsoluteStat', 'FlavorQCD', 'Fragmentation', 'PileUpDataMC', 'PileUpPtBB',
#     'PileUpPtEC1', 'PileUpPtEC2', 'PileUpPtHF', 'PileUpPtRef', 'RelativeBal', 'RelativeFSR', 'RelativeJEREC1',
#     'RelativeJEREC2', 'RelativeJERHF', 'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativePtHF',
#     'RelativeStatEC', 'RelativeStatFSR', 'RelativeStatHF', 'SinglePionECAL', 'SinglePionHCAL', 'TimePtEta',
# ]
#
# jes_uncertainty_sources = {
#     '2016': _jes_uncertainty_sources + ['RelativeSample'],
#     '2017': _jes_uncertainty_sources + ['RelativeSample'],
#     '2018': _jes_uncertainty_sources,
# }

jes_uncertainty_sources = {
    '2016': ['Absolute', 'Absolute_2016', 'BBEC1', 'BBEC1_2016', 'EC2', 'EC2_2016', 'FlavorQCD', 'HF', 'HF_2016', 'RelativeBal', 'RelativeSample_2016'],
    '2017': ['Absolute', 'Absolute_2017', 'BBEC1', 'BBEC1_2017', 'EC2', 'EC2_2017', 'FlavorQCD', 'HF', 'HF_2017', 'RelativeBal', 'RelativeSample_2017'],
    '2018': ['Absolute', 'Absolute_2018', 'BBEC1', 'BBEC1_2018', 'EC2', 'EC2_2018', 'FlavorQCD', 'HF', 'HF_2018', 'RelativeBal', 'RelativeSample_2018'],
}


def parse_sample_xsec(cfgfile):
    xsec_dict = {}
    with open(cfgfile) as f:
        for l in f:
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            pieces = l.split()
            samp = None
            xsec = None
            isData = False
            for s in pieces:
                if '/MINIAOD' in s or '/NANOAOD' in s:
                    samp = s.split('/')[1]
                    if '/MINIAODSIM' not in s and '/NANOAODSIM' not in s:
                        isData = True
                        break
                else:
                    try:
                        xsec = float(s)
                    except ValueError:
                        try:
                            import numexpr
                            xsec = numexpr.evaluate(s).item()
                        except:
                            pass
            if samp is None:
                logging.warning('Ignore line:\n%s' % l)
            elif not isData and xsec is None:
                logging.error('Cannot find cross section:\n%s' % l)
            else:
                if samp in xsec_dict and xsec_dict[samp] != xsec:
                    raise RuntimeError('Inconsistent entries for sample %s' % samp)
                xsec_dict[samp] = xsec
                if 'PSweights_' in samp:
                    xsec_dict[samp.replace('PSweights_', '')] = xsec
    return xsec_dict


def add_weight_branch(file, xsec, lumi=1000., treename='Events', wgtbranch='xsecWeight'):
    from array import array
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True

    def _get_sum(tree, wgtvar):
        print("AL test test", tree)
        htmp = ROOT.TH1D('htmp', 'htmp', 1, 0, 10)
        tree.Project('htmp', '1.0', wgtvar)
        return float(htmp.Integral())

    def _fill_const_branch(tree, branch_name, buff, lenVar=None):
        if lenVar is not None:
            b = tree.Branch(branch_name, buff, '%s[%s]/F' % (branch_name, lenVar))
            b_lenVar = tree.GetBranch(lenVar)
            buff_lenVar = array('I', [0])
            b_lenVar.SetAddress(buff_lenVar)
        else:
            b = tree.Branch(branch_name, buff, branch_name + '/F')

        b.SetBasketSize(tree.GetEntries() * 2)  # be sure we do not trigger flushing
        for i in range(tree.GetEntries()):
            if lenVar is not None:
                b_lenVar.GetEntry(i)
            b.Fill()

        b.ResetAddress()
        if lenVar is not None:
            b_lenVar.ResetAddress()
    print("AL test file", file)
    f = ROOT.TFile(file, 'UPDATE')
    run_tree = f.Get('Events')
    tree = f.Get('Friends')
    
    # fill cross section weights to the 'Events' tree
    sumwgts = _get_sum(run_tree, 'genWeight')
    xsecwgt = xsec * lumi / sumwgts
    print('AL print total number event= ', sumwgts)
    print('AL print xsec weight= ', xsecwgt)
    return xsecwgt


    #xsec_buff = array('f', [xsecwgt])
    #_fill_const_branch(tree, wgtbranch, xsec_buff)

   # bytesWritten = tree.Write(treename, ROOT.TObject.kOverwrite)
   # f.Close()
   # if bytesWritten == 0:
    #    raise RuntimeError('Failed to update the tree!')

def run_add_weight(args):
    if args.weight_file:
        xsec_dict = parse_sample_xsec(args.weight_file)
    import subprocess
    md = load_metadata(args)
    parts_dir = os.path.join(args.inputdir, '')
    status_file = os.path.join(parts_dir, '.success')
    #if os.path.exists(status_file): #AL commented out
    #    return
    if not os.path.exists(parts_dir):
        os.makedirs(parts_dir)
    for samp in md['samples']:
        infile = '{parts_dir}/{samp}/{samp}.root'.format(parts_dir=parts_dir,samp=samp)
     #AL all commented out for testing  # cmd = 'haddnano.py {outfile} {outputdir}/{samp}/{samp}_*_tree.root'.format(outfile=outfile, outputdir=args.outputdir, samp=samp)
       # logging.debug('...' + cmd)
       # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       # log = p.communicate()[0]
       # log_lower = log.lower().decode('utf-8')
       # if 'error' in log_lower or 'fail' in log_lower:
       #     logging.error(log)
       # if p.returncode != 0:
       #     raise RuntimeError('Hadd failed on %s!' % samp)
        # add weight
        if args.weight_file:
            try:
                print('AL test samp', samp)
                xsec = xsec_dict[samp]
                print('AL test xsec:', xsec)
                if xsec is not None:
                    logging.info('Adding xsec weight to file %s, xsec=%f' % (infile, xsec))
                    args.xsecWgt=[('{samp}'.format(samp=samp),add_weight_branch(infile, xsec))]
                    
            except KeyError as e:
                if '-' not in samp and '_' not in samp:
                    # data
                    logging.info('Not adding weight to sample %s' % samp)
                else:
                    raise e
    with open(status_file, 'w'):
        pass

def load_metadata(args):
    metadatafile = os.path.join(args.jobdir, args.metadata)
    with open(metadatafile) as f:
        md = json.load(f)
    return md


def _base_cut(year, channel):
    # FIXME: remember to update this whenever the selections change in svTreeProducer.py
    basesels = { '2L': ''
       # '0L': 'Sum$(Electron_pt>20 && abs(Electron_eta)<2.5 && Electron_mvaFall17V2Iso_WP90) == 0 && '
        #      'Sum$(Muon_pt>20 && abs(Muon_eta)<2.4 && Muon_looseId && Muon_pfRelIso04_all<0.25) == 0'
    }
    cut = basesels[channel]
    return cut


def _process(args):
    year = args.year
    channel = args.run_channel
    default_config['year'] = year
    default_config['channel'] = channel

    if not args.run_data:
       args.weight_file = 'samples/xsec.conf'
       print('AL test arg:', args)
       run_add_weight(args)
       
#     args.batch = True
    basename = os.path.basename(args.outputdir) + '_' + year + '_' + channel
    args.outputdir = os.path.join(os.path.dirname(args.outputdir), basename, 'data' if args.run_data else 'mc')
    args.jobdir = os.path.join('jobs_%s' % basename, 'data' if args.run_data else 'mc')
    args.datasets = 'samples/%s_%s.yaml' % (channel,
                                               'data' if args.run_data else 'mc')
    args.cut = _base_cut(year, channel)

    args.imports = [('PhysicsTools.BPH_DisplacedLeptons.producers.svTreeProducer', 'SVTreeProducer')]
    if not args.run_data:
        args.imports.extend([
            ('PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer',
              'lepSFProducer'),
            # ('PhysicsTools.NanoTrees.producers.puJetIdSFProducer', 'puJetIdSF_' + year),
            # ('PhysicsTools.NanoTrees.producers.nloWeightProducer', 'nloWeight_' + year),
            ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer',
             'puAutoWeight_2017' if year == '2017' else 'puWeight_' + year),
        ])

    # data, or just nominal MC
    if args.run_data or not args.run_syst:
        args.cut = _base_cut(year, channel)
        cfg = copy.deepcopy(default_config)
        cfg['tagger_threshold'] = None
        if args.run_data:
            cfg['jes'] = None
            cfg['jer'] = None
            cfg['jmr'] = None
            cfg['met_unclustered'] = None
        run(args, configs={run_cfgname: cfg})
        return

    # MC for syst.
    if not args.run_data and args.run_syst:

        # nominal w/ PDF/Scale weights
        logging.info('Start making nominal trees with PDF/scale weights...')
        syst_name = 'LHEWeight'
        opts = copy.deepcopy(args)
        cfg = copy.deepcopy(default_config)
        opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
        opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
        opts.branchsel_out = 'keep_and_drop_output_LHEweights.txt'
        run(opts, configs={run_cfgname: cfg})

        # JER up/down
        for variation in ['up', 'down']:
            syst_name = 'jer_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jer'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            run(opts, configs={run_cfgname: cfg})

        # MET unclustEn up/down
        if channel != '2L':
            for variation in ['up', 'down']:
                syst_name = 'met_%s' % variation
                logging.info('Start making %s trees...' % syst_name)
                opts = copy.deepcopy(args)
                cfg = copy.deepcopy(default_config)
                cfg['met_unclustered'] = variation
                opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
                opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
                run(opts, configs={run_cfgname: cfg})

        # JES sources
        for source in jes_uncertainty_sources[year]:
            for variation in ['up', 'down']:
                syst_name = 'jes_%s_%s' % (source, variation)
                logging.info('Start making %s trees...' % syst_name)
                opts = copy.deepcopy(args)
                cfg = copy.deepcopy(default_config)
                cfg['jes_source'] = source
                cfg['jes'] = variation
                opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
                opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
                run(opts, configs={run_cfgname: cfg})

        # HEM15/16 unc
        if year == '2018':
            for variation in ['down']:
                syst_name = 'HEMIssue_%s' % variation
                logging.info('Start making %s trees...' % syst_name)
                opts = copy.deepcopy(args)
                cfg = copy.deepcopy(default_config)
                cfg['applyHEMUnc'] = True
                opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
                opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
                run(opts, configs={run_cfgname: cfg})


def main():
    parser = get_arg_parser()

    parser.add_argument('--year',
                        required=False,
                        help='year: 2016, 2017, 2018'
                        )

    parser.add_argument('--ul',
                        action='store_true', default=False,
                        help='UL samples'
                        )

    parser.add_argument('--run-channel',
                        required=False, default='2L',
                        help='VH channel: 0L'
                        )

    parser.add_argument('--run-syst',
                        action='store_true', default=False,
                        help='Run all the systematic trees. Default: %(default)s'
                        )

    parser.add_argument('--run-data',
                        action='store_true', default=False,
                        help='Run over data. Default: %(default)s'
                        )

    parser.add_argument('--run-all',
                        action='store_true', default=False,
                        help='Run over all three years and all channels. Default: %(default)s'
                        )

    args = parser.parse_args()

    if not (args.post or args.add_weight or args.merge):
        tar_cmssw(args.tarball_suffix)

    if args.run_all:
        years = ['2018']
        channels = ['2L']
        categories = ['data', 'mc']
    else:
        years = args.year.split(',')
        channels = args.run_channel.split(',')
        categories = ['data' if args.run_data else 'mc']

    for year in years:
        for chn in channels:
            for cat in categories:
                opts = copy.deepcopy(args)
                if cat == 'data':
                    opts.run_data = True
                    opts.nfiles_per_job *= 2
                opts.inputdir = opts.inputdir.rstrip('/').replace('_YEAR_', year)
               # print("AL year", opts.inputdir)
               # assert(year in opts.inputdir)
               # if opts.inputdir.rsplit('/', 1)[1] not in ['data', 'mc']:
               #     opts.inputdir = os.path.join(opts.inputdir, cat)
               # assert(opts.inputdir.endswith(cat))
                opts.year = year
                opts.run_channel = chn
                logging.info('inputdir=%s, year=%s, channel=%s, cat=%s, syst=%s', opts.inputdir, opts.year,
                             opts.run_channel, 'data' if opts.run_data else 'mc', 'syst' if opts.run_syst else 'none')
                _process(opts)


if __name__ == '__main__':
    main()
