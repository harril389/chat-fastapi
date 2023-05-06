import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)


# @sio_server.event
# async def connect(sid, environ, auth):
#     print(f'{sid}: connected')
#     await sio_server.emit('join', {'sid': sid})


@sio_server.on('send_data_client')
async def chat(sid, message):
    await sio_server.emit('send_data_server', {'message': message}, None, None, sid)


# @sio_server.on('message')
# async def receive(sid, message):
#     await sio_server.emit('chat', {'sid': sid, 'message': '1111'})


# @sio_server.event
# async def disconnect(sid):
#     print(f'{sid}: disconnected')
