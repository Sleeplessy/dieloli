import os
from Core import CacheContorl,ValueHandle,GameData,TextLoading,GamePathConfig,GameConfig
from Design import AttrCalculation,MapHandle

language = GameConfig.language
gamepath = GamePathConfig.gamepath

# 初始化角色数据
def initCharacterList():
    characterListPath = os.path.join(gamepath,'data',language,'character')
    characterList = GameData.getPathList(characterListPath)
    for i in range(0,len(characterList)):
        AttrCalculation.initTemporaryObject()
        playerId = str(i + 1)
        CacheContorl.playObject['object'][playerId] = CacheContorl.temporaryObject.copy()
        AttrCalculation.setDefaultCache()
        characterDataName = characterList[i]
        characterAttrTemPath = os.path.join(characterListPath,characterDataName,'AttrTemplate.json')
        characterData = GameData._loadjson(characterAttrTemPath)
        characterName = characterData['Name']
        characterSex = characterData['Sex']
        characterSexTem = TextLoading.getTextData(TextLoading.temId,'TemList')[characterSex]
        CacheContorl.playObject['object'][playerId]['Sex'] = characterSex
        characterDataKeys = ValueHandle.dictKeysToList(characterData)
        defaultAttr = AttrCalculation.getAttr(characterSexTem)
        defaultAttr['Name'] = characterName
        defaultAttr['Sex'] = characterSex
        AttrCalculation.setSexCache(characterSex)
        defaultAttr['Features'] = CacheContorl.featuresList.copy()
        if 'Age' in characterDataKeys:
            ageTem = characterData['Age']
            characterAge = AttrCalculation.getAge(ageTem)
            defaultAttr['Age'] = characterAge
        elif 'Features' in characterDataKeys:
            AttrCalculation.setAddFeatures(characterData['Features'])
            defaultAttr['Features'] = CacheContorl.featuresList.copy()
        temList = AttrCalculation.getTemList()
        height = AttrCalculation.getHeight(temList[characterSex], defaultAttr['Age'])
        defaultAttr['Height'] = height
        if 'Weight' in characterData:
            weightTemName = characterData['Weight']
        else:
            weightTemName = 'Ordinary'
        weight = AttrCalculation.getWeight(weightTemName, height['NowHeight'])
        defaultAttr['Weight'] = weight
        measurements = AttrCalculation.getMeasurements(temList[characterSex], height['NowHeight'], weightTemName)
        defaultAttr['Measurements'] = measurements
        for keys in defaultAttr:
            CacheContorl.temporaryObject[keys] = defaultAttr[keys]
        CacheContorl.featuresList = {}
        CacheContorl.playObject['object'][playerId] = CacheContorl.temporaryObject.copy()
        CacheContorl.temporaryObject = CacheContorl.temporaryObjectBak.copy()
    initPlayerPosition()
    pass

# 获取角色最大数量
def getCharacterIndexMax():
    playerData = CacheContorl.playObject['object']
    playerMax = ValueHandle.indexDictKeysMax(playerData) - 1
    return playerMax

# 获取角色id列表
def getCharacterIdList():
    playerData = CacheContorl.playObject['object']
    playerList = ValueHandle.dictKeysToList(playerData)
    return playerList


# 初始化角色的位置
def initPlayerPosition():
    characterListPath = os.path.join(gamepath, 'data', language, 'character')
    characterList = GameData.getPathList(characterListPath)
    for i in range(0, len(characterList)):
        playerIdS = str(i + 1)
        characterDataName = characterList[i]
        characterAttrTemPath = os.path.join(characterListPath, characterDataName, 'AttrTemplate.json')
        characterData = GameData._loadjson(characterAttrTemPath)
        characterInitPosition = characterData['Position']
        characterPosition = CacheContorl.playObject['object'][playerIdS]['Position']
        MapHandle.playerMoveScene(characterPosition, characterInitPosition, playerIdS)
    pass