from ipaddress import IPv4Network
from math import ceil, log2
import pandas as pd

def calculate_subnet_sizes(hosts_required):
    """Повертає потрібну маску для кожної кількості хостів."""

    result = []
    for h in hosts_required:
        needed_hosts = h + 2  # включаючи network + broadcast
        bits = ceil(log2(needed_hosts))
        subnet_size = 2 ** bits
        prefix_length = 32 - bits
        result.append((h, subnet_size, prefix_length))
    return result


def allocate_subnets(base_network, hosts_required):
    base = IPv4Network(base_network)
    current_ip = int(base.network_address)
    result = []

    total_available_hosts = base.num_addresses
    used_hosts = 0

    subnet_infos = calculate_subnet_sizes(hosts_required)

    # Сортуємо підмережі за спаданням розміру (по block_size)
    subnet_infos.sort(key=lambda x: x[1], reverse=True)

    for host_count, block_size, prefix in subnet_infos:
        # Вирівнюємо current_ip вгору до кратного block_size
        aligned_ip = (current_ip + block_size - 1) // block_size * block_size

        subnet = IPv4Network((aligned_ip, prefix))

        if subnet.broadcast_address > base.broadcast_address:
            raise ValueError(f"Підмережа {subnet} виходить за межі базової мережі {base}!")

        used_hosts += subnet.num_addresses

        result.append({
            'network_address': str(subnet.network_address),
            'prefix': f"/{subnet.prefixlen}",
            'range': f"{subnet.network_address} - {subnet.broadcast_address}",
            'broadcast': str(subnet.broadcast_address),
            'hosts': host_count
        })

        current_ip = int(subnet.broadcast_address) + 1

    remaining = base.num_addresses - used_hosts
    return result, remaining


# Запуск
hosts = [100, 50, 25, 10, 2]
subnets_info = allocate_subnets("10.0.0.0/8", hosts)

def main():
    base_networks = [
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.0.0.0/13",
        "192.32.0.0/14",
        "192.48.0.0/15",
        "192.64.0.0/16",
        "192.168.0.0/17",
        "192.168.128.0/18",
        "192.168.192.0/19",
        "192.168.224.0/20",
        "192.168.240.0/21",
        "192.168.248.0/22",
        "192.168.252.0/23",
        "192.168.254.0/24",
        "192.168.255.0/25",
        "192.168.255.128/26",
        "192.168.255.192/27",
        "192.168.255.224/28"
    ]

    hosts_needed = [500, 200, 200, 100, 25, 25, 10, 2]
    # hosts_needed = [10, 18]
    result, remaining = allocate_subnets(base_networks[10], hosts_needed)
    # result, remaining = allocate_subnets("192.168.1.64/26", hosts_needed)
    df = pd.DataFrame(result)
    print(df)

    # if isinstance(result, dict) and "error" in result:
    #     print(result["error"])
    # else:
    #     for subnet in result:
    #         print(subnet)

    print(f"\n Залишилось вільних IP-адрес у базовій мережі: {remaining}")

    #зберегти у файл:
    # df.to_csv("subnets_result.csv", index=False)

if __name__ == "__main__":
    main()