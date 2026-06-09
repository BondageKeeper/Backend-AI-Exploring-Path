from random import randint
trailer = str(randint(1,1000000000))

json_data = {
  "operator_username": f"cyber_architect_2026_{trailer}",
  "operator_corporate_email": "architect.dev@cloud-core.corp",
  "infrastructure_nodes": [
    {
      "agent_alias": "llm-router-prod",
      "network_protocol": "gRPC",
      "is_active": 'true',
      "connection_details": {
        "endpoint_url": "https://cloud-core.corp",
        "proxy_address": "socks5://192.168.1.55:1080",
        "allocated_memory_gb": 32,
        "monthly_budget_usd": 1500.50
      }
    },
    {
      "agent_alias": "analyzer-node",
      "network_protocol": "Websocket",
      "is_active": 'false',
      "connection_details": {
        "endpoint_url": "wss://socket.cloud-core.corp:443/v1/live",
        "proxy_address": "http://10.0.0.12:9050",
        "allocated_memory_gb": 16,
        "monthly_budget_usd": 450.00
      }
    },
    {
      "agent_alias": "data-cleansing-agent",
      "network_protocol": "HTTP/2",
      "is_active": 'true',
      "connection_details": {
        "endpoint_url": "https://cloud-core.corp",
        "proxy_address": "socks5://10.0.0.12:9050",
        "allocated_memory_gb": 64,
        "monthly_budget_usd": 2800.00
      }
    }
  ]
}

from sqlalchemy.orm import DeclarativeBase , relationship , Mapped , mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine
from sqlalchemy import ForeignKey
import asyncio
from loguru import logger
from pydantic import BaseModel , Field , field_validator

'''Pydantic classes:'''

class ConnectionDetails(BaseModel):
    endpoint_url: str = Field(min_length=3,max_length=50)
    proxy_address: str = Field(min_length=3,max_length=50)
    allocated_memory_gb: int = Field(ge=0)
    monthly_budget_usd: float = Field(ge=0.0)
    @field_validator('endpoint_url')
    @classmethod
    def url_validation(cls, url: str):
        import re
        url = url.strip(' ')
        if not re.findall(r'^(https|wss)://[\w_.:/-]+$', url):
            raise ValueError('Url is invalid!')
        return url
    @field_validator('proxy_address')
    @classmethod
    def proxy_address_validation(cls, proxy_address: str):
        import re
        if not re.findall(r'[\w_]+://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{4}',proxy_address,flags=re.IGNORECASE):
            raise ValueError('proxy_address is invalid!')
        return proxy_address

class InfrastructureNodes(BaseModel):
    agent_alias: str = Field(min_length=3,max_length=50)
    network_protocol: str = Field(min_length=3,max_length=10)
    is_active: str
    connection_details: ConnectionDetails
    @field_validator('agent_alias')
    @classmethod
    def agent_alias_validation(cls,agent_alias: str):
        import re
        if re.findall(r'(scam|spam|harm|lottery|raffle|violance|advertisement|threat)',agent_alias,flags=re.IGNORECASE):
            raise ValueError('agent_alias might be harmful for platform!')
        return agent_alias

class OperatorDetails(BaseModel):
    operator_username: str = Field(min_length=3,max_length=50)
    operator_corporate_email: str
    infrastructure_nodes: list[InfrastructureNodes]
    @field_validator('operator_corporate_email')
    @classmethod
    def email_validation(cls,email: str):
        import re
        if not re.findall(r'[\w._-]+@[\w_-]+\.[corp|net]',email):
            raise ValueError('email is invalid!')
        elif len(email.strip(' ')) == 0:
            raise ValueError('email is empty!')
        return email

"""SQLAlchemy classes:"""

class SQLAlchemyMetadata(DeclarativeBase):
    pass

class OperatorTable(SQLAlchemyMetadata):
    __tablename__ = 'operator_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    operator_username: Mapped[str] = mapped_column(unique=True)
    operator_corporate_email: Mapped[str]
    agent_info: Mapped[list['AgentTable']] = relationship(back_populates='operator_info')
    ai_config_info: Mapped[list['AIConfigConnection']] = relationship(back_populates='operator_info')

