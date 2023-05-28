import os
import pickle
from libpytunes import Library
import datetime

def LibraryInputs(Lib1 , Lib2=None):
    if Lib2==None:
        FileModUTC=datetime.datetime.utcfromtimestamp(os.path.getmtime(Lib1))
        binDateName=f"{FileModUTC.day}-{FileModUTC.month}-{FileModUTC.year}"
        Lib1Dict, TotalTime = ConvertXML(Lib1)
        PickleDict(Lib1Dict, Lib1)
        ArtistTime, AlbumTime=ParsePlaytime(Lib1Dict)
        DisplayResults(TotalTime, ArtistTime, AlbumTime)
        return None
    FileModUTC1=datetime.datetime.utcfromtimestamp(os.path.getmtime(Lib1))
    FileModUTC2=datetime.datetime.utcfromtimestamp(os.path.getmtime(Lib2))
    binDateName1=f"{FileModUTC1.day}-{FileModUTC1.month}-{FileModUTC1.year}"
    binDateName2=f"{FileModUTC2.day}-{FileModUTC2.month}-{FileModUTC2.year}"
    if os.path.getmtime(Lib1) > os.path.getmtime(Lib2):
        #first lib is newer, need to flipflop
        FileModUTC1, FileModUTC2= FileModUTC2, FileModUTC1
        binDateName1, binDateName2 = binDateName2, binDateNam1
    Lib1Dict, Lib1TT = ConvertXML(Lib1)
    Lib2Dict, Lib2TT = ConvertXML(Lib2)
    PickleDict(Lib1Dict, Lib1)
    PickleDict(Lib2Dict, Lib2)
    #return ParseDiffPlaytime(Lib1Dict,Lib2Dict)
    DiffArtistPlaytime, DiffAlbumPlaytime = ParseDiffPlaytime(Lib1Dict,Lib2Dict)
    DisplayResults((Lib2TT-Lib1TT),DiffArtistPlaytime,DiffAlbumPlaytime)
    return None
    
def ConvertXML(libraryFile : "name of iTunes XML library file"):
    libsource=Library(libraryFile)
    ArtistPC={} #{Artist : {Albums: {Album name : {PlayCount : int, playtime: int}}} }

    """Organize all tracks by Artist, then by Album in a nested disctionary, sotring play counts per album and play time per album"""
    #print(binlib.songs.items())
    TotalTime=0
    for id, song in libsource.songs.items():
        if song.play_count != None:
            TotalTime+=(song.play_count*song.length)/3600000
        #print(ArtistPC)
        #print(str(song.name))
        #print(song.artist in ArtistPC)
        if song.album_artist in ArtistPC:
            #print("artist: "+str(song.artist)+" in ArtistPC")
            if song.album in ArtistPC[song.album_artist]["Albums"]:
                """
                if song.play_count != None:
                    print("album: "+str(song.album)+" in ArtistPC")
                    toldpc=ArtistPC[song.artist]["Albums"][song.album]["PlayCount"]
                    print("old pc: "+str(toldpc))
                    try:
                        print("new pc should be"+str(toldpc+song.play_count))
                    except:
                        print("no pcs")
                """
                if song.play_count == None:
                    pass
                else:
                    if ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]==None:
                        ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=song.play_count
                        ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=(song.play_count*song.length)/3600000
                    else:
                        ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]+song.play_count
                        ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]+(song.play_count*song.length)/3600000
                """
                if song.play_count != None:
                    print(str(ArtistPC[song.artist]["Albums"][song.album]["PlayCount"]))
                """
            else:
                #print("album: "+str(song.album)+"not in ArtistPC")
                ArtistPC[song.album_artist]["Albums"][song.album]={}
                if song.play_count == None:
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=None
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=None
                else:
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=song.play_count
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=(song.play_count*song.length)/3600000
        else:
            #print("artist: "+str(song.artist)+" not in ArtistPC")
            ArtistPC[song.album_artist]={}
            ArtistPC[song.album_artist]["Albums"]={}
            ArtistPC[song.album_artist]["Albums"][song.album]={}
            if song.play_count == None:
                ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=None
                ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=None
            else:
                ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=song.play_count
                ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=(song.play_count*song.length)/3600000

    """remove unplayed albums"""
    PrunedArtistPC={}
    for Artist in ArtistPC.keys():
        if Artist==None:
            continue
        for album in ArtistPC[Artist]["Albums"].keys():
            if ArtistPC[Artist]["Albums"][album]["PlayCount"]!=None:
                if Artist in PrunedArtistPC:
                    PrunedArtistPC[Artist]["Albums"][album]={}
                    PrunedArtistPC[Artist]["Albums"][album]["PlayCount"]=ArtistPC[Artist]["Albums"][album]["PlayCount"]
                    PrunedArtistPC[Artist]["Albums"][album]["PlayTime"]=ArtistPC[Artist]["Albums"][album]["PlayTime"]
                else:
                    PrunedArtistPC[Artist]={"Albums" : {}}
                    PrunedArtistPC[Artist]["Albums"][album]={}
                    PrunedArtistPC[Artist]["Albums"][album]["PlayCount"]=ArtistPC[Artist]["Albums"][album]["PlayCount"]
                    PrunedArtistPC[Artist]["Albums"][album]["PlayTime"]=ArtistPC[Artist]["Albums"][album]["PlayTime"]
            else:
                pass
                #print("pruned unplayed album: "+ str(album))
    
    ArtistPC=PrunedArtistPC
    return ArtistPC, TotalTime

