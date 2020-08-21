import asyncio
import signal


async def main():
    proc = await asyncio.create_subprocess_shell(
        "/Users/jomar/Documents/GitHub/Python-Remote-Debugger/dist/test2.app/Contents/MacOS/test2"
    )
    await asyncio.sleep(15)
    proc.send_signal(signal.SIGKILL)
    await proc.wait()


asyncio.run(main())