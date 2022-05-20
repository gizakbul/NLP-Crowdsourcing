from cmath import tan
from pickle import FALSE
import string
from tkinter.tix import CheckList
import pandas as pd      

data = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\4\\Bitirme\\NLP-Crowdsourcing\\Natural Language Processing\\test.csv',sep=",")
characterList    = [['b', 'p'], ['c','ç'], ['d','t'], ['g','k'], ['ğ','k']]
rowList          = list() #Key-Tag ikilisi tutar.
stemList         = list() #cümle içinde sözlükte geçenleri stemListe atarız
ortakKelimeler   = list()
indexs           = list()
etiketList       = list()
likeDatas        = list()
newSentence      = list() 
clearSentence    = list()
AllProduct       = list() #Bir cumle 2'den fazla ürün içeriyorsa
dataType         = list()
searchToken      = list()
productIndexList = list() #cümle içindeki ürünlerin indexini tutar
keepWord         = list() #ortak kelimelerdeki verileri hangi ürüne göre eklediğini yazar (örn: Tire Süt Kooperatifi, keepWord: süt)
createdSentence  = list() 
CheckControlList = list() 
SimilarityWord   = list() 

def ClearData(sentence):
    sentence = sentence.translate(sentence.maketrans('', '', string.punctuation))
    sentence = sentence.lower()
    words    = sentence.split(" ")

    for i in range(0,len(words)):
        words[i] = words[i].capitalize()
        
    return words



for col in data.columns:
        if data[col].isnull().any():
             data[col] = data[col].fillna("Bilinmiyor")
        
def findElements(data):
        result = dict()
        for col in data.columns:
            temp = []
            if col != "Id":
                for i in data[col]:
                    if i != "Bilinmiyor":
                        temp.append(i)
                result[col] = temp
        return result


def CreateRowList():  #verileri Key-Tag ikili liste olarak tutma
        myDic    = findElements(data)
        allKeys  = ",".join(myDic["Key"])
        allWords = allKeys.split(",") 
        allTags  = ",".join(myDic["Tag"])
        allTags  = allTags.split(",")
        for k in range (0,len(allWords)):
            key = allWords[k]
            tag = allTags[k]
            rowList.append([key,tag])
        return rowList


def Check(word): #kelimeyi veri tabanında arayan fonksiyon
    i = 0
    while i < len(rowList):
        """if((word in rowList[i][0]) & (word!=rowList[i][0])):
            ortakKelimeler.append(rowList[i][0])"""
        if (word==rowList[i][0]):
            dataType.append([rowList[i][0],rowList[i][1]])
            print("-------word: ",word,", dataType: ",dataType)
            return True
        i = i +1
        
    return False
           

def CreateStemList(word):  #StemList oluşturur. Cümledeki kelimelerin verisetinde olanlarını StemList'e atar.
    i = 0
    if Check(word):
        print("Listede var. SteamListe Ekleniyor...")
        stemList.append(word)
    else:
        
        print("Listede yok. Temizleniyor")
        while(len(word) > 1):
            word = word[:-1]
            print("word =>" , word)
            if(Check(word)):
                stemList.append(word)
                break
            
            i = i  + 1
    return word

def Check_AllWord_ForStemList(sentence):
    
    for i in range(0,len(sentence)):
        rWord=CreateStemList(sentence[i])
        print("sentence[",i,"] : ", sentence[i], " -------> ",rWord)
        newSentence.append(rWord)
    print("New Sentence -----> ",newSentence)
    for i in range(0,len(newSentence)):
        for j in range(0,len(rowList)):
            if((len(newSentence[i])>1)):
                if(newSentence[i]==rowList[j][0]):
                   clearSentence.append([newSentence[i],rowList[j][1]])
                   CheckControlList.append([sentence[i],rowList[j][1]])
                   break
            if(len(newSentence[i])<2):
                clearSentence.append([sentence[i],"Bilinmiyor"])
                CheckControlList.append([sentence[i],"Bilinmiyor"])
                break
    
    
            
    print("Clear Sentence -----> ",clearSentence, "  len: ",len(clearSentence))
    print("Check Sentence -----> ",CheckControlList, "  len: ",len(CheckControlList))



    for i in range(0, len(rowList)):
        for j in range(0,len(clearSentence)):
            if ((clearSentence[j][0] in rowList[i][0]) & (clearSentence[j][0]!=rowList[i][0])):
                #print("Word: ",clearSentence[j][0]," rowlist word: ",rowList[i][0])
                ortakKelimeler.append([rowList[i][0],rowList[i][1]])
                keepWord.append(clearSentence[j][0])
            if ((clearSentence[j][0] in rowList[i][0]) & (clearSentence[j][0]==rowList[i][0])):
                #print("**Word: ",clearSentence[j][0]," rowlist word: ",rowList[i][0])
                etiketList.append([rowList[i][0],rowList[i][1]])

    for i in range(0,len(etiketList)):
        for j in range(0,len(ortakKelimeler)):
            if((etiketList[i][0] in ortakKelimeler[j][0]) & (etiketList[i][1]==ortakKelimeler[j][1])):
                likeDatas.append(ortakKelimeler[j])

    for i in range(0,len(clearSentence)):
        for j in range(0,len(etiketList)):
            if (clearSentence[i] == etiketList[j][0]) & (etiketList[j][1] == "ÜRÜN"):
                print("Ürünün bulunduğu index: ",i," - Ürün: ",clearSentence[i])
                break

    for i in range(0,len(clearSentence)):
        flag=0
        searched_word=clearSentence[i]
        stem=[]
        key=[]
        if ((flag == 0) & len(searched_word) > 1):
            variant = []
            endOfWord = list(searched_word)
            #print("endofWord: ",endOfWord)
            lastCharacter = endOfWord[len(endOfWord) - 1]
            #print("lastCH: ",lastCharacter)
            for i in range(0, len(characterList)):
                result = lastCharacter.find(characterList[i][0])
                #print("result: ",result)
                if result==0:
                    print(lastCharacter," -------> ",characterList[i][1])
                    lastCharacter = characterList[i][1]
                else:
                    lastCharacter=lastCharacter

            variant = searched_word[0:len(searched_word)-1]+lastCharacter
            #print("variant: ",variant)


