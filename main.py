from load_balancer.balancer import LoadBalancer

def main():
    load_balancer = LoadBalancer()
    load_balancer.load_vps_list('vps_list.txt')

    for _ in range(10):
        load_balancer.distribute_load()

if __name__ == '__main__':
    main()
