#regular expressions are themselves a little langauge that you
#   use within other programming languages. Most all PLs
#   have some mechanism to support the use of Regular Expressions.
#Using the RE language, you specify rules that describe strings. This
#   then allows you to ask questions like....
#   "Does this string match the pattern?", or
#   "Is there a match for the pattern anywhere in this string?"


#Simple patterns
#simple character matching
import re

#Lets start with question 1
#"Does this string match the pattern?

print("Example 1")
#create a Regular Expression pattern (its called pat)
pat = re.compile("Computer Science", re.IGNORECASE)
#does this string match my pattern?
mat = pat.match("COMPUTER SCIENCE")
#mat is a match object. If the string "COMPUTER SCIENCE" didn't match
#   the pattern, then mat would be None (remember the Nonetype)
if(mat != None):
    print("We matched!")
else:
    print("We didn't match!")

#the following are metacharacters that do something beyond
#    simply matching a string . ^ $ * + ? { } [ ] \ | ( )
#we'll see what some of them do in our examples today
#but if you want to use one of them in your string to literally match
#   that character, you have to put a \ in front of it

print("\nExample 2")
#metacharacters
#   * means 0 or more occurences
#   + means 1 or more occurences
#   ? means 0 or 1 occurences
#   [ and ] - specify a character class, which is a set of characters that you wish to match.
#         Characters can be listed individually, or a range of characters can be indicated by '-'
#         For example, [abc] will match any of the characters a, b, or c; this is the same as [a-c],
#         If you wanted to match only lowercase letters, your RE would be [a-z].
#   [a-z!]* would match to 0 or more occurences of characters in the set a-z or !
phone_number = "(555)123-4567"
pat = re.compile("\([0-9]+\)[0-9]+-[0-9]+", re.IGNORECASE)
mat = pat.match(phone_number)
if(mat != None):
    print("We matched!")
else:
    print("We didn't match!")

print("\nExample 3")
#Collecting the parts of the match (extracting stuff from the string)
phone_number = "(555)123-4567"
pat = re.compile("\(([0-9]+)\)([0-9]+)-([0-9]+)", re.IGNORECASE)
mat = pat.match(phone_number)
if(mat != None):
    print("We matched!")
    print(mat.group(1))
    print(mat.group(2))
    print(mat.group(3))
else:
    print("We didn't match!")

print("\nExample 4")
#Naming the parts of the match (bc group(1), etc aren't very meaningful)
phone_number = "(555)123-4567"
pat = re.compile("\((?P<areacode>([0-9]+))\)(?P<first>([0-9]+))-(?P<second>([0-9]+))", re.IGNORECASE)
mat = pat.match(phone_number)
if(mat != None):
    print("We matched!")
    print(f"areacode: {mat.group('areacode')}")
    print(f"first: {mat.group('first')}")
    print(f"second: {mat.group('second')}")
else:
    print("We didn't match!")

#now moving on to the second question
#   "Is there a match for the pattern anywhere in this string?"

print("\nExample 5")
#FINDING a phone number withing a larger piece of text
#I get my voicemails transcribed through google voice so that I don't have to listen to them.
#   so lets imagine I want to extract a phone number from this transcribed voicemail.
voice_mail = "Hi, this is Timmy's mom Judy. Timmy wants to schedule a playdate with Lincoln \
               for sometime next week. Can you give me a call back at (909)234-9996 and we'll \
               find a time? Also, the Mr. Michel said that Lincoln left his backpack at school. \
               He wants you to call the main office at (847)325-3451."
pat = re.compile("\([0-9]+\)[0-9]+-[0-9]+", re.IGNORECASE)
mat_lst = pat.findall(voice_mail)
#mat is a list
if(mat_lst != []):
    print("We matched!")
    print(mat_lst)
else:
    print("We didn't match!")

print("\nExample 6")
#FINDING money mention in a paragraph
# predefined sets of characters:
#\d
#Matches any decimal digit; this is equivalent to the class [0-9].
#\D
#Matches any non-digit character; this is equivalent to the class [^0-9].
#\s
#Matches any whitespace character; this is equivalent to the class [ \t\n\r\f\v].
#\S
#Matches any non-whitespace character; this is equivalent to the class [^ \t\n\r\f\v].
#\w
#Matches any alphanumeric character; this is equivalent to the class [a-zA-Z0-9_].
#\W
#Matches any non-alphanumeric character; this is equivalent to the class [^a-zA-Z0-9_].
question = "alexa - what is the conversion from $15.75 to rupees?"
pat = re.compile("\$[\d]+.[\d]+", re.IGNORECASE)
mat_lst = pat.findall(question)
#mat is a list
if(mat_lst != []):
    print("We matched!")
    print(mat_lst)
else:
    print("We didn't match!")

print("\nExample 7")
#repetition
song = "Everything is awesome, everything is cool when your part of a team. \
Everything is awesome, when you're living out a dream."
pat = re.compile("Everything is awesome, ([^.]*).", re.IGNORECASE)
mat_lst = pat.findall(song)
#mat is a list
if(mat_lst != []):
    print("We matched!")
    print(mat_lst)
else:
    print("We didn't match!")

song2 = "Y M C A, you'll find it at the Y M C A. Y M C A, just go to the Y M C A."
pat = re.compile("Y M C A, ([^.]*).", re.IGNORECASE)
mat_lst = pat.findall(song2)
#mat is a list
if(mat_lst != []):
    print("We matched!")
    print(mat_lst)
else:
    print("We didn't match!")