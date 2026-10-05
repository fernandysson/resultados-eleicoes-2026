#!/usr/bin/env python3

import pandas as pd
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

from config import settings
import utils as u

logger = logging.getLogger(__name__)

def get_json(url, wait=False):
    r = requests.get(url)
    if wait:
        result = url
    else:
        result = r.json()
    logger.debug(result)
    return result

def pull_configs(eleicao, filename):
    _r = r.get_mun_config(eleicao)
    df = u.zona2df(_r)
    df.to_csv(filename, index=False)
    return df

def mun_config_file(eleicao):
    return f"mun-e{eleicao}-cm.json"

def secoes_config_file(pleito, uf):
    return f"{uf}/{uf}-p{pleito}-cs.json"

def secoes_unificado_file(eleicao, cargo, uf, mun, zona):
    return f"{uf}/{uf}{mun}-z{zona}-c{cargo}-e{eleicao}-u.json"

def get_general_config():
    url = settings.url_general_config
    logger.info(f"URL: {url}")
    return get_json(url)

def get_mun_config(eleicao):
    logger.info(f"Eleição: {eleicao}")
    url = f"{settings.url_config}/{mun_config_file(eleicao)}"
    logger.info(f"URL: {url}")
    return get_json(url)

def get_secoes_config(pleito, uf):    
    logger.info(f"Pleito: {pleito} \t UF: {uf}")
    url = f"{settings.url_config_secoes}/{secoes_config_file(pleito,uf)}"
    logger.info(f"URL: {url}")
    return get_json(url)

def get_zonas_unificadas(eleicao, cargo, uf, mun_cd, mun, zona):
    eleicao = u.normalize_chars(eleicao, 6)
    cargo = u.normalize_chars(cargo, 4)
    mun_cd = u.normalize_chars(mun_cd, 5)
    zona = u.normalize_chars(zona, 4)
    url = f"{settings.url_dados}/{secoes_unificado_file(eleicao, cargo, uf, mun_cd, zona)}"
    logger.info(f"URL: {url}")

    return (uf, mun_cd, mun, zona, get_json(url))


def parallel_get_zonas(df, eleicao, cargo, uf, mun=None):
    logger.info(f"ELEICAO {eleicao}, CARGO {cargo}")
    if mun:
        df = df[(df["mun"] == mun)]
    df = df[(df["uf"] == uf)][["uf", "mun_cd", "mun", "zona"]]
    df["mun_cd"] = df["mun_cd"].apply(u.cd_char6)
    df["zona"] = df["zona"].apply(u.cd_char6).apply(lambda x: x[2:])
    with ThreadPoolExecutor(max_workers=settings.max_threads) as executor:
        resp_zonas = list(executor.map(lambda args: get_zonas_unificadas(eleicao, cargo, *tuple(args)), df.values.tolist()))
    return resp_zonas

