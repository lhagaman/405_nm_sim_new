import rat
import ROOT
import sys
import runCheckTools as RCT
import json

# Get command line arguments
cmdArgs = sys.argv

configNumber = cmdArgs[1]
nodeNumber = cmdArgs[2]

pathToData = '/data/snoplus/home/cbenson/VUV/VUV_Analysis/geoFactorSim/newGeoSim/data/config_'+str(configNumber)
theFileName = pathToData+'/pos'+str(nodeNumber)+'.root'

### Write something that will find the TPB surface boundaries and then break out of the loop
fileIterator = rat.dsreader(theFileName)
TPBboundaryValues = []
breakOut = False
for index,anEntry in enumerate(fileIterator):
	if index%1000 == 0:
		print index
	if index == 10000:
		break
	tempMC = anEntry.GetMC()
	tempTrackCount = tempMC.GetMCTrackCount()
	if tempTrackCount == 1:
		continue
	for iTrack in range(1,tempTrackCount):
		tempTrack = tempMC.GetMCTrack(iTrack)
		leftTPB = False
		for iStep in range(tempTrack.GetMCTrackStepCount()):
			tempStep = tempTrack.GetMCTrackStep(iStep)
			if tempStep.GetVolume() != 'tpbVolume' and leftTPB == False:
				leftTPB = True
				previousStep = tempTrack.GetMCTrackStep(iStep-1)
				if previousStep.GetEndpoint().x() not in TPBboundaryValues:
					TPBboundaryValues.append(previousStep.GetEndpoint().x())
				if len(TPBboundaryValues) == 2:
					breakOut = True
					break
		if breakOut:
			break
	if breakOut:
		break
print TPBboundaryValues
if len(TPBboundaryValues) == 0:
	TPBboundaryValues = [-1,0]


# Init the hists
#RCT.quickTH1D(name,title,nbins,lowbin,highbin,xlabel,ylabel)
numTracksHist = RCT.quickTH1D("numTracks","numTracks",10,0,10,"Num Tracks","Entries")
allphotons_WavelengthHist = RCT.quickTH1D("allphotons_Wavelength","allphoton_Wavelength",750,50,700,"Wavelength [nm]","Entries")
UVphotons_WavelengthHist = RCT.quickTH1D("UVphotons_Wavelength","UVphotons_Wavelength",750,50,700,"Wavelength [nm]","Entries")
visPhotons_WavelengthHist = RCT.quickTH1D("visphotons_Wavelength","visphotons_Wavelength",int(750./5),50,700,"Wavelength [nm]","Entries")

# check conservation of energy
excessEnergyHist = RCT.quickTH1D("excessEnergyAfterWLS","excessEnergyAfterWLS",int(25/0.1),-5,20,"Energy [ev]","Entries")

# Some histograms to cross check the terminating position of stuff
UVTermX = RCT.quickTH1D("UVTerminationX","UVTerminationX",400,-100,300,"UV Termination X Coord","Entries")
UVTermY = RCT.quickTH1D("UVTerminationY","UVTerminationY",100,-50,50,"UV Termination Y Coord","Entries")
UVTermZ = RCT.quickTH1D("UVTerminationZ","UVTerminationZ",100,-50,50,"UV Termination Z Coord","Entries")
UVTermAtSlit = ROOT.TH2D("UVTermAtSlit","UVTermAtSlit",200,-100,100,200,-100,100)
UVPenetrationDepth = RCT.quickTH1D("UVPenetrationDepth","UVPenetrationDepth",100,0.0,(max(TPBboundaryValues)-min(TPBboundaryValues))*10**3,"UV TPB Penetration Depth","Entries")
UVDotProdAtUpstreamTracking = RCT.quickTH1D("UVDotProdAtUpstreamTracking","UVDotProdAtUpstreamTracking",120,-1.1,1.1,"UV Termination X Coord","Entries")

