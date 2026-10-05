#!/usr/bin/env python3

import requests
import logging
import pandas as pd

import constants as c

logger = logging.getLogger(__name__)


def zonas2df(resp_json):
    df = pd.DataFrame.from_dict({})

    _l_uf = [ abr["cd"] for abr in resp_json["abr"]]

    for uf in _l_uf:
        _l = [ abr["mu"] for abr in resp_json["abr"] if abr["cd"] == uf][0]
        _df = pd.DataFrame.from_dict(_l)
        _df["uf"] = uf
        df = pd.concat([df, _df], ignore_index=True)
    return  df


def get_zones(df, uf, mun, mun_type="nm"):
    return list(df[
        (df["uf"] == uf) & (df[mun_type] == mun)
    ]["z"])[0]


def zona2df(resp_json):
    df = pd.DataFrame.from_dict({})
    _l_uf = resp_json["abr"]
    for uf in _l_uf:
        uf_cd = uf["cd"]
        _l_mun = uf["mu"]    
        for mun in _l_mun:
            mun_nm = mun["nm"]
            mun_cd = mun["cd"]
            _df = pd.DataFrame.from_dict({"zona": mun["z"]})
            _df[["uf", "mun", "mun_cd"]] = uf_cd, mun_nm, mun_cd
            df = pd.concat([df, _df], ignore_index=True)
    return  df

def votos_secoes2df(resp_json):
    pass

def coeficiente_eleitoral(cargo, uf):
    votantes = 10000000
    if cargo == "DEP_FED":
        vagas = c.DEP_FED_UF[uf]
    return votantes / vagas

def cd_char6(cd: str) -> str:
    _cd = str(cd)
    if len(_cd) < 6:
        _extra_zeros = 6 - len(_cd)
    return str((_extra_zeros * "0")) + _cd

def normalize_chars(cd: str, n_chars: int) -> str:
    cd_int = int(cd)
    _cd = str(cd_int)
    _extra_zeros = 0
    if len(_cd) < n_chars:
        _extra_zeros = n_chars - len(_cd)
    return str((_extra_zeros * "0")) + _cd

def extract_mun_cd(df, uf, mun):
    l_cd = df[(df["uf"] == uf) & (df["mun"] == mun)]["mun_cd"].unique()
    assert len(l_cd) == 1
    return l_cd[0]
            
def extract_mun_list(df, uf):
    return df[(df["uf"] == uf)]["mun"].unique()

def extract_mun_cd_list(df, uf):
    return df[(df["uf"] == uf)]["mun_cd"].unique()

def extract_zonas_list(df, uf, mun):
    logger.debug(f"UF: {uf}\tMunicípio: {mun}")
    return df[(df["uf"] == uf) & (df["mun_cd"] == mun)]["zona"].unique()

def extract_secoes_list(df, uf, mun, zona):
    logger.debug(f"UF: {uf}\tMunicípio: {mun}\tZona: {zona}")
    return df[(df["uf"] == uf) & (df["mun_cd"] == mun) & (df["zona"])]["ns"].unique()

def agg_votos_por_zona(resp_zonas, uf, federacao, dataset_eleitorado):
    UF = uf.upper()
    filename = dataset_eleitorado
    df = pd.read_csv(
        f"datasets/eleitorado_local_votacao_2026_{uf.upper()}.csv",
        sep=";",
        encoding="latin-1"
    )
    

    
    votos_por_zona = []
    
    for _z_resp in resp_zonas:
        uf = _z_resp[0]
        mun_cd = _z_resp[1]
        mun = _z_resp[2]
        zona = _z_resp[3]
        _res = _z_resp[4]
        vv_zona = _res["v"]["vv"]
        
        # votos_por_zona[zona] = {}
        agremiacoes = _res["carg"][0]["agr"]
        
        for a in agremiacoes:
            # logger.info(a)
            if federacao in a["com"]:
                for p in a["par"]:
                    for c in p["cand"]:
                        _l = df[(df["NM_MUNICIPIO"] == mun) & (df["NR_ZONA"] == int(zona))]["NM_BAIRRO"].unique()
                        zona_nm = "-".join(_l)
                        votos_por_zona.append(
                            {
                                "zona": zona,
                                "bairros_zona": zona_nm,
                                "uf": uf,
                                "mun": mun,
                                "mun_cd": mun_cd,
                                "nome_cand": [c["nm"]][0],
                                "numero_cand": [c["n"]][0],
                                "votos": int(c["vap"]),
                                "votos_zona": int(vv_zona)
                            }
                        )
    return votos_por_zona
