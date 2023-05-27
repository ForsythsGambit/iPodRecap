import os
import pickle
from libpytunes import Library
import datetime

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

def PickleDict(LibraryDictionary : "Pickled iTunes library dictionary",LibraryFile : "name of iTunes XML library file"):
    FileModUTC=datetime.datetime.utcfromtimestamp(os.path.getmtime(LibraryFile))
    binDateName=f"{FileModUTC.day}-{FileModUTC.month}-{FileModUTC.year}"
    with open(f"{binDateName}.dat", "wb") as binfile:
        pickle.dump(LibraryDictionary, binfile)
    return binDateName
    
apc, tt=ConvertXML("testxml.xml")
dateStamp=PickleDict(apc, "testxml.xml")
arpt, alpt=ParsePlaytime(apc)
"""
with open(f"{dateStamp}.dat", "wb") as binfile:
    pickle.dump(apc,binfile)
with open(f"{dateStamp}.dat", "rb") as binfile:
    bindictlib = pickle.load(binfile)
#print(ArtistPC)
"""



"""Display Results"""
#print(ArtistPT)
print(" ")
#print(alpt)
print("total listening time: "+str(tt)+" hours")
print("Your top artist in total playtime was: " + str(arpt[0][0]) + " with "+str(arpt[0][1]) +" hours!")
print("Your second was: " + str(arpt[1][0]) + " with "+str(arpt[1][1]) +" hours, and "+str(arpt[2][0]) + " with "+str(arpt[2][1]) +" hours in third. \nFollowed by "+str(arpt[3][0]) + " with "+str(arpt[3][1]) +" hours, and "+str(arpt[4][0]) + " with "+str(arpt[4][1]) +" hours in fifth.")
print(' ')
print("Your top album in total playtime was: " + str(alpt[0][0]) + " with "+str(alpt[0][2]) +" hours!")
print("Your second was: " + str(alpt[1][0]) + " with "+str(alpt[1][2]) +" hours, and "+str(alpt[2][0]) + " with "+str(alpt[2][2]) +" hours in third. \nFollowed by "+str(alpt[3][0]) + " with "+str(alpt[3][2]) +" hours, and "+str(alpt[4][0]) + " with "+str(alpt[4][2]) +" hours in fifth.")
