import re
import requests
import jmespath
import csv

class beca:
    def __init__(self,country,name,requirements,study_level,study_field="ingenieria"):
        self.country = country
        self.name = name
        self.requirements = requirements
        self.study_level = study_level
        self.study_field = study_field 
    def __iter__(self):
        return iter([self.country,self.name,self.requirements,self.study_level,self.study_field])
class ApiCall:

    page=''
    url = 'https://api-manager.universia.net/becas-programs/api/search?page='+page+'&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true'

    headers = {
        "authority": "api-manager.universia.net",
        "method": "GET",
        "path": "/becas-programs/api/search?page=1&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language": "es",
        "cache-control":"no-cache",
        "origin":"https://app.becas-santander.com",
        "pragma": "no-cache",
        "referer": "https://app.becas-santander.com/",
        "req_uuid":"eb7804b0-4e68-11ed-b8e2-89bbc632ed1b",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    JmesPath_Expressions = {
        'country_host':'ownerCountry',
        'name':'slug',
        'requirements':'requirements',
        'study_field':'',
        'study_level':'addressed',
        'exclusive':"exclusive",
        "requirements":"requirements"
        
    }

    StudyLevelsAllowed = ["postGraduates","students","graduates"]
    def EvalStudyLevel(self,study_levels):
        study_level =""
        for i in study_levels:
            if study_levels[i] and i in self.StudyLevelsAllowed:
                study_level += " "+i
        return study_level

    def ParseRequirements(self,requirements):

        RegexForHtlmTags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') # regex for delete html tags
        cleanRequirements = re.sub(RegexForHtlmTags,'',requirements)
        str_en = cleanRequirements.encode("ascii","replace") # replace unicode characters
        return str_en

    def DumpBecasToCsv(self,BecasList):
        with open("DT-Santander.csv","w") as stream:
            wr = csv.writer(stream)
            wr.writerows(BecasList) 
    
    def DataFromJsonResponse(self):
        cleanlist = list()
        for i in range(3):
            page = str(i+1)
            url = 'https://api-manager.universia.net/becas-programs/api/search?page='+page+'&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true'
            
            response = requests.get(url,headers=self.headers) # llamada al API de becas
            SantanderResponse = response.json() # Response en json
            becasList = SantanderResponse['data']['hits'] # la data que importa 

            """compilar expresiones regulares para aplicar sobre el json"""

            country = jmespath.compile(self.JmesPath_Expressions["country_host"]) 
            name = jmespath.compile(self.JmesPath_Expressions["name"])
            requirements = jmespath.compile(self.JmesPath_Expressions["requirements"])
            #exclusive = jmespath.compile(self.JmesPath_Expressions["exclusive"]) # Esta expresion determina la exclusividad de la beca
            study_level = jmespath.compile(self.JmesPath_Expressions["study_level"])
            
            for i in becasList:
                """ if exclusive.search(i):
                    continue"""
                study_levels = self.EvalStudyLevel(study_level.search(i))
                requisitos = self.ParseRequirements(requirements.search(i))
                if study_levels != "":
                    becaAux = beca(country.search(i),name.search(i),requisitos,study_levels)
                    cleanlist.append(becaAux)
        return cleanlist
    


call  = ApiCall()
SantaderBecas = call.DataFromJsonResponse()

csv = call.DumpBecasToCsv(SantaderBecas)

#out_file = open("SantanderResponse.json", "w") 
#json.dump(becasList,out_file,indent=6)
#out_file.close()




