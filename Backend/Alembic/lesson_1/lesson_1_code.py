from random import randint
addition = str(randint(1,100000))
raw_json = {
  "client_name": f"cleaner_mop{addition}",
  "client_email": "devradius@github.com",
  "ai_infrastructure": [
    {
      "bot_purpose": "Code_Reviewer",
      "ai_temperature": 0.2,
      "estimated_tokens_cost": 450
    },
    {
      "bot_purpose": "Bug_Hunter",
      "ai_temperature": 0.7,
      "estimated_tokens_cost": 1200
    },
    {
      "bot_purpose": "Filter",
      "ai_temperature": 1.5,
      "estimated_tokens_cost": 300
    }
  ]
}

from pydantic import Field , field_validator , BaseModel
from loguru import logger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship , Mapped , mapped_column , DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
import asyncio

class AllAI(BaseModel):
    bot_purpose: str = Field(min_length=4,max_length=20)
    ai_temperature: float = Field(ge = 0.0 , le = 2.0)
    estimated_tokens_cost: int = Field(gt = 0)
    @field_validator('bot_purpose')
    @classmethod
    def validate_bot_purpose(cls,purpose: str):
        import re
        if re.findall(r'(scam|spam)',purpose,flags=re.IGNORECASE):
            raise ValueError('Bot has dangerous or prohibited purpose!')
        return purpose

class MainCoverValidation(BaseModel):
    client_name: str = Field(min_length=3,max_length=20)
    client_email: str = Field(min_length=3,max_length=40)
    age: int = 18
    ai_infrastructure: list[AllAI]
    @field_validator('client_email')
    @classmethod
    def validate_user_email(cls,email: str):
        import re
        if not re.findall(r'[\w_]+@[\w_]+\.\w+',email,flags=re.IGNORECASE):
            raise ValueError('User email is wrong!')
        elif re.findall(r'[\w_]+@[\w_]?(spam|scam|lottery|raffle)[\w_]?\.\w+',email,flags=re.IGNORECASE):
            raise ValueError('User email has dangerous links!')
        return email

class SQLAlchemyBasement(DeclarativeBase):
    pass

class UsersTable(SQLAlchemyBasement):
    __tablename__ = 'All_users'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(unique=True)
    client_email: Mapped[str]
    age: Mapped[int | None] = mapped_column(default=18) #here I add a new attribute to the database
    ai_relation: Mapped[list['AIOptions']] = relationship(back_populates='user_relation')

class AIOptions(SQLAlchemyBasement):
    __tablename__ = 'All_ai_options'
    id: Mapped[int] = mapped_column(primary_key=True)
    bot_purpose: Mapped[str]
    ai_temperature: Mapped[float]
    estimated_tokens_cost: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('All_users.id',ondelete="CASCADE"))
    user_relation: Mapped['UsersTable'] = relationship(back_populates='ai_relation')

DATABASE_URL = "postgresql+asyncpg://postgres:0631@127.0.0.1:5432/user_ai_options"
engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(engine,expire_on_commit=False)
from sqlalchemy.orm import selectinload
from sqlalchemy import func , select
async def main_loading(initial_json:dict):
    validated_user_data = MainCoverValidation(**initial_json)
    db_user_data = UsersTable(client_name = validated_user_data.client_name,
                              client_email = validated_user_data.client_email
                                                                     )
    for ai_bot in validated_user_data.ai_infrastructure:
        db_bot_data = AIOptions(bot_purpose = ai_bot.bot_purpose,
                                ai_temperature = ai_bot.ai_temperature,
                                estimated_tokens_cost = ai_bot.estimated_tokens_cost
                                )
        db_user_data.ai_relation.append(db_bot_data)
    async with engine.begin() as render_structure:
        await render_structure.run_sync(SQLAlchemyBasement.metadata.create_all)
    async with session() as structure_data:
        structure_data.add_all([db_user_data])
        await structure_data.commit()
    request = (
        select(UsersTable)
        .options(selectinload(UsersTable.ai_relation))
    )
    result = await structure_data.execute(request)
    total_result = result.scalars().all()
    for user in total_result:
        for ai_bot in user.ai_relation:
            logger.info(f'Bot temperature {ai_bot.ai_temperature} | Bot name {ai_bot.bot_purpose}')
    avg_request = (select(
        UsersTable.client_name,
        func.count(AIOptions.id).label('AI_amount'),
        func.sum(AIOptions.estimated_tokens_cost).label('Total_cost')
    ).join(AIOptions).group_by(UsersTable.client_name))
    avg_result = await structure_data.execute(avg_request)
    for row in avg_result.all():
        logger.info(f'Amount of bots: {row.AI_amount} | Total tokens: {row.Total_cost}')
    await structure_data.close()
if __name__ == '__main__':
    try:
        asyncio.run(main_loading(raw_json))
        logger.success('Table was created successfully in database!')
    except Exception as error:
        print(f'Something is wrong! Error: {error}')
