import logging
import pandas as pd
import json

from config import settings
import resultados as r
import utils as u
import upload

logger = logging.getLogger(__name__)


def main():

    logging_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    logger.info(settings)

    uf = settings.uf
    eleicao = settings.cd6_eleicao
    cargo = settings.cargo_dep_fed

    
    if settings.debug:
        general_config = r.get_general_config()
        logger.debug(json.dumps(general_config, indent=4))
    
    if settings.pull_configs:
        df = r.pull_configs(cd6_eleicao, settings.zonas_filename)
    else:
        df = pd.read_csv(settings.zonas_filename)

    logger.debug(df.head)

    if settings.enable_totalizacao:
        resp_zonas = r.parallel_get_zonas(df, eleicao, cargo, uf, mun=settings.municipio)
    
        votos_por_zona = u.agg_votos_por_zona(
            resp_zonas,
            uf,
            federacao=settings.federacao_psol,
            dataset_eleitorado=f"datasets/eleitorado_local_votacao_2026_{uf.upper()}.csv"
        )
        
        logger.info("Upload")
        logger.debug(votos_por_zona)
        if settings.enable_upload:
            upload.upload2spreadsheet(pd.DataFrame(votos_por_zona) )
        return(votos_por_zona)
    #logger.info(_r)
    
    

if __name__ == "__main__":
    main()
