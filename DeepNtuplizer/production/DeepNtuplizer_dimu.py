import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import sys

options = VarParsing.VarParsing()

options.register('inputScript','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"input Script")
options.register('outputFile','output',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"output File (w/o .root)")
options.register('maxEvents', -1,VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.int,"maximum events")
options.register('skipEvents', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "total jobs")
options.register('reportEvery', 1000, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "report every")
options.register('gluonReduction', 0.0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.float, "gluon reduction")
options.register('selectJets', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "select jets with good gen match")
options.register('phase2', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "apply jet selection for phase 2. Currently sets JetEtaMax to 3.0 and picks slimmedJetsPuppi as jet collection.")
options.register('puppi', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use puppi jets")
options.register('eta', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use eta up to 5.0")
options.register('isMC', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use MC info (gen) or not")
options.register('isDomain', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Flag as domain event jets or not")
options.register('isemu', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use emu info (gen) or not")
options.register('ismutau', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use mutau info (gen) or not")
options.register('isdimu', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use dimu info (gen) or not")

import os
release=os.environ['CMSSW_VERSION'][6:]
print("Using release "+release)

options.register(
	'inputFiles','',
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"input files (default is the tt RelVal)"
	)

if hasattr(sys, "argv"):
    options.parseArguments()

if options.puppi:
    usePuppi = True
else:
    usePuppi = False
process = cms.Process("DNNFiller")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2023_realistic_postBPix_v2', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(False)
)

process.load('DeepNTuples.DeepNtuplizer.samples.TTJetsPhase1_cfg') #default input

if options.inputFiles:
	process.source.fileNames = options.inputFiles
if options.inputScript != '' and options.inputScript != 'DeepNTuples.DeepNtuplizer.samples.TTJetsPhase1_cfg':
    process.load(options.inputScript)

numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job

process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)

process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
process.maxEvents  = cms.untracked.PSet( 
    input = cms.untracked.int32 (options.maxEvents) 
)
releases = release.split("_")

bTagInfos = ['pfDeepFlavourTagInfos',
             'pfImpactParameterTagInfos',
             'pfInclusiveSecondaryVertexFinderTagInfos',
             'pfParticleNetAK4TagInfos',]

from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsAll as pfParticleNetAK4JetTagsAll
from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs
from RecoBTag.ONNXRuntime.pfUnifiedParticleTransformerAK4_cff import _pfUnifiedParticleTransformerAK4JetTagsAll

if (int(releases[0])>8) or ( (int(releases[0])==8) and (int(releases[1]) >= 4) ) :
 bTagDiscriminators = [
     'pfDeepFlavourJetTags:probb',
     'pfDeepFlavourJetTags:probbb',
     'pfDeepFlavourJetTags:problepb',
     'pfDeepFlavourJetTags:probc',
     'pfDeepFlavourJetTags:probuds',
     'pfDeepFlavourJetTags:probg',
     'pfParticleTransformerAK4JetTags:probb',
     'pfParticleTransformerAK4JetTags:probbb',
     'pfParticleTransformerAK4JetTags:problepb',
     'pfParticleTransformerAK4JetTags:probc',
     'pfParticleTransformerAK4JetTags:probuds',
     'pfParticleTransformerAK4JetTags:probg',
 ] + _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs + pfParticleNetAK4JetTagsAll + _pfUnifiedParticleTransformerAK4JetTagsAll
else :
  bTagDiscriminators = [
      'pfDeepFlavourJetTags:probb',
      'pfDeepFlavourJetTags:probbb',
      'pfDeepFlavourJetTags:problepb',
      'pfDeepFlavourJetTags:probc',
      'pfDeepFlavourJetTags:probuds',
      'pfDeepFlavourJetTags:probg',
      'pfParticleTransformerAK4JetTags:probb',
      'pfParticleTransformerAK4JetTags:probbb',
      'pfParticleTransformerAK4JetTags:problepb',
      'pfParticleTransformerAK4JetTags:probc',
      'pfParticleTransformerAK4JetTags:probuds',
      'pfParticleTransformerAK4JetTags:probg',
 ] + _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs + pfParticleNetAK4JetTagsAll + _pfUnifiedParticleTransformerAK4JetTagsAll

jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
if options.phase2:
    usePuppi = True

if usePuppi:
    jetCorrectionsAK4 = ('AK4PFPuppi', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
    
###########################################################################
#
# Setup puppi modules and set them to recalculate weights
#
###########################################################################
from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
makePuppiesFromMiniAOD(process, False)
process.puppi.useExistingWeights = False
process.puppiNoLep.useExistingWeights = False

###########################################################################
#
# Make function wrapper around PatAlgos helper functions
#
###########################################################################
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
def addProcessAndTask(proc, label, module):
  task = getPatAlgosToolsTask(proc)
  addToProcessAndTask(label, module, proc, task)

###########################################################################
#
# Recluster AK4 Puppi jets
#
###########################################################################
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi
jetCollectionRecluster = "ak4PFJetsPuppiRecluster"
#addToProcessAndTask(process, jetCollectionRecluster, ak4PFJetsPuppi.clone(
addProcessAndTask(process, jetCollectionRecluster, ak4PFJetsPuppi.clone(
      src = "packedPFCandidates",
      srcWeights = "puppi"
    )
)

###########################################################################
#
# Patify reclustered AK4 Puppi jets
#
###########################################################################
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
addJetCollection(
  process,
  postfix            = "Recluster",
  labelName          = "AK4Puppi",
  jetSource          = cms.InputTag(jetCollectionRecluster),
  algo               = "ak", #name of algo must be in this format
  rParam             = 0.4,
  pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
  pfCandidates       = cms.InputTag("packedPFCandidates"),
  svSource           = cms.InputTag("slimmedSecondaryVertices"),
  muSource           = cms.InputTag("slimmedMuons"),
  elSource           = cms.InputTag("slimmedElectrons"),
  genJetCollection   = cms.InputTag("ak4GenJetsRecluster"), # This is setup below
  genParticles       = cms.InputTag("prunedGenParticles"),
  jetCorrections     = jetCorrectionsAK4,
)

process.patJetsAK4PuppiRecluster.addGenPartonMatch = cms.bool(options.isMC)
process.patJetsAK4PuppiRecluster.addGenJetMatch = cms.bool(options.isMC)
process.patJetsAK4PuppiRecluster.getJetMCFlavour = cms.bool(options.isMC)
getattr(process, "patJetFlavourAssociationAK4PuppiRecluster").weights = cms.InputTag("puppi")

if usePuppi:
    jet_collection = 'patJetsAK4PuppiRecluster'
else:
    jet_collection = 'slimmedJets'

updateJetCollection(
        process,
        labelName = "DeepFlavour",
        jetSource = cms.InputTag(jet_collection),  # 'ak4Jets'
        jetCorrections = jetCorrectionsAK4,
        pfCandidates = cms.InputTag('packedPFCandidates'),
        pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        muSource = cms.InputTag('slimmedMuons'),
        elSource = cms.InputTag('slimmedElectrons'),
        btagInfos = bTagInfos,
        btagDiscriminators = bTagDiscriminators,
        explicitJTA = False
)

if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
  process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True) 
  process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)
else:
  raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')

if options.isMC:
    from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
    process.ak4GenJetsWithNu = ak4GenJets.clone(src ='packedGenParticles')
 
    ## Filter out neutrinos from packed GenParticles
    process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
    ## Define GenJets
    process.ak4GenJetsRecluster = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')

    if options.isemu or options.isdimu or options.ismutau:
        jet_coll_gen = 'selectedCleanJets'
    else:
        jet_coll_gen = 'selectedUpdatedPatJetsDeepFlavour'


    process.patGenJetMatchAllowDuplicates = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
                                                           src         = cms.InputTag(jet_coll_gen),      # RECO jets (any View<Jet> is ok) 
                                                           matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
                                                           mcPdgId     = cms.vint32(),                      # n/a   
                                                           mcStatus    = cms.vint32(),                      # n/a   
                                                           checkCharge = cms.bool(False),                   # n/a   
                                                           maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
                                                           #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)
                                                           resolveAmbiguities    = cms.bool(False),          # Forbid two RECO objects to match to the same GEN object 
                                                           resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first
                                                           )
 
 
    process.patGenJetMatchWithNu = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
                                                  src         = cms.InputTag(jet_coll_gen),      # RECO jets (any View<Jet> is ok) 
                                                  matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
                                                  mcPdgId     = cms.vint32(),                      # n/a   
                                                  mcStatus    = cms.vint32(),                      # n/a   
                                                  checkCharge = cms.bool(False),                   # n/a   
                                                  maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
                                                  #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
                                                  resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
                                                  resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
                                                  )
    
    process.patGenJetMatchRecluster = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
                                                     src         = cms.InputTag(jet_coll_gen),      # RECO jets (any View<Jet> is ok) 
                                                     matched     = cms.InputTag("ak4GenJetsRecluster"),        # GEN jets  (must be GenJetCollection)              
                                                     mcPdgId     = cms.vint32(),                      # n/a   
                                                     mcStatus    = cms.vint32(),                      # n/a   
                                                     checkCharge = cms.bool(False),                   # n/a   
                                                     maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
                                                     #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
                                                     resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
                                                     resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
                                                     )

    process.genJetReclusterTask = cms.Task(process.packedGenParticlesForJetsNoNu,process.ak4GenJetsWithNu,process.ak4GenJetsRecluster) 
    process.genJetMatchTask = cms.Task(process.patGenJetMatchAllowDuplicates,process.patGenJetMatchWithNu,process.patGenJetMatchRecluster)

# Very Loose IVF SV collection
from PhysicsTools.PatAlgos.tools.helpers import loadWithPrefix
loadWithPrefix(process, 'RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff', "looseIVF")
process.looseIVFinclusiveCandidateVertexFinder.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFinclusiveCandidateVertexFinder.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLen2DSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLenSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.fitterSigmacut = 20

process.looseIVFcandidateVertexArbitrator.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFcandidateVertexArbitrator.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFcandidateVertexArbitrator.secondaryVertices = cms.InputTag("looseIVFcandidateVertexMerger")
process.looseIVFcandidateVertexArbitrator.fitterSigmacut = 20


outFileName = options.outputFile + '_' + str(options.job) +  '.root'
print ('Using output file ' + outFileName)

process.TFileService = cms.Service("TFileService", 
                                   fileName = cms.string(outFileName))

# DeepNtuplizer
process.load("DeepNTuples.DeepNtuplizer.DeepNtuplizer_cfi")

#Domain region
if options.isdimu:
    print ("add dimuon process selection")
    process.load('DeepNTuples.DeepNtuplizer.dimu_skim_cff');
    process.deepntuplizer.leptonPairs = cms.InputTag("dimuonPairs")
    process.deepntuplizer.jets = cms.InputTag('selectedCleanJets')
elif options.isemu:
    from DeepNTuples.DeepNtuplizer.emu_skim_cff import emuSelection
    print ("add emu process selection")
    process = emuSelection(process,"pfParticleNetFromMiniAODAK4PuppiCentral");
    process.deepntuplizer.leptonPairs = cms.InputTag("emuPairs")
    process.deepntuplizer.jets = cms.InputTag('selectedCleanJets')
elif options.ismutau:
    from DeepNTuples.DeepNtuplizer.mutau_skim_cff import mutauSelection
    print ("add mutau process selection")
    process = mutauSelection(process,"pfParticleNetFromMiniAODAK4PuppiCentral");
    process.deepntuplizer.leptonPairs = cms.InputTag("mutauPairs")
    process.deepntuplizer.jets = cms.InputTag('selectedCleanJets')
else:
    process.deepntuplizer.jets = cms.InputTag('selectedUpdatedPatJetsDeepFlavour')

process.deepntuplizer.bDiscriminators = bTagDiscriminators 
process.deepntuplizer.LooseSVs = cms.InputTag("looseIVFinclusiveCandidateSecondaryVertices")

process.deepntuplizer.applySelection = cms.bool(options.selectJets)

if ( int(releases[0]) > 8 ) or ( (int(releases[0])==8) and (int(releases[1]) >= 4) ):
   process.deepntuplizer.tagInfoName = cms.string('pfDeepCSV')

if options.isMC:
    process.deepntuplizer.MC = cms.bool(True)
if options.isDomain:
    process.deepntuplizer.Domain = cms.bool(True)
if options.isemu:
    process.deepntuplizer.emu = cms.bool(True)
if options.isdimu:
    process.deepntuplizer.dimu = cms.bool(True)
if options.ismutau:
    process.deepntuplizer.mutau = cms.bool(True)
if options.eta :
    process.deepntuplizer.jetAbsEtaMax = cms.double(5.0)
else:
    process.deepntuplizer.jetAbsEtaMax = cms.double(2.5)
if options.phase2 :
    process.deepntuplizer.jetAbsEtaMax = cms.double(3.0)

process.deepntuplizer.gluonReduction  = cms.double(options.gluonReduction)

from PhysicsTools.PatAlgos.tools.coreTools import runOnData
if not(options.isMC):
    runOnData(process, names=["Jets","METs"], outputModules = [])

process.ProfilerService = cms.Service (
      "ProfilerService",
       firstEvent = cms.untracked.int32(1631),
       lastEvent = cms.untracked.int32(1641),
       paths = cms.untracked.vstring('p') 
)

process.tsk = cms.Task()
for mod in process.producers_().values(): #.itervalues():
    process.tsk.add(mod)
for mod in process.filters_().values(): #.itervalues():
    process.tsk.add(mod)

process.patAlgosToolsTask = getPatAlgosToolsTask(process)

if (options.isMC and options.isemu): #All the MC+Skimming
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
        process.patAlgosToolsTask, 
        process.genJetReclusterTask, 
        process.genJetMatchTask
    )
elif (options.isMC and options.isdimu):
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
        process.patAlgosToolsTask, 
        process.genJetReclusterTask, 
        process.genJetMatchTask
    )
elif (options.isMC and options.ismutau):
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
        process.patAlgosToolsTask, 
        process.genJetReclusterTask, 
        process.genJetMatchTask
    )
elif (options.isMC): #OG Ntupler
    process.p = cms.Path(
        process.deepntuplizer,
        process.tsk, 
        process.patAlgosToolsTask, 
        process.genJetReclusterTask, 
        process.genJetMatchTask
    )
elif (options.isemu): #Data+Skimming
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
    )
elif (options.isdimu): #Data+Skimming
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
    )
elif (options.ismutau): #Data+Skimming
    process.p = cms.Path(
        process.leptonSelection *
        process.jetSelection *
        process.deepntuplizer,
        process.tsk, 
    )
