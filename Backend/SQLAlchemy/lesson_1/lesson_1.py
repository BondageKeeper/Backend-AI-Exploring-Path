#The most important thing of ORM(Object-Relational Mapping) - it translates python code into SQL-requests
#without ORM out code can be too diverse , thanks to ORM code will consist of mainly python code
#also in ORM there is a validation which can check types of data of specific variables
#in SQL to tie up tables we used JOIN - it is uncomfortable in ORM everything becomes simple
#it will look something like user.orders(and ORM will automatically understand what things must be tied up)
#ORM also presents security preventing SQL-injections
#tables in SQLAlchemy resemble classes in python due to class DeclarativeBase
#from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column
#class Base(DeclarativeBase): #main parent class for creating migrations
#    pass
##here we create our first table
##Mapped[] - tells python what type of data column will have
##mapped_column() - creates settings for column
#class User(Base):
#    __tablename__ = 'users202'
#    id: Mapped[int] = mapped_column(primary_key=True)
#    username: Mapped[str] = mapped_column(unique=True)
#    ai_tokens_spent: Mapped[int] = mapped_column(default=0)
#
#
#from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
##create_async_engine - a point of connection with database , due to echo we will see clean SQL code in console
##async_sessionmaker - this is a fabric which generates sessions(session - specific connection) to carry out operations
##expire_on_commit=False - doesn't allow to kill objects after saving in database
#DATABASE_URL = "postgresql+asyncpg://postgres:0631@127.0.0.1:5432/users202"
#engine = create_async_engine(DATABASE_URL,echo=True)
#async_session = async_sessionmaker(engine,expire_on_commit=False)
#
##and so if we want to add object in database here is a brief plan what to do:
##1) first of all we create asyncio function
##2) than we open session(to create specific connection)
##3) after that we create class object and at the end commit()
#
#async def create_user(username: str):
#    async with async_session() as session: #async_session() - will automatically close session after accomplishing code
#        new_user = User(username=username,ai_tokens_spent=150)
#        session.add(new_user) #here we add our class in session to send
#        await session.commit() #only at this moment data physically goes to PostgreSQL
##here all these methods combined , eventually creating database:
#
#class Fundamentals(DeclarativeBase):
#    pass
#import asyncio
#class AIModel(Fundamentals):
#    __tablename__ = "ai_models"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    name: Mapped[str] = mapped_column(unique=True)
#    is_active: Mapped[bool] = mapped_column(default=True)
#
#async def main(): #main function for launching
#    async with engine.begin() as conn:
#        await conn.run_sync(Fundamentals.metadata.create_all) #metadata stores structure of all tables
#    print('Tables were created successfully')
#    async with async_session() as session:
#        model1 = AIModel(name='GPT-4')
#        model2 = AIModel(name='LLama-3')
#        model3 = AIModel(name='DeepSeek-R1',is_active=False)
#        session.add_all([model1,model2,model3]) #here we add this pack in session
#        await session.commit()
#if __name__ == '__main__':
#    asyncio.run(main())
#
###Let's try to create another database:
from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
import asyncio
from faker import Faker
fake = Faker('en_US')
from loguru import logger
DATABASE_NEW_URL = 'postgresql+asyncpg://postgres:0631@127.0.0.1:5432/prompts308'
engine = create_async_engine(DATABASE_NEW_URL,echo=True)
async_session = async_sessionmaker(engine,expire_on_commit=False)#expire_on_commit=False - leaves python data available after commit
class ParentClass(DeclarativeBase):
    pass
class AIRequest(ParentClass):
    __tablename__ = 'ai_requests'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    prompt: Mapped[str]
    response: Mapped[str]
    tokens_used: Mapped[int] = mapped_column(default=0)
    is_success: Mapped[bool] = mapped_column(default=True)
async def main_function():
    async with engine.begin() as conn:
        await conn.run_sync(ParentClass.metadata.create_all)
    logger.info('Connection was settled!')
    async with async_session() as session:
        launch1 = AIRequest(user_id = fake.random_int(min=1,max=999),
                            prompt = fake.sentence(nb_words=10),
                            response = fake.sentence(nb_words=5),
                            tokens_used = 150
                            )
        launch2 = AIRequest(user_id = fake.random_int(min=1,max=999),
                            prompt=fake.sentence(nb_words=10),
                            response=fake.sentence(nb_words=5),
                            is_success = False
        )
        session.add_all([launch1,launch2])
        await session.commit()
if __name__ == '__main__':
    asyncio.run(main_function())


#also we know that in SQL there are INSERT , SELECT , UPDATE and so on so in SQLAlchemy there are methods like:
#select() , where() - where serves as a filter
#this is just a layout:
from sqlalchemy import select
async def get_successful_requests():
    async with async_session as session:
        query = select(AIRequest).where(AIRequest.is_success == True)
        #result = await session.execute(query)
#usually session.execute(query) returns data as tuple - uncomfortable / so if we want to turn them into neat list of python models
#we use method .scalars()
        result = await session.execute(query)
        requests_result_list = result.scalars().all()
        #if we need only one data we instead of all() we will use .first() or .one_or_none()
        for request in requests_result_list:
            print(f'Prompt of user: {result.prompt} -> Answer: {result.response}')

#layout of UPDATE:
async def update_tokens(request_id: int , real_tokens: int):
    async with async_session as session:
        query = select(AIRequest).where(AIRequest.id == request_id)
        result = await session.execute(query)
        db_request = result.scalar_one_or_none() #finds one object
        if db_request:
            #we simply change value in the memory of python
            db_request.tokens_used = real_tokens
            db_request.is_success = True
            await session.commit()


#TASK_1:
async def analyze_failed_requests():
    async with async_session as session:
        query = select(AIRequest).where(AIRequest.is_success == True)
        result = await session.execute(query)
        result_list = result.scalars().all()
        if result_list:
            for req in result_list:
                logger.warning(f"Request completed {req.prompt}")

async def charge_tokens_for_success(update_id:int):
    async with async_session as session:
        query = select(AIRequest).where(AIRequest.is_success == True,AIRequest.user_id == update_id)
        result = await session.execute(query)
        outcome_request = result.scalar_one_or_none()
        if outcome_request:
            outcome_request.tokens_used += 500
            await session.commit()
            logger.success('All tokens were printed out')

