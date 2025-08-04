# DeepNTuples ( Unified2025 branch )

High–throughput Ntuple production for CMS *DeepFlavour/ParT* studies and training. DeepNTuples converts CMS MINIAOD samples into **training-ready ROOT ntuples** that feed the DeepFlavour / ParT taggers, together with a set of helper scripts for large-scale grid or HTCondor production and post-processing.


Installation (CMSSW 15_0_2)
============

```
cmsrel CMSSW_15_0_2
cd CMSSW_15_0_2/src/
cmsenv
git cms-init
git clone https://github.com/AlexDeMoor/DeepTuples.git
cd DeepNTuples
git checkout trimmed_beyond_1B
# Add JetToolBox
git submodule init
git submodule update

scram b -j 8
```

Further settings
============

It is important to create your grid proxy in a location that is accessible by other nodes (there is no security issue, your full credentials are still needed for access). For this purpose, redirect the grid proxy location by adding the following to your login script:

```
export X509_USER_PROXY=${HOME}/.gridproxy.pem
```

Production
==========

Before doing a batch submission you can test the ntuplizer locally in the production directory with:
```
cmsRun DeepNtuplizer.py inputFiles=/path/to/file.root
```
The jobs can be submitted using the following syntax
```
jobSub.py --file <sample file> DeepNtuplizer.py <batch directory> --outpath /path/to/output/directory/
```
For an example of sample files, please refer to the .cfg files already in the production directory. You first specify the number of jobs to be submitted, then the input dataset name, which should then be followed by the name of the output. Other arguments such as gluonReduction can then be specified if needed. Each argument need to be separted by at least two whitespaces.
 
The large job output (root files) will NOT be stored in the batch directory. The storage directory is specified by the --outpath argument. The batch directory will contain a symlink to this directory. If the outpath is not specified the ntuples are stored in the deepjet directory, where you need write permission.

The status of the jobs can be checked with
```
cd <batch directory>
check.py <sample subdirectories to be checked>
```

The check.py script provides additional options to resubmit failed jobs or to create sample lists in case a satisfying fraction of jobs ended successfully. 
In this case do:
```
check.py <sample subdirectories to be checked> --action filelist
```
This will create file lists that can be further processed by the DeepJet framework
For resubmitting failed jobs, do:
```
check.py <sample subdirectories to be checked> --action resubmit
```

When the file lists are created, the part used for training of the ttbar and QCD samples (or in principle any other process) can be merged using the executable:
```
mergeSamples.py <no of jets per file> <output dir> <file lists 1> <file lists 2> <file lists 3> ...
```
Here the output directory cannot already exist. For example:
```
mergeSamples.py 400000 /path/to/dir/merged ntuple_*/train_val_samples.txt
```
This will take a significant amount of time - likely more than the ntuple production itself. It is therefore recommended to run the command within 'screen'. In the 106X branch you can also submit via batch by doing --batch. This will create a batch directory in the folder the command is called from.

```
mergeSamples.py 400000 /path/to/dir/merged ntuple_*/train_val_samples.txt --batch
```

Main production params (command-line flags):
==========

DeepNtuplizer’s Python config exposes a rich set of **runtime flags** that can be overridden directly on the command line, e.g.
One can run on Data or MC easily, switching from usual BTV training selection like:

```bash
cmsRun DeepNtuplizer.py maxEvents=100000 isMC=True reportEvery=500
```

To Domain jet selection (Data or MC) or even a specific analysis selection for tagger fine tuning:

```bash
cmsRun DeepNtuplizer.py maxEvents=-1 isMC=True/False isDomain=True isemu=True reportEvery=500
```

| Flag               | Type  | Default | Purpose / behaviour |
|--------------------|-------|---------|---------------------|
| **outputFile**     | str   | "output"| Prefix of the output ROOT file (`.root` is auto-appended) |
| **maxEvents**      | int   | 50001   | Hard stop after *N* events (`-1` for all) |
| **skipEvents**     | int   | 0       | Skip first *N* events |
| **job**            | int   | 0       | Job index inside a multi-job split |
| **nJobs**          | int   | 1       | Total number of jobs for this dataset |
| **reportEvery**    | int   | 1000    | Frequency of FWK progress messages |
| **gluonReduction** | float | 0.0     | Down-weight gluon-jets by this factor (0 ⇢ off) |
| **selectJets**     | bool  | True    | Keep only jets with “good” gen-level match |
| **phase2**         | bool  | False   | Activate Phase-2 jet selection (η < 3.0, PUPPI jets) |
| **puppi**          | bool  | True    | Use `slimmedJetsPuppi` jets |
| **eta**            | bool  | False   | Extend acceptance to |η| < 5.0 (default 4.7) |
| **isMC**           | bool  | True    | Toggle use of generator info (set **False** for data) |
| **isDomain**       | bool  | False   | Tag jets as “domain” samples for domain-adaptation studies |
| **isemu**          | bool  | False   | Mark event as eµ control region (for specialised skims) |
| **ismutau**        | bool  | False   | Mark event as µτₕ control region |
| **isdimu**         | bool  | False   | Mark event as µµ control region |

Customising the Config:
==========

Note we most of the time keep this untouched (we edit the params in the production file) except if we add any new config param.
DeepNtuplizer/python/DeepNtuplizer_cfi.py exposes all switches of the EDAnalyzer. Highlights:

| Parameter                     | Default | Meaning |
|-------------------------------|---------|---------|
| `jets`, `fatjets`             | `slimmedJetsPuppi`, `slimmedJetsAK8` | PF- or PUPPI-jets, AK4 or AK8 |
| `MC`, `Domain`                | `True`, `False` | Toggle MC matching & domain tagging |
| `gluonReduction`              | `0.0`   | Down-weight gluon jets fraction |
| `jetPtMin`, `jetAbsEtaMax`    | `10 GeV`, `5.0` | Kinematic acceptance |
| Domain selections.            | `emu`, `dimu`, `mutau` |

Contributing
==========
* Fork and create a feature branch.
* Respect the CMSSW code style (clang-format).
* Run scram b runtests if you add plugins.
* Open a pull request whenever you are done and have contribution for the rest of the collaboration
