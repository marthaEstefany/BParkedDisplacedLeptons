#!/usr/bin/env python3
from __future__ import print_function

import os
import copy

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


def _base_cut(year, channel):
    # FIXME: remember to update this whenever the selections change in svTreeProducer.py
    basesels = {
        '0L': 'Sum$(Electron_pt>20 && abs(Electron_eta)<2.5 && Electron_mvaFall17V2Iso_WP90) == 0 && '
              'Sum$(Muon_pt>20 && abs(Muon_eta)<2.4 && Muon_looseId && Muon_pfRelIso04_all<0.25) == 0'
    }
    cut = basesels[channel]
    return cut


def _process(args):
    year = args.year
    channel = args.run_channel
    default_config['year'] = year
    default_config['channel'] = channel

    if year in ('2017', '2018'):
        args.weight_file = 'samples/xsec_2017.conf'

#     args.batch = True
    basename = os.path.basename(args.outputdir) + '_' + year + '_' + channel
    args.outputdir = os.path.join(os.path.dirname(args.outputdir), basename, 'data' if args.run_data else 'mc')
    args.jobdir = os.path.join('jobs_%s' % basename, 'data' if args.run_data else 'mc')
    args.datasets = 'samples/%s/%s_%s.yaml' % (year + ('UL' if args.ul else ''), channel,
                                               'data' if args.run_data else 'mc')
    args.cut = _base_cut(year, channel)

    args.imports = [('PhysicsTools.BPHDisplacedLeptons.producers.svTreeProducer', 'svTreeFromConfig')]
    if not args.run_data:
        args.imports.extend([
            # ('PhysicsTools.NanoTrees.producers.leptonSFProducerV2',
            #  'electronSF_{year}_{chn},muonSF_{year}_{chn}'.format(year=year, chn=channel)),
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
                        required=False, default='0L',
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
        years = ['2016', '2017', '2018']
        channels = ['0L', '1L', '2L']
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
                assert(year in opts.inputdir)
                if opts.inputdir.rsplit('/', 1)[1] not in ['data', 'mc']:
                    opts.inputdir = os.path.join(opts.inputdir, cat)
                assert(opts.inputdir.endswith(cat))
                opts.year = year
                opts.run_channel = chn
                logging.info('inputdir=%s, year=%s, channel=%s, cat=%s, syst=%s', opts.inputdir, opts.year,
                             opts.run_channel, 'data' if opts.run_data else 'mc', 'syst' if opts.run_syst else 'none')
                _process(opts)


if __name__ == '__main__':
    main()
