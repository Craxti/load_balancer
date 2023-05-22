import asyncio
from load_balancer.balancer import LoadBalancer


async def main():
    load_balancer = LoadBalancer()
    load_balancer.load_vps_list('vps_list.txt')

    await load_balancer.distribute_load_concurrently(10)


if __name__ == '__main__':
    asyncio.run(main())
