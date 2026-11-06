dns_dict = {"nbc.com": "2.21.109.123", "cnn.com": "151.101.195.5", "google.com": "142.250.75.78"}


def get_ip(name):
    """
    Returns the ip address of a dns record of exists in memory
    :param name: the domain name to check
    :return: IP address if exists, None otherwise
    """
    if name in dns_dict:
        return dns_dict[name]
    return None


def get_domain(ip):
    """
    Returns the domain name of a dns record of exists in memory
    :param ip: the ip address to check
    :return: domain name if exists, None otherwise
    """
    for key, value in dns_dict.items():
        if value == ip:
            return key

    return None


def main():
    choice = "1"

    while choice in ["1", "2"]:
        choice = input("\n1. ip -> domain name\n2. domain name -> ip\n3. exit\nPlease choose: ")
        if choice == "1":
            ip = input("Please enter the ip address: ")
            domain_name = get_domain(ip)
            if domain_name:
                print(domain_name)
            else:
                print("No domain name found")
        if choice == "2":
            domain_name = input("Please enter the domain name to check: ")
            ip = get_ip(domain_name)
            if ip:
                print(ip)
            else:
                print("No ip address found")

    print("\n\nSee you later...")


if __name__ == "__main__":
    main()
