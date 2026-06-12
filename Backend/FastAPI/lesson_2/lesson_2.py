#also , there is method 'put' - let's just imagine that our user wants to change initial settings say change description or name or other
#things of his profile
#in that case we use validator 'put'
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field
app = FastAPI()
users_config = {
    1: {"model": "gpt-4", "temperature": 0.7}
}
#Pydantic validated class:
class UpdateConfig(BaseModel):
    model: str
    temperature: float = Field(ge=0.0, le=1.0)

@app.put('/config/{user_id}')
async def update_user_config(user_id: int,new_data: UpdateConfig):
    if user_id not in users_config:
        raise HTTPException(status_code=404, detail="User config not found")
    users_config[user_id] = {
        "model" : new_data.model,
        "temperature" : new_data.temperature
    }
    return {"status" : "updated", "new_config" : users_config[user_id]}


#and if user wants to delete log or just other things of course there is validator delete
from fastapi import FastAPI , HTTPException , status
app = FastAPI()
ai_prompts_db = {
    105: "Draw a space cat",
    106: "Write a python script"
}
@app.delete('/prompts/{prompt_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(prompt_id: int):
    if prompt_id not in ai_prompts_db:
        raise HTTPException(status_code=404,detail='Prompt is not found')
    del ai_prompts_db[prompt_id]
    return None

#method PATCH is used to rewrite the object:
#if we don't send some field in put - it will have default value(or might be lost)
#Patch is used when we want to update one specific field and get when we want to update an entire object
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import Optional
app = FastAPI()
ai_logs = {
    1: {"user_id": 10, "prompt": "Old Prompt", "status": "done"}
}
#we don't need all fields here
class PatchLog(BaseModel):
    user_id: Optional[int] = None
    prompt: Optional[str] = None
@app.patch("/api/logs/{log_id}")
async def partial_update_log(log_id: int , incoming_data: PatchLog):
    if log_id not in ai_logs:
        raise HTTPException(status_code=404, detail="Log not found")
    #and here we get field which were sent BY USER - we won't get rubbish default fields
    update_fields = incoming_data.model_dump(exclude_unset=True)

    ai_logs[log_id].update(update_fields)
    return {"status": "partially_updated", "result": ai_logs[log_id]}
#if user sends {"prompt": "New Prompt"} (in case we have validator PATCH) - id will be just skipped and not damaged at all

#HEAD is a request of metadata
from fastapi import FastAPI, Response, HTTPException
app = FastAPI()
@app.head("/api/ai-models/heavy-weights")
async def check_weights_exist(response: Response):
    file_exists = True  #imitation of file checking
    if not file_exists:
        raise HTTPException(status_code=404)
    #we add information in headers
    response.headers["Content-Length"] = "524288000"  # 500 MB
    response.headers["X-Model-Status"] = "Ready"
    return Response()

from fastapi import FastAPI, Response
app = FastAPI()
@app.options("/api/predict") #what methods are allowed to use
async def get_predict_options(response: Response):
    #we tell frontend what methods work here and what data we wait for
    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return {"message": "Preflight CORS check safe"}

