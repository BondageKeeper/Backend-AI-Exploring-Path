#imaginary task for autoservice:
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column , relationship
from sqlalchemy.ext.asyncio import async_sessionmaker , AsyncSession , create_async_engine
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import ForeignKey
from loguru import logger

class Sample(DeclarativeBase):
    pass

class SpareParts(Sample):
    __tablename__ = 'SpareParts'
    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str]
    price: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey('Orders.id'))
    client_order: Mapped['Orders'] = relationship(back_populates='part_info')

class Orders(Sample):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str]
    client_email: Mapped[str]
    car_model: Mapped[str]
    status: Mapped[str] = mapped_column(default='In process')
    part_info: Mapped[list['SpareParts']] = relationship(back_populates='client_order')

class SparePartsValidation(BaseModel):
    part_name: str = Field(min_length=2)
    price: float = Field(ge=0.0)

class OrdersValidation(BaseModel):
    client_name: str = Field(min_length=3,max_length=30)
    client_email: str
    car_model: str = Field(min_length=3)
    parts: list[SparePartsValidation]
    logger.add('Unsafe_users.log', rotation='100 MB', retention=2, level='INFO')
    @field_validator('client_email',mode='after')
    @classmethod
    def email_validation(cls,email: str):
        import re
        if not re.findall(r'[\w\-_]+@[\w\-_]+\.\w+',email) or re.findall(r'(spam|lottery|raffle|bot)',email,flags=re.I):
            logger.error(f'invalid email: {email}')
            raise ValueError('Email is invalid!')
        return email

from fastapi import FastAPI , HTTPException , Depends , status
app = FastAPI()
DATABASE_URL = 'postgresql+asyncpg://postgres:[WRITE HERE YOUR PASSWORD]@127.0.0.1:5432/custom_orders_total'
engine = create_async_engine(DATABASE_URL)
engine_session = async_sessionmaker(engine,expire_on_commit=False)

async def open_db():
    async with engine_session() as session:
        yield session

@app.post('/api/orders')
async def api_orders(orders: OrdersValidation,session: AsyncSession = Depends(open_db)):
    for part in orders.parts:
        import re
        if re.findall(r'nitro',part.part_name,flags=re.IGNORECASE):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Illegal modification: Nitro is not allowed!')

    validated_orders = Orders(client_name=orders.client_name,
                              client_email=orders.client_email,
                              car_model=orders.car_model,
                              )
    for part in orders.parts:
        validated_parts = SpareParts(part_name=part.part_name,
                                     price=part.price
                                     )
        validated_orders.part_info.append(validated_parts)
    session.add_all([validated_orders])
    await session.commit()
    await session.refresh(validated_orders)

    return {
        "status" : 201,
        "your id" : validated_orders.id,
        "customer" : validated_orders.client_name
    }

@app.get('/api/orders/{orders_id}')
async def present_order_info(orders_id: int,session: AsyncSession = Depends(open_db)):
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    request = select(Orders).where(Orders.id==orders_id).options(selectinload(Orders.part_info))
    result = await session.execute(request)                         
    order = result.scalar_one_or_none()                            
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User didn't simply take a call to the service")
    return {
        "status" : "In Queue or almost finished",
        "order_id" : order.id,
        "customer" : order.client_name,
        "car" : order.car_model,
        "parts": [{"part_name" : part.part_name ,"price" : part.price } for part in order.part_info]
    }

@app.patch('/api/orders/{orders_id}/status')
async def change_status(orders_id: int ,session: AsyncSession = Depends(open_db)):
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    request = select(Orders).where(Orders.id == orders_id).options(selectinload(Orders.part_info))
    result = await session.execute(request)
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User didn't simply take a call to the service")
    outcomes = ['Ready','In process']
    chance = [50,50]
    import random
    item = random.choices(outcomes,chance,k=1)
    return {
        "status": item, #here there is just an imitation of real work
        "order_id": order.id,
        "customer": order.client_name,
        "car": order.car_model,
        "parts": [{"part_name": part.part_name, "price": part.price} for part in order.part_info]
    }

async def test_out_models():
    try:
        async with engine.begin() as structure_data:
            await structure_data.run_sync(Sample.metadata.create_all)
        logger.info('everything is good')
    except Exception as error:
        print('ERROR')

@app.on_event("startup")
async def start_server_task():
    await test_out_models()

