import xml.etree.ElementTree as ET

tree = ET.parse('config/configuration.xml')
root = tree.getroot()


def read_config(tag):
    value = root.find(tag).text
    return value
