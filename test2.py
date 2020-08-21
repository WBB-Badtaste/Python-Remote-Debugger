import asyncio
import functools
import signal


async def main():
    while 1:
        print(1111)
        await asyncio.sleep(1)


def exit(sign_name):
    print(f"获取信号{sign_name}: exit")
    loop.stop()


try:
    loop = asyncio.get_event_loop()
    for sign_name in ("SIGINT", "SIGTERM", "SIGKILL"):
        loop.add_signal_handler(getattr(signal, sign_name),
                                functools.partial(exit, sign_name))
    loop.run_until_complete(main())
except Exception as e:
    print(e)
finally:
    loop.close()
