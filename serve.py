from DobotRPC import RPCServer, loggers
import asyncio
import platform
import os

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "init",
    "params": {
        "code": 111111,
        "portname": 222
    }
}


class WebConsole(asyncio.streams.StreamWriter):
    def __init__(self, rpc_server: RPCServer):
        self.__rpc_server = rpc_server

    @property
    def seekable(self):
        return False

    @property
    def writable(self):
        return True

    @property
    def encoding(self):
        return 'utf-8'

    @property
    def closed(self):
        return self._stop_all.is_set()

    def _run_server(self, host, port):
        pass

    def readline(self):
        pass

    read = readline

    def writeline(self, data):
        pass

    write = writeline

    def flush(self):
        pass

    def close(self):
        pass

    async def drain(self):
        pass


def start_serve(level: str) -> None:
    APP_NAME = "Dobot_Debugger_Serve"
    IP = "127.0.0.1"
    PORT = 9098
    loop = asyncio.get_event_loop()
    server = RPCServer(loop, IP, PORT)

    def quit() -> None:
        loop.stop()

    async def debugger_init(portname: str, code: str) -> None:
        debugger = "debugger.exe" if platform.system(
        ) == "windows" else "debugger"
        app_dir = os.getcwd()
        cmd = f"{app_dir}/{debugger} --portname {portname} --code {code}"
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    loggers.set_level(loggers.DEBUG)
    loggers.set_use_console(True)
    loggers.set_use_file(False)
    loggers.set_filename(APP_NAME)
    if level == "info":
        loggers.set_level(loggers.INFO)
    elif level == "debug":
        loggers.set_level(loggers.DEBUG)
    else:
        loggers.set_level(loggers.ERROR)

    server.register('quit', quit)
    server.register('init', debugger_init)

    loggers.get(APP_NAME).info("running...")
    try:
        loop.run_forever()
    finally:
        loop.close()
    loggers.get(APP_NAME).info("quited.")