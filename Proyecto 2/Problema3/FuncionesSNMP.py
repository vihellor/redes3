from pysnmp.hlapi import *
import time
import rrdtool
import xml.etree.cElementTree as ET
import multiprocessing
tiempoInicio= int(time.time())

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad, mpModel=0),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))
    if errorIndication:
        print(errorIndication)
        resultado = "-1"
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        resultado = "-1"
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            if oid == '1.3.6.1.2.1.1.1.0':
                resultado = varB
            else:
                resultado= varB.split()[2]
    return resultado

def ObtenerDatosPrincipales (agente):
    tree = ET.parse('agentesAgregados.xml')
    root2 = tree.findall("dispositivo")
    DatosAgente = ""
    for dispositivo  in root2:
        if dispositivo.attrib['name'] == agente:
            nombre = dispositivo.findtext("nombre")
            version = dispositivo.findtext("version")
            comunidad = dispositivo.findtext("comunidad")
            so = consultaSNMP(str(comunidad), nombre, '1.3.6.1.2.1.1.1.0')
            localizacion = consultaSNMP(str(comunidad), str(nombre), '1.3.6.1.2.1.1.6.0')
            tiempoConectado = consultaSNMP(str(comunidad), str(nombre), '1.3.6.1.2.1.1.3.0')
            puerto = "9001"
            DatosAgente = "Nombre del agente: "+nombre+"\n"+"Version SNMP: "\
                          +version+"\n Comunidad SNMP: "+comunidad+"\n Sistema Operativo: "\
                          +so+"\n Localizacion: "+localizacion+"\n Tiempo conectado(ms): "\
                          +tiempoConectado+"\n Puerto: "+puerto
    return DatosAgente
def VerificarArgumentos(nombre, comunidad):
    resultado = consultaSNMP(str(comunidad),str(nombre),'1.3.6.1.2.1.1.1.0')
    return resultado

def VerificarActividad (agente):
    tree = ET.parse('agentesAgregados.xml')
    root2 = tree.findall("dispositivo")
    resultado = ""
    for dispositivo in root2:
        if dispositivo.attrib['name'] == agente:
            nombre = dispositivo.findtext("nombre")
            version = dispositivo.findtext("version")
            comunidad = dispositivo.findtext("comunidad")
            resultado = consultaSNMP(str(comunidad), nombre, '1.3.6.1.2.1.1.1.0')
    if resultado == "-1":
        return -1
    else:
        return 1

def CreacionAgenteRDDTOOL(agente, tiempoInicio2):
    nombrerdd = agente + ".rrd"
    nombreXML= agente + ".xml"
    ret = rrdtool.create(str(nombrerdd),"--step", "3",
                         "--start", str(tiempoInicio2),
                         "DS:ipIn:COUNTER:60:U:U",
                         "DS:ipOut:COUNTER:60:U:U",
                         "DS:icmpIn:COUNTER:60:U:U",
                         "DS:icmpOut:COUNTER:60:U:U",
                         "DS:TCP:COUNTER:60:U:U",
                         "DS:TCPIn:COUNTER:60:U:U",
                         "DS:TCPOut:COUNTER:60:U:U",
                         "DS:SNMPIn:COUNTER:60:U:U",
                         "DS:SNMPOut:COUNTER:60:U:U",
                         "RRA:AVERAGE:0.5:1:5",
                         "RRA:AVERAGE:0.5:1:2016",
                     	 "RRA:HWPREDICT:1440:0.1:0.0035:288",
                         "RRA:FAILURES:1d:7:9:5"
                         )
    rrdtool.dump(str(nombrerdd),str(nombreXML));

