# iPodRecap
A year in review for your itunes library like spotify, built with python.
This project is still in early alpha and will likely change significantly.

# Usage
Substituting `"testxml.xml"` with your iTunes library xml file and running the following

```
ParsedDictionary, TotalTimeListened=ConvertXML("testxml.xml")

FileDateStamp=PickleDict(ParsedDictionary, "testxml.xml")

ArtistPlaytimeDictionary, AlbumPlaytimeDictionary=ParsePlaytime(ParsedDictionary)
```
will return two final dictionaries: `ArtistPlaytimeDictionary` and `AlbumPlaytimeDictionary`. Each containing the top five Artists and Albums respectively along with the corresponding playtime of each. 
An example output might be:
```
[('Pinback', 41.82342388888889), ('TTNG', 18.18224972222222), ('Tortoise', 15.097830833333335), ('Harry Callaghan (Harry101UK)', 12.221599999999999), ('31knots', 0.5548444444444445)]
```
and 
```
[('Animals', 'TTNG', 18.18224972222222), ('TNT', 'Tortoise', 13.181833611111113), ('Portal Stories: Mel Soundtrack', 'Harry Callaghan (Harry101UK)', 12.221599999999999), ('Summer in Abaddon', 'Pinback', 10.128097499999999), ('Blue Screen Life', 'Pinback', 9.5586825)]
```
