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

MODUE_NAME = "Serve"


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


class Serve(object):
    def __init__(self, ip: str, port: int, log_name: str, log_level: str):
        super().__init__()
        self.__loop = asyncio.get_event_loop()
        self.__server = RPCServer(self.__loop, ip, port)
        loggers.set_level(loggers.DEBUG)
        loggers.set_use_console(True)
        loggers.set_use_file(False)
        loggers.set_filename(log_name)
        if log_level == "info":
            loggers.set_level(loggers.INFO)
        elif log_level == "debug":
            loggers.set_level(loggers.DEBUG)
        else:
            loggers.set_level(loggers.ERROR)

    def __quit(self) -> None:
        self.__loop.stop()

    async def __debugger_init(self, portname: str, code: str) -> None:
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

    def start(self) -> None:
        self.__server.register('quit', self.__quit)
        self.__server.register('init', self.__debugger_init)

        loggers.get(MODUE_NAME).info("running...")
        try:
            self.__loop.run_forever()
        finally:
            self.__loop.close()
        loggers.get(MODUE_NAME).info("quited.")