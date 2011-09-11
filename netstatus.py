#!/usr/bin/env python3
"""This Python 3 module provides a simple wrapper to Net-SNMP in order to retrieve basic internet speed
data from a Belkin router.
"""

__author__ = 'Adam Gibson'

import time
import subprocess

class SNMPInternetStatus():
    def __init__(self, ip_address, snmp_version='2c', snmp_community='public'):
        self.ip_address = ip_address
        self.snmp_version = snmp_version
        self.snmp_community = snmp_community
        self.inboundSyncSpeed = 0
        self.outboundSyncSpeed = 0
        self.inboundAvgSpeed = 0
        self.outboundAvgSpeed = 0
        self.sample_period = 2

    def __str__(self):
        self.getSyncSpeed()
        self.getCurrentSpeed()
        divider1 = "="*45
        divider2 = "-"*45
        inSyncSpeed = str(round((self.inboundSyncSpeed/1024),2))
        inAvgSpeed = str(round((self.inboundAvgSpeed/1024),2))
        outAvgSpeed = str(round((self.outboundAvgSpeed/1024),2))
        samplePeriod = str(self.sample_period)
        outputString =  divider1 +\
                        '\nLine Sync Speed\n' +\
                        divider2 +\
                        '\nInbound: '+ inSyncSpeed + ' kbps\n' +\
                        divider1 +\
                        '\nCurrent Average Speed ' +\
                        '(' + samplePeriod + ' second average)\n' +\
                        divider2 +\
                        '\nInbound: '+ inAvgSpeed + ' kBps' +\
                        '\nOutbound: '+ outAvgSpeed + ' kBps\n' +\
                        divider1
        return outputString

    def getSNMPData(self, mib):
        #TODO Documentation
        #TODO Exception Handling
        cmd = 'snmpget -v ' + self.snmp_version + ' -c ' + self.snmp_community + ' ' + self.ip_address + ' ' + mib
        output = subprocess.getoutput(cmd)
        return output

    def getCurrentSpeed(self, sample_period=2):
        #TODO Documentation
        self.sample_period = sample_period
        mibInboundBytes = 'IF-MIB::ifOutOctets.2' #count of bytes received.
        mibOutboundBytes = 'IF-MIB::ifInOctets.2' #count of bytes sent.
        inSpeedSample1 = int(self.getSNMPData(mibInboundBytes).split()[3])
        outSpeedSample1 = int(self.getSNMPData(mibOutboundBytes).split()[3])
        time.sleep(self.sample_period)
        inSpeedSample2 = int(self.getSNMPData(mibInboundBytes).split()[3])
        outSpeedSample2 = int(self.getSNMPData(mibOutboundBytes).split()[3])
        self.inboundAvgSpeed = (inSpeedSample2 - inSpeedSample1) / sample_period #bytes per second
        self.outboundAvgSpeed = (outSpeedSample2 - outSpeedSample1) / sample_period #bytes per second
        return self.inboundAvgSpeed, self.outboundAvgSpeed

    def getSyncSpeed(self):
        #TODO Documentation
        mibInboundSync = 'IF-MIB::ifSpeed.4' # bits per second
        self.inboundSyncSpeed = int(self.getSNMPData(mibInboundSync).split()[3])
        self.outboundSyncSpeed = None #not implemented
        return self.inboundSyncSpeed, self.outboundSyncSpeed

if __name__ == '__main__':
    netSpeed = SNMPInternetStatus('10.1.1.1')
    while True:
        try:
            print(netSpeed)
        except ValueError:
            print('ValueError')
            continue