def ip_to_int(ip):
    a, b, c, d = map(int, ip.split('.'))
    return a * 256**3 + b * 256**2 + c * 256 + d

def is_network_address(ip, cidr):
    ip_int = ip_to_int(ip)
    block_size = 2 ** (32 - cidr)
    return ip_int % block_size == 0

print(is_network_address("172.16.16.0", 22))  # True
print(is_network_address("172.16.17.0", 22))  # False

def main():
    tests = [
        ("172.16.16.0", 22),
        ("172.16.17.0", 22),
        ("10.0.0.0", 8),
        ("192.168.1.128", 25),
        ("192.168.1.129", 25),
    ]

    for ip, cidr in tests:
        result = is_network_address(ip, cidr)
        print(f"{ip}/{cidr} => {'Network address' if result else 'Not a network address'}")

if __name__ == "__main__":
    main()