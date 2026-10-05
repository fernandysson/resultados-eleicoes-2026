#!/usr/bin/env python3

from pydantic import BaseModel, HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
import utils as u

class Settings(BaseSettings):
    url_base: HttpUrl  = "https://resultados-sim.tse.jus.br/simulado" # "https://resultados.tse.jus.br"
    ambiente: str = "simulado2026"
    ciclo: str = "ele2026"
    cd_eleicao: str = "21272"
    pleito: str = "017801"
    eleicao_federal_cd: str = "21271"
    eleicao_estadual_cd: str = "21272"
    cargo_presidente: str = "000001"
    cargo_governador: str = "000003"
    cargo_senador: str = "000005"
    cargo_dep_fed: str = "000006"
    cargo_dep_est: str = "000007"
    cargo_dep_dis: str = "000008"
    uf: str = "ba"
    pull_configs: bool = False
    max_threads: int = 4
    zonas_filename: str = "datasets/zonas_2026.csv"
    debug: bool = False
    enable_totalizacao: bool = True
    municipio: str = ""
    federacao_pt: str = "PT"
    federacao_psol: str = "PSOL"
    json_keyfile: str = ""
    enable_upload: bool = True
    @computed_field
    @property
    def cd6_eleicao(self) -> str:
        return(u.cd_char6(self.cd_eleicao))
            
    @computed_field
    @property
    def url_base_full(self) -> HttpUrl:
        return f"{self.url_base}/{self.ambiente}/{self.ciclo}/{self.cd_eleicao}"

    @computed_field
    @property
    def url_config(self) -> HttpUrl:
        return f"{self.url_base_full}/config"

    @computed_field
    @property
    def url_general_config(self) -> HttpUrl:
        return f"{self.url_base}/{self.ambiente}/comum/config/ele-c.json"

    
    @computed_field
    @property
    def url_config_secoes(self) -> HttpUrl:
        return f"{self.url_base}/{self.ambiente}/{self.ciclo}/arquivo-urna/{self.pleito[2:]}/config"


    @computed_field
    @property
    def url_dados(self) -> HttpUrl:
        return f"{self.url_base_full}/dados"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
