Este projeto consiste em um **Sistema Especialista** desenvolvido em Python utilizando a biblioteca `experta` (baseada no CLIPS).
O objetivo é simular o raciocínio de um geólogo especialista para classificar reservatórios de petróleo.

Através de um motor de inferência com **Encadeamento para Frente** (*Forward Chaining*), o sistema realiza uma entrevista técnica com o usuário, coletando dados geológicos e petrofísicos para determinar:

1.  **O Risco Exploratório** (Baixo, Moderado ou Alto).
2.  **A Viabilidade Comercial** (Econômica ou Inviável).

O sistema avalia diferentes caminhos baseados na entrada do usuário como:
(Tipos de Reservatório, Subtipos, Porosidade e Permeabilidade, Carbono Orgânico Total e Espessura do Reservatório).

Possibilidades Futuras:
- Substituir o terminal por uma Interface Gráfica criando formulários visuais
- Implementar Lógica Fuzzy para aceitar valores numéricos exatos
- Salvar as consultas realizadas em um banco de dados
