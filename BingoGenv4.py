import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

print("Welcome to u/AVeryHappyTeddy's Bingo Generator!")
loadOld = input("Do you want to load a previously generated board? (Y/N)")


def BingoStitcher(): #Actually creates the bingo sheets
    termsList = open("termsList.txt").readlines()
    terms = len(termsList)
    print("Found {} terms".format(terms))
    imgList = []
    for x in range(len(termsList)+1): #Pregenerate and cache all of the tiles so that we don't have to regenerate the same tiles over and over
        if x == len(termsList): #Generating the Free Space tile without adding it to the terms list
            tempString = "Free Space"
        else:
            tempString = termsList[x].strip("\n") #Removing the new line characters
        myFont = ImageFont.truetype("arial.ttf", 20) #Get that font boiii
        Max_W = 100
        Max_H = 100
        img = Image.new('RGB', (Max_W, Max_H), color = 'white') #Create the individual tile for the term
        ImageDraw.Draw(img).rectangle([(0,0),(Max_W-1,Max_H-1)], fill=None, outline='black') #Draw a border around the tile        
        w, h = ImageDraw.Draw(img).textsize(tempString, font=myFont) #Calculate optimal dimensions of the text
        if w > 80: #If the term is too long then we gotta get fanncccyy
            para = textwrap.wrap(tempString, width=7)
            current_h, pad = 40/len(para), 1
            for line in para:
                w, h = ImageDraw.Draw(img).textsize(line, font=myFont)
                ImageDraw.Draw(img).text(((Max_W-w)/2, current_h), line, font=myFont, fill='black') #Adds the formatted text to the tile
                current_h += h + pad
        else:
            ImageDraw.Draw(img).text(((Max_W-w)/2,(Max_H-h)/2), tempString, font=myFont, fill='black') #Draw the text
        imgList.append(img) #Add the pregenerated image to the list of images
    teamNum = int(input("Your team number? (If you don't want to include this just put 0): "))
    quanity = int(input("How many bingo sheets do you want to create?: "))
    for i in range(quanity): #Begin generating the sheets
        print("Creating Bingo Sheet {}".format(i+1))
        bsheet = Image.new('RGB',(502,702), color='white')
        ImageDraw.Draw(bsheet).rectangle([(0,150),(501,651)], fill=None, outline='black') #Add the border to the overall sheet
        for line in range(3): #This loop just handles all the heading text on the sheet
            if line == 1 and teamNum == 0: #If no number entered, skip
                pass
            else:
                fontSize = [70,20,14]
                textCont = ['Bingo!','From Team #{}'.format(teamNum),'https://git.io/fjTqM']
                textHeight = [24,110,670]
                univFont = ImageFont.truetype("arial.ttf", fontSize[line])
                w, h = ImageDraw.Draw(bsheet).textsize(textCont[line], font=univFont)
                ImageDraw.Draw(bsheet).text(((502-w)/2, textHeight[line]), textCont[line], font=univFont, fill='black')
        rantiles = random.sample(range(terms), 24) #Pick 24 random tile numbers to use
        rantiles.insert(12,len(termsList)) #Adding the Free Space tile to the randomly selected set
        #print(rantiles)
        for x in range(25): #Draw the tiles and paste them in
            x_pos = Max_W*((x) % 5) + 1 #Calculate the column position based on x
            y_pos = ((x)//5)*Max_H + 151 #Calculate the row position based on y
            bsheet.paste(imgList[rantiles[x]], (x_pos, y_pos)) #Paste the tile into the sheet
            #print("({},{})".format(x_pos,y_pos))
        bsheet.save("BingoSheet_{}.png".format(i))


if loadOld in ['Y', 'y']: #Can reuse already generated list because retyping all the terms is annoying as fucccckkk
    BingoStitcher()
else:
    print("Generating new board, please enter at least 24 terms")
    print("When done creating your list type 'done'")
    i = 0
    termsList = []
    file = open("termsList.txt","w")
    while True: #Generating terms list
        newTerm = input("Term {}: ".format(i+1))
        if newTerm == 'done':
            if i < 24: #Not enough terms to create a sheet
                print("You only have {} terms, 24 are needed to generate a board".format(i-1))
            else:
                break
        else:
            termsList.append(newTerm)
            i += 1
    file.write('\n'.join(termsList)) #Write the term document for saving stuffs
    file.close()
    print("List created with {} terms!".format(i))
    BingoStitcher()
