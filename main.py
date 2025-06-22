from fastapi import FastAPI
from controllers import  users 
from controllers.accounts import router as AccountsRouter  
from controllers.users import router as UsersRouter 


app = FastAPI()

#app.include_router(users.router)
app.include_router(AccountsRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")

@app.get("/")
def home():
    return {"Welcome to Zaianb Bank :)"}