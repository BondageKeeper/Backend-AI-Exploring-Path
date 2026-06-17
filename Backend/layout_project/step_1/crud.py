from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import relationship , Mapped , mapped_column , DeclarativeBase
from datetime import datetime
from PC_Bang.app.validation import UserInfo

class AlchemyLaunch(DeclarativeBase):
    pass

class BookingInfoDB(AlchemyLaunch):
    __tablename__ = 'booking_info'
    id: Mapped[int] = mapped_column(primary_key=True)
    computer_model: Mapped[str]
    gaming_hours: Mapped[int]
    additional_services: Mapped[bool]
    arrival_time: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey('users_info_registration.user_id',ondelete='CASCADE'))
    knot_user: Mapped['UserInfoDB'] = relationship(back_populates='knot_booking',)

class UserInfoDB(AlchemyLaunch):
    __tablename__ = 'users_info_registration'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    phone_number: Mapped[str]
    register_time: Mapped[str] = mapped_column(default=datetime.now)
    knot_booking: [Mapped[list['BookingInfoDB']]] = relationship(back_populates='knot_user')

DATABASE_URL = 'postgresql+asyncpg://postgres:[WRITE HERE YOUR PASSWORD]@127.0.0.1:5432/PC_customers'
engine = create_async_engine(DATABASE_URL,echo=True)
engine_session = async_sessionmaker(engine,expire_on_commit=False)

async def keep_open_db():
    async with engine_session() as session:
        yield session

from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_order_info(order_id: int,session:AsyncSession):
    request = select(BookingInfoDB).where(BookingInfoDB.id == order_id).options(selectinload(BookingInfoDB.knot_user))
    result = await session.execute(request)
    order = result.scalar_one_or_none()
    return {
        "status" : "success",
        "nickname" : BookingInfoDB.knot_user.nickname,
        "order_id" : order.id,
        "computer_model" : order.computer_model,
        "gaming_hours" : order.gaming_hours,
        "additional_services" : order.additional_services,
        "arrival_time" : order.arrival_time
    }

async def create_order_info(order_data: UserInfo,session: AsyncSession):
    validated_user_info = UserInfoDB(nickname=order_data.nickname,
                                     email=order_data.email,
                                     phone_number=order_data.phone_number,
                                     register_time=order_data.register_time,
                                     )
    for order in order_data.knot_booking:
        validated_order_booking = BookingInfoDB(computer_model = order.computer_model,
                          gaming_hours = order.gaming_hours,
                          additional_services = order.additional_services,
                          arrival_time = order.arrival_time
                          )
        validated_user_info.knot_booking.append(validated_order_booking)
    session.add_all([validated_user_info])
    await session.commit()
    await session.refresh(validated_user_info)
    return {
        "status" : 201,
        "personal_id" : validated_user_info.user_id,
        "order_id" : validated_user_info.knot_booking.id
    }

async def delete_order_info(order_id: int,session: AsyncSession):
    request = select(BookingInfoDB).where(BookingInfoDB.id == order_id).options(selectinload(BookingInfoDB.knot_user))
    result = await session.execute(request)
    deleted_order = result.scalar_one_or_none()
    if deleted_order is None:
        return False
    else:
        await session.delete(deleted_order)
        await session.commit()
        return True
