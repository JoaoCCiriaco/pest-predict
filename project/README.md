# Soluinsect - Sistema de Controle de Pragas

## Descrição

O Soluinsect é um sistema web desenvolvido para auxiliar no gerenciamento de caixas de monitoramento utilizadas em serviços de controle de pragas.

O sistema permite cadastrar clientes, cadastrar caixas de monitoramento, registrar inspeções realizadas pelos técnicos e consultar o histórico de cada caixa.

Cada caixa possui um QR Code que permite acessar rapidamente o histórico durante uma inspeção.

## Objetivo

O objetivo do projeto é digitalizar o processo de monitoramento das caixas de controle de pragas, reduzindo registros manuais e facilitando o acompanhamento das inspeções realizadas pelos técnicos.

## Funcionalidades

- Cadastro de clientes
- Edição de clientes
- Exclusão de clientes
- Cadastro de caixas
- Edição de caixas
- Exclusão de caixas
- Cadastro de inspeções
- Edição de inspeções
- Exclusão de inspeções
- Histórico individual de cada caixa
- Registro do técnico responsável
- Registro automático do horário
- Registro de consumo de isca
- Registro de observações
- QR Code individual para cada caixa
- Dashboard com indicadores
- Gráfico de resultados das inspeções
- Visualização da última inspeção

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js

## Estrutura do projeto

```text
project/
│
├── app.py
├── database.py
├── database.db
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── clientes.html
    ├── lista_clientes.html
    ├── editar_cliente.html
    ├── caixas.html
    ├── lista_caixas.html
    ├── editar_caixa.html
    ├── nova_inspecao.html
    ├── nova_inspecao_caixa.html
    ├── editar_inspecao.html
    ├── historico_caixa.html
    └── qr_code_caixa.html

