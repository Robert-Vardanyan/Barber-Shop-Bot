from sqlalchemy import select, update,         delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Users
from datetime import datetime, timedelta

async def orm_add_user(session: AsyncSession, user_info: dict):
    user = Users(
        user_id = int(user_info['user_id']),
        name = user_info['name'],
        n_order = int(user_info['n_order']),
        phone = int(user_info['phone']),
        mail = user_info['mail'],
        verify = user_info['verify'],
        reg = datetime.now()

    )
    session.add(user)
    await session.commit()

async def orm_check_user(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_order(session: AsyncSession, user_id: int):
    query = update(Users).where(Users.user_id == user_id).values(
        n_order = Users.n_order + 1,
        last_order = datetime.now())
    await session.execute(query)
    await session.commit()

async def orm_delete_order(session: AsyncSession, user_id: int):
    query = update(Users).where(Users.user_id == user_id).values(
        n_order = Users.n_order - 1,
        last_order = datetime.now() - timedelta(days = 15))
    await session.execute(query)
    await session.commit()  

async def orm_check_order(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    delta = datetime.now() - result.scalar().last_order
    return delta.days


