from DobotRPC import loggers, RPCServer
import asyncio
from functools import wraps
import re
import time
import platform
import signal

MODUE_NAME = "Debugger"


def logit(func):
    @wraps(func)
    async def with_logging(*args, **kwargs):
        log = f"{func.__name__} << {args} << {kwargs}"
        loggers.get(MODUE_NAME).debug(log)
        res = await func(*args, **kwargs)
        log = f"{func.__name__} >> {res}"
        loggers.get(MODUE_NAME).debug(log)
        return res

    return with_logging


def timestamp(t):
    data_secs = (t - int(t)) * 1000
    data_head = time.strftime("%H:%M:%S", time.localtime(t))
    return "%s.%03d" % (data_head, data_secs)


class Debugger(object):
    def __init__(self, loop, server: RPCServer):
        super().__init__()
        self.__loop = loop
        self.__server = server
        self.__proc = None
        self.__pid = None
        self.__read_out_task = None
        self.__read_err_task = None

        self.__pipe_hooks = []
        self.__state = None

        self.__progress = -1

        self.__out_timestamp = time.time()
        self.__out_datas = []
        self.__progress_timestamp = time.time()

    @property
    def pid(self):
        return self.__pid

    @property
    def state(self):
        return self.__state

    async def __waitting_worker(self):
        try:
            await asyncio.gather(self.__proc.wait(), self.__read_out_task,
                                 self.__read_err_task)

            if len(self.__out_datas) > 0:
                await self.__server.notify("procOut", {
                    "pid": self.__pid,
                    "out": self.__out_datas
                })
                self.__out_datas.clear()

            if self.__progress > 0:
                await self.__server.notify("progressFresh", {
                    "pid": self.__pid,
                    "progress": self.__progress
                })
        except Exception as e:
            loggers.get(MODUE_NAME).warn(
                f"PID({self.__pid}), Exception in waitting worker: {e}",
                exc_info=True)
        finally:
            loggers.get(MODUE_NAME).debug(
                f"PID({self.__pid}) waitting worker exit.")

    async def __read_err_worker(self):
        try:
            while not self.__proc.stderr.at_eof():
                err = await self.__proc.stderr.readline()
                if len(err) <= 0:
                    await asyncio.sleep(0.1, loop=self.__loop)
                    continue
                err = str(err, encoding="utf-8")
                await self.__do_err(err)
        except Exception as e:
            loggers.get(MODUE_NAME).warn(
                f"PID({self.__pid}), Exception in read err worker: {e}",
                exc_info=True)
        finally:
            loggers.get(MODUE_NAME).debug(
                f"PID({self.__pid}) read err worker exit.")

    async def __do_progress(self, progress):
        if self.__progress <= 0:
            return

        t = time.time()
        if t - self.__progress_timestamp > 1:
            self.__progress_timestamp = t
        else:
            return

        if self.__progress != progress:
            self.__progress = progress
            await self.__server.notify("progressFresh", {
                "pid": self.__pid,
                "progress": self.__progress
            })

    async def __do_out(self, out):
        t = time.time()
        self.__out_datas.append({"time": timestamp(t), "data": out})

        if t - self.__out_timestamp > 0.1:
            self.__out_timestamp = t
        else:
            return

        await self.__server.notify("procOut", {
            "pid": self.__pid,
            "out": self.__out_datas
        })
        self.__out_datas.clear()

    async def __do_err(self, err):
        await self.__server.notify(
            "procErr", {
                "pid": self.__pid,
                "err": [{
                    "time": timestamp(time.time()),
                    "data": err
                }]
            })

    async def __read_out_worker(self):
        try:
            reg_progress = re.compile(
                r"> <string>\((\d+)\)<module>\(([\w|\W]*)\)")
            reg_pdb = re.compile(r"\(Pdb\) ([\w|\W]*)")

            while not self.__proc.stdout.at_eof():
                out = await self.__proc.stdout.readline()

                if len(out) <= 0:
                    await asyncio.sleep(0.1, loop=self.__loop)
                    continue

                out = str(out, encoding="utf-8")

                match_pdb = reg_pdb.match(out)
                if match_pdb:
                    prog_out = match_pdb.groups()[0]
                    match_progress = reg_progress.match(prog_out)
                    if match_progress:
                        progress, _ = match_progress.groups()
                        await self.__do_progress(int(progress))
                    else:
                        await self.__do_out(prog_out)
                    # 需要輸入
                    if len(self.__pipe_hooks) > 0:
                        coro = self.__pipe_hooks.pop(0)
                        await coro()
                    else:
                        await self.__write("n")
                    continue

                if "--Return--" in out:
                    await self.__do_out(out)
                    await self.__write("q")
                    continue

                match_progress = reg_progress.match(out)
                if match_progress:
                    progress, _ = match_progress.groups()
                    await self.__do_progress(int(progress))
                    continue

                await self.__do_out(out)
        except Exception as e:
            loggers.get(MODUE_NAME).warn(
                f"PID({self.__pid}), Exception in read out worker: {e}",
                exc_info=True)
        finally:
            loggers.get(MODUE_NAME).debug(
                f"PID({self.__pid}) read out worker exit.")

    @logit
    async def create_process(self, cmd: str) -> int:
        loggers.get(MODUE_NAME).info(cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        while True:
            out, err = await asyncio.gather(proc.stdout.readline(),
                                            proc.stderr.readline())

            if len(out) > 0:
                out = str(out, encoding="utf-8")
                match_pid = re.match(r"pid (\d+)\r\n", out)
                if match_pid:
                    pid = match_pid.groups()[0]
                    self.__pid = int(pid)
                    break
            elif len(err) > 0:
                e = str(err, encoding="utf-8")
                loggers.get(MODUE_NAME).error(e)
            else:
                await asyncio.sleep(0.1, loop=self.__loop)

        self.__proc = proc
        self.__read_out_task = asyncio.ensure_future(self.__read_out_worker(),
                                                     loop=self.__loop)
        self.__read_err_task = asyncio.ensure_future(self.__read_err_worker(),
                                                     loop=self.__loop)
        self.__waitting_task = asyncio.ensure_future(self.__waitting_worker(),
                                                     loop=self.__loop)

        self.__state = "idle"

    async def __write(self, data: str):
        data = bytes(f"{data}\n", encoding="utf8")
        self.__proc.stdin.write(data)
        await self.__proc.stdin.drain()

    @logit
    async def wait(self):
        await self.__waitting_task

    @logit
    async def start(self, portname: str, script: str):
        if self.__state not in ["stop", "idle"]:
            raise Exception("Invaild state")

        await self.__write(portname)
        await self.__write(script)
        event = asyncio.Event(loop=self.__loop)
        event.clear()

        await self.__write("n")

        async def __start_hook():
            event.set()
            await self.__write("n")

        self.__pipe_hooks.append(__start_hook)
        await event.wait()

        self.__state = "running"

    @logit
    async def pause(self):
        if self.__state != "running":
            raise Exception("Invaild state")

        event = asyncio.Event(loop=self.__loop)
        event.clear()

        async def __pause_hook():
            event.set()

        self.__pipe_hooks.append(__pause_hook)
        await event.wait()

        self.__state = "paused"

    @logit
    async def resume(self):
        if self.__state != "paused":
            raise Exception("Invaild state")

        event = asyncio.Event(loop=self.__loop)
        event.clear()

        await self.__write("n")

        async def __resume_hook():
            event.set()
            await self.__write("n")

        self.__pipe_hooks.append(__resume_hook)
        await event.wait()

        self.__state = "running"

    @logit
    async def stop(self):
        if self.__state not in ["running", "idle", "paused"]:
            raise Exception("Invaild state")

        if self.__state == "idle":
            await self.__write("quit")
        elif self.__state == "paused":
            await self.__write("q")
        else:

            async def __stop_hook():
                await self.__write("q")

            self.__pipe_hooks.append(__stop_hook)

        t = time.time()
        while not self.__waitting_task.done():
            if time.time() - t > 3:
                if platform.system() == "Windows":
                    self.__proc.send_signal(signal.CTRL_C_EVENT)
                else:
                    self.__proc.send_signal(signal.SIGINT)
                # self.__proc.kill()
            await asyncio.sleep(1, loop=self.__loop)

        self.__state = "stoped"

    @logit
    async def emergency_stop(self):
        await self.stop()
