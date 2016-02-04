__author__ = 'agentnola'
import praw
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

#Loads the JSON Key, which is provided seperately
json_key = json.load(open('VoteCounter2-af942bc69325.json'))
scope = ['https://spreadsheets.google.com/feeds']
# Initilises all the credentials, and GoogleSheet stuff 
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit("Vote Counting Bot")
gc = gspread.authorize(credentials)
sh = gc.open('MHoC Master Sheet')
wks = sh.worksheet("8th Govt Voting Record")
#User Input for Reddit/ Reddit information
user = str(input("Reddit Username:"))
print("Reddit Password:")
password = str(input())
r.login(user,password)
print("Post Voting Thread Link")
tread = str(input())
legtype = int(input("Press 1 For Bills 2 For Motions 3 For Lord Bills"))
if legtype == 1:
	print("Post billnumber(without the B infront of it)")
	bill = 'B'+input("Bill Number:")
if legtype == 2:
	print("Post motionnumber(without the M infront of it)")
	bill = 'M'+input("Motion Number:")	

if legtype == 3:
	print("Post billnumber(without the LB infront of it)")
	bill = 'LB'+input("Lord Bill Number:")	

def VoteCount(thread,billnum):
    column = int(wks.find(billnum).col)

    already_done = []
    submission = r.get_submission(thread)
    submission.replace_more_comments(limit=None, threshold=0)
    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        if comment.id not in already_done:
            print(comment.body)
            print(comment.author)
            try:
                already_done.append(comment.id)
                if "aye" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = int(wks.find(str(comment.author).lower()).row)

                    val = wks.cell(row,column)
                    if "N/A" not in val.value:
                        wks.update_cell(row,column,"Aye")

                if "nay" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = wks.find(str(comment.author).lower()).row
                    val = wks.cell(row,column).value
                    if "N/A" not in val:
                        wks.update_cell(row,column,"Nay")
                if "abstain" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = wks.find(str(comment.author).lower()).row
                    val = wks.cell(row,column).value
                    if "N/A" not in val:
                        wks.update_cell(row,column,"Abst")
            except gspread.exceptions.CellNotFound:
                print("Automod Comment")



def deformat():
    cell_list = wks.range("C3:C141")
    for cell in cell_list:
        value = str(cell.value).lower()



        wks.update_cell(cell.row,cell.col,value)







##deformat()
VoteCount(tread,bill)
