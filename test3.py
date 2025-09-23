#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class BuildingTopo(Topo):
    def build(self):
        # Add switches with DPIDs matching FAUCET YAML
        s1 = self.addSwitch('s1', dpid='0000000000000001')
        s2 = self.addSwitch('s2', dpid='0000000000000002')
        s10 = self.addSwitch('s10', dpid='0000000000000010')

        s3 = self.addSwitch('s3', dpid='0000000000000003')
        s4 = self.addSwitch('s4', dpid='0000000000000004')
        s5 = self.addSwitch('s5', dpid='0000000000000005')
        s11 = self.addSwitch('s11', dpid='0000000000000011')

        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        h5 = self.addHost('h5', ip='10.0.0.5/24')

        # Connect hosts to edge switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)

        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h5, s5)

        # Connect edge switches to central switch
        self.addLink(s1, s10)
        self.addLink(s2, s10)

        self.addLink(s3, s11)
        self.addLink(s4, s11)
        self.addLink(s5, s11)

        self.addLink(s10, s11)

def run_building_topo():
    setLogLevel('info')

    topo = BuildingTopo()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6653),
        switch=OVSKernelSwitch,
        build=True
    )

    net.start()
    print("*** Network started. Available nodes:")
    print(net.hosts)
    print(net.switches)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    run_building_topo()
