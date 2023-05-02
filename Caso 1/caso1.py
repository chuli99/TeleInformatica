#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='192.168.100.0/24')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    
    #SWITCHES
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, failMode='standalone')

    #ROUTER PADRE
    r0 = net.addHost('r0', cls=Node, ip='192.168.100.1/29')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')

    #ROUTERS HIJOS
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.9/29')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.17/29')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r3 = net.addHost('r3', cls=Node, ip='192.168.100.25/29')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute='192.168.100.9/29')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute='192.168.100.17/29')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute='192.168.100.25/29')

    info( '*** Add links\n')
    net.addLink(r0, s1)
    net.addLink(r0, s2)
    net.addLink(r0, s3)
    net.addLink(s1, r1)
    net.addLink(s2, r2)
    net.addLink(s3, r3)
    net.addLink(r1, s4)
    net.addLink(r2, s5)
    net.addLink(r3, s6)
    net.addLink(s4, h1)
    net.addLink(s5, h2)
    net.addLink(s6, h3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s4').start([])
    net.get('s5').start([])
    net.get('s6').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


