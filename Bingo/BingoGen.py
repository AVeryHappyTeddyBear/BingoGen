import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

print("Welcome to u/AVeryHappyTeddy's Bingo Generator!")
loadOld = input("Do you want to load a previously generated board? (Y/N)")


def BingoStitcher(): #Actually creates the bingo sheets
    terms = 1
    while True: #Gotta find all the pre-created tiles so we know which to use
        try:
            im = Image.open("term_{}.png".format(terms))
            #print("Found term {}".format(terms)) DEBUG LINE
            terms += 1
        except:
            print("Found {} terms".format(terms-1))
            break
    teamNum = int(input("Your team number? (If you don't want to include this just put 0): "))
    quanity = int(input("How many bingo sheets do you want to create?: "))
    for i in range(quanity): #Begin generating the sheets
        print("Creating Bingo Sheet {}".format(i+1))
        bsheet = Image.new('RGB',(502,702), color='white')
        ImageDraw.Draw(bsheet).rectangle([(0,150),(501,651)], fill=None, outline='black') #Add the border to the overall sheet
        #Adding all the text in a really uncompact way
        headerFont = ImageFont.truetype("arial.ttf", 70) #Header font
        teamFont = ImageFont.truetype("arial.ttf", 20) #Team number font
        plugFont = ImageFont.truetype("arial.ttf", 14) #Shameless plug font
        w, h = ImageDraw.Draw(bsheet).textsize('Bingo!', font=headerFont) #Finding the center for the text
        ImageDraw.Draw(bsheet).text(((502-w)/2, 24), 'Bingo!', font=headerFont, fill='black') #Adding the header text
        if teamNum != 0: #Check if a team number was entered
            teamNumText = "From Team #{}".format(teamNum)
            w, h = ImageDraw.Draw(bsheet).textsize(teamNumText, font=teamFont) #Finding the center for the text
            ImageDraw.Draw(bsheet).text(((502-w)/2, 110), teamNumText, font=teamFont, fill='black') #Adding the team number text
        plugText = 'https://git.io/fjTqM' #Shameless plug for the bottom of the sheet
        w, h = ImageDraw.Draw(bsheet).textsize(plugText, font=plugFont) #Finding the center for the text
        ImageDraw.Draw(bsheet).text(((502-w)/2, 670), plugText, font=plugFont, fill='black') #Adding the plug text
        #The text wall is finally over
        rantiles = random.sample(range(1,terms), 24) #Pick 24 random tiles to use
        rantiles.insert(12,"free")
        #print(rantiles) DEBUG
        for x in range(25): #BEGIN THE STITCHENING!
            tile = Image.open("term_{}.png".format(rantiles[x]))
            x_pos = 100*((x) % 5) + 1 #Calculate the column position based on x, adding 1 because of the border on the sheet
            y_pos = ((x)//5)*100 + 151 #Calculate the row position based on x
            bsheet.paste(tile, (x_pos, y_pos)) #Paste the tile into the sheet
            #print("({},{})".format(x_pos,y_pos)) DEBUG
        bsheet.save("BingoSheet_{}.png".format(i))


if loadOld in ['Y', 'y']: #Can reuse already generated list because retyping all the terms is annoying as fucccckkk
    BingoStitcher()
else:
    print("Generating new board, please enter at least 24 terms")
    print("When done creating your list type 'done'")
    i = 1
    termsList = ['']
    while True: #Generating terms list
        newTerm = input("Term {}: ".format(i))
        if newTerm == 'done':
            if i < 24: #Not enough terms to create a sheet
                print("You only have {} terms, 24 are needed to generate a board".format(i-1))
            else:
                break
        else:
            termsList.append(newTerm)
            i += 1
    print("List created with {} terms!".format(i-1))
    print("Generating template") #Begin generating the individual images
    for x in range(1,i):
        myFont = ImageFont.truetype("arial.ttf", 20) #Get that font boiii
        Max_W = 100
        Max_H = 100
        img = Image.new('RGB', (Max_W, Max_H), color = 'white') #Create the individual tile for the term
        ImageDraw.Draw(img).rectangle([(0,0),(99,99)], fill=None, outline='black') #Draw a border around the tile        
        w, h = ImageDraw.Draw(img).textsize(termsList[x], font=myFont) #Calculate optimal dimensions of the text
        if w > 70: #If the term is too long then we gotta get fanncccyy
            para = textwrap.wrap(termsList[x], width=6)
            current_h, pad = 14, 2
            for line in para:
                w, h = ImageDraw.Draw(img).textsize(line, font=myFont)
                ImageDraw.Draw(img).text(((Max_W-w)/2, current_h), line, font=myFont, fill='black') #Adds the text to the tile
                current_h += h + pad
        else:
            ImageDraw.Draw(img).text(((Max_W-w)/2,(Max_H-h)/2), termsList[x], font=myFont, fill='black') #Draw the text
        img.save("term_{}.png".format(x)) #Save the individual terms
    print("Finished generating individual tiles")
    BingoStitcher()