class AgentTable(SQLAlchemyMetadata):
    __tablename__ = 'agent_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    agent_alias: Mapped[str]
    network_protocol: Mapped[str]
    is_active: Mapped[str]
    server_location: Mapped[str | None] = mapped_column(default='UNDEFINED') #added for alembic usage! Be careful
    operator_id: Mapped[int] = mapped_column(ForeignKey('operator_table.id',ondelete='CASCADE'))
    operator_info: Mapped['OperatorTable'] = relationship(back_populates='agent_info')

class AIConfigConnection(SQLAlchemyMetadata):
    __tablename__ = 'aiconfig_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_url: Mapped[str]
    proxy_address: Mapped[str]
    allocated_memory_gb: Mapped[int]
    monthly_budget_usd: Mapped[float]
    operator_id: Mapped[int] = mapped_column(ForeignKey('operator_table.id', ondelete='CASCADE'))
    operator_info: Mapped['OperatorTable'] = relationship(back_populates='ai_config_info')

DATABASE_URL = "postgresql+asyncpg://postgres:[WRITE HERE YOUR PASSWORD]@127.0.0.1:5432/operator_monitoring"
engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(engine,expire_on_commit=False)
from sqlalchemy.orm import selectinload
from sqlalchemy import func , select
async def main_rendering(full_json: dict):
    entire_validated_data = OperatorDetails(**full_json)
    operator_data = OperatorTable(operator_username=entire_validated_data.operator_username,
                                  operator_corporate_email=entire_validated_data.operator_corporate_email
                                  )
    for agent in entire_validated_data.infrastructure_nodes:
        agent_data = AgentTable(agent_alias=agent.agent_alias,
                                network_protocol=agent.network_protocol,
                                is_active=agent.is_active
                                )
        operator_data.agent_info.append(agent_data)
        ai_config_data = AIConfigConnection(endpoint_url=agent.connection_details.endpoint_url,
                                            proxy_address=agent.connection_details.proxy_address,
                                            allocated_memory_gb=agent.connection_details.allocated_memory_gb,
                                            monthly_budget_usd=agent.connection_details.monthly_budget_usd
                                            )
        operator_data.ai_config_info.append(ai_config_data)
    async with engine.begin() as render_structure:
        await render_structure.run_sync(SQLAlchemyMetadata.metadata.create_all)
    async with session() as data_filler:
        data_filler.add_all([operator_data])
        await data_filler.commit()
    request = (select(OperatorTable)
    .options(selectinload(OperatorTable.agent_info),selectinload(OperatorTable.ai_config_info))
    )
    result = await data_filler.execute(request)
    final_results = result.scalars().all()
    logger.add('operator_configs.log', rotation='1 GB', retention='3 days', level='INFO')
    for operator in final_results:
        logger.info(f'name of operator: {operator.operator_username}')
        for bot , config in zip(operator.agent_info,operator.ai_config_info):
            logger.info(
            f'Bot: {bot.agent_alias} | Protocol:({bot.network_protocol}) |'
            f'Proxy: {config.proxy_address} |'
            f'Memory: {config.allocated_memory_gb}GB |'
            f'Budget: {config.monthly_budget_usd}$'
            )
    agg_request = (select(
    OperatorTable.operator_username,
    func.count(AgentTable.id).label('all_agents'),
    func.sum(AIConfigConnection.allocated_memory_gb).label('all_memory'),
    func.sum(AIConfigConnection.monthly_budget_usd)
    .label('all_budget')).join(AgentTable).join(AIConfigConnection).group_by(OperatorTable.operator_username))
    final_agg_result = await data_filler.execute(agg_request)
    for row in final_agg_result.all():
        logger.info(f'Agents: {row.all_agents} | Total memory: {row.all_memory} | Full budget: {row.all_budget}')
    await data_filler.commit()
    await data_filler.close()
if __name__ == '__main__':
    try:
        asyncio.run(main_rendering(json_data))
        logger.success('Tables were created successfully!')
    except Exception as error:
        print(f'It seems we have got a problem! | Error: {error}')



