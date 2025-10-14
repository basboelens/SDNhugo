#!/usr/bin/env python3

import subprocess
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class BuildingTopo(Topo):
    def build(self):
        # ----------------------------
        # Add switches
        # ----------------------------
        # Building A
        sA1 = self.addSwitch('sA1', dpid='00000000000000A1')
        sA2 = self.addSwitch('sA2', dpid='00000000000000A2')
        sA10 = self.addSwitch('sA10', dpid='0000000000000A10')

        # Building B
        sB1 = self.addSwitch('sB1', dpid='00000000000000B1')
        sB2 = self.addSwitch('sB2', dpid='00000000000000B2')
        sB3 = self.addSwitch('sB3', dpid='00000000000000B3')
        sB10 = self.addSwitch('sB10', dpid='0000000000000B10')

        # ----------------------------
        # Add hosts
        # ----------------------------
        # Building A VLAN 100 (employee)
        hA1 = self.addHost('hA1', ip='0.0.0.0', mac='00:00:00:00:10:02')
        hA2 = self.addHost('hA2', ip='0.0.0.0', mac='00:00:00:00:10:03')

        # Building A VLAN 200 (management)
        hA3 = self.addHost('hA3', ip='0.0.0.0', mac='00:00:00:00:20:02')

        # Building A VLAN 300 (guest)
        hA4 = self.addHost('hA4', ip='0.0.0.0', mac='00:00:00:00:30:02')

        # Building B VLAN 100 (employee)
        hB1 = self.addHost('hB1', ip='0.0.0.0', mac='00:00:00:00:10:04')
        hB2 = self.addHost('hB2', ip='0.0.0.0', mac='00:00:00:00:10:05')

        # Building B VLAN 200 (management)
        hB3 = self.addHost('hB3', ip='0.0.0.0', mac='00:00:00:00:20:03')

        # Building B VLAN 300 (guest)
        hB4 = self.addHost('hB4', ip='0.0.0.0', mac='00:00:00:00:30:03')

        # ----------------------------
        # DHCP servers (per VLAN)
        # ----------------------------
        dhcp10 = self.addHost('dhcp10', ip='10.0.10.10/24')
        dhcp20 = self.addHost('dhcp20', ip='10.0.20.10/24')
        dhcp30 = self.addHost('dhcp30', ip='10.0.30.10/24')

        # ----------------------------
        # Connect hosts to edge switches (access ports)
        # ----------------------------
        # Building A
        self.addLink(hA1, sA1)
        self.addLink(hA2, sA1)
        self.addLink(hA3, sA2)
        self.addLink(hA4, sA2)

        # Building B
        self.addLink(hB1, sB1)
        self.addLink(hB2, sB1)
        self.addLink(hB3, sB2)
        self.addLink(hB4, sB3)

        # ----------------------------
        # Connect edge switches to central switches (trunks)
        # ----------------------------
        # Building A
        self.addLink(sA1, sA10)
        self.addLink(sA2, sA10)

        # Building B
        self.addLink(sB1, sB10)
        self.addLink(sB2, sB10)
        self.addLink(sB3, sB10)

        # Connect central switches between buildings (trunk)
        self.addLink(sA10, sB10)

        # ----------------------------
        # Connect DHCP servers to sA10 (VLAN isolation)
        # ----------------------------
        self.addLink(dhcp10, sA10, intfName1='dhcp10-eth0', intfName2='sA10-eth4')
        self.addLink(dhcp20, sA10, intfName1='dhcp20-eth0', intfName2='sA10-eth5')
        self.addLink(dhcp30, sA10, intfName1='dhcp30-eth0', intfName2='sA10-eth6')


def run_building_topo():
    print("*** Cleaning Mininet environment")
    subprocess.run(["sudo", "mn", "-c"], check=True)

    setLogLevel('info')
    topo = BuildingTopo()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6653),
        switch=OVSKernelSwitch,
        build=True
    )
    net.start()
    print("*** Network started")

    # ----------------------------
    # Start DHCP servers
    # ----------------------------

    print("*** Starting DHCP pools")
    net.get('dhcp10').cmd(
        "dnsmasq --no-daemon --interface=dhcp10-eth0 --bind-interfaces "
        "--dhcp-range=10.0.10.11,10.0.10.253,12h --dhcp-sequential-ip "
        "--dhcp-leasefile=/tmp/dnsmasq-dhcp10.leases & "
    )
    net.get('dhcp20').cmd(
        "dnsmasq --no-daemon --interface=dhcp20-eth0 --bind-interfaces "
        "--dhcp-range=10.0.20.11,10.0.20.253,12h --dhcp-sequential-ip "
        "--dhcp-leasefile=/tmp/dnsmasq-dhcp20.leases & "
    )
    net.get('dhcp30').cmd(
        "dnsmasq --no-daemon --interface=dhcp30-eth0 --bind-interfaces "
        "--dhcp-range=10.0.30.11,10.0.30.253,12h --dhcp-sequential-ip "
        "--dhcp-leasefile=/tmp/dnsmasq-dhcp30.leases & "
    )
    print("*** DHCP pools setup successfully")

    # ----------------------------
    # Acquire DHCP IP for hosts that need it
    # ----------------------------
    net.get('hA1').cmd("dhclient -v hA1-eth0 &")
    net.get('hA2').cmd("dhclient -v hA2-eth0 &")
    net.get('hA3').cmd("dhclient -v hA3-eth0 &")
    net.get('hA4').cmd("dhclient -v hA4-eth0 &")
    net.get('hB1').cmd("dhclient -v hB1-eth0 &")
    net.get('hB2').cmd("dhclient -v hB2-eth0 &")
    net.get('hB3').cmd("dhclient -v hB3-eth0 &")
    net.get('hB4').cmd("dhclient -v hB4-eth0 &")

    print("*** Hosts acquired DHCP IP successfully")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    run_building_topo()