# Some visible histograms
VisTermX =  RCT.quickTH1D("VisTerminationX","VisTerminationX",400,-100,300,"Vis Termination X Coord","Entries")
VisTermY = RCT.quickTH1D("VisTerminationY","VisTerminationY",100,-50,50,"Vis Termination Y Coord","Entries")
VisTermZ = RCT.quickTH1D("VisTerminationZ","VisTerminationZ",100,-50,50,"Vis Termination Z Coord","Entries")
VisLocalReemissionDotProd = RCT.quickTH1D("VisLocalReemissionDotProd","VisLocalReemissionDotProd",120,-1.1,1.1,"Vis Local Reemission Dist Dot X","Entries")
VisPhotonCreationX = RCT.quickTH1D("VisCreationCoordX","VisCreationCoordX",100,0.0,(max(TPBboundaryValues)-min(TPBboundaryValues))*10**3,"Vis Creation X Coord","Entries")
VisPhotonAbsX = RCT.quickTH1D("VisAbsCoordX","VisAbsCoordX",100,0.0,(max(TPBboundaryValues)-min(TPBboundaryValues))*10**3,"Vis Abs X Coord","Entries")
VisPhotonAbsLength = RCT.quickTH1D("VisAbsLength","VisAbsLength",100,0.0,20.,"Vis Abs Length","Entries")
VisUpstreamDiskDotProd = RCT.quickTH1D("VisUpstreamDiskDotProd","VisUpstreamDiskDotProd",120,-1.1,1.1,"Vis Upstream Disk Flux Dot X","Entries")
VisDownstreamDiskDotProd = RCT.quickTH1D("VisDownstreamDiskDotProd","VisDownstreamDiskDotProd",120,-1.1,1.1,"Vis Downstream Disk Flux Dot X","Entries")
VisPhotonsCreatedByUVPhoton = RCT.quickTH1D("VisPhotonsCreatedByUVPhoton","VisPhotonsCreatedByUVPhoton",10,0,10,"Number of Visible Photons Produced By UV","Entries")

allTheHists = [numTracksHist,allphotons_WavelengthHist,UVphotons_WavelengthHist,visPhotons_WavelengthHist]
allTheHists += [UVTermX,UVTermY,UVTermZ,UVTermAtSlit,UVPenetrationDepth,UVDotProdAtUpstreamTracking]
allTheHists += [VisTermX,VisTermY,VisTermZ,VisLocalReemissionDotProd,VisPhotonCreationX,VisPhotonAbsX,VisPhotonAbsLength,VisUpstreamDiskDotProd,VisDownstreamDiskDotProd,VisPhotonsCreatedByUVPhoton]

testTermX = RCT.quickTH1D("testTermX","testTermX",400,-100,300,"Num Tracks","Entries")
test3d = ROOT.TH3D("test3d","test3d",400,-100,300,100,-50,50,100,-50,50)

### UV hists and dataStructures
UVStepVolumes = {}
UVStepProcesses = {}
UVStepEndVolumes = {}
UVStepEndProcess = {}

VisStepVolumes = {}
VisStepProcesses = {}
VisStepEndVolumes = {}
VisStepEndProcess = {}

# Photon Counter 
vis_detect_count = 0
vis_total_count = 0

# Some UV Photon counting
UVPhotonStopInTPBAnNoVis = 0
UVPhotonStopInTPBAndVis = 0
UVPhotonPassThroughTPB = 0
UVPhotonsPassThroughUpstream = 0
UVPhotonsReflectedOffUpstreamTPBSurf = 0

# Some visible photon counting
VisPhotonsNotCreatedByParentUV = 0
VisPhotonsCreatedByParentUV = 0
VisPhotonsPassingUpstreamDisk = 0
VisPhotonsPassingDownstreamDisk = 0
VisPhotonsAbsInTPB = 0
VisPhotonsAbsInAcrylic = 0
VisPhotonDetectedFromUV = 0 
VisPhotonDetectedFromVis = 0 

