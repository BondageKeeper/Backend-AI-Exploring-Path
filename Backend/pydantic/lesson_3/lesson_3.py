#LESSON_3
#usually flat and neat dicts appear rarely , usually we just get more complicated dicts which can contain for eexample
#other dicts(like one subject in main dict can have many keys and values in one dict and this dict is a value itself
#so we can create ANOTHER mini object(class) for these so-called additional embedded dicts
#an example:

class WeaponSchema(BaseModel):
    name: str
    damage: int

class CharacterSchema(BaseModel):
    nickname: str
    level: int
    current_weapon: WeaponSchema #we use daughter model as a type of data for the field
    inventory: list[WeaponSchema] #and so , all values will be transmitted in so called another class(it is like DOUBLE-OPENING)

character_data = { #here there is more complicated dict
    "nickname": "Gamer777",
    "level": 80,
    "current_weapon": {"name": "Frost Sword", "damage": 50,},
    "inventory": [ #NOTICE! THERE IS a list here that is why we write another type 'list' nearby inventory
        {"name": "Health Potion", "damage": 0},
        {"name": "Fire Bow", "damage": 45}
    ]
}
hero = CharacterSchema.model_validate(character_data) #we instantly validate this model (we just don't use **)
print(hero.current_weapon.name) #so-called DOUBLE-REFERENCE

#before that we created classes and used methods and so on , but what if we want to put new Pydantic arguments into simple
#Pydantic function? - I mean we want them to be checked like in Pydantic using simple function
#in that case we use decorator @validate_call
from pydantic import validate_call
@validate_call
def send_ai_report(user_email: EmailStr , retry_count: int):
    print(f'We sent your a report on {user_email}, try number {retry_count}')
try:
    send_ai_report("noemail.com",5) #it will be working like in simple pydantic method(class sometimes not needed)
except Exception as error:
    print('defense was turned on')

#also let's just imagine that we have to send back json to our user and there is some secret token(or just secret key
#that shouldn't be sent openly to the user browser - in that case instead of using model_validate()
#we use so-called model_dump(include=?,exclude=?) where we exclude some keys using flags of this method
#Notice! model_dump is basically the same as model_validate() but with useful flags
class AIServiceSession(BaseModel):
    session_id: int
    prompt: str
    secret_token: str #must be hidden from user(just imagine)
session = AIServiceSession(session_id=1, prompt="Hello AI", secret_token="xyz123secret")
public_data = session.model_dump(exclude={"secret_token"})
print(public_data)

#Task_1
raw_json_list = [
    {
        "user_id": "777",
        "model_name": "gpt-4o",
        "usage": {
            "prompt_tokens": "150",
            "completion_tokens": "45"
        },
        "internal_server_time": "2026-05-29"
    },
    {
        "user_id": 888,
        "model_name": "llama-3",
        "usage": {
            "prompt_tokens": 300,
            "completion_tokens": "120"
        }
    }
]

class TokenUsageSchema(BaseModel):
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)

class AIQueryLogSchema(BaseModel):
    user_id: int
    model_name: str
    usage: TokenUsageSchema
    internal_server_time: str = "2026-05-29"

@validate_call
def process_log_entry(log: AIQueryLogSchema): #here we give a validated class
    outcome_data = log.model_dump(exclude={"internal_server_time"})
    print(f'Successful clean: {outcome_data}')
for raw_item in raw_json_list: #here we iterate our dicts
    try:
        #validated_log = AIQueryLogSchema.model_validate(raw_item)
        process_log_entry(raw_item)
    except Exception as error:
        print(f'Error happened: {error}')

#for example in the model of AI or in the database we have got complicated object(for example datetime or path to the image)
#but if we want to send it back t our client we must convert all these types into string(JSON)
#@field_serializer is used for changing format(instead of ISO-string we can get simple string from datetime object)
#it is just a tool for changing standard format on our desirable format , an example with datetime in the exact same moment
#as we convert model into dict JSON , here is an example for more clarity:
from pydantic import field_serializer
from datetime import datetime
class AIEventSchema(BaseModel):
    event_name: str
    created_at: datetime #store like a datetime object(it would default value ISO-string)
    @field_serializer("created_at") #here we simply say what key default format will be turned into our desirable format
    def serialize_data(self,dt:datetime): #YEAH , now we can change our format and make our own string(instead of ISO-string)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
