import FWCore.ParameterSet.Config as cms

def ttcharmSelection(process,scoreLabel="pfParticleNetFromMiniAODAK4PuppiCentral"):
    ## trigger selection
    process.triggerResultFilter = cms.EDFilter('TriggerResultsFilter',
        hltResults = cms.InputTag('TriggerResults','',"HLT"),
        l1tResults = cms.InputTag(''),
        l1tIgnoreMaskAndPrescale = cms.bool(False),
        throw = cms.bool(False),
        triggerConditions = cms.vstring('HLT_IsoMu24_v*')
    );

    ## tag muon selection
    process.tagMuons = cms.EDFilter("PATMuonSelector",
        src = cms.InputTag("slimmedMuons"),
        cut = cms.string("pt > 26 && abs(eta) < 2.4 && passed('CutBasedIdTight') && passed('PFIsoTight')"),
        filter = cms.bool(False)
    );

    process.filterTagMuons = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("tagMuons"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(1)
    );

    ## electron veto
    process.vetoElectrons = cms.EDFilter("PATElectronSelector",
        src = cms.InputTag("slimmedElectrons"),
        cut = cms.string("pt > 15 && abs(eta) < 2.5 && electronID('mvaEleID-RunIIIWinter22-iso-V1-wp90')"),
        filter = cms.bool(False)
    );

    process.filterVetoElectrons = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("vetoElectrons"),
        minNumber = cms.uint32(0),
        maxNumber = cms.uint32(0)
    );

    ## muon veto
    process.vetoMuons = cms.EDFilter("PATMuonSelector",
        src = cms.InputTag("slimmedMuons"),
        cut = cms.string("pt > 15 && abs(eta) < 2.4 && passed('CutBasedIdLoose') && passed('PFIsoLoose')"),
        filter = cms.bool(False)
    );

    process.filterVetoMuons = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("vetoMuons"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(1)
    );

    ## final sequence
    process.leptonSelection = cms.Sequence(
        process.triggerResultFilter+
        process.tagMuons+
        process.filterTagMuons+
        process.vetoMuons+
        process.filterVetoMuons+
        process.vetoElectrons+
        process.filterVetoElectrons
    )

    ## require dR between jets and the tag muons
    process.cleanJets = cms.EDProducer("PATJetCleaner",
        src = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),
        preselection = cms.string(''),
        checkOverlaps = cms.PSet(
            muons = cms.PSet(
                src          = cms.InputTag("tagMuons"),
                algorithm    = cms.string("byDeltaR"),
                preselection = cms.string(""),
                deltaR       = cms.double(0.4),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True)
            ),
        ),
        finalCut = cms.string('')
    )

    from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
    process.selectedCleanJets = selectedPatJets.clone();
    process.selectedCleanJets.src = cms.InputTag("cleanJets");
    process.selectedCleanJets.cut = cms.string("correctedJet('Uncorrected').pt() > 25 && abs(eta) < 2.5");
    process.selectedCleanJets.filter = cms.bool(False)

    process.filterCleanJets = cms.EDFilter("PATCandViewCountFilter",
            src = cms.InputTag("selectedCleanJets"),
            minNumber = cms.uint32(4),
            maxNumber = cms.uint32(99)
    );

    process.selectedBJetCandidates =  selectedPatJets.clone();
    process.selectedBJetCandidates.src = cms.InputTag("selectedCleanJets");
    process.selectedBJetCandidates.cut = cms.string("(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb'))/(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb')+bDiscriminator('"+scoreLabel+"JetTags:probc')+bDiscriminator('"+scoreLabel+"JetTags:probu')+bDiscriminator('"+scoreLabel+"JetTags:probd')+bDiscriminator('"+scoreLabel+"JetTags:probs')+bDiscriminator('"+scoreLabel+"JetTags:probg')) > 0.2");
    process.selectedBJetCandidates.filter = cms.bool(False)

    process.filterBJetCandidates = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("selectedBJetCandidates"),
        minNumber = cms.uint32(2),
        maxNumber = cms.uint32(99)
    );

    process.bjetPairs = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("selectedBJetCandidates@+ selectedBJetCandidates@-"),
        cut = cms.string("deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi) > 1.57"),
        checkCharge = cms.bool(False)
    );

    process.filterBjetPairs = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("bjetPairs"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(99)
    );

    process.selectedBVetoJetCandidates =  selectedPatJets.clone();
    process.selectedBVetoJetCandidates.src = cms.InputTag("selectedCleanJets");
    process.selectedBVetoJetCandidates.cut = cms.string("(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb'))/(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb')+bDiscriminator('"+scoreLabel+"JetTags:probc')+bDiscriminator('"+scoreLabel+"JetTags:probu')+bDiscriminator('"+scoreLabel+"JetTags:probd')+bDiscriminator('"+scoreLabel+"JetTags:probs')+bDiscriminator('"+scoreLabel+"JetTags:probg')) < 0.5");
    process.selectedBVetoJetCandidates.filter = cms.bool(False)

    process.filterBVetoJetCandidates = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("selectedBVetoJetCandidates"),
        minNumber = cms.uint32(2),
        maxNumber = cms.uint32(99)
    );

    process.selectedCJetCandidatesB =  selectedPatJets.clone();
    process.selectedCJetCandidatesB.src = cms.InputTag("selectedBVetoJetCandidates");
    process.selectedCJetCandidatesB.cut = cms.string("bDiscriminator('"+scoreLabel+"JetTags:probc')/(1.-(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb'))) > 0.90");
    process.selectedCJetCandidatesB.filter = cms.bool(False)

    process.filterCJetCandidatesB = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("selectedCJetCandidatesB"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(99)
    );

    process.selectedCJetCandidates =  selectedPatJets.clone();
    process.selectedCJetCandidates.src = cms.InputTag("selectedCJetCandidatesB");
    process.selectedCJetCandidates.cut = cms.string("bDiscriminator('"+scoreLabel+"JetTags:probc')/(bDiscriminator('"+scoreLabel+"JetTags:probb')+bDiscriminator('"+scoreLabel+"JetTags:probbb')+bDiscriminator('"+scoreLabel+"JetTags:problepb')+bDiscriminator('"+scoreLabel+"JetTags:probc')) > 0.800");
    process.selectedCJetCandidates.filter = cms.bool(False)

    process.filterCJetCandidates = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("selectedCJetCandidates"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(99)
    );

    
    process.wjetPairs = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("selectedCJetCandidates@+ selectedBVetoJetCandidates@-"),
        cut = cms.string("mass > 50 && mass < 110"),
        checkCharge = cms.bool(False)
    );

    process.filterWjetPairs = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("wjetPairs"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(99)
    );

    process.leptonJetPairs = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("tagMuons@+ selectedCJetCandidates@-"),
        cut = cms.string(""),
        checkCharge = cms.bool(False)
    );

    process.jetSelection = cms.Sequence(
        process.cleanJets+
        process.selectedCleanJets+
        process.filterCleanJets+
        process.selectedBJetCandidates+
        process.filterBJetCandidates+
        process.bjetPairs+
        process.filterBjetPairs+
        process.selectedBVetoJetCandidates+
        process.filterBVetoJetCandidates+
        process.selectedCJetCandidatesB+
        process.filterCJetCandidatesB+
        process.selectedCJetCandidates+
        process.filterCJetCandidates+
        process.wjetPairs+
        process.filterWjetPairs+
        process.leptonJetPairs
    )

    return process;