fileIterator = rat.dsreader(theFileName)
for iEntry,anEntry in enumerate(fileIterator):
	#if iEntry > 100000:
	#	break
	if iEntry%10000 == 0 and iEntry != 0:
		print iEntry

	tempMC = anEntry.GetMC()
	numTracks = tempMC.GetMCTrackCount()
	numTracksHist.Fill(numTracks)	

	UVTrack = tempMC.GetMCTrack(0)
	UVFirstStep = UVTrack.GetMCTrackStep(0)

	for iTrack in range(numTracks):
		tempTrack = tempMC.GetMCTrack(iTrack)
		
		trackFirstStep = tempTrack.GetMCTrackStep(0)
		tempWavelength = 1.2398/(trackFirstStep.GetKE()*10**6)*1000.
		allphotons_WavelengthHist.Fill(tempWavelength)

		if iTrack == 0:
			UVphotons_WavelengthHist.Fill(tempWavelength)	
		else:
			visPhotons_WavelengthHist.Fill(tempWavelength)

	# Check conservation of energy
	if numTracks > 1:
		energySum = 0.0 # in ev
		for iTrack in range(1,numTracks):
			tempTrack = tempMC.GetMCTrack(iTrack)
			tempStep = tempTrack.GetMCTrackStep(0)
			energySum += tempStep.GetKE()*10**6

		excessEnergyHist.Fill(UVFirstStep.GetKE()*10**6 - energySum)
		#if energySum > UVFirstStep.GetKE()*10**6:
	#		print 'bad Conv Energy'
	# Now check the fate of the UV photons
	tempUVTrackVolumes = []
	for iUVStep in range(UVTrack.GetMCTrackStepCount()):
		tempStep = UVTrack.GetMCTrackStep(iUVStep)
		tempVolume = tempStep.GetVolume()
		tempUVTrackVolumes.append(tempVolume)
		tempProcess = tempStep.GetProcess()
		tempMomentum = tempStep.GetMomentum()
		tempEndpoint = tempStep.GetEndpoint()

		tempUVTrackVolumes.append(tempVolume)

		if tempVolume not in UVStepVolumes.keys():
			UVStepVolumes[tempVolume] = 1
		else:
			UVStepVolumes[tempVolume] += 1

		if tempProcess not in UVStepProcesses.keys():
			UVStepProcesses[tempProcess] = 1
		else:
			UVStepProcesses[tempProcess] += 1

		if (iUVStep == UVTrack.GetMCTrackStepCount()-1):
			stepEndpoint = tempStep.GetEndpoint()
			if 140. < stepEndpoint.x() < 150.:
				UVTermAtSlit.Fill(stepEndpoint.y(),stepEndpoint.z())
			UVTermX.Fill(stepEndpoint.x())
			UVTermY.Fill(stepEndpoint.y())
			UVTermZ.Fill(stepEndpoint.z())
			if tempVolume not in UVStepEndVolumes.keys():
				UVStepEndVolumes[tempVolume] = 1
			else:
				UVStepEndVolumes[tempVolume] += 1

			if tempProcess not in UVStepEndProcess.keys():
				UVStepEndProcess[tempProcess] = 1
			else:
				UVStepEndProcess[tempProcess] += 1

			if tempVolume == 'tpbVolume':
				UVPenetrationDepth.Fill(tempStep.GetLength()*10**3)

		if tempVolume == 'upstreamTrackingDisk':
			# Dot product of momeuntum unit vector with X axis
			UVDotProdAtUpstreamTracking.Fill((tempMomentum.Unit()).Dot(ROOT.TVector3(1.0,0.0,0.0)))

	if 'tpbVolume' in tempUVTrackVolumes and 'upstreamTrackingDisk' in tempUVTrackVolumes:
		lastUVStep =  UVTrack.GetMCTrackStep(UVTrack.GetMCTrackStepCount()-1)
		lastStepEndpoint = lastUVStep.GetEndpoint()
		lastStepVolume = lastUVStep.GetVolume()
		lastStepMomentum = lastUVStep.GetMomentum()
		lastProcess = lastUVStep.GetProcess()
		lastStepXDot = (lastStepMomentum.Unit()).Dot(ROOT.TVector3(1.0,0.0,0.0))

		if lastStepXDot > 0.0:
			UVPhotonsPassThroughUpstream += 1
		elif lastStepXDot < 0.0 and lastStepEndpoint.x() < min(TPBboundaryValues):
			# This is the likely reflection scenario
			UVPhotonsReflectedOffUpstreamTPBSurf += 1

		if lastStepVolume == 'tpbVolume' and  numTracks > 1:
			UVPhotonStopInTPBAndVis += 1
		elif lastStepVolume == 'tpbVolume' and  numTracks == 1:
			UVPhotonStopInTPBAnNoVis += 1
		elif lastStepVolume != 'tpbVolume' and numTracks == 1 and lastStepXDot > 0.0 and lastStepEndpoint.x() > max(TPBboundaryValues):
			UVPhotonPassThroughTPB += 1
		
		#for iUVStep in range(UVTrack.GetMCTrackStepCount()):	
		#	tempStep = UVTrack.GetMCTrackStep(iUVStep)
			

	########################################################################################################
	########################## Now do the visible ##########################################################
	########################################################################################################

	tempVisPhotonsProduced = 0
	tempVisPhotonsProducedByUV = 0
	for iTrack in range(numTracks): 
		if iTrack == 0:
			continue

		vis_total_count += 1
		tempTrack = tempMC.GetMCTrack(iTrack)
		numVisSteps = tempTrack.GetMCTrackStepCount()

		UVTrack = tempMC.GetMCTrack(0)
		UVEndpoint = ((UVTrack).GetMCTrackStep(UVTrack.GetMCTrackStepCount()-1)).GetEndpoint()
		# We want to enforce that any visible photons not starting from the UV photon endpoint are ignored.
		firstVisStep = tempTrack.GetMCTrackStep(0)
		firstVisStepEndpoint = firstVisStep.GetEndpoint()
		VisWavelength = 1.2398/(firstVisStep.GetKE()*10**6)*1000.
	
		VisParentWasntUV = False	
		if firstVisStepEndpoint.x() == UVEndpoint.x() and firstVisStepEndpoint.y() == UVEndpoint.y() and firstVisStepEndpoint.z() == UVEndpoint.z() and VisWavelength > 350.:
			tempVisPhotonsProducedByUV += 1
			VisParentWasntUV = False
		elif VisWavelength > 350 and (firstVisStepEndpoint.x() == UVEndpoint.x() and firstVisStepEndpoint.y() == UVEndpoint.y() and firstVisStepEndpoint.z() == UVEndpoint.z()) == False:
			# This is probably the case where the parent photon was not from the UV photon, but instead another visible
			VisPhotonsNotCreatedByParentUV += 1
			VisParentWasntUV = True
			#continue
		tempVisPhotonsProduced += 1

		# loop through the steps of the visible photon
		for iStep in range(numVisSteps):
			tempStep = tempTrack.GetMCTrackStep(iStep)
			tempEndpoint = tempStep.GetEndpoint()
			tempMomentum = tempStep.GetMomentum()
			tempVolume = tempStep.GetVolume()
			tempProcess = tempStep.GetProcess()	
		
			if tempVolume not in VisStepVolumes.keys():
				VisStepVolumes[tempVolume] = 1
			else:
				VisStepVolumes[tempVolume] += 1

			if tempProcess not in VisStepProcesses.keys():
				VisStepProcesses[tempProcess] = 1
			else:
				VisStepProcesses[tempProcess] += 1
	
			#Check if the first step
			if iStep == 0:
				VisLocalReemissionDotProd.Fill((tempMomentum.Unit()).Dot(ROOT.TVector3(1.0,0.0,0.0)))	
				VisPhotonCreationX.Fill((tempEndpoint.x()-min(TPBboundaryValues))*10**3)
	
			if iStep != 0 and iStep != numVisSteps-1:
				if tempVolume == 'upstreamTrackingDisk':
					VisUpstreamDiskDotProd.Fill((tempMomentum.Unit()).Dot(ROOT.TVector3(1.0,0.0,0.0)))
					VisPhotonsPassingUpstreamDisk += 1
				elif tempVolume == 'downstreamTrackingDisk':
					VisDownstreamDiskDotProd.Fill((tempMomentum.Unit()).Dot(ROOT.TVector3(1.0,0.0,0.0)))
					VisPhotonsPassingDownstreamDisk += 1

			# Check if the last step 
			if iStep == numVisSteps-1:
				VisTermX.Fill(tempEndpoint.x())
				VisTermY.Fill(tempEndpoint.y())
				VisTermZ.Fill(tempEndpoint.z())
				
				if tempVolume not in VisStepEndVolumes.keys():
					VisStepEndVolumes[tempVolume] = 1
				else:
					VisStepEndVolumes[tempVolume] += 1

				if tempProcess not in VisStepEndProcess.keys():
					VisStepEndProcess[tempProcess] = 1
				else:
					VisStepEndProcess[tempProcess] += 1
	
				if tempVolume == 'tpbVolume': 
					VisPhotonAbsX.Fill((tempEndpoint.x()-min(TPBboundaryValues))*10**3)
					VisPhotonAbsLength.Fill(tempStep.GetLength()*10**3)
					VisPhotonsAbsInTPB += 1
				elif tempVolume == 'detector_vol_vac':
					vis_detect_count += 1
					if VisParentWasntUV == True:
						VisPhotonDetectedFromVis += 1
					else:
						VisPhotonDetectedFromUV += 1
				elif tempVolume == 'acrylicSampleDisk':
					VisPhotonsAbsInAcrylic += 1
					#print tempEndpoint.x()
					#test3d.Fill(tempEndpoint.x(),tempEndpoint.y(),tempEndpoint.z())
					#print tempProcess

	if tempVisPhotonsProduced != 0:
		VisPhotonsCreatedByParentUV += tempVisPhotonsProducedByUV
		VisPhotonsCreatedByUVPhoton.Fill(tempVisPhotonsProducedByUV)

