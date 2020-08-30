import pandas as pd
import re 

class Songs():
    planningCenterSongs = pd.read_csv("songs.csv", dtype = {"CCLI":str})
    planningCenterSongs['Title'] = planningCenterSongs.apply(lambda x: x.Title.lower(),axis = 1)
    songOptions = planningCenterSongs[['Id','Title','CCLI','Arrangement 1 Chord Chart']]

    def __init__(self,*argv):
        #self.lyrics = self.planning_center_songs['Arrangement 1 Chord Chart']
        self.selected = [a for a in argv]
        self.selected = list(map(lambda x: str(x).lower(),self.selected))
        self.songOptions = self.songOptions[self.songOptions.Title.isin(self.selected)]
        self.stop_words = ["Verse 1","Verse 2","Verse 3","Verse 4","Verse 5","Pre-Chorus","Chorus","Bridge","Tag","Ending","Chorus 1","Chorus 2","Verse"]
        
    def __cleanText(self,regex,text):
        """
        Function to remove the chords/numbers from the lyrics 
        """
        new_text = text
        new_text = re.sub(regex,'',new_text)
        ret_text = " ".join(new_text.replace("\r","").replace("\n"," ").split())
        return ret_text

    def __findPositions(self,words):
        """
        Function to find the start and stop position of each 
        stop word within the lyrics 
        
        """
        d = {}
        for w in self.stop_words:
            if w == 'Chorus':
                s = "(?<!Pre-)Chorus(?!\s\d+?)"
            elif w == 'Verse':
                s = "Verse(?!\s\d+?)"
            else:          
                s = w
            m = re.search(s,words,flags = re.IGNORECASE)
            if m is not None:
                pos = m.span()
                d.__setitem__(w,pos)
        return d 

    def __extractLyrics(self,start,cleaned_words):
        """
        Function to extract the text between 2 stop words 
        """
        pat = f"{start}\s*?(.*?)\s*?(Verse 1|Verse 2|Verse 3|Verse 4|Verse 5|Pre-Chorus|Chorus|Bridge|Tag|Ending|Chorus 1|Chorus 2|$)"
        res = re.search(pat,cleaned_words,flags=re.IGNORECASE)
        return res.groups()[0]


    def getLyrics(self):
        """
        This function will output a dictionary in the following format {Song: {Section: Lyrics}}
        
        Example:

        {Our God Saves: {Chorus 1: Our God saves Our God saves There is hope in your name}}
        
        """
        d = {}
        for s in self.selected:
            temp_str = self.songOptions[(self.songOptions.Title == s)].iloc[(0,3)]
            cleaned = self.__cleanText("\[.{1,4}\]",temp_str)
            positions = self.__findPositions(cleaned) ## identifies the positions (verse 1, verse 2, chorus)
            dd = {}
            for p in positions.keys():
                lyrs = self.__extractLyrics(p,cleaned)
                dd[p] = lyrs
            d[s] = dd
        return d

    def getArrangement(self):
        pass



test = Songs("Our God Saves","Mighty to save")
#test.songOptions[(test.songOptions.Title == 'our god saves')].iloc[(0,3)]
ret = test.getLyrics()