def MoniteroAgente(comunidad,agente,tiempoInicio2):
    nombrerdd = agente + ".rrd"
    nombreXML= agente + ".xml"
    tree = ET.parse('agentesAgregados.xml')
    root2 = tree.findall("dispositivo")


    i = 0
    while(i<1):
        for dispositivo in root2:
            if dispositivo.attrib['name'] ==agente:

                #valor = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.4.3.0')) #PaquetesEntradaIP
                #valor2= int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.4.10.0')) #PaquetesSalidaIP
                #valor3 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.5.1.0')) #PaquetesEntradaICMP
                #valor4 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.5.14.0')) #PaquetesSalidaICMP 
		valor = valor2 = valor3 = valor4 = valor7 = 0
                #CAMBIAR LAS VARIABLES
                valor5 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.4.1.2021.4.6.0')) #MEMORIA RAM EN USO

                valor6 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.4.1.2021.9.1.8.1')) #ALMACENAMIENTO

                #valor7 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.6.11.0')) #Segmentos TCPEnviados

                valor8 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.25.3.3.1.2.196609')) #USO DE CPU
                print valor8

                valor9 = int(consultaSNMP(str(comunidad), str(agente), '1.3.6.1.2.1.11.2.0'))  #PaquetesSNMPEnviados
                upd = rrdtool.update(str(nombrerdd), 'N:%s:%s:%s:%s:%s:%s:%s:%s:%s'%((valor),valor2,valor3,valor4,valor5,valor6,valor7,valor8,valor9))
                rrdtool.dump(str(nombrerdd), str(nombreXML));
                #print rrdtool.fetch(str(nombrerdd), 'AVERAGE',
                  #                      "--start", str(tiempoInicio2),
                   #                     "--end", 'N')
                    #time.sleep()
        i += 1
    print"GRAFICA"

    gra = rrdtool.graph(str(agente + "_TCPConnections.png"),
                            "--start", str(tiempoInicio2),
                            "--end", 'N', '--watermark=playground.in.supportex.net',
                            "-w 500",
                            "DEF:myTCP=" + str(nombrerdd) + ":TCP:AVERAGE",
                            "CDEF:idle=myTCP,0.00,EQ,INF,0,IF",
                            "VDEF:avg=myTCP,AVERAGE",
                            "VDEF:slope=myTCP,LSLSLOPE",
                            "VDEF:cons=myTCP,LSLINT",
                            "CDEF:lsl2=myTCP,POP,slope,COUNT,*,cons,+",
                            "CDEF:pred=lsl2,90,100,LIMIT",
                            "VDEF:minpred=pred,FIRST",
                            "VDEF:maxpred=pred,LAST",
                            "GPRINT:myTCP:AVERAGE:'PR\: %8.0lf'",
                            "AREA:myTCP#f2e46a:'Ar'",
                            "AREA:idle#282720",
                            "AREA:pred#BCD2EE",
                            "LINE2:avg#00FF00:Avg:dashes=5",
                            "LINE3:lsl2#ff0000:Least Sqr Pred.\n:dashes=8",
                            "LINE2:90",
                            "AREA:5#FF000022::STACK",
                            "AREA:5#FF000044::STACK",
                            "GPRINT:minpred:'EX 90 on \: %c\n':strftime",
                            "GPRINT:maxpred:'Ex 100 on \: %c\n':strftime",
                            "COMMENT:'\s'",
                            "LINE1:myTCP#FF0000:Memoria Ram en uso\r")

    gra = rrdtool.graph(str(agente + "_TCPSegments.png"),
                            "--start", str(tiempoInicio2),
                            "--end", 'N', '--watermark=playground.in.supportex.net',
                            "-w 500",
                            "DEF:myTCPIn=" + str(nombrerdd) + ":TCPIn:AVERAGE",
                            "CDEF:idle=myTCPIn,0.00,EQ,INF,0,IF",
                            "VDEF:avg=myTCPIn,AVERAGE",
                            "VDEF:slope=myTCPIn,LSLSLOPE",
                            "VDEF:cons=myTCPIn,LSLINT",
                            "CDEF:lsl2=myTCPIn,POP,slope,COUNT,*,cons,+",
                            "CDEF:pred=lsl2,90,100,LIMIT",
                            "VDEF:minpred=pred,FIRST",
                            "VDEF:maxpred=pred,LAST",
                            "GPRINT:myTCPIn:AVERAGE:'PR\: %8.0lf'",
                            "AREA:myTCPIn#00B2EE:'Area'",
                            "AREA:idle#AFEEEE",
                            "AREA:pred#BCD2EE",
                            "LINE2:avg#00FF00:Avg:dashes=5",
                            "LINE3:lsl2#ff0000:Least Sqr Pred.\n:dashes=8",
                            "LINE2:90",
                            "AREA:5#FF000022::STACK",
                            "AREA:5#FF000044::STACK",
                            "GPRINT:minpred:'Ex 90 \: %c\n':strftime",
                            "GPRINT:maxpred:'Ex 100 on \: %c\n':strftime",
                            "COMMENT:'\s'",
                            "LINE1:myTCPIn#FF0000:Almacenamiento en uso\r")

    gra = rrdtool.graph(str(agente + "_SNMPPackets.png"),
                            "--start", str(tiempoInicio2),
                            "--end", 'N', '--watermark=playground.in.supportex.net',
                            "-w 500",
                            "DEF:mySNMPIn=" + str(nombrerdd) + ":SNMPIn:AVERAGE",
                            "DEF:pred="+ str(nombrerdd) +":SNMPIn:HWPREDICT",
                            "DEF:dev="+ str(nombrerdd) +":SNMPIn:DEVPREDICT",
			    "DEF:fail="+ str(nombrerdd) +":SNMPIn:FAILURES",
                            "TICK:fail#ffffa0:1.0:Fallo",
                            # "RRA:DEVSEASONAL:1d:0.1:2",
                            # "RRA:DEVPREDICT:5d:5",
                            # "RRA:FAILURES:1d:7:9:5""
                            "CDEF:scaledobs=mySNMPIn,8,*",
                            "CDEF:upper=pred,dev,2,*,+",
                            "CDEF:lower=pred,dev,2,*,-",
                            "CDEF:scaledupper=upper,8,*",
                            "CDEF:scaledlower=lower,8,*",
                            "LINE1:scaledobs#00FF00:Uso CPU",
                            "LINE1:scaledupper#ff0000:UMBRAL S.",
                            "LINE1:scaledlower#ff0000:UMBRAL I.")

    print ":D\n"