event = AIEventSchema(event_name="Model_Trained",created_at=datetime.now())
print(event.model_dump())

#in classes we usually can change values of fields of pydantic but in backend some logs mustn't be changed
#so in that case we put flag frozen = True right in our instance(scheme or so-called class) - or in the ConfigDict(new version I guess)
class ImmutableConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    api_url: str
    timeout: int
config = ImmutableConfig(api_url='https://openai.com',timeout=30)
try:
    config.timeout = 60 #we cannot change the field otherwise our instance will be angry:(
except Exception as error:
    print(f'Instance is frozen , error: {error}')

#and of course sometimes we don't need even to change something we just need to calculate some data according to the values of fields
#in that case we use validator @computed_field
#for example:
from pydantic import computed_field
class TokenPriceCalculator(BaseModel):
    model_name: str
    tokens_used: int
    price_per_token: float
    @computed_field(return_type=float) #it is useful to create new fields that are literally computed on other fields
    @property     #function to be used for getting an attribute value(to create new field_
    def total_cost(self):
        return self.tokens_used * self.price_per_token
calc = TokenPriceCalculator(model_name="gpt-4o",tokens_used=1500,price_per_token=0.002)
print(calc.model_dump())

#TASK_2:
print('*' * 100)
class AICostCalculator(BaseModel):
    model_config = ConfigDict(frozen=True)
    model_name: str
    hours_trained: int
    price_per_hour: float
    @computed_field(return_type=float)
    @property
    def total_cost(self):
        return self.hours_trained * self.price_per_hour
    @field_serializer("total_cost")
    def rounding(self,value:float): #value store a value of field "total_cost"
        return round(value,1)
try:
    call = AICostCalculator(model_name="llama-3-70b", hours_trained=12, price_per_hour=2.777)
    #call.model_name = 'broken'
    print(call.model_dump()) #Generates a dictionary representation of the model
except Exception as error:
    print('*' * 100)
    print(f'Here is the error: {error}')

#TASK_3(BOSS):
raw_incoming_logs = [
    {
        "meta": {
            "request_id": "1001",
            "client_email": "hackerman@cyber.io",
            "api_version": "v2.5"
        },
        "task_details": {
            "pipeline_type": "video_generation",
            "raw_prompt": "   An astronaut riding a horse on Mars, cinematic, 4k   ",
            "frames_count": "120"
        },
        "billing": {
            "is_premium": "true",
            "gpu_seconds": "45.55"
        }
    },
    {
        "meta": {
            "request_id": 1002,
            "client_email": "bademail@tall.com",
            "api_version": "v2.5"
        },
        "task_details": {
            "pipeline_type": "text_generation",
            "raw_prompt": "Write a short poem about coding",
            "frames_count": 0
        },
        "billing": {
            "is_premium": "false",
            "gpu_seconds": "10.0"
        }
    }
]
class MetaManager(BaseModel):
    model_config = ConfigDict(extra='forbid',frozen=True)
    request_id: int = Field(ge=0)
    client_email: EmailStr
    api_version: str

class TaskManager(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    pipeline_type: str = "text_generation"
    raw_prompt: str = Field(min_length=2,max_length=4000)
    frames_count: int = Field(ge=0)
    @field_serializer("raw_prompt")
    def delete_space(self, value: str):
        return value.strip().title()
    @field_validator("pipeline_type")
    @classmethod
    def check_frames(cls, value: str):
        import re
        if not re.search(r'^(text_generation|video_generation)', value):
            raise ValueError('Warning! User chose not existing format')
        return value

class BillingManager(BaseModel):
    is_premium: bool = False
    gpu_seconds: float = Field(ge=0)

class LogsManager(BaseModel):
    meta: MetaManager
    task_details: TaskManager
    billing: BillingManager
    @computed_field(return_type=float)
    @property
    def total_usd_cost(self):
        return self.billing.gpu_seconds * 0.005
    @field_serializer("total_usd_cost")
    def rounding(self,value:float):
        return f'{round(value,2)} USD'
@validate_call
def dump_data(log: LogsManager):
    final_data = log.model_dump(exclude={'meta':{"api_version"}})
    print(f'*** {final_data} ***')
for log in raw_incoming_logs:
    try:
        validated_log = LogsManager.model_validate(log)
        dump_data(validated_log)
    except Exception as error:
        print(f'Error happened: {error}')

