#By default Pydantic class is not able to read data from other classes - pydantic gives mistake
#from_attributes=True from ConfigDict allows to read data from attributes of OTHER CLASSES
class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
class DBUser:
    def __init__(self,username,email):
        self.username = username
        self.email = email
db_user = DBUser(username='developer',email='dev@test.com')
validated_user = UserResponseSchema.model_validate(db_user)
print(validated_user.username) #so we can make it - just get value from other class literally

#sometimes we don't know what fields will come in handy , for example user on his own creates form of callback network
#and points out what fields an instance has , we can write Schema-class - because we simply don't know a structure yet
#it is created during work of the program
#function 'create_model' allows us to generate fully-fledged classes Pydantic 'instantly'
#an example:
from pydantic import create_model
DynamicModel = create_model(
    'DynamicAIModel',
    model_name = (str,...), #so-called compulsory field
    max_tokens = (int,100) #optional field
)
#now DynamicModel is a fully-fledged class Pydantic , now we create an object
instance = DynamicModel(model_name="gpt-4o")
print(instance.max_tokens)
print(instance.model_dump())
#sometimes we need to copy field and change only some values(we want to update profile or something like that)
#so to prevent creating new object we just use method .model_copy() which makes exact same copy of object and allows us to make
#new fields which we point out in our dict of uploading
class AISettings(BaseModel):
    model: str
    temperature: float
    stream: bool
current_settings = AISettings(model='llama-3',temperature=0.7,stream=False)
incoming_update = {"temperature":0.3}
new_settings = current_settings.model_copy(update=incoming_update) #copy and what we update(update value is in the dict)
print(new_settings.model_dump())

#TASK_1:
class LegacyConfig:
    def __init__(self,api_provider,system_prompt):
        self.api_provider = api_provider
        self.system_prompt = system_prompt

class AIConfigSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_provider: str
    system_prompt: str

source_instance = LegacyConfig(api_provider = "openai",system_prompt = "You are a helpful assistant")
validated_step = AIConfigSchema.model_validate(source_instance)
update_itself = {"system_prompt":"You are a senior python developer"}
new_prompt = validated_step.model_copy(update=update_itself)
print('*' * 100)
print(new_prompt.model_dump_json())