savingRootFile = ROOT.TFile(pathToData+'/geoCalcs/pos_'+str(nodeNumber)+'_photonTrack.root',"RECREATE")
for aHist in allTheHists:
	savingRootFile.WriteTObject(aHist)
savingRootFile.Close()

jsonFileOut = open(pathToData+'/geoCalcs/pos_'+str(nodeNumber)+'_photonTrack.json','w+')
jsonStructOut = {'UVStepVolumes':UVStepVolumes,'UVStepProcesses':UVStepProcesses,'UVStepEndVolumes':UVStepEndVolumes,'UVStepEndProcess':UVStepEndProcess,
				'VisStepVolumes':VisStepVolumes,'VisStepProcesses':VisStepProcesses,'VisStepEndVolumes':VisStepEndVolumes,'VisStepEndProcess':VisStepEndProcess,
				'vis_detect_count':vis_detect_count,'vis_total_count':vis_total_count,
				'UVPhotonStopInTPBAnNoVis':UVPhotonStopInTPBAnNoVis,'UVPhotonStopInTPBAndVis':UVPhotonStopInTPBAndVis,'UVPhotonPassThroughTPB':UVPhotonPassThroughTPB,'UVPhotonsPassThroughUpstream':UVPhotonsPassThroughUpstream,'UVPhotonsReflectedOffUpstreamTPBSurf':UVPhotonsReflectedOffUpstreamTPBSurf,
				'VisPhotonsNotCreatedByParentUV':VisPhotonsNotCreatedByParentUV,'VisPhotonsCreatedByParentUV':VisPhotonsCreatedByParentUV,'VisPhotonsPassingUpstreamDisk':VisPhotonsPassingUpstreamDisk,'VisPhotonsPassingDownstreamDisk':VisPhotonsPassingDownstreamDisk,'VisPhotonsAbsInTPB':VisPhotonsAbsInTPB,'VisPhotonsAbsInAcrylic':VisPhotonsAbsInAcrylic,'VisPhotonDetectedFromVis':VisPhotonDetectedFromVis,'VisPhotonDetectedFromUV':VisPhotonDetectedFromUV,'VisPhotonsNotCreatedByParentUV':VisPhotonsNotCreatedByParentUV}
json.dump(jsonStructOut,jsonFileOut)
jsonFileOut.close()


