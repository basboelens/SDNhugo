#!/usr/bin/env python3

import subprocess
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class BuildingTopo(Topo):
    def build(self):
        # Add switches
        # Group 1 (2 edge switches + central)
        sA1 = self.addSwitch('sA1', dpid='00000000000000A1')
        sA2 = self.addSwitch('sA2', dpid='00000000000000A2')
        sA10 = self.addSwitch('sA10', dpid='0000000000000A10')

        # Group 2 (3 edge switches + central)
        sB1 = self.addSwitch('sB1', dpid='00000000000000B1')
        sB2 = self.addSwitch('sB2', dpid='00000000000000B2')
        sB3 = self.addSwitch('sB3', dpid='00000000000000B3')
        sB10 = self.addSwitch('sB10', dpid='0000000000000B10')

        # Add hosts for building A

        # VLAN 100
        hA1 = self.addHost('hA1', ip='10.0.10.2/24', mac='00:00:00:00:10:02')
        hA2 = self.addHost('hA2', ip='10.0.10.3/24', mac='00:00:00:00:10:03')

        # VLAN 200
        hA3 = self.addHost('hA3', ip='10.0.20.2/24', mac='00:00:00:00:20:02')

        # VLAN 300
        hA4 = self.addHost('hA4', ip='10.0.30.2/24', mac='00:00:00:00:30:02')


        # Add hosts for building B

        # VLAN 100
        hB1 = self.addHost('hB1', ip='10.0.10.4/24', mac='00:00:00:00:10:04')
        hB2 = self.addHost('hB2', ip='10.0.10.5/24', mac='00:00:00:00:10:05')

        # VLAN 200
        hB3 = self.addHost('hB3', ip='10.0.20.3/24', mac='00:00:00:00:20:03')

        # VLAN 300
        hB4 = self.addHost('hB4', ip='10.0.30.3/24', mac='00:00:00:00:30:03')

        # Connect hosts to edge switches (access ports)
        self.addLink(hA1, sA1)
        self.addLink(hA2, sA1)
        self.addLink(hA3, sA2)
        self.addLink(hA4, sA2)

        self.addLink(hB1, sB1)
        self.addLink(hB2, sB1)
        self.addLink(hB3, sB2)
        self.addLink(hB4, sB3)

        # Connect edge switches to central switches (trunk ports)
        self.addLink(sA1, sA10)
        self.addLink(sA2, sA10)
        self.addLink(sB1, sB10)
        self.addLink(sB2, sB10)
        self.addLink(sB3, sB10)

        # Connect the two central switches (trunk)
        self.addLink(sA10, sB10)

def run_building_topo():

    print("*** Running pre-topology command: sudo mc -c")
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
    CLI(net)
    net.stop()

if __name__ == "__main__":
    run_building_topo()