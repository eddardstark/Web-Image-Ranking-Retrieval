import flickr
import urllib, urlparse
import os
import sys
import math
import time
from nltk.corpus import wordnet as wn  
import webbrowser


# Provide Users' Groups here

user1 = ['beach','sand','sun','wave','surf']
user2 = ['city','europe','music','asia']
user3 = ['soccer','barcelona','brazil','london','europe', 'cup']
user4 = ['fruit']
user5 = ['dog' , 'canine' ]
user6 = ['movies','books','harry','hogwarts']
user7 = ['pottery','clay']
user8 = ['islam','quran']

#set user here

user = user8

#set output file nam
output_file = "output1.html"


#############################################################################
contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<title>Social Context Based Image Optimization </title>
<head>
<style>
div.img {
    margin: 5px;
    padding: 5px;
    border: 1px solid #0000ff;
    height: auto;
    width: auto;
    float: left;
    text-align: center;
}	

div.img img {
    display: inline;
    margin: 5px;
    border: 1px solid #ffffff;
}

div.img a:hover img {
    border: 1px solid #0000ff;
}

div.desc {
  text-align: center;
  font-weight: normal;
  width: 100%;
  margin: 5px;
}
</style>
</head>
<body  bgcolor="#708890">
'''
#############################################################################




# Progress Bar
def progress(width, percent):
    marks = math.floor(width * (percent / 100.0))
    spaces = math.floor(width - marks)
 
    loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
 
    sys.stdout.write("%s %d%%\r" % (loader, percent))
    if percent >= 100:
        sys.stdout.write("n")
    sys.stdout.flush()

# Get Social Relevance Score
def get_score(tags, groups):
  sscore = 0
  scount = 0 
  illegal_word = 0

  if (tags != None ) :
   for g in groups:
    
    for x in k.tags:
     try : 
      #print str(x.text), 
      #check substring else calculate words similarity score
      if g in str(x.text).lower():
	sscore += 2.0
        scount += 1
      else:
       tag = wn.synset(str(x.text).lower()+'.n.01')
       group = wn.synset(g+ '.n.01')  
       sem = wn.path_similarity(group,tag)
       if sem >= 0.3 :
        sscore += sem
	scount += 1     
     except:
	illegal_word += 1
  if scount != 0 :
    return sscore/scount
  else :
    return 0


if len(sys.argv)>1:
    text = sys.argv[1]
else:
    print 'no text specified'
    sys.exit()



# searching images
f = flickr.photos_search(text=text,sort='interestingness-desc')
urllist = [] #store a list of urls
VRS = [] # store list of VR scores
SRS = [] # store list of SR scores 
FRS = [] # store list of Final scores
i = 1
print '\n Querying images from Flickr.. This may take a few minutes..\n' 
# Ranking each image
for k in f  :
  try  :
    #time.sleep(1)
    url = k.getURL(size='Medium', urlType='source')
    urllist.append(url) 
    #Visual Score
    VRS.append((1 - (i - 1)/len(f))/math.log(i + 1,2))
    # Social score
    #print get_score(k.tags , user1)
    SRS.append(get_score(k.tags , user))
    #Final Score
    FRS.append(1 * VRS[i-1] + 2 * SRS[i-1]) # boosting Social score for personalized results
    progress(50, (i * 100/len(f)))
    i= i + 1
  except:
   pass
print 'Calculating VRS and SRS...'

# download and display
print 'Generating ' , output_file
zipped = zip(urllist,FRS)


file = open(output_file, 'w')
file.write(contents)
file.write('<h1>Flickr Rank</h1>' + '\n')
j=0

for c1, c2 in zipped:
     file.write('<div class="img">\n<img src="' + c1 + '" width="175" height="110"/>' + '\n</div>')
     j += 1
     if j>5:break

zipped.sort(key = lambda t: t[1], reverse = True)
file.write("\n <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/> \n ") 
file.write('<h1>SVR Rank</h1>' + '\n')
j = 0 

for c1, c2 in zipped:
     file.write('<div class="img">\n<img src="' + c1 + '" width="175" height="110"/>' + '\n</div>')
     j += 1
     if j>5:break



file.write('</body>' + '\n')
file.write('</html>')
file.close()

webbrowser.open("file:///" + os.path.abspath(output_file))


#############################################################################







