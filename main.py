import os
import pickle
from libpytunes import Library

libsource=Library('testxml.xml')
pickle.dump(libsource, open("binrawlib.dat", "wb"))
binlib = pickle.load(open("binrawlib.dat", "rb"))
ArtistPC={} #{Artist : {Albums: {Album name : {PlayCount : int, playtime: int}}} }

"""Organize all tracks by Artist, then by Album in a nested disctionary, sotring play counts per album and play time per album"""
#print(binlib.songs.items())
for id, song in binlib.songs.items():
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
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=song.play_count*song.length
                else:
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]=ArtistPC[song.album_artist]["Albums"][song.album]["PlayCount"]+song.play_count
                    ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]+song.play_count*song.length
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
                ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=song.play_count*song.length
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
            ArtistPC[song.album_artist]["Albums"][song.album]["PlayTime"]=song.play_count*song.length


"""remove unplayed albums"""
print(ArtistPC)
PrunedArtistPC={}
for Artist in ArtistPC.keys():
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
            print("pruned unplayed album: "+ str(album))
ArtistPC=PrunedArtistPC
pickle.dump(ArtistPC, open("bindictlib.dat", "wb"))
bindictlib = pickle.load(open("bindictlib.dat", "rb"))
