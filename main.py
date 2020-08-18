from DobotRPC import RPCServer, loggers
import asyncio

APP_NAME = "Dobot_Python_Debugger"
IP = "127.0.0.1"
PORT = 9097

loop = asyncio.get_event_loop()
server = RPCServer(loop, IP, PORT)


def quit():
    loop.stop()


if __name__ == "__main__":
    loggers.set_level(loggers.DEBUG)
    loggers.set_use_console(True)
    loggers.set_use_file(False)
    loggers.set_filename(APP_NAME)

    server.register('quit', quit)

    loggers.get(APP_NAME).info("running...")
    try:
        loop.run_forever()
    finally:
        loop.close()
    loggers.get(APP_NAME).info("quited.")
