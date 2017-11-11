import xml.etree.cElementTree as ET
import FuncionesSNMP
def agregaragente(nombre, version, comunidad):
    doc = ET.parse("agentesAgregados.xml")
    root_node = doc.getroot()
    ET.SubElement(root_node, "dispositivo", name=nombre)
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name']==nombre:
            ET.SubElement(subelemento, "nombre").text = nombre
            ET.SubElement(subelemento, "version").text = version
            ET.SubElement(subelemento, "comunidad").text = comunidad
            #Para agregar el resto de los elementos hay que hacer la consulta snmp, por lo mientras son valores estativos
            ET.SubElement(subelemento, "ip").text = "1.1.1.1"
            ET.SubElement(subelemento, "sistema-operativo").text =  str(FuncionesSNMP.consultaSNMP(str(comunidad), nombre, '1.3.6.1.2.1.1.1.0'))
            ET.SubElement(subelemento, "ubicacion").text = FuncionesSNMP.consultaSNMP(str(comunidad), str(nombre), '1.3.6.1.2.1.1.6.0')
            ET.SubElement(subelemento, "puertos").text = "8547835"
            ET.SubElement(subelemento, "actividad").text = FuncionesSNMP.consultaSNMP(str(comunidad), str(nombre), '1.3.6.1.2.1.1.3.0')
            ET.SubElement(subelemento, "estado").text = "UP"
            ET.SubElement(subelemento, "puertos-disponibles").text = "324543"
    tree = ET.ElementTree(root_node)
    tree.write("agentesAgregados.xml")
    print("Agente agregado");

def consultarcomunidad(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("comunidad").text
    return estado

def eliminaragente(nombre):
    doc = ET.parse("agentesAgregados.xml")
    root_node = doc.getroot()
    ET.SubElement(root_node, "dispositivo", name=nombre)
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            root_node.remove(subelemento)

    tree = ET.ElementTree(root_node)
    tree.write("agentesAgregados.xml")

    print("Agente eliminado");


def modificaragente(nombre, version, comunidad):
    eliminaragente(nombre)
    agregaragente(nombre, version, comunidad)
    print("Agente modificado")


def consultaragente(elemento, valor):
    resultado = []
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.find(elemento).text == valor:
            resultado.append(subelemento.attrib['name'])
    return resultado


def consultaragentes():
    agentes = []
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        agentes.append(subelemento.attrib['name'])
    return agentes


def consultarestado(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("estado").text
    return estado

def modificarestado(nombre):
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            subelemento.find("estado").text = "DOWN"

def nombres():
    estado = []
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        estado.append(subelemento.find("nombre").text)
    return estado

def ubicaciones():
    estado = []
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        estado.append(subelemento.find("ubicacion").text)
    return estado


def sistemasoperativos():
    estado = []
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        estado.append(subelemento.find("sistema-operativo").text)
    return estado

def consultarcomunidad(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("comunidad").text
    return estado
def consultarpuertos(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("puertos").text
    return estado


def consultarversion(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("version").text
    return estado


def consultarso(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("sistema-operativo").text
    return estado


def consultarubicacion(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("ubicacion").text
    return estado


def consultartiempo(nombre):
    estado = ''
    doc = ET.parse("agentesAgregados.xml")
    subelementos = doc.findall("dispositivo")
    for subelemento in subelementos:
        if subelemento.attrib['name'] == nombre:
            estado = subelemento.find("actividad").text
    return estado