#CreacionAgenteRDDTOOL("Windows")
#CreacionAgenteRDDTOOL("Ubuntu")
#CreacionAgenteRDDTOOL("Windows3")

piscina = []

# Creamos la piscina (Pool)
def Monitoreo():
    tree = ET.parse('agentesAgregados.xml')
    root2 = tree.findall("dispositivo")
    i=0
    for dispositivo in root2:
        nombre =  dispositivo.findtext("nombre")
        comunidad = dispositivo.findtext("comunidad")
        piscina.append(multiprocessing.Process(name="Proceso {0}".format(nombre+str(i)), target=MoniteroAgente, args=(comunidad,nombre,tiempoInicio)))
        i+=1
    for proceso in piscina:
        proceso.start()
    #print("PADRE: esperando a que los procesos hijos hagan su trabajo")
    #print piscina
    # Mientras la piscina tenga procesos
    while piscina:
        # Para cada proceso de la piscina
        for proceso in piscina:
            # Revisamos si el proceso ha muerto
            if not proceso.is_alive():
                # Recuperamos el proceso y lo sacamos de la piscina
                proceso.join()
                piscina.remove(proceso)
                del (proceso)

        # Para no saturar, dormimos al padre durante 1 segundo
        #print("PADRE: esperando a que los procesos hijos hagan su trabajo")
        #time.sleep(1)

def AgregarMultiProceso():
    print("Se eliminara proceso")
    #print piscina
    for proceso in piscina:
        proceso.join()
        piscina.remove(proceso)
        proceso.cancel()
        del (proceso)
        print "Elimino proceso"
