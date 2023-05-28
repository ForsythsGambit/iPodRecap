# iPodRecap
A year in review for your itunes library like spotify, built with python.
This script will take an iTunes XML Library file, or compare two of them, to calculate your top 5 artists and top 5 albums by your playtime.

# Usage
For now, a copy of the iTunes Library XML file must be placed in the same directory.
Executing `main.py` as __main__ will cause a prompt asking for file name(s) of the xml files and will print a summary of the playtime statistics.

To use import iPodRecap as a module call the `LibraryInputs()` function, which wraps all of the internal functions to return the final result.
To receive the total playtime statistics of one library file call `LibraryInputs()` with one filename as an argument.
For example:

`LibraryInputs("testxml.xml")`

To calculate the difference of playtime statistics to find the top albums and artists over an interval of time call `LibraryInputs()` with two filenames as arguments.
The script will subtract the playtime of each item of the older XML file from the newer to calculate the most played items in the time between each files copying.
For example:

`LibraryInputs("oldxml.xml", "newxml.xml")`

To toggle whether `LibraryInputs()` prints the playtime summary you may pass the `Verbose` flag as True, but is False by default.The argument must be named as below
when only passing one filename as an argument like the below example.

`LibraryInputs("testxml.xml",Verbose = True)`

Regardless of the number of library filenames passed `LibraryInputs()` will return a tuple of the following: (total playtime (float), a nested ordered list of the top 5 artists and corresponding playtime, then a similar list containing the top 5 albums and playtime.
For example:

`TotalPlaytime, ArtistPlaytimeList, AlbumPlaytimeList = LibraryInputs("oldxml.xml", "newxml.xml")`