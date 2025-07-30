/*
 * ntuple_SV.cc
 *
 *  Created on: 13 Feb 2017
 *      Author: jkiesele
 */


#include "../interface/ntuple_SV.h"
// for ivf
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TVector3.h"

/*class TrackInfoBuilder{
public:
  TrackInfoBuilder(edm::ESHandle<TransientTrackBuilder> & build):
    builder(build),
    trackMomentum_(0),
    trackEta_(0),
    trackEtaRel_(0),
    trackPtRel_(0),
    trackPPar_(0),
    trackDeltaR_(0),
    trackPtRatio_(0),
    trackPParRatio_(0),
    trackSip2dVal_(0),
    trackSip2dSig_(0),
    trackSip3dVal_(0),
    trackSip3dSig_(0),

    trackJetDecayLen_(0),
    trackJetDistVal_(0),
    trackJetDistSig_(0),
    ttrack_(0)
  {

  }

  void buildTrackInfo(const pat::PackedCandidate* PackedCandidate_ ,const math::XYZVector&  jetDir, GlobalVector refjetdirection, const reco::Vertex & pv){
    TVector3 jetDir3(jetDir.x(),jetDir.y(),jetDir.z());
    if(!PackedCandidate_->hasTrackDetails()) {
      TVector3 trackMom3(
			 PackedCandidate_->momentum().x(),
			 PackedCandidate_->momentum().y(),
			 PackedCandidate_->momentum().z()
			 );
      trackMomentum_=PackedCandidate_->p();
      trackEta_= PackedCandidate_->eta();
      trackEtaRel_=reco::btau::etaRel(jetDir, PackedCandidate_->momentum());
      trackPtRel_=trackMom3.Perp(jetDir3);
      trackPPar_=jetDir.Dot(PackedCandidate_->momentum());
      trackDeltaR_=reco::deltaR(PackedCandidate_->momentum(), jetDir);
      trackPtRatio_=trackMom3.Perp(jetDir3) / PackedCandidate_->p();
      trackPParRatio_=jetDir.Dot(PackedCandidate_->momentum()) / PackedCandidate_->p();
      trackSip2dVal_=0.;
      trackSip2dSig_=0.;
      trackSip3dVal_=0.;
      trackSip3dSig_=0.;
      trackJetDecayLen_=0.;
      trackJetDistVal_=0.;
      trackJetDistSig_=0.;
      return;
    }

    const reco::Track & PseudoTrack =  PackedCandidate_->pseudoTrack();

    reco::TransientTrack transientTrack;
    transientTrack=builder->build(PseudoTrack);
    Measurement1D meas_ip2d=IPTools::signedTransverseImpactParameter(transientTrack, refjetdirection, pv).second;
    Measurement1D meas_ip3d=IPTools::signedImpactParameter3D(transientTrack, refjetdirection, pv).second;
    Measurement1D jetdist=IPTools::jetTrackDistance(transientTrack, refjetdirection, pv).second;
    Measurement1D decayl = IPTools::signedDecayLength3D(transientTrack, refjetdirection, pv).second;
    math::XYZVector trackMom = PseudoTrack.momentum();
    double trackMag = std::sqrt(trackMom.Mag2());
    TVector3 trackMom3(trackMom.x(),trackMom.y(),trackMom.z());

    trackMomentum_=std::sqrt(trackMom.Mag2());
    trackEta_= trackMom.Eta();
    trackEtaRel_=reco::btau::etaRel(jetDir, trackMom);
    trackPtRel_=trackMom3.Perp(jetDir3);
    trackPPar_=jetDir.Dot(trackMom);
    trackDeltaR_=reco::deltaR(trackMom, jetDir);
    trackPtRatio_=trackMom3.Perp(jetDir3) / trackMag;
    trackPParRatio_=jetDir.Dot(trackMom) / trackMag;

    trackSip2dVal_=(meas_ip2d.value());
    trackSip2dSig_=(meas_ip2d.significance());
    trackSip3dVal_=(meas_ip3d.value());
    trackSip3dSig_=meas_ip3d.significance();

    trackJetDecayLen_= decayl.value();
    trackJetDistVal_= jetdist.value();
    trackJetDistSig_= jetdist.significance();

    ttrack_ = transientTrack;

  }

  const float& getTrackDeltaR() const {return trackDeltaR_;}
  const float& getTrackEta() const {return trackEta_;}
  const float& getTrackEtaRel() const {return trackEtaRel_;}
  const float& getTrackJetDecayLen() const {return trackJetDecayLen_;}
  const float& getTrackJetDistSig() const {return trackJetDistSig_;}
  const float& getTrackJetDistVal() const {return trackJetDistVal_;}
  const float& getTrackMomentum() const {return trackMomentum_;}
  const float& getTrackPPar() const {return trackPPar_;}
  const float& getTrackPParRatio() const {return trackPParRatio_;}
  const float& getTrackPtRatio() const {return trackPtRatio_;}
  const float& getTrackPtRel() const {return trackPtRel_;}
  const float& getTrackSip2dSig() const {return trackSip2dSig_;}
  const float& getTrackSip2dVal() const {return trackSip2dVal_;}
  const float& getTrackSip3dSig() const {return trackSip3dSig_;}
  const float& getTrackSip3dVal() const {return trackSip3dVal_;}
  const reco::TransientTrack getTTrack() const {return ttrack_;}

private:

  edm::ESHandle<TransientTrackBuilder>& builder;
  edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> track_builder_token_;
    
  float trackMomentum_;
  float trackEta_;
  float trackEtaRel_;
  float trackPtRel_;
  float trackPPar_;
  float trackDeltaR_;
  float trackPtRatio_;
  float trackPParRatio_;
  float trackSip2dVal_;
  float trackSip2dSig_;
  float trackSip3dVal_;
  float trackSip3dSig_;

  float trackJetDecayLen_;
  float trackJetDistVal_;
  float trackJetDistSig_;
  reco::TransientTrack ttrack_;

  };*/