def ParsePlaytime(LibraryDictionary : "Pickled iTunes library dictionary"):
    """Find artist with longest play time"""
    ArtistPT=[] #[(Artist,playtime)]
    AlbumPT=[]#[(Album, Artist,playtime)]
    for Artist in LibraryDictionary.keys():
        tArtistPC=0
        """
        print(" ")
        print("artist: "+str(Artist))
        print("albums: "+str(ArtistPC[Artist]["Albums"].keys()))
        """
        for album in LibraryDictionary[Artist]["Albums"].keys():
            #print(album)
            AlbumTime=0
            AlbumTime=LibraryDictionary[Artist]["Albums"][album]["PlayTime"]
            tArtistPC+=AlbumTime
            #print("len AlbumPT: "+str(len(AlbumPT)))
            for x in range(0, len(AlbumPT)):
                if AlbumTime>AlbumPT[x][2]:
                    #print("album: "+album+"Album time greater than "+str(AlbumTime)+" to "+str(AlbumPT[x][2]))
                    AlbumPT.insert(x, (str(album),str(Artist),AlbumTime))
                    if len(AlbumPT)>5:
                        AlbumPT.pop(len(AlbumPT)-1)
                    break
                if x==(len(AlbumPT)-1) and (len(AlbumPT)<5):
                    #print("adding album: "+album+"list not full")
                    AlbumPT.append((str(album),str(Artist),AlbumTime))
            if len(AlbumPT)==0:
                #print("list empty, adding album "+album)
                AlbumPT.append((str(album),str(Artist),AlbumTime))

        #print(" ")
        for x in range(0, len(ArtistPT)):
            if tArtistPC>ArtistPT[x][1]:
                ArtistPT.insert(x, (str(Artist),tArtistPC))
                if len(ArtistPT)>5:
                        ArtistPT.pop(len(AlbumPT)-1)
                break
            elif x==(len(ArtistPT)-1) and (len(ArtistPT)<5):
                ArtistPT.append((str(Artist),tArtistPC))
        if len(ArtistPT)==0:
                ArtistPT.append((str(Artist),tArtistPC))
    return ArtistPT,AlbumPT

