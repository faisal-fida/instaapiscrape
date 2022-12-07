from fastapi import FastAPI
from bot import get_userDetail as getUser

app = FastAPI()

@app.get('/{username}')
async def root(username):
    if '@' in username:
        username = username.replace('@','')
    dataF = await getUser(str(username))
    return dataF