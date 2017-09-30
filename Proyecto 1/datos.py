from pysnmp.hlapi import *

def datos(comunidad, ip):
	errorIndication, errorStatus, errorIndex, varBinds = next(
		nextCmd(SnmpEngine(),
		CommunityData(comunidad, mpModel=0),
		UdpTransportTarget((ip, 161)),
		ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0'))))

	if errorIndication:
		print(errorIndication)
		return None

	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
		return None
		
	else:
		datos = '' 
		for varBind in varBinds:
			data = str(varBind).split('=')
			datos = datos + ' ' + data[1] 
		return datos
