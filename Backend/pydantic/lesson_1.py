from pydantic import BaseModel
class UserSchema(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool
#when class gets data(JSON for example) Pydantic automatically checks all crucial variables in class(does id or name exist?)-
#if it doesn't exist it will give an error / also checks types of data(which are given in class)

bad_data = {
   "id": "123",
   "name": "Alex",
   "age": "25",
   "is_active": "true"
}
user = UserSchema(**bad_data) #** - unpacks tuple into arguments of class
print(user.id) #prints out clean integer id like was given in the base model(in BaseModel)
print(user.is_active)

from typing import Optional
class NewUserSchema(BaseModel):
    id: int
    name: str
    is_active: bool = True #this is a field with a default value(user sometimes must not give all data - only a part of it)
    bio: Optional[str] = None
minimal_data = {"id": 1 , "name": "Ivan"}
user = NewUserSchema(**minimal_data)
print(user.is_active) #automatically True
print(user.bio)

#an example of creating another model:
class ItemSchema(BaseModel):
    title: str
    price: float
    count: int
    in_stock: bool = 'true'
dirty_json = {"price": "99.9","count": "5","title": "skibidi"}
user = ItemSchema(**dirty_json)
print(user.in_stock)
print(user.title)
print(type(user.count))
