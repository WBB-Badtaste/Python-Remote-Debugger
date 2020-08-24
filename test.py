import asyncio
import signal


async def main():
    proc = await asyncio.create_subprocess_shell(
        "\\\\Mac\\Home\\Documents\\GitHub\\Python-Remote-Debugger\\debugger.exe --portname 222 --script cHJpbnQoMTExMSk=")
    # await asyncio.sleep(15)
    # proc.send_signal(signal.SIGKILL)
    await proc.wait()


asyncio.run(main())