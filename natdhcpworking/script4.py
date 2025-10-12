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
        hostA1v3 = self.addHost('hA1v3', ip='0.0.0.0') # management vlan

# ------ Verdieping 2 ------------------------------------------------------------------------------------- #

        # Switch
        switchA2 = self.addSwitch('sA2', dpid='0000000000000002', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostA2v1 = self.addHost('hA2v1', ip='0.0.0.0') # office vlan
        hostA2v2 = self.addHost('hA2v2', ip='0.0.0.0') # guest vlan
        hostA2v3 = self.addHost('hA2v3', ip='0.0.0.0') # management vlan

# ------ Center Switch A ---------------------------------------------------------------------------------- #

        switchAC = self.addSwitch('sAC', dpid='0000000000000006', cls=OVSSwitch, protocols='OpenFlow13')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
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
        hostB1v3 = self.addHost('hB1v3', ip='0.0.0.0') # management vlan

# ------- Verdieping 2 ------------------------------------------------------------------------------------ #

        # Switch
        switchB2 = self.addSwitch('sB2', dpid='0000000000000004', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostB2v1 = self.addHost('hB2v1', ip='0.0.0.0') # office vlan
        hostB2v2 = self.addHost('hB2v2', ip='0.0.0.0') # guest vlan
        hostB2v3 = self.addHost('hB2v3', ip='0.0.0.0') # management vlan

# ------- verdieping 3 ------------------------------------------------------------------------------------ #

        # Switch
        switchB3 = self.addSwitch('sB3', dpid='0000000000000005', cls=OVSSwitch, protocols='OpenFlow13')

        # Hosts
        hostB3v1 = self.addHost('hB3v1', ip='0.0.0.0') # office vlan
        hostB3v2 = self.addHost('hB3v2', ip='0.0.0.0') # guest vlan
        hostB3v3 = self.addHost('hB3v3', ip='0.0.0.0') # management vlan

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # ISP
        isp = self.addHost('isp', ip='0.0.0.0')

        # NAT nodes
        natA = self.addNode('natA', cls=NAT, ip='10.0.30.1/24', defaultRoute='via 10.0.30.254')
        natB = self.addNode('natB', cls=NAT, ip='10.1.30.1/24', defaultRoute='via 10.1.30.254')

# ------ Center Switch B ---------------------------------------------------------------------------------- #

        switchBC = self.addSwitch('sBC', dpid='0000000000000007', cls=OVSSwitch, protocols='OpenFlow13')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # DHCP for building A (unchanged)
        dhcp10 = self.addHost('dhcp10', ip='10.0.10.10/24', defaultRoute='via 10.0.10.254')
        dhcp20 = self.addHost('dhcp20', ip='10.0.20.10/24', defaultRoute='via 10.0.20.254')
        dhcp30 = self.addHost('dhcp30', ip='10.0.30.10/24', defaultRoute='via 10.0.30.254')

        # DHCP for building B (new nodes)
        # We place these behind sBC and they will serve 10.1.x.0/24 pools
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

        # NAT
        self.addLink(switchAC, natA, port1=20, port2=1)
        self.addLink(switchBC, natB, port1=20, port2=1)

        # ISP
        self.addLink(natA, isp, port1=2, port2=1)
        self.addLink(natB, isp, port1=2, port2=2)

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

    def intf_to_peer(node, peername):
        for intf in node.intfList():
            link = intf.link
            if not link:
                continue
            other = link.intf1 if link.intf1.node != node else link.intf2
            if other.node.name == peername:
                return intf.name
        return None

    natA_node = net.get('natA')
    natB_node = net.get('natB')

    isp_node = net.get('isp')

    natA_lan = intf_to_peer(natA_node, 'sAC')
    natA_wan = intf_to_peer(natA_node, 'isp')
    isp_to_natA = intf_to_peer(isp_node, 'natA')

    natB_lan = intf_to_peer(natB_node, 'sBC')
    natB_wan = intf_to_peer(natB_node, 'isp')
    isp_to_natB = intf_to_peer(isp_node, 'natB')

    # ISP addresses
    isp_node.cmd(f'ip addr flush dev {isp_to_natA}; ip addr add 221.1.1.1/30 dev {isp_to_natA}')
    isp_node.cmd(f'ip addr flush dev {isp_to_natB}; ip addr add 221.1.1.5/30 dev {isp_to_natB}')

    # NAT configuration
    # A
    natA_node.cmd(f'ip addr replace 10.0.30.1/24 dev {natA_lan}')
    natA_node.cmd(f'ip addr replace 221.1.1.2/30 dev {natA_wan}')
    natA_node.cmd(f'ip route replace default via 221.1.1.1 dev {natA_wan}')
    natA_node.cmd(f'ip route replace 10.0.10.0/24 via 10.0.30.254 dev {natA_lan}')
    natA_node.cmd(f'ip route replace 10.0.20.0/24 via 10.0.30.254 dev {natA_lan}')

    natA_node.cmd('sysctl -w net.ipv4.ip_forward=1')
    natA_node.cmd('iptables -t nat -F POSTROUTING')
    natA_node.cmd('iptables -F FORWARD')
    natA_node.cmd(f'iptables -t nat -A POSTROUTING -o {natA_wan} -j MASQUERADE')
    natA_node.cmd(f'iptables -A FORWARD -i {natA_wan} -o {natA_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    natA_node.cmd(f'iptables -A FORWARD -i {natA_lan} -o {natA_wan} -j ACCEPT')

    # B
    natB_node.cmd(f'ip addr replace 10.1.30.1/24 dev {natB_lan}')
    natB_node.cmd(f'ip addr replace 221.1.1.6/30 dev {natB_wan}')
    natB_node.cmd(f'ip route replace default via 221.1.1.5 dev {natB_wan}')
    natB_node.cmd(f'ip route replace 10.1.10.0/24 via 10.1.30.254 dev {natB_lan}')
    natB_node.cmd(f'ip route replace 10.1.20.0/24 via 10.1.30.254 dev {natB_lan}')

    natB_node.cmd('sysctl -w net.ipv4.ip_forward=1')
    natB_node.cmd('iptables -t nat -F POSTROUTING')
    natB_node.cmd('iptables -F FORWARD')
    natB_node.cmd(f'iptables -t nat -A POSTROUTING -o {natB_wan} -j MASQUERADE')
    natB_node.cmd(f'iptables -A FORWARD -i {natB_wan} -o {natB_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    natB_node.cmd(f'iptables -A FORWARD -i {natB_lan} -o {natB_wan} -j ACCEPT')

    # DHCP servers

    # A
    dhcp10 = net.get('dhcp10')
    dhcp20 = net.get('dhcp20')
    dhcp30 = net.get('dhcp30')

    # B
    dhcp10b = net.get('dhcp10b')
    dhcp20b = net.get('dhcp20b')
    dhcp30b = net.get('dhcp30b')

    # Start dnsmasq servers
    dhcp10.cmd('dnsmasq --interface=dhcp10-eth1 --bind-interfaces --dhcp-range=10.0.10.11,10.0.10.200,12h --dhcp-option=3,10.0.10.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp10.leases &')
    dhcp20.cmd('dnsmasq --interface=dhcp20-eth1 --bind-interfaces --dhcp-range=10.0.20.11,10.0.20.200,12h --dhcp-option=3,10.0.20.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp20.leases &')
    dhcp30.cmd('dnsmasq --interface=dhcp30-eth1 --bind-interfaces --dhcp-range=10.0.30.11,10.0.30.200,12h --dhcp-option=3,10.0.30.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp30.leases &')

    dhcp10b.cmd('dnsmasq --interface=dhcp10b-eth1 --bind-interfaces --dhcp-range=10.1.10.11,10.1.10.200,12h --dhcp-option=3,10.1.10.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp10b.leases &')
    dhcp20b.cmd('dnsmasq --interface=dhcp20b-eth1 --bind-interfaces --dhcp-range=10.1.20.11,10.1.20.200,12h --dhcp-option=3,10.1.20.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp20b.leases &')
    dhcp30b.cmd('dnsmasq --interface=dhcp30b-eth1 --bind-interfaces --dhcp-range=10.1.30.11,10.1.30.200,12h --dhcp-option=3,10.1.30.254 --dhcp-option=6,8.8.8.8 --no-daemon --dhcp-leasefile=/tmp/dnsmasq-dhcp30b.leases &')

    time.sleep(10)

    # Trigger DHCP on all hosts
    for name in ['hA1v1', 'hA1v2', 'hA1v3', 'hA2v1', 'hA2v2', 'hA2v3', 'hB1v1', 'hB1v2', 'hB1v3', 'hB2v1', 'hB2v2', 'hB2v3', 'hB3v1', 'hB3v2', 'hB3v3']:
        host = net.get(name)
        host.cmd(f'dhclient -v {name}-eth1 &')

    time.sleep(10)

    CLI(net)

    dhcp10.cmd('sudo pkill dnsmasq')
    dhcp20.cmd('sudo pkill dnsmasq')
    dhcp30.cmd('sudo pkill dnsmasq')
    dhcp10b.cmd('sudo pkill dnsmasq')
    dhcp20b.cmd('sudo pkill dnsmasq')
    dhcp30b.cmd('sudo pkill dnsmasq')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()