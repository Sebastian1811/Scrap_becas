from  dotenv import load_dotenv
import os

load_dotenv()

BECAS_URL_SOURCE = []
url = 'BECAS_URL'
for i in range(2):
    url+=str(i+1)
    BECAS_URL_SOURCE.append(os.environ[url])
    url= 'BECAS_URL'