# SrcSuperSearch
Two Scripts, one is supposed to get all users ID from src using the API (right now it only gets 50%) and the other script gets farming related data from every the users found.

First Use the GetAllIDs.py to run through every user on sr.c and put their ids on a csv.
Then run the GetData.py to write a csv with all the farming related data from every users on the csv.

the data get by the script : id, name, pronouns, area, area Label, power Level, color 1, color 2, is the color Animated?, signup Date, has donated?, number of donations, coin, supporter End Date, boost End Date, is a Game Moderator, is Translator, is Supporter, is Boosted, runs ILs, runs FGs, runs, categories ILs, categories FGs, categories, amount of unique games played for ILs, amount of unique games played for FGs, amount of unique games, platforms ILs, platforms FGs, platforms, wrs ILs, wrs FGs, wrs, podiums ILs, podiums FGs, podiums, obsoletes ILs, obsoletes FGs, obsoletes, Games with at least 1 wrs, amount of unique Misc categories, amount of unique levels

the GetData.py uses only one request per user, and each user takes more or less 1 second to be processed.

a few problems to solve with the scripts:

 - discover what coin means

 - GetAllIDs.py doesn't get all the users on speedrun.com, it only gets users that starts with one of these characters: _-.|@0123456789abcdefghijklmnopqrstuvwxyz not case sensitive,
 - it doesn't get users names started with accented letters like áàä...
 - it doesn't get users started with the plus characters "+"
 
 - GetData.py dates are not formatted
