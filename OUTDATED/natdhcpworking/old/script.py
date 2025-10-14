from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class MyTopo(Topo):
    "Topology with management VLAN changed to 10.0.30.x"

    def build(self):
        # Building A, Floor 1
        switch1 = self.addSwitch('s1', dpid='0000000000000001', cls=OVSSwitch, protocols='OpenFlow13')
        controller = self.addHost('c1', ip='10.0.30.3/24', defaultRoute='via 10.0.30.254')
        host1 = self.addHost('h1', ip='0.0.0.0')  # office vlan

        DHCP_Vlan1 = self.addHost('dhcp1', ip='10.0.10.10/24', defaultRoute='via 10.0.10.254')
        DHCP_Vlan2 = self.addHost('dhcp2', ip='10.0.20.10/24', defaultRoute='via 10.0.20.254')
        DHCP_Vlan3 = self.addHost('dhcp3', ip='10.0.30.10/24', defaultRoute='via 10.0.30.254')

        # Floor 2
        switch2 = self.addSwitch('s2', dpid='0000000000000002', cls=OVSSwitch, protocols='OpenFlow13')
        host2 = self.addHost('h2', ip='0.0.0.0')  # office vlan
        host3 = self.addHost('h3', ip='0.0.0.0')  # guest vlan

        # Building B, Floor 1
        switch3 = self.addSwitch('s3', dpid='0000000000000003', cls=OVSSwitch, protocols='OpenFlow13')
        host4 = self.addHost('h4', ip='0.0.0.0')  # office vlan
        c2 = self.addHost('c2', ip='10.0.30.4/24', defaultRoute='via 10.0.30.254')

        # Floor 2
        switch4 = self.addSwitch('s4', dpid='0000000000000004', cls=OVSSwitch, protocols='OpenFlow13')
        host5 = self.addHost('h5', ip='0.0.0.0')  # management vlan

        # Floor 3
        switch5 = self.addSwitch('s5', dpid='0000000000000005', cls=OVSSwitch, protocols='OpenFlow13')
        host6 = self.addHost('h6', ip='0.0.0.0')  # guest vlan

        # ISP
        isp = self.addHost('isp', ip='221.1.1.1/28', defaultRoute='via 221.1.1.3')

        # NAT nodes
        nat1 = self.addNode('nat1', cls=NAT, ip='10.0.30.1/24', defaultRoute='via 10.0.30.254')
        nat2 = self.addNode('nat2', cls=NAT, ip='10.0.30.2/24', defaultRoute='via 10.0.30.254')

        # Links
        self.addLink(switch1, host1, port1=1, port2=1)
        self.addLink(switch1, DHCP_Vlan1, port1=18, port2=1)
        self.addLink(switch1, DHCP_Vlan2, port1=19, port2=1)
        self.addLink(switch1, DHCP_Vlan3, port1=20, port2=1)
        self.addLink(switch1, switch3, port1=21, port2=24)
        self.addLink(switch1, controller, port1=22, port2=1)
        self.addLink(switch1, nat1, port1=23, port2=1)
        self.addLink(switch1, switch2, port1=24, port2=24)

        self.addLink(switch2, host2, port1=1, port2=1)
        self.addLink(switch2, host3, port1=2, port2=1)

        self.addLink(switch3, host4, port1=1, port2=1)
        self.addLink(switch3, c2, port1=2, port2=1)
        self.addLink(switch3, nat2, port1=21, port2=1)
        self.addLink(switch3, switch5, port1=22, port2=24)
        self.addLink(switch3, switch4, port1=23, port2=24)

        self.addLink(switch4, host5, port1=1, port2=1)
        self.addLink(switch5, host6, port1=1, port2=1)

        self.addLink(nat1, isp, port1=2, port2=1)
        self.addLink(nat2, isp, port1=2, port2=2)


def run():
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

    nat1_node = net.get('nat1')
    nat2_node = net.get('nat2')
    isp_node = net.get('isp')

    nat1_lan = intf_to_peer(nat1_node, 's1')
    nat1_wan = intf_to_peer(nat1_node, 'isp')
    nat2_lan = intf_to_peer(nat2_node, 's3')
    nat2_wan = intf_to_peer(nat2_node, 'isp')
    isp_to_nat1 = intf_to_peer(isp_node, 'nat1')
    isp_to_nat2 = intf_to_peer(isp_node, 'nat2')

    # ISP addresses
    isp_node.cmd(f'ip addr flush dev {isp_to_nat1}; ip addr add 221.1.1.1/28 dev {isp_to_nat1}')
    isp_node.cmd(f'ip addr flush dev {isp_to_nat2}; ip addr add 221.1.1.2/28 dev {isp_to_nat2}')

    # NAT configuration
    nat1_node.cmd(f'ip addr replace 10.0.30.1/24 dev {nat1_lan}')
    nat1_node.cmd(f'ip addr replace 221.1.1.3/28 dev {nat1_wan}')
    nat1_node.cmd(f'ip route replace default via 221.1.1.1 dev {nat1_wan}')
    nat1_node.cmd(f'ip route replace 10.0.10.0/24 via 10.0.30.254 dev {nat1_lan}')
    nat1_node.cmd(f'ip route replace 10.0.20.0/24 via 10.0.30.254 dev {nat1_lan}')
    nat1_node.cmd(f'ip route replace 10.0.30.0/24 via 10.0.30.1 dev {nat1_lan}')

    nat2_node.cmd(f'ip addr replace 10.0.30.2/24 dev {nat2_lan}')
    nat2_node.cmd(f'ip addr replace 221.1.1.4/28 dev {nat2_wan}')
    nat2_node.cmd(f'ip route replace default via 221.1.1.2 dev {nat2_wan}')

    nat1_node.cmd('sysctl -w net.ipv4.ip_forward=1')
    nat1_node.cmd('iptables -t nat -F; iptables -F')
    nat1_node.cmd(f'iptables -t nat -A POSTROUTING -o {nat1_wan} -j MASQUERADE')
    nat1_node.cmd(f'iptables -A FORWARD -i {nat1_wan} -o {nat1_lan} -m state --state ESTABLISHED,RELATED -j ACCEPT')
    nat1_node.cmd(f'iptables -A FORWARD -i {nat1_lan} -o {nat1_wan} -j ACCEPT')

    # DHCP servers
    DHCP_Vlan1 = net.get('dhcp1')
    DHCP_Vlan2 = net.get('dhcp2')
    DHCP_Vlan3 = net.get('dhcp3')

    DHCP_Vlan1.cmd('dnsmasq --interface=dhcp1-eth1 --bind-interfaces --dhcp-range=10.0.10.11,10.0.10.200,12h --dhcp-option=3,10.0.10.254 --dhcp-option=6,8.8.8.8 --no-daemon &')
    DHCP_Vlan2.cmd('dnsmasq --interface=dhcp2-eth1 --bind-interfaces --dhcp-range=10.0.20.11,10.0.20.200,12h --dhcp-option=3,10.0.20.254 --dhcp-option=6,8.8.8.8 --no-daemon &')
    DHCP_Vlan3.cmd('dnsmasq --interface=dhcp3-eth1 --bind-interfaces --dhcp-range=10.0.30.11,10.0.30.200,12h --dhcp-option=3,10.0.30.1 --dhcp-option=6,8.8.8.8 --no-daemon &')

    time.sleep(2)

    for name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        host = net.get(name)
        host.cmd(f'dhclient -v {name}-eth1 &')

    CLI(net)
    DHCP_Vlan1.cmd('sudo pkill dnsmasq')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()