const reco::Vertex * ntuple_SV::spvp_;

ntuple_SV::ntuple_SV(std::string prefix, double jetR):ntuple_content(jetR),sv_num_(0){
    prefix_ = prefix;
}
ntuple_SV::~ntuple_SV(){}


void ntuple_SV::getInput(const edm::ParameterSet& iConfig){

}

void ntuple_SV::initBranches(TTree* tree){
    // SV candidates
    addBranch(tree,(prefix_+"n_sv").c_str()         ,&sv_num_         ,(prefix_+"sv_num_/I").c_str()     );
    addBranch(tree,(prefix_+"nsv").c_str()          ,&nsv_          ,(prefix_+"nsv_/F").c_str()         );
    addBranch(tree,(prefix_+"sv_pt").c_str()          ,&sv_pt_          ,(prefix_+"sv_pt_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_px").c_str()          ,&sv_px_          ,(prefix_+"sv_px_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_py").c_str()          ,&sv_py_          ,(prefix_+"sv_py_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_pz").c_str()          ,&sv_pz_          ,(prefix_+"sv_pz_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_eta").c_str()          ,&sv_eta_          ,(prefix_+"sv_eta_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_phi").c_str()          ,&sv_phi_          ,(prefix_+"sv_phi_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_e").c_str()          ,&sv_e_          ,(prefix_+"sv_e_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_etarel").c_str()         ,&sv_etarel_         ,(prefix_+"sv_etarel_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_phirel").c_str()         ,&sv_phirel_         ,(prefix_+"sv_phirel_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_deltaR").c_str()         ,&sv_deltaR_         ,(prefix_+"sv_deltaR_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_mass").c_str()        ,&sv_mass_        ,(prefix_+"sv_mass_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_ntracks").c_str()     ,&sv_ntracks_     ,(prefix_+"sv_ntracks_["+prefix_+"sv_num_]/F").c_str()     );
    addBranch(tree,(prefix_+"sv_chi2").c_str()        ,&sv_chi2_        ,(prefix_+"sv_chi2_["+prefix_+"sv_num_]/F").c_str()        );
    addBranch(tree,(prefix_+"sv_ndf").c_str()         ,&sv_ndf_         ,(prefix_+"sv_ndf_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_normchi2").c_str()    ,&sv_normchi2_   ,(prefix_+"sv_normchi2_["+prefix_+"sv_num_]/F").c_str()     );
    addBranch(tree,(prefix_+"sv_dxy").c_str()         ,&sv_dxy_         ,(prefix_+"sv_dxy_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_dxyerr").c_str()      ,&sv_dxyerr_      ,(prefix_+"sv_dxyerr_["+prefix_+"sv_num_]/F").c_str()      );
    addBranch(tree,(prefix_+"sv_dxysig").c_str()      ,&sv_dxysig_      ,(prefix_+"sv_dxysig_["+prefix_+"sv_num_]/F").c_str()      );
    addBranch(tree,(prefix_+"sv_d3d").c_str()         ,&sv_d3d_         ,(prefix_+"sv_d3d_["+prefix_+"sv_num_]/F").c_str()         );
    addBranch(tree,(prefix_+"sv_d3derr").c_str()      ,&sv_d3derr_      ,(prefix_+"sv_d3err_["+prefix_+"sv_num_]/F").c_str()       );
    addBranch(tree,(prefix_+"sv_d3dsig").c_str()      ,&sv_d3dsig_      ,(prefix_+"sv_d3dsig_["+prefix_+"sv_num_]/F").c_str()      );
    addBranch(tree,(prefix_+"sv_costhetasvpv").c_str(),&sv_costhetasvpv_,(prefix_+"sv_costhetasvpv_["+prefix_+"sv_num_]/F").c_str());
    addBranch(tree,(prefix_+"sv_enratio").c_str()     ,&sv_enratio_     ,(prefix_+"sv_enratio_["+prefix_+"sv_num_]/F").c_str());
}


void ntuple_SV::readSetup(const edm::EventSetup& iSetup){

  builder = iSetup.getHandle(track_builder_token_);
}

void ntuple_SV::readEvent(const edm::Event& iEvent){


}


