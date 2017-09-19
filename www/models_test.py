import orm,asyncio 
from models import User, Blog, Comment

@asyncio.coroutine
def test(loop):
    yield from orm.create_pool(loop=loop,user='www-data', password='www-data', db='awesome')

    # u = User(id='0015057486724538420f1498b98449396a6b612fbc4be18000',name='Testorg', email='test@example.com', passwd='1234567890', image='about:blank',created_at=1505748672.45334,admin=0)
    u = User(id='0015057486724538420f1498b98449396a6b612fbc4be18000')
    # yield from u.save()
    # yield from u.update()
    yield from u.remove()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()

