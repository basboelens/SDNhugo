import subprocess
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class MyTopo(Topo):

    def build(self):

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ----------------------- #
# ------- Gebouw A ------ #
# ----------------------- #

# ------ Verdieping 1 ------------------------------------------------------------------------------------- #

        # Switch
        switchA1 = self.addSwitch('sA1', dpid='0000000000000001', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostA1v1 = self.addHost('hA1v1', ip='0.0.0.0') # office vlan
        hostA1v2 = self.addHost('hA1v2', ip='0.0.0.0') # guest vlan
        hostA1v3 = self.addHost('hA1v3', ip='0.0.0.0', mac='00:00:0A:01:01:01') # management vlan

# ------ Verdieping 2 ------------------------------------------------------------------------------------- #

        # Switch
        switchA2 = self.addSwitch('sA2', dpid='0000000000000002', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostA2v1 = self.addHost('hA2v1', ip='0.0.0.0') # office vlan
        hostA2v2 = self.addHost('hA2v2', ip='0.0.0.0') # guest vlan
        hostA2v3 = self.addHost('hA2v3', ip='0.0.0.0', mac='00:00:0A:01:01:02') # management vlan

# ------ Center Switch A ---------------------------------------------------------------------------------- #

        switchAC = self.addSwitch('sAC', dpid='0000000000000006', cls=OVSSwitch, protocols='OpenFlow13')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ----------------------- #
# ------- Gebouw B ------ #
# ----------------------- #

# ------- Verdieping 1 ------------------------------------------------------------------------------------ #

        # Switch
        switchB1 = self.addSwitch('sB1', dpid='0000000000000003', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostB1v1 = self.addHost('hB1v1', ip='0.0.0.0') # office vlan
        hostB1v2 = self.addHost('hB1v2', ip='0.0.0.0') # guest vlan
        hostB1v3 = self.addHost('hB1v3', ip='0.0.0.0', mac='00:00:0B:01:01:01') # management vlan

# ------- Verdieping 2 ------------------------------------------------------------------------------------ #

        # Switch
        switchB2 = self.addSwitch('sB2', dpid='0000000000000004', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostB2v1 = self.addHost('hB2v1', ip='0.0.0.0') # office vlan
        hostB2v2 = self.addHost('hB2v2', ip='0.0.0.0') # guest vlan
        hostB2v3 = self.addHost('hB2v3', ip='0.0.0.0', mac='00:00:0B:01:01:02') # management vlan

# ------- verdieping 3 ------------------------------------------------------------------------------------ #

        # Switch
        switchB3 = self.addSwitch('sB3', dpid='0000000000000005', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostB3v1 = self.addHost('hB3v1', ip='0.0.0.0') # office vlan
        hostB3v2 = self.addHost('hB3v2', ip='0.0.0.0') # guest vlan
        hostB3v3 = self.addHost('hB3v3', ip='0.0.0.0', mac='00:00:0B:01:01:03') # management vlan

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # ISP
        isp = self.addHost('isp', ip='0.0.0.0')

        # NAT nodes
        nat = self.addNode('nat', cls=NAT, inNamespace=True)

# ------ Center Switch B ---------------------------------------------------------------------------------- #

        switchBC = self.addSwitch('sBC', dpid='0000000000000007', cls=OVSSwitch, protocols='OpenFlow13')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # DHCP for building A 
        dhcp10 = self.addHost('dhcp10', ip='10.0.10.10/24', defaultRoute='via 10.0.10.254')
        dhcp20 = self.addHost('dhcp20', ip='10.0.20.10/24', defaultRoute='via 10.0.20.254')
        dhcp30 = self.addHost('dhcp30', ip='10.0.30.10/24', defaultRoute='via 10.0.30.254')

        # DHCP for building B 
        dhcp10b = self.addHost('dhcp10b', ip='10.1.10.10/24', defaultRoute='via 10.1.10.254')
        dhcp20b = self.addHost('dhcp20b', ip='10.1.20.10/24', defaultRoute='via 10.1.20.254')
        dhcp30b = self.addHost('dhcp30b', ip='10.1.30.10/24', defaultRoute='via 10.1.30.254')

# -------------------- #
# ------- links ------ #
# -------------------- #

# ------- Switch A1 --------------------------------------------------------------------------------------- #

        # Hosts
        self.addLink(switchA1, hostA1v1, port1=1, port2=1)
        self.addLink(switchA1, hostA1v2, port1=2, port2=1)
        self.addLink(switchA1, hostA1v3, port1=3, port2=1)

# ------- Switch A2 ---------------------------------------------------------------------------------------- #

        # Hosts
        self.addLink(switchA2, hostA2v1, port1=1, port2=1)
        self.addLink(switchA2, hostA2v2, port1=2, port2=1)
        self.addLink(switchA2, hostA2v3, port1=3, port2=1)

# ------- Switch B1 ---------------------------------------------------------------------------------------- #

        # Hosts
        self.addLink(switchB1, hostB1v1, port1=1, port2=1)
        self.addLink(switchB1, hostB1v2, port1=2, port2=1)
        self.addLink(switchB1, hostB1v3, port1=3, port2=1)

# ------- Switch B2 ---------------------------------------------------------------------------------------- #

        # Hosts
        self.addLink(switchB2, hostB2v1, port1=1, port2=1)
        self.addLink(switchB2, hostB2v2, port1=2, port2=1)
        self.addLink(switchB2, hostB2v3, port1=3, port2=1)

# ------ Switch B3 ----------------------------------------------------------------------------------------- #

        # Hosts
        self.addLink(switchB3, hostB3v1, port1=1, port2=1)
        self.addLink(switchB3, hostB3v2, port1=2, port2=1)
        self.addLink(switchB3, hostB3v3, port1=3, port2=1)

# ------ Switch - Switch ----------------------------------------------------------------------------------- #

        # A
        self.addLink(switchAC, switchA1, port1=2 , port2=25)
        self.addLink(switchAC, switchA2, port1=3 , port2=25)

        # B
        self.addLink(switchBC, switchB1, port1=2 , port2=25)
        self.addLink(switchBC, switchB2, port1=3 , port2=25)
        self.addLink(switchBC, switchB3, port1=4 , port2=25)

        # Darkfiber
        self.addLink(switchAC, switchBC, port1=1 , port2=1)

        # ISP
        self.addLink(nat, isp, port1=3, port2=1)
        self.addLink(nat, switchAC, port1=1, port2=50)
        self.addLink(nat, switchBC, port1=2, port2=50)

        # DHCP A
        self.addLink(switchAC, dhcp10, port1=100, port2=1)
        self.addLink(switchAC, dhcp20, port1=200, port2=1)
        self.addLink(switchAC, dhcp30, port1=300, port2=1)

        # DHCP B
        self.addLink(switchBC, dhcp10b, port1=100, port2=1)
        self.addLink(switchBC, dhcp20b, port1=200, port2=1)
        self.addLink(switchBC, dhcp30b, port1=300, port2=1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def run():
    subprocess.run(["sudo", "mn", "-c"], check=True)
    subprocess.run(["sudo", "pkill", "-f", "dnsmasq"], check=False)
    topo = MyTopo()
    net = Mininet(topo=topo, controller=None, switch=OVSSwitch, autoSetMacs=True)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    # --- IPv6 CONSTANTS ---
    NAT_A_V6 = "2042:300::1"
    NAT_B_V6 = "2042:330::1"
    ISP_WAN_V6 = "2001:db8::1"
    NAT_WAN_V6 = "2001:db8::2"
    DHCP_GW_A_V6 = "2042:300::10" 
    DHCP_GW_B_V6 = "2042:330::10" 
    # ----------------------
    
    # --- DEFINE HOST NAMES EERST (FIX VOOR UnboundLocalError) ---
    HOST_NAMES = ['hA1v1', 'hA1v2', 'hA1v3', 'hA2v1', 'hA2v2', 'hA2v3', 'hB1v1', 'hB1v2', 'hB1v3', 'hB2v1', 'hB2v2', 'hB2v3', 'hB3v1', 'hB3v2', 'hB3v3']
    
    def intf_to_peer(node, peername):
        for intf in node.intfList():
            link = intf.link
            if not link:
                continue
            other = link.intf1 if link.intf1.node != node else link.intf2
            if other.node.name == peername:
                return intf.name
        return None

    def defaultIntf(host):
        return f'{host.name}-eth1'
    
    nat_node = net.get('nat')
    isp_node = net.get('isp')
    natA_lan = intf_to_peer(nat_node, 'sAC')
    natB_lan = intf_to_peer(nat_node, 'sBC')
    nat_wan = intf_to_peer(nat_node, 'isp')
    isp_to_nat = intf_to_peer(isp_node, 'nat')

    # ISP addresses
    isp_node.cmd(f'ip addr flush dev {isp_to_nat}; ip addr add 221.1.1.1/30 dev {isp_to_nat}')
    isp_node.cmd(f'ip addr add {ISP_WAN_V6}/64 dev {isp_to_nat}') # IPv6 ISP
    isp_node.cmd(f'ip -6 route add 2042::/48 via {NAT_WAN_V6} dev {isp_to_nat}')

    # NAT configuration
    # Flush old IPs
    nat_node.cmd(f'ip addr flush dev {natA_lan}')
    nat_node.cmd(f'ip addr flush dev {natB_lan}')
    # A (IPv4/IPv6 LANs)
    nat_node.cmd(f'ip addr replace 10.0.30.1/24 dev {natA_lan}')
    nat_node.cmd(f'ip addr replace 10.1.30.1/24 dev {natB_lan}')
    nat_node.cmd(f'ip addr add {NAT_A_V6}/64 dev {natA_lan}')
    nat_node.cmd(f'ip addr add {NAT_B_V6}/64 dev {natB_lan}')
    # WAN (IPv4/IPv6)
    nat_node.cmd(f'ip addr replace 221.1.1.2/30 dev {nat_wan}')
    nat_node.cmd(f'ip addr add {NAT_WAN_V6}/64 dev {nat_wan}')
    # Default Routes
    nat_node.cmd(f'ip route replace default via 221.1.1.1 dev {nat_wan}') # IPv4 Default Route
    nat_node.cmd(f'ip -6 route replace default via {ISP_WAN_V6} dev {nat_wan}') # IPv6 Default Route
    # Static Routes to other VLANs (via Faucet VIPs)
    nat_node.cmd(f'ip route replace 10.0.10.0/24 via 10.0.30.254 dev {natA_lan}')
    nat_node.cmd(f'ip route replace 10.0.20.0/24 via 10.0.30.254 dev {natA_lan}')
    nat_node.cmd(f'ip -6 route replace 2042::/48 via 2042:300::254 dev {natA_lan}')
    nat_node.cmd(f'ip route replace 10.1.10.0/24 via 10.1.30.254 dev {natB_lan}')
    nat_node.cmd(f'ip route replace 10.1.20.0/24 via 10.1.30.254 dev {natB_lan}')
    nat_node.cmd(f'ip -6 route replace 2042::/48 via 2042:330::254 dev {natB_lan}')
    # IP Forwarding and NAT (IPv4 & IPv6)
    nat_node.cmd('sysctl -w net.ipv4.ip_forward=1')
    nat_node.cmd('sysctl -w net.ipv6.conf.all.forwarding=1') # Enable IPv6 Forwarding
    # IPv4 IPtables
    nat_node.cmd('iptables -t nat -F POSTROUTING')
    nat_node.cmd('iptables -F FORWARD')
    nat_node.cmd(f'iptables -t nat -A POSTROUTING -o {nat_wan} -j MASQUERADE')
    nat_node.cmd(f'iptables -A FORWARD -i {nat_wan} -o {natA_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    nat_node.cmd(f'iptables -A FORWARD -i {nat_wan} -o {natB_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    nat_node.cmd(f'iptables -A FORWARD -i {natA_lan} -o {nat_wan} -j ACCEPT')
    nat_node.cmd(f'iptables -A FORWARD -i {natB_lan} -o {nat_wan} -j ACCEPT')
    # IPv6 IPtables
    nat_node.cmd('ip6tables -t nat -F POSTROUTING')
    nat_node.cmd('ip6tables -F FORWARD')
    nat_node.cmd(f'ip6tables -A FORWARD -i {nat_wan} -o {natA_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    nat_node.cmd(f'ip6tables -A FORWARD -i {nat_wan} -o {natB_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    nat_node.cmd(f'ip6tables -A FORWARD -i {natA_lan} -o {nat_wan} -j ACCEPT')
    nat_node.cmd(f'ip6tables -A FORWARD -i {natB_lan} -o {nat_wan} -j ACCEPT')

    # DHCP servers
    dhcp10 = net.get('dhcp10')
    dhcp20 = net.get('dhcp20')
    dhcp30 = net.get('dhcp30')
    dhcp10b = net.get('dhcp10b')
    dhcp20b = net.get('dhcp20b')
    dhcp30b = net.get('dhcp30b')
    
    # --- STAP 1: Schakel RA acceptance uit op ALLE HOSTS (NDP Fix) ---
    for name in HOST_NAMES:
        host = net.get(name)
        host_intf = defaultIntf(host)
        # Forceer accept_ra=0 om Link-Local routing te voorkomen
        host.cmd(f'sysctl -w net.ipv6.conf.{host_intf}.accept_ra=0') 
        # NIEUW: Verhoog de NDP cache timeouts (Cruciaal voor stabiliteit)
        host.cmd(f'sysctl -w net.ipv6.conf.{host_intf}.retrans_time=1000') 
        host.cmd(f'sysctl -w net.ipv6.neigh.{host_intf}.retrans_time_ms=1000')
        host.cmd(f'sysctl -w net.ipv6.neigh.{host_intf}.base_reachable_time_ms=600000') # 10 minuten
        host.cmd(f'sysctl -w net.ipv6.neigh.{host_intf}.gc_stale_time=600') # 10 minuten
    # -------------------------------------------------------------------

    # NIEUW: Schakel IP Forwarding in op de DHCP-hosts (Crucial for stable NDP/VIP response)
    for dhcp_node in [dhcp10, dhcp20, dhcp30, dhcp10b, dhcp20b, dhcp30b]:
        dhcp_node.cmd('sysctl -w net.ipv4.ip_forward=1')
        dhcp_node.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')
    
    # # Assign IPv6 to DHCP server interfaces
    # # NIEUW: Voeg Faucet VIPs toe aan de DHCP Hosts (Linux kernel NDP fix)
    dhcp10.cmd('ip addr add 10.0.10.254/24 dev dhcp10-eth1')
    dhcp10.cmd('ip addr add 2042:100::10/64 dev dhcp10-eth1')
    dhcp10.cmd('ip addr add 2042:100::254/64 dev dhcp10-eth1') # Office A VIP
    
    dhcp20.cmd('ip addr add 10.0.20.254/24 dev dhcp20-eth1')
    dhcp20.cmd('ip addr add 2042:200::10/64 dev dhcp20-eth1')
    dhcp20.cmd('ip addr add 2042:200::254/64 dev dhcp20-eth1') # Guest A VIP
    
    dhcp30.cmd('ip addr add 10.0.30.254/24 dev dhcp30-eth1')
    dhcp30.cmd(f'ip addr add 2042:300::10/64 dev dhcp30-eth1')
    dhcp30.cmd(f'ip addr add 2042:300::254/64 dev dhcp30-eth1') # Management A VIP

    dhcp10b.cmd('ip addr add 10.1.10.254/24 dev dhcp10b-eth1')
    dhcp10b.cmd('ip addr add 2042:110::10/64 dev dhcp10b-eth1')
    dhcp10b.cmd('ip addr add 2042:110::254/64 dev dhcp10b-eth1') # Office B VIP
    
    dhcp20b.cmd('ip addr add 10.1.20.254/24 dev dhcp20b-eth1')
    dhcp20b.cmd('ip addr add 2042:220::10/64 dev dhcp20b-eth1')
    dhcp20b.cmd('ip addr add 2042:220::254/64 dev dhcp20b-eth1') # Guest B VIP
    
    dhcp30b.cmd('ip addr add 10.1.30.254/24 dev dhcp30b-eth1')
    dhcp30b.cmd(f'ip addr add 2042:330::10/64 dev dhcp30b-eth1')
    dhcp30b.cmd(f'ip addr add 2042:330::254/64 dev dhcp30b-eth1') # Management B VIP
    
    # Zorg dat de oorspronkelijke DHCP Gateway (DHCP_GW_A_V6/B_V6) niet dubbel wordt ingesteld
    # Deze IPs zijn al behandeld door de nieuwe VIP toewijzing of zijn niet strikt nodig hier.

    # Start dual-stack dnsmasq servers (ZONDER --enable-ra)
    dhcp10.cmd(
        f"dnsmasq --interface={defaultIntf(dhcp10)} --bind-interfaces "
        f"--dhcp-range=10.0.10.11,10.0.10.250,12h "
        f"--dhcp-range=2042:100::11,2042:100::fffe,64,12h "
        f"--dhcp-option=3,10.0.10.254 "
        f"--dhcp-option=6,8.8.8.8 "
        f"--dhcp-option=option6:dns-server,[2606:4700:4700::1111] "
        f"--dhcp-sequential-ip "
        f"--no-daemon &"
    )
    
    # DHCP VLAN 2 (Guest A - 10.0.20.x / 2042:200::/64)
    dhcp20.cmd(f"dnsmasq --interface={defaultIntf(dhcp20)} --bind-interfaces --dhcp-range=10.0.20.11,10.0.20.250,12h --dhcp-range=2042:200::11,2042:200::fffe,64,12h --dhcp-option=3,10.0.20.254 --dhcp-option=6,8.8.8.8 --dhcp-option=option6:dns-server,[2606:4700:4700::1111] --dhcp-sequential-ip --no-daemon &")
    dhcp30.cmd(f"dnsmasq --interface={defaultIntf(dhcp30)} --bind-interfaces --dhcp-range=10.0.30.11,10.0.30.250,12h --dhcp-range=2042:300::11,2042:300::fffe,64,12h --dhcp-option=3,10.0.30.254 --dhcp-option=6,8.8.8.8 --dhcp-option=option6:dns-server,[2606:4700:4700::1111] --dhcp-sequential-ip --no-daemon &")
    dhcp10b.cmd(f"dnsmasq --interface={defaultIntf(dhcp10b)} --bind-interfaces --dhcp-range=10.1.10.11,10.1.10.250,12h --dhcp-range=2042:110::11,2042:110::fffe,64,12h --dhcp-option=3,10.1.10.254 --dhcp-option=6,8.8.8.8 --dhcp-option=option6:dns-server,[2606:4700:4700::1111] --dhcp-sequential-ip --no-daemon &")
    dhcp20b.cmd(f"dnsmasq --interface={defaultIntf(dhcp20b)} --bind-interfaces --dhcp-range=10.1.20.11,10.1.20.250,12h --dhcp-range=2042:220::11,2042:220::fffe,64,12h --dhcp-option=3,10.1.20.254 --dhcp-option=6,8.8.8.8 --dhcp-option=option6:dns-server,[2606:4700:4700::1111] --dhcp-sequential-ip --no-daemon &")
    dhcp30b.cmd(f"dnsmasq --interface={defaultIntf(dhcp30b)} --bind-interfaces --dhcp-range=10.1.30.11,10.1.30.250,12h --dhcp-range=2042:330::11,2042:330::fffe,64,12h --dhcp-option=3,10.1.30.254 --dhcp-option=6,8.8.8.8 --dhcp-option=option6:dns-server,[2606:4700:4700::1111] --dhcp-sequential-ip --no-daemon &")

    time.sleep(10)

    # Trigger DHCP on all hosts
    for name in HOST_NAMES:
        host = net.get(name)
        host_intf = defaultIntf(host)
        
        # 1. Explicitly request IPv4 address
        host.cmd(f'dhclient -v -4 -cf /dev/null {host_intf} &') 

        # 2. Explicitly request IPv6 address
        host.cmd(f'dhclient -v -6 -cf /dev/null {host_intf} &')

    time.sleep(10)
    
    # ----------------------------------------------------
    # FIX: Correct IPv6 address prefix, ADD DEFAULT ROUTE, and FORCE NDP LEARNING
    # ----------------------------------------------------
    info('*** Applying IPv6 default route, clearing stale routes, and forcing NDP learning on all hosts ***\n')
    
    for name in HOST_NAMES:
        host = net.get(name)
        intf_name = defaultIntf(host)
        
        # 1. Bepaal de Faucet VIP (Default Gateway)
        if 'A' in name:
            if 'v1' in name: 
                router_ip = '2042:100::254'
            elif 'v2' in name: 
                router_ip = '2042:200::254'
            else: 
                router_ip = '2042:300::254'
        else:
            if 'v1' in name: 
                router_ip = '2042:110::254'
            elif 'v2' in name: 
                router_ip = '2042:220::254'
            else: 
                router_ip = '2042:330::254'

        # --- Gedeelte 1: Prefix Fix ---
        target_ip_full = None
        ip_addr_output = host.cmd(f'ip -6 addr show dev {intf_name}')
        
        for line in ip_addr_output.splitlines():
            line = line.strip()
            if 'inet6' in line and '/128' in line and 'scope global' in line:
                parts = line.split()
                try:
                    target_ip_full = next(p for p in parts if '/' in p and p.endswith('/128'))
                    if target_ip_full:
                        break
                except StopIteration:
                    continue

        if target_ip_full:
            info(f'{name}: Deleting incorrect address {target_ip_full}...\n')
            host.cmd(f'ip -6 addr del {target_ip_full} dev {intf_name}')
            new_ip = target_ip_full.replace('/128', '/64')
            info(f'{name}: Adding correct address {new_ip}...\n')
            host.cmd(f'ip -6 addr add {new_ip} dev {intf_name}')
        else:
            info(f'{name}: IPv6 address prefix OK (Skipping /128 fix).\n')


        # --- Gedeelte 2: Default Route Fix (Verwijder Link-Local en voeg de correcte route toe) ---
        
        # 1. Verwijder ALLE default routes via Router Advertisement (Link-Local / .10 routes)
        info(f'{name}: Flushing RA routes...\n')
        host.cmd(f'ip -6 route flush dev {intf_name} proto ra 2>/dev/null || true')
        
        # 2. Verwijder ALLE andere default routes
        info(f'{name}: Deleting existing default route...\n')
        host.cmd(f'ip -6 route del default dev {intf_name} 2>/dev/null || true')
        
        # 3. Voeg de correcte default route toe
        info(f'{name}: Adding final default route via {router_ip}...\n')
        host.cmd(f'ip -6 route add default via {router_ip} dev {intf_name}')


        # --- Gedeelte 3: NDP Learning Fix (CRUCIAAL voor cache-instabiliteit) ---
        # Forceer de host om direct de gateway te pingen om het MAC-adres te leren in Faucet's cache.
        info(f'{name}: Pinging gateway {router_ip} to prime NDP cache...\n')
        host.cmd(f'ping6 -c 1 {router_ip} > /dev/null 2>&1')

    CLI(net)

    # Cleanup dnsmasq processes gracefully
    for host in [dhcp10, dhcp20, dhcp30, dhcp10b, dhcp20b, dhcp30b]:
        host.cmd('sudo pkill dnsmasq')
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()