bool ntuple_SV::compareDxyDxyErr(const reco::VertexCompositePtrCandidate &sva,const reco::VertexCompositePtrCandidate &svb){
    reco::Vertex pv=*spvp_;
    float adxy= ntuple_SV::vertexDxy(sva,pv).value();
    float bdxy= ntuple_SV::vertexDxy(svb,pv).value();
    float aerr=ntuple_SV::vertexDxy(sva,pv).error();
    float berr=ntuple_SV::vertexDxy(svb,pv).error();

    float asig=ntuple_SV::catchInfs(adxy/aerr,0.);
    float bsig=ntuple_SV::catchInfs(bdxy/berr,0.);
    return bsig<asig;
}

bool ntuple_SV::fillBranches(const pat::Jet & jet, const size_t& jetidx, const  edm::View<pat::Jet> * coll){


    const float jet_uncorr_e=jet.correctedJet("Uncorrected").energy();
    const reco::Vertex & pv =    vertices()->at(0);
    GlobalVector jetRefTrackDir(jet.px(),jet.py(),jet.pz());

    sv_num_ = 0;
    reco::VertexCompositePtrCandidateCollection cpvtx=*secVertices();
    spvp_ =   & vertices()->at(0);
    std::sort(cpvtx.begin(),cpvtx.end(),ntuple_SV::compareDxyDxyErr);

    float etasign=1;
    etasign++; //avoid unused warning
    if(jet.eta()<0)etasign=-1;

    double jet_radius = jetR();
    if (jet_radius<0){
      // subjets: use maxDR(subjet, pfcand)
      for (unsigned idau=0; idau<jet.numberOfDaughters(); ++idau){
        double dR = reco::deltaR(*jet.daughter(idau), jet);
        if (dR>jet_radius)
          jet_radius = dR;
      }
    }

    for (const reco::VertexCompositePtrCandidate &sv : cpvtx) {

        if (reco::deltaR(sv,jet)>jet_radius) { continue; }
        if((int)max_sv>sv_num_){


            sv_pt_[sv_num_]           = sv.pt();
            sv_px_[sv_num_]           = sv.px();
            sv_py_[sv_num_]           = sv.py();
            sv_pz_[sv_num_]           = sv.pz();
            sv_eta_[sv_num_]          = sv.eta();
            sv_phi_[sv_num_]          = sv.phi();
            sv_etarel_[sv_num_]       = catchInfsAndBound(fabs(sv.eta()-jet.eta())-0.5,0,-2,0);
            sv_phirel_[sv_num_]       = catchInfsAndBound(fabs(reco::deltaPhi(sv.phi(),jet.phi()))-0.5,0,-2,0);
            sv_deltaR_[sv_num_]       = catchInfsAndBound(fabs(reco::deltaR(sv,jet))-0.5,0,-2,0);
            sv_mass_[sv_num_]         = sv.mass();
            sv_ntracks_[sv_num_]      = sv.numberOfDaughters();
            sv_chi2_[sv_num_]         = sv.vertexChi2();
            sv_ndf_[sv_num_]          = sv.vertexNdof();
            sv_normchi2_[sv_num_]     = catchInfsAndBound(sv_chi2_[sv_num_]/sv_ndf_[sv_num_],1000,-1000,1000);
            sv_dxy_[sv_num_]          = vertexDxy(sv,pv).value();
            sv_dxyerr_[sv_num_]       = catchInfsAndBound(vertexDxy(sv,pv).error()-2,0,-2,0);
            sv_dxysig_[sv_num_]       = catchInfsAndBound(sv_dxy_[sv_num_]/vertexDxy(sv,pv).error() ,0,-1,800);
            sv_d3d_[sv_num_]          = vertexD3d(sv,pv).value();
            sv_d3derr_[sv_num_]       = catchInfsAndBound(vertexD3d(sv,pv).error()-2,0,-2,0);
            sv_d3dsig_[sv_num_]       = catchInfsAndBound(vertexD3d(sv,pv).value()/vertexD3d(sv,pv).error(),0,-1,800);
            sv_costhetasvpv_[sv_num_] = vertexDdotP(sv,pv); // the pointing angle (i.e. the angle between the sum of the momentum

            sv_enratio_[sv_num_]=sv.energy()/jet_uncorr_e;
            sv_e_[sv_num_]=sv.energy();

            sv_num_++;
        }
    } // end of looping over the secondary vertices
    nsv_=sv_num_;

    return true;
}

///helpers seldomly touched

Measurement1D ntuple_SV::vertexDxy(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv)  {
    VertexDistanceXY dist;
    reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
    reco::Vertex svtx(svcand.vertex(), csv);
    return dist.distance(svtx, pv);
}

Measurement1D ntuple_SV::vertexD3d(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv)  {
    VertexDistance3D dist;
    reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
    reco::Vertex svtx(svcand.vertex(), csv);
    return dist.distance(svtx, pv);
}

float ntuple_SV::vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const reco::Vertex &pv)  {
    reco::Candidate::Vector p = sv.momentum();
    reco::Candidate::Vector d(sv.vx() - pv.x(), sv.vy() - pv.y(), sv.vz() - pv.z());
    return p.Unit().Dot(d.Unit());
}

