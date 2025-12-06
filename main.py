import collections.abc

# --- CORREÇÃO DE COMPATIBILIDADE (Monkey Patch) ---
# Necessário para rodar 'experta' em Python 3.10+
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
# --------------------------------------------------

from experta import *

# Função auxiliar de loop while para garantir inputs corretos
def fazer_pergunta(pergunta, opcoes_validas):
    resposta = ""
    while resposta not in opcoes_validas: #enquanto a resposta não estiver nas 'opcoes_validas', o loop continua
        print(f"\n[PERGUNTA]: {pergunta}")
        print(f"Opções: {opcoes_validas}")
        resposta = input("Sua resposta: ").lower().strip() #deixa string de resposta minuscula e corta espaços em brancos
        if resposta not in opcoes_validas:
            print("Entrada inválida. Tente novamente.")
    return resposta


class ViabilidadePetroleo(KnowledgeEngine): # KnowledgeEngine comando para herdar a biblioteca experta

    # --- INÍCIO DO PROCESSO ---
    @DefFacts() # inicio do sistema, garante um fato inicial usado somente no momento que começa
    def _initial_action(self): # self é uma convenção do Python, representa parâmetro e a própria instância do objeto
        print("--- INICIANDO SISTEMA ESPECIALISTA DE VIABILIDADE DE PETRÓLEO ---")
        yield Fact(action="inicio") #yield é como se fosse um return, porém ele gera os fatos de inicialização

    # ----------------------------------------------------------------
    # PERGUNTA 1: Tipo de Reservatório
    # ----------------------------------------------------------------
    @Rule(Fact(action="inicio")) #rule transforma a função logo abaixo em uma regra de raciocínio.
    def pergunta_tipo_reservatorio(self):
        resp = fazer_pergunta(
            "Qual o tipo de reservatório?",
            ["convencional", "não convencional"]
        )
        self.declare(Fact(tipo_res=resp)) # continuidade do programa, self.declare para adicionar um novo Fato à memória de trabalho
                                          # Fact(tipo_res=resp), novo fato criado vai receber a resposta da pegunta
    # ----------------------------------------------------------------
    # PERGUNTA 2: Sub-tipos
    # ----------------------------------------------------------------

    # Caminho Convencional
    @Rule(Fact(tipo_res="convencional"))
    def pergunta_subtipo_convencional(self):
        resp = fazer_pergunta(
            "Qual o subtipo do reservatório convencional?",
            ["carbonático", "silicoclástico"]
        )
        self.declare(Fact(subtipo=resp))

    # Caminho Não Convencional
    @Rule(Fact(tipo_res="não convencional"))
    def pergunta_subtipo_nao_convencional(self):
        resp = fazer_pergunta(
            "Qual o subtipo do reservatório não convencional?",
            ["shale gas", "shale oil"]
        )
        self.declare(Fact(subtipo=resp))

    # ----------------------------------------------------------------
    # PERGUNTA 3: Critérios de Qualidade (Específicos por subtipo)
    # ----------------------------------------------------------------

    # Caso 3a: Carbonático -> Porosidade > 15% e Permeabilidade > 10mD
    @Rule(Fact(tipo_res="convencional"), Fact(subtipo="carbonático")) #se o fato tipo_res for X E o fato subtipo for Y, então faça:
    def criterio_carbonatico(self):
        resp = fazer_pergunta(
            "A porosidade é > 15% E a permeabilidade é > 10mD?",
            ["sim", "não"]
        )
        self.declare(Fact(criterio_q3=resp))

    # Caso 3b: Silicoclástico -> Porosidade > 25% e Permeabilidade > 100mD
    @Rule(Fact(tipo_res="convencional"), Fact(subtipo="silicoclástico"))
    def criterio_silicoclastico(self):
        resp = fazer_pergunta(
            "A porosidade é > 25% E a permeabilidade é > 100mD?",
            ["sim", "não"]
        )
        self.declare(Fact(criterio_q3=resp))

    # Caso 3c: Shale Gas -> COT > 4%
    @Rule(Fact(tipo_res="não convencional"), Fact(subtipo="shale gas"))
    def criterio_shale_gas(self):
        resp = fazer_pergunta(
            "O Carbono Orgânico Total (COT) é maior que 4%?",
            ["sim", "não"]
        )
        self.declare(Fact(criterio_q3=resp))

    # Caso 3d: Shale Oil -> COT > 2%
    @Rule(Fact(tipo_res="não convencional"), Fact(subtipo="shale oil"))
    def criterio_shale_oil(self):
        resp = fazer_pergunta(
            "O Carbono Orgânico Total (COT) é maior que 2%?",
            ["sim", "não"]
        )
        self.declare(Fact(criterio_q3=resp))

    # ----------------------------------------------------------------
    # PERGUNTA 4: Espessura (Acionada após termos a resposta da Q3)
    # ----------------------------------------------------------------
    @Rule(Fact(criterio_q3=MATCH.q3))
    # MATCH é um coringa da experta, usado apenas dentro da regra para capturar o valor de um Fato
    # ele captura esse valor e o armazena temporariamente na variável interna .q3
    def pergunta_espessura(self, q3):
    # A pergunta 4 é feita independente do resultado da 3,
    # pois precisamos das duas para a conclusão.
        resp = fazer_pergunta(
            "A espessura do reservatório é maior que 10m?",
            ["sim", "não"]
        )
        self.declare(Fact(criterio_q4=resp))

    # ----------------------------------------------------------------
    # CONCLUSÕES
    # ----------------------------------------------------------------

    # Cenário 1: Q3=Sim e Q4=Sim
    @Rule(Fact(criterio_q3="sim"), Fact(criterio_q4="sim"))
    def conclusao_baixo_risco(self):
        print("\n" + "=" * 60)
        print("RESULTADO: BAIXO RISCO EXPLORATÓRIO")
        print("Boas chances de comercialização do reservatório.")
        print("=" * 60 + "\n")

    # Cenário 2: Q3=Não e Q4=Não
    @Rule(Fact(criterio_q3="não"), Fact(criterio_q4="não"))
    def conclusao_alto_risco_inviavel(self):
        print("\n" + "=" * 60)
        print("RESULTADO: ALTO RISCO - INVIABILIDADE ECONÔMICA")
        print("Reservatório considerado não comercial.")
        print("=" * 60 + "\n")

    # Cenário 3: Q3=Sim e Q4=Não
    @Rule(Fact(criterio_q3="sim"), Fact(criterio_q4="não"))
    def conclusao_moderado_risco(self):
        print("\n" + "=" * 60)
        print("RESULTADO: RISCO MODERADO / RESERVATÓRIO DE BOA QUALIDADE")
        print("O reservatório possui boa qualidade de rocha, porém a espessura é baixa.")
        print("Condição: Viável se identificada alta continuidade lateral.")
        print("Caso contrário: Não comercial pelo baixo Netpay.")
        print("=" * 60 + "\n")

    # Cenário 4: Q3=Não e Q4=Sim
    @Rule(Fact(criterio_q3="não"), Fact(criterio_q4="sim"))
    def conclusao_alto_risco_baixa_qualidade(self):
        print("\n" + "=" * 60)
        print("RESULTADO: ALTO RISCO EXPLORATÓRIO (BAIXA QUALIDADE)")
        print("Embora tenha espessura, a qualidade da rocha (porosidade/perm/COT) é insuficiente.")
        print("=" * 60 + "\n")

# --- EXECUÇÃO DO SISTEMA ---
if __name__ == "__main__":
    engine = ViabilidadePetroleo()
    engine.reset()  # Prepara o motor de inferência
    engine.run()  # Executa as regras