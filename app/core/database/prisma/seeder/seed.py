import bcrypt
import asyncio

from prisma import Prisma
from prisma.errors import UniqueViolationError


def set_password(pw: str):
    pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
    password_hash = pwhash.decode("utf8")  # decode the hash to prevent is encoded twice
    return password_hash


async def createRoles(client: Prisma):
    await client.role.create(data={"name": "ADMIN", "description": "ADMIN"})

    await client.execute_raw("ALTER SEQUENCE role_id_seq restart 2")


async def createUsers(client: Prisma):
    try:
        await client.user.create(
            data={
                "name": "Admin",
                "lastName": "Admin",
                "session": {
                    "create": {
                        "email": "admin@mail.com",
                        "password": set_password("12345678"),
                        "roleId": 1,
                    }
                },
            },
        )
        await client.execute_raw("ALTER SEQUENCE user_id_seq restart 2")
    except UniqueViolationError as e:
        print(e)
        pass


async def mainSeeder():
    client = Prisma()
    await client.connect()
    await createRoles(client)
    await createUsers(client)
    await client.disconnect()


asyncio.run(mainSeeder())