def ParseDiffPlaytime(Library1, Library2):
    ArtistPT=[] #[(Artist,playtime)]
    AlbumPT=[]#[(Album, Artist,playtime)]
    def CheckArtistTime(artist,time):
        #print("")
        nonlocal ArtistPT
        #print(f"{artist} : {time}")
        #print(ArtistPT)
        for x in range(0,len(ArtistPT)):
            if time>ArtistPT[x][1]:
                ArtistPT.insert(x, (str(artist),time))
                #print("insert")
                if len(ArtistPT)>5:
                    #print(f"{ArtistPT}")
                    ArtistPT.pop(len(ArtistPT)-1)
                    #print("pop")
                    #print(f"{ArtistPT}")
                return True
            elif x==(len(ArtistPT)-1) and (len(ArtistPT)<5):
                ArtistPT.append((str(artist),time))
                #print("app to fill")
                return True
        if len(ArtistPT)==0:
            ArtistPT.append((str(artist),time))
            #print("app to start")
            return True
        return False
    def CheckAlbumTime(album,time):
        #print(f"{album}: {time}")
        nonlocal AlbumPT
        for x in range(0, len(AlbumPT)):
            if time>AlbumPT[x][2]:
                AlbumPT.insert(x, (str(album),str(Artist),AlbumTime))
                if len(AlbumPT)>5:
                    AlbumPT.pop(len(AlbumPT)-1)
                return True
            elif x==(len(AlbumPT)-1) and (len(AlbumPT)<5):
                AlbumPT.append((str(album),str(Artist),AlbumTime))
                return True
        if len(AlbumPT)==0:
            AlbumPT.append((str(album),str(Artist),AlbumTime))
            return True
        return False
    
    for Artist in Library2.keys():
        ArtistTime=0
        #print(f"Artist: {Artist}")
        for album in Library2[Artist]["Albums"].keys():
            #print(f"Album: {album}")
            AlbumTime=0
            if Artist not in Library1.keys():
                #print("artist not in L1")
                AlbumTime=Library2[Artist]["Albums"][album]["PlayTime"]
            elif album not in Library1[Artist]["Albums"].keys():
                #print("album not in l1")
                AlbumTime=Library2[Artist]["Albums"][album]["PlayTime"]
            else:
                #print("existing album")
                AlbumTime=Library2[Artist]["Albums"][album]["PlayTime"]-Library1[Artist]["Albums"][album]["PlayTime"]
            CheckAlbumTime(album,AlbumTime)
            ArtistTime+=AlbumTime
        CheckArtistTime(Artist,ArtistTime)
    return ArtistPT,AlbumPT

            
def PickleDict(LibraryDictionary : "Pickled iTunes library dictionary",LibraryFile : "name of iTunes XML library file"):
    FileModUTC=datetime.datetime.utcfromtimestamp(os.path.getmtime(LibraryFile))
    binDateName=f"{FileModUTC.day}-{FileModUTC.month}-{FileModUTC.year}"
    with open(f"{binDateName}.dat", "wb") as binfile:
        pickle.dump(LibraryDictionary, binfile)
    return binDateName

def DisplayResults(TotalTime,ArtistList, AlbumList):
    """Display Results"""
    print(" ")
    print("total listening time: "+str(TotalTime)+" hours")
    print("Your top artist in total playtime was: " + str(ArtistList[0][0]) + " with "+str(ArtistList[0][1]) +" hours!")
    print("Your second was: " + str(ArtistList[1][0]) + " with "+str(ArtistList[1][1]) +" hours, and "+str(ArtistList[2][0]) + " with "+str(ArtistList[2][1]) +" hours in third. \nFollowed by "+str(ArtistList[3][0]) + " with "+str(ArtistList[3][1]) +" hours, and "+str(ArtistList[4][0]) + " with "+str(ArtistList[4][1]) +" hours in fifth.")
    print(' ')
    print("Your top album in total playtime was: " + str(AlbumList[0][0]) + " with "+str(AlbumList[0][2]) +" hours!")
    print("Your second was: " + str(AlbumList[1][0]) + " with "+str(AlbumList[1][2]) +" hours, and "+str(AlbumList[2][0]) + " with "+str(AlbumList[2][2]) +" hours in third. \nFollowed by "+str(AlbumList[3][0]) + " with "+str(AlbumList[3][2]) +" hours, and "+str(AlbumList[4][0]) + " with "+str(AlbumList[4][2]) +" hours in fifth.")

if __name__ == "__main__":
    L1=input("name of first library xml file: ")
    L2=input("name of second file, leave blank if none: ")
    if L2=="":
        LibraryInputs(L1)
    else:
        LibraryInputs(L1,L2)
