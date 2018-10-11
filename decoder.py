import base64
import gzip
import shutil
import xml.etree.ElementTree as ET
import psycopg2


NAMESPACE = {'nfe': "http://www.portalfiscal.inf.br/nfe"}


class Nfe:
    produtos = []
    fornecedor = {}
    dados_nfe = {}


def get_encoded_nfe_gzip(idnfe, config):
    '''Consulta ID da NFE no banco de dados'''

    conn = psycopg2.connect(
        f"dbname=erp user=postgres password=123456 host={config.ip}")
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                "select xmls_texto from xmlnfe where xmls_idnfe=%s", (idnfe,))
            return curs.fetchone()


def encoded_text_to_binary(encoded_str, path):
    '''Converte de texto para binário e salva no disco'''
    xml_zip_decode = base64.decodestring(encoded_str.encode())
    image_result = open(path, 'wb')
    image_result.write(xml_zip_decode)


def extract_xml(path_gz, path_xml):
    '''Extrai arquivo xml para o disco'''
    with gzip.open(path_gz, 'r') as f_in, open(path_xml, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def get_data_of_nfe(path_xml):
    '''Abre e itera o XML'''
    nfe = Nfe()
    tree = ET.parse(path_xml)
    root = tree.getroot()

    xml_produtos = root[0][0].findall('./nfe:det/nfe:prod', NAMESPACE)
    xml_fornecedor = root[0][0].findall('./nfe:emit', NAMESPACE)
    xml_nfe = root[0][0].findall('./nfe:ide', NAMESPACE)
    produtos = []
    for item in xml_produtos:
        produtos.append((item.find('nfe:cEAN', NAMESPACE).text or "",
                         item.find('nfe:xProd', NAMESPACE).text.title()))
    fornecedor = {}
    for item in xml_fornecedor:
        fornecedor['cnpj'] = item.find('nfe:CNPJ', NAMESPACE).text
        fornecedor['nome'] = item.find('nfe:xNome', NAMESPACE).text

    dados_nfe = {}
    for item in xml_nfe:
        dados_nfe['numero'] = item.find('nfe:nNF', NAMESPACE).text
        dados_nfe['serie'] = item.find('nfe:serie', NAMESPACE).text

    nfe.produtos = produtos
    nfe.fornecedor = fornecedor
    nfe.dados_nfe = dados_nfe

    return nfe
