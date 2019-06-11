import pandas as pd
import re
import datetime
import json

class  Bandeco():
    def __init__(self):
        # Funções de Crawler do Cardápio

        self.guarnicao= "GUARNIÇÃO"
        self.prato_principal= "PRATO PRINCIPAL:"
        self.salada= "SALADA:"
        self.sobremesa= "SOBREMESA:"
        self.suco= "SUCO:"
        self.obs= "OBSERVAÇÕES:"
        self.dia_semana = ""
        self.dia_cardapio = []
    def extrai_refeicao(self,ref,ref_op):
        if ref_op == self.guarnicao and self.prato_principal in ref :
            return ref[0:ref.find(self.prato_principal)].strip()
        if ref_op == self.prato_principal and self.prato_principal in ref and self.salada in ref:
            pp = ref.find(self.prato_principal) + len(self.prato_principal)
            return ref[pp:ref.find(self.salada)].strip()
        elif ref_op == self.salada and self.salada in ref and self.sobremesa in ref:
            sp = ref.find(self.salada) + len(self.salada)
            return ref[sp:ref.find(self.sobremesa)].strip()
        elif ref_op == self.sobremesa and self.sobremesa in ref and self.suco in ref:
            sp = ref.find(self.sobremesa) + len(self.sobremesa)
            return ref[sp:ref.find(self.suco)].strip()
        elif ref_op == self.suco and self.suco in ref and self.obs in ref:
            sp = ref.find(self.suco) + len(self.suco)
            return ref[sp:ref.find(self.obs)].strip()
        elif ref_op == self.obs and self.obs in ref:
            op = ref.find(self.obs) + len(self.obs)
            return ref[op:].strip()
        else: return ""
    def cardapio_em_dia(self,hoje):
        """
        retorna  True se estiver atualizado
        retorna False se estiver desatualizado
        """
        d_dia_cardapio = datetime.datetime(year=self.dia_cardapio[2],month=self.dia_cardapio[1],day=self.dia_cardapio[0])
        d_hoje = datetime.datetime(year=hoje[2],month=hoje[1],day=hoje[0])
        if d_dia_cardapio >= d_hoje:
            return True
        return False
    def atualiza_cardapio(self):
        """
        Verifica e atualiza o cardápio
        """
        hoje = datetime.datetime.now()
        hoje = [hoje.day,hoje.month,hoje.year]
        if hoje != self.dia_cardapio:
            if self.dia_cardapio == []:
                self.atualiza_tabela_cardapio()
            elif not cardapio_em_dia(self.dia_cardapio,hoje):
                self.atualiza_tabela_cardapio()

    def atualiza_tabela_cardapio(self):

        # Scrapy data
        tables = pd.read_html("https://www.prefeitura.unicamp.br/apps/site/cardapio.php")

        # Parsing das refeições
        cardapio = tables[1].loc[2:].copy()
        cardapio_header = cardapio.iloc[0]
        cardapio_header.name = ''
        cardapio = pd.DataFrame(cardapio.values[1:], columns=cardapio_header)
        cafe = tables[1].loc[0:1].copy()
        cafe = cafe.drop(cafe.columns[1:],axis=1)
        cafe_header =cafe.iloc[0]
        cafe = cafe.iloc[1]
        cafe_header.name = ''
        cafe = pd.DataFrame(cafe.values, columns=cafe_header)
        cardapio = pd.concat([cardapio, cafe],axis=1)
        data = tables[0][0][0]

        # REFEIÇÕES
        self.almoco = cardapio["Almoço"].values[0].upper()
        self.almoco_veg = cardapio["Almoço Vegetariano"].values[0].upper()
        self.jantar = cardapio["Jantar"].values[0].upper()
        self.jantar_veg = cardapio["Jantar Vegetariano"].values[0].upper()
        self.cafe = cardapio["Café da manhã"].values[0].upper()
        self.dia_cardapio = [int(data) for data in (re.findall('\d{2}/\d{2}/\d{4}',data)[0].split("/")) ]
        self.dia_semana = data[data.find("(")+1:data.find(")")]