def CheckSimilarityCount(): #Cümledeki Ürün sayısını bulur
    SimilarityCount =0
    for i in range(0,len(etiketList)):
        if etiketList[i][1] == "ÜRÜN":
            SimilarityWord.append(etiketList[i][0])
            SimilarityCount = SimilarityCount+1
    return SimilarityCount

def CheckSimilarityWord(): #Eğer ürün sayısı 2'den büyükse ürün kontrolü yap"
 
    if CheckSimilarityCount() >=2:
        for i in range(0,len(clearSentence)):
            for j in range(0,len(CheckControlList)):
                if((clearSentence[i][1] == "ÜRÜN")):
                    productIndexList.append(i)
                    break
        
        for i in range(0,len(ortakKelimeler)):
            index=[] #veri indexlerini int oalrak tutar
            tmp=0 #tmp, ortak kelimeler içindeki verilerde kaç tane kelimenin ortak olduğunu tutar
            
            for j in range (0,len(productIndexList)):
                
                index.append(int(productIndexList[j]))
                print("\n\nindex:",index)
                #print("cSI: ",clearSentence[index[j]])
                #print("cSI: ",CheckControlList[index[j]])
                print("Ortak Kelime: ",ortakKelimeler[i][0]," aranan: ",CheckControlList[index[j]][0])
                result = str(ortakKelimeler[i][0]).find(CheckControlList[index[j]][0]) #ortak kelimelerde kakaolu, fındıklı, ve süt kelimelerini her datada tek tek ara, üçünün de içinde geçtiği bir veri varsa yeni veri o olabilir. 
                print("result: ",result)
                
                if(result>-1):
                    tmp=tmp+1
                print("tmp: ",tmp)
               
            if(tmp==len(index)):
                real_data = [ortakKelimeler[i][0],ortakKelimeler[i][1]]
                #print("\n",ortakKelimeler[i][0], " verisinde aranan ürünler bulunmaktadır\n\nAsıl veri ",ortakKelimeler[i][0]," olabilir.")
                return real_data
                    #INCELEEEEEEEE************************
  
def CreateNewSentence(real_data):
    for i in range(0,len(CheckControlList)):
        if(CheckControlList[i][1]!="ÜRÜN"):
            createdSentence.append(CheckControlList[i])
        else:
            if((str(createdSentence).find(str(real_data))) == -1):
                createdSentence.append(real_data)
            else:
                continue
          
    print("\n\nNew Sentence: ",createdSentence)
    print("\n\nYeni cümle: ")
 
    for i in range(0,len(createdSentence)):
        print(createdSentence[i][0])
    print("olabilir.")



    


"""for i in range(0,len(etiketList)):
            for j in range(0,len(CheckControlList)):
                if ((etiketList[i][1] == "ÜRÜN") & (etiketList[i][0] == CheckControlList[j])):
                    print("deneme")
                    searchToken.append(etiketList[i][0])
                   
                    break
                elif((etiketList[i][1] == "ÜRÜN")  & (etiketList[i][0] != CheckControlList[j])):
                    searchToken.append(CheckControlList[j])
                    break
            break"""

                    
sentence = ClearData("Migrosa gittim 1 Litre kakaolu fındıklı süt aldım 5 TL idi!!") # aralarda 1 den fazla boşluk olduğunda yeni karakter algılıyor incele    
CreateRowList()        
Check_AllWord_ForStemList(sentence)
print("Ürün Adedi: ",CheckSimilarityCount(),", Ürünler: ",SimilarityWord)
real_data = CheckSimilarityWord()
print("REAL DATA: ",real_data)
print("Etiket List: ",etiketList)
print("Ortak Kelimeler: ",ortakKelimeler)
print("Keep Word: ",keepWord)
print("Clear Sentence: ",clearSentence, " \nÜrün indexleri: ",productIndexList)
print("***",productIndexList[0:len(productIndexList)])

CreateNewSentence(real_data)

"""for k in range(0,len(stemList)):
    print(stemList[k]  + " => " + etiketList[k][1])

print(ortakKelimeler,"  LENGTH: ",len(ortakKelimeler))
print("----------------------------------------------------")
print(likeDatas,"  LENGTH: ",len(likeDatas))"""