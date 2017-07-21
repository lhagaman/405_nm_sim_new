import ROOT


def quickTH1D(name, title, nbins, lowbin, highbin, xlabel, ylabel):
    tempHist = ROOT.TH1D(name, name, int(nbins), float(lowbin), float(highbin))
    tempHist.GetXaxis().SetTitle(xlabel)
    tempHist.GetYaxis().SetTitle(ylabel)
    tempHist.SetTitle(title)
    return tempHist


def quickTH2D(name, title, nbinsX, lowbinX, highBinX, nbinsY, lowbinY, highbinY, xlabel, ylabel):
    tempHist = ROOT.TH2D(name, name, int(nbinsX), float(lowbinX), float(highBinX), int(nbinsY), float(lowbinY),
                         float(highbinY))
    tempHist.GetXaxis().SetTitle(xlabel)
    tempHist.GetYaxis().SetTitle(ylabel)
    tempHist.SetTitle(title)
    tempHist.SetOption('COLZ')
    return tempHist


def fillTH1DWithList(theHist, theList):
    for aVal in theList:
        theHist.Fill(aVal)


def fillTH2DwithNestedPMTList(theHist, theList):
    for iPMT, theSet in enumerate(theList):
        for pulseTime in theSet:
            theHist.Fill(iPMT, pulseTime)


def snapshotOfFullHistSet(theDirHistSet):
    setOut = []
    for aSubset in theDirHistSet:
        tempSet = []
        tempSet.append(aSubset[0])
        tempDict = {}
        for tempKey in aSubset[1].keys():
            tempDict[tempKey] = aSubset[1][tempKey].Clone()
        tempSet.append(tempDict)
        setOut.append(tempSet)
    return setOut


def standardHistSet(postFix, uniqueName, theType=''):
    nameKey = postFix
    if theType == '':
        dictElement = {
            'numTrig': quickTH1D("NumTrigs_" + nameKey + '_' + str(uniqueName), "Number Trig " + nameKey, 11, -2, 9,
                                 'Trigger Type', 'Entries'),
            'trigRate': quickTH1D("TrigsRate_" + nameKey + '_' + str(uniqueName), "Trigger Rate " + nameKey, 11, -2, 9,
                                  'Trigger Type', 'Entries'),
            'passCuts': quickTH1D("passCuts" + nameKey + '_' + str(uniqueName), "Events that pass all cuts", 11, -2, 9,
                                  'Pass Cut Result', 'Entries'),
            'fprompt': quickTH1D("fprompt_" + nameKey + '_' + str(uniqueName), "fprompt " + nameKey, 100, -0.1, 1.1,
                                 'fprompt', 'Entries'),
            'chargeRatio': quickTH1D("chargeRatio_" + nameKey + '_' + str(uniqueName), "Charge Ratio " + nameKey, 100,
                                     -0.1, 1.1, 'Charge Ratio', 'Entries'),
            'chargePE': quickTH1D("chargePE_" + nameKey + '_' + str(uniqueName), "Total Charge PE " + nameKey, 100, 0,
                                  1000, "Charge [PE]", "Entries"),
            'PETimes': quickTH1D("PETimes_" + nameKey + '_' + str(uniqueName), "Pulse Times " + nameKey, 4282, -1064,
                                 16064, 'PE Times', 'Entries'),
            'PETimes_PMT': quickTH2D('PETimes_PMTNumber_' + nameKey + '_' + str(uniqueName),
                                     'PE Times vs. PMT Number' + nameKey, 92, 0, 92, 4282, -1064, 16064, 'PMT Number',
                                     'Pulse Time'),
            'fpromptChargeRatio': quickTH2D('fprompt_ChargeRatio_' + nameKey + '_' + str(uniqueName),
                                            'Charge Ratio vs. Fprompt ' + nameKey, 100, -0.1, 1.1, 100, -0.1, 1.1,
                                            'fprompt', 'Charge Ratio'),
            'fpromptCharge': quickTH2D('fprompt_ChargePE_' + nameKey + '_' + str(uniqueName),
                                       'ChargePE vs. Fprompt ' + nameKey, 100, -0.1, 1.1, 100, -10, 1000, 'fprompt',
                                       'Charge (PE)'),
            'ChargeRatio_ChargePE': quickTH2D('ChargeRatio_ChargePE_' + nameKey + '_' + str(uniqueName),
                                              'Charge Ratio vs. Charge PE ' + nameKey, 100, 0, 1000, 100, -0.1, 1.1,
                                              "Charge PE", "Charge Ratio"),
            'PMT_trigger_rates': quickTH1D("PMTTrigRate_" + nameKey + '_' + str(uniqueName),
                                           "PMT Trig Rates " + nameKey, 92, 0, 92, "PMT Index", "Rate [Hz]"),
            'PMT_Pulse_rate': quickTH1D("PMTPulseRate_" + nameKey + '_' + str(uniqueName), "PMT Pulse Rate " + nameKey,
                                        92, 0, 92, "PMT Index", "Pulse Rate [Hz]"), }
        return dictElement
    elif theType == 'trigger':
        dictElement = {'numTriggers': quickTH1D("numTriggers_" + nameKey + '_' + str(uniqueName),
                                                "Number of Trigers For Each Type", 11, -2, 9, 'Trigger Type',
                                                'Entries'),
                       'passCuts': quickTH1D("passCuts" + nameKey + '_' + str(uniqueName), "Events that pass all cuts",
                                             11, -2, 9, 'Pass Cut Result', 'Entries')}
        return dictElement


# Generate Histogram Set
def createHistoDictSet(uniqueID):
    masterDict = {"Observ": {}, "NHit": {}, "NHit_PassAll": {}, "Ar39": {}, "Set1": {}, "Set2": {}, "Set3": {},
                  "Set4": {}}

    for aKey in masterDict.keys():
        masterDict[aKey] = standardHistSet(aKey, uniqueID)

    return masterDict


def cloneHistoDictSet(histDictSet, uniqueID):
    dictOut = {}
    for aKey in histDictSet.keys():
        tempDictHandle = {}
        for aNestedKey in histDictSet[aKey].keys():
            tempDictHandle[aNestedKey] = histDictSet[aKey][aNestedKey].Clone()
        dictOut[aKey] = tempDictHandle

    return dictOut


def subtractTwoHistoDictSets(currentDictSet, previousDictSet):
    for aKey in currentDictSet.keys():
        for aNestedKey in currentDictSet[aKey].keys():
            currentDictSet[aKey][aNestedKey].Add(previousDictSet[aKey][aNestedKey], -1.0)
    return currentDictSet
