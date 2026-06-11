#API - is an interface of the program . This is a kit of hidden rules and addresses and due to them one program
#can communicate with another one
#an example of first most important method:
from fastapi import FastAPI
app = FastAPI()
@app.get('/vibor') #this validator checks the link of our user , If our user goes to address /vibor than function will be launched
#user just gets data from us(from db)
async def check_shauha():
    return {"status":"working","meat":"chicken"}

#here is the code with pydantic validation
from pydantic import BaseModel
app = FastAPI()
class ShaurmaOrder(BaseModel):
    size: str
    with_garlic: bool
@app.post('/order') #post means that here in this link(window) user fetches his data
async def create_shauna(order: ShaurmaOrder):
    if order.with_garlic:
        outcome = f'We created {order.size} shaurma with garlic'
    else:
        outcome = f'We created {order.size} shaurma without garlic'
    return {'result':outcome}

#also some neuro models can take from 3 to 30 seconds , so we want of course more stable approach:
import asyncio
from fastapi import HTTPException , status
app = FastAPI()
@app.post('/generate_text') #we simply get data
async def generate_text(prompt: str,model_type: str):
    """validation must be the first step"""
    if model_type not in ["gpt-4","claude-3"]:
        #if model is invalid we interrupt commitment:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f'Model: {model_type} is not supported. Use gpt-4 or claude-3'
        )
    'here is imitation of work of complicated network:'
    try:
        await asyncio.sleep(5)
        return {
            "status": "success",
            "generated_text": f"This is an AI response for prompt: '{prompt}'"
        }
    except Exception as error: #here we retake some invalid models btw
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='AI model is currently overloaded. Please try again later'
        )
#path-parameters(dynamic URLs)
#let's just imagine that every user has its own private account and of course we don't want to create one window for each person
#instead of this we create a dynamic address where instead of putting {user_id} we can add any number
#dynamic means that every user will have his own address
app = FastAPI()
#imitation of the database
users_db = {
    1: {"name": "Alex" ,"role": "admin"},
    2: {"name": "Bro" , "role": "user"}
}
#{} - these parentheses mean the variable
@app.get('/users/{user_id}')
async def get_user_profile(user_id: int): #FastAPI on his own will turn URL string into int type(don't forget {} )!
    #here we try to find our user in database:
    if user_id not in users_db:
        raise HTTPException(status_code=404,detail='User not found')
    return users_db[user_id]

#futhermore there are QUERY-parameters / Let's just imagine that user goes to the page 'history of the generated AI prompts'
#there are maybe 1000 prompts over there and we should . We have to create a search according to the text and print , for example:
#ten prompts on each page / for that case we use QUERY-parameters(they are not written in the validator , they are written in the
#function and browser adds ? in request , so let's just check a layout:
app = FastAPI
app.get('/history')
async def get_ai_history(search: str = None , limit: int = 10):
    #THERE ARE NO THESE VARIABLES IN THE ADDRESS
    """
    search: text for searching(by default - None)
    limit: how much notes we have to return(by default - 10)
    """
    return {
        "message": "Filtering AI history",
        "search query": search,
        "records_limit": limit
    }
#so , to sum up:
#Path (/users/{user_id}) is used to point out the specific object(model) - specific user , specific picture AI , specific post
# - without such parameters address does not have any sense for a SPECIFIC user(and as we know 99% sites have some profiles -
#of again specific users like profile and so on
#QUery (/history?limit=10) is used to sort , to filter or change the display of list of objects - we can put default values btw

#SO , let's learn about dependencies
#let's just imagine that we have ten different windows(routes):
#generation of text , generation of pictures , generation of the text and in each of these windows we have to make the same default
#actions:
#1) to check either user is log in
#2) to open the session with database
#3) to check either user has limits on balance for AI generation
#instead of copying this code in each of these ten windows(routes) we write this main code once in main dependency-function
#and after this we just put this dependency function into desirable routes due to Depends()
#simple example with AI token access:
from fastapi import Depends
app = FastAPI()
def verify_ai_token(token: str = None):
    """This function checks an addressed token"""
    if token != "secret-bro-token-2026":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or missing AI Access Token'
        )
    return "authorized_user"
#here we turn on this dependency for all routes:
@app.post('/generate_text')
async def generate(prompt: str ,user_status: Depends(verify_ai_token)):
    """This route will work only if verify_ai_token does not give a mistake 401"""
    return {
        "result" : f"Generated text for prompt: '{prompt}'",
        "auth_info" : user_status #if there is no mistake we have got here authorized_user - just recheck
    }
@app.post('/generate_image')
async def generate_img(prompt: str,user_status: Depends(verify_ai_token)):
    #this route is also under the defense of this dependency function
    return {"result" : "Image generated successfully!"}

#yield is used instead of return / we need yield for things which require compulsory closing
def get_db_session():
    db = 'we open the session with database'
    try:
        yield db
    finally:
        print('We closed connection with database')

#here is an explanation
#1) user goes into a route
#2) FastAPI launches get_db_session and code goes to 'yield db'
#3) FastAPI gives this connection with db(session) to the route - after that route does commit() and makes changes in db
#4) as route finishes working and gave answer to the client FastAPI returns to function dependency and commits code after 'yield'
#5) after that session is closed automatically 

