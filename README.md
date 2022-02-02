# cryptos-realtime


O projeto consiste em acessar a API pública da Poloniex, gerar candles de 1, 5 e 10 minutos, e depois persistir esses candles em um banco de dados.
## 
Escolhi utilizar o flask por possibilitar e as suas ferramentas para simplificar a criação de uma API REST que entregue os candles gerados.

## Utilização

- É necessário ter instalado o Docker e o docker compose
- Dentro da raiz do projeto executar:
    ```bash
    docker-compose up --build
    ```