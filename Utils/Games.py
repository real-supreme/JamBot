import aiohttp, requests, json
from config import base_api_link, base_trivia

class Games:
    def __init__(self, base_api_link=base_api_link(), trivia=base_trivia()):
        self.base_link = base_api_link if base_api_link.startswith("http") else "https://" + base_api_link 
        self.triv_url = trivia if trivia.startswith("http") else "https://" + trivia
    
    async def __process_question(self, resp):
        x = await resp.text()
        data = x[x.find("\"type\":"):]
        return json.loads("{"+data)['question']
    
    async def get_truth(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_link+"/v1/truth") as resp:
                return await self.__process_question(resp)
    
    
    async def get_dare(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_link+"/api/truth") as resp:
                return await self.__process_question(resp)
            
    async def get_wyr(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_link+"/api/wyr") as resp:
                return await self.__process_question(resp)
            
    async def get_nhie(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_link+"/api/nhie") as resp:
                return await self.__process_question(resp)
            
    async def get_paranoia(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_link+"/api/paranoia") as resp:
                return await self.__process_question(resp)
    
    async def get_trivia(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.triv_url) as resp:
                data = await resp.json()
                print(data)
                if data["response_code"] == 0:
                     return data["results"][0]
    
if __name__=='__main__':
    ...