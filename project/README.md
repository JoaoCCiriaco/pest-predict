# Sistema de Controle de Caixas de Rato - Soluinsect

## Sobre o projeto

Este projeto foi desenvolvido para auxiliar no controle de caixas de rato utilizadas em serviços de controle de pragas. A ideia surgiu da necessidade de organizar de forma mais prática as informações sobre os clientes, as caixas instaladas em cada local e as inspeções realizadas pelos técnicos.

Em vez de depender apenas de anotações ou registros separados, o sistema reúne essas informações em um único lugar. Dessa forma, é possível saber quais caixas estão cadastradas, em qual cliente e local cada uma está instalada, qual é o seu status e quais inspeções já foram realizadas.

O sistema também foi pensado para facilitar o trabalho durante uma inspeção. Cada caixa pode possuir um QR Code próprio. Ao escanear esse QR Code, o técnico pode acessar diretamente a página de registro de uma nova inspeção daquela caixa, evitando a necessidade de procurar manualmente a caixa no sistema.

## Como o sistema funciona

O sistema possui um painel inicial que apresenta um resumo das informações cadastradas. Nesse painel é possível visualizar a quantidade total de caixas, caixas ativas e inativas, quantidade de clientes, número de inspeções realizadas e quantidade de inspeções em que foi registrado consumo de isca.

Também existe um gráfico que apresenta a relação entre inspeções com consumo e inspeções sem consumo. O painel mostra ainda os dados da última inspeção realizada, incluindo cliente, local, caixa, técnico, data, horário, consumo e observações.

## Clientes

O sistema permite cadastrar clientes informando nome, telefone e e-mail.

Depois do cadastro, os clientes podem ser visualizados em uma lista e seus dados podem ser editados. Também é possível excluir um cliente. Quando um cliente é excluído, suas caixas e as inspeções relacionadas a essas caixas também são removidas para evitar que permaneçam registros relacionados a um cliente que não existe mais no sistema.

## Caixas

As caixas de rato são cadastradas e vinculadas a um cliente.

Para cada caixa são armazenadas informações como:

- Cliente responsável;
- Local onde a caixa está instalada;
- Status da caixa;
- Identificação da caixa através de um número.

As caixas podem ser visualizadas em uma lista, editadas ou excluídas.

O sistema também permite consultar o histórico individual de cada caixa.

## Inspeções

As inspeções são a principal forma de registrar o acompanhamento das caixas.

Ao realizar uma inspeção, o sistema registra:

- Data da inspeção;
- Horário;
- Técnico responsável;
- Se houve ou não consumo de isca;
- Observações realizadas durante a inspeção.

Cada inspeção fica vinculada à caixa correspondente. Dessa forma, o histórico de uma caixa permite consultar todas as inspeções realizadas anteriormente naquele ponto.

As inspeções também podem ser editadas ou excluídas quando necessário.

## Histórico das caixas

Cada caixa possui uma página de histórico própria.

Nessa página são apresentados os dados do cliente, local e status da caixa, além de uma tabela contendo todas as inspeções registradas.

O histórico apresenta a data, horário, técnico, informação sobre consumo e observações de cada inspeção. Também é possível criar uma nova inspeção diretamente a partir dessa página.

Isso permite acompanhar a evolução de cada caixa ao longo do tempo e consultar registros anteriores sempre que necessário.

## QR Code

Uma das funcionalidades desenvolvidas para facilitar o trabalho em campo é o QR Code individual de cada caixa.

O sistema gera uma página específica para o QR Code de cada caixa, mostrando informações como cliente, local e status.

O QR Code contém o endereço da página de nova inspeção daquela caixa. Assim, o técnico pode escanear o código durante uma visita e acessar diretamente o formulário de inspeção correspondente.

A página também possui uma opção para imprimir o QR Code, permitindo que ele seja colocado fisicamente na caixa.

## Banco de dados

O projeto utiliza SQLite para armazenar os dados.

O banco possui tabelas para clientes, caixas e inspeções. As caixas possuem uma relação com os clientes e as inspeções possuem uma relação com as caixas.

Essa estrutura permite manter os registros organizados e relacionar cada inspeção ao local e ao cliente correto.

O arquivo `database.py` é responsável pela criação das tabelas principais do banco de dados, enquanto o `app.py` realiza as operações de consulta, cadastro, edição e exclusão das informações.

## Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- QRCode.js

O Flask é utilizado para criar as rotas e controlar a lógica da aplicação. O SQLite é utilizado para armazenar os dados. HTML e CSS são utilizados na construção e estilização das páginas, enquanto JavaScript é utilizado em funcionalidades como o gráfico do painel e a geração dos QR Codes.

## Estrutura do projeto

`app.py` contém a aplicação principal em Flask, suas rotas e a lógica de funcionamento do sistema.

`database.py` é responsável pela configuração inicial das tabelas do banco de dados.

`database.db` é o banco de dados SQLite utilizado pela aplicação.

A pasta `templates` contém as páginas HTML utilizadas pelo sistema.

A pasta `static` contém arquivos estáticos utilizados pela aplicação.

`styles.css` contém estilos utilizados na interface.

## Objetivo

O objetivo deste projeto é criar uma ferramenta simples e prática para auxiliar no gerenciamento de caixas de rato utilizadas em serviços de controle de pragas.

A aplicação busca centralizar os registros de clientes, caixas e inspeções, facilitar o acompanhamento do consumo de isca e manter um histórico organizado das atividades realizadas em cada caixa.

Além disso, o uso de QR Codes foi pensado para aproximar o sistema da rotina de trabalho em campo, tornando o registro de uma inspeção mais rápido e reduzindo a necessidade de procurar manualmente uma caixa dentro do sistema.


VIDEO: 
https://youtu.be/YRD8hG1N2X8
