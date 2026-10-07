# Checkout & Order Processing Engine (Design Patterns com Spring)

## Sobre o Projeto
Este projeto foi desenvolvido como uma resolução avançada para o desafio "Explorando Padrões de Projeto na Prática com Java" da Digital Innovation One (DIO). 
Diferente de um simples CRUD, foi arquitetado um **Motor de Processamento de Pedidos (Checkout)** focando em boas práticas de engenharia de software e consolidando diversos Padrões de Projeto (GoF) nativamente integrados ao ecossistema do Spring Boot.

## Tecnologias e Stack
- **Java 17**
- **Spring Boot 3**
- **Spring Data JPA**
- **Spring Cloud OpenFeign** (Integração com a API ViaCEP para cálculo de entrega)
- **H2 Database** (Banco em memória)
- **Lombok**
- **Springdoc OpenAPI / Swagger** (Documentação interativa da API)

## Padrões de Projeto Aplicados

A arquitetura orientada ao domínio de Checkout se beneficiou dos seguintes *Design Patterns*:

1. **Singleton:** Uso transparente dos *Beans* gerenciados pelo ciclo de vida do Spring IoC (Inversion of Control) com as anotações `@Service`, `@RestController` e `@Component`.
2. **Strategy + Factory / Registry:** Implementação sofisticada das regras de métodos de pagamento (`PixPaymentStrategy`, `CreditCardPaymentStrategy`, `BoletoPaymentStrategy`). Elas são resolvidas em tempo de execução através da classe `PaymentStrategyFactory`, utilizando a injeção nativa do Spring para mapeamento, o que elimina totalmente blocos extensos e engessados de código usando `if-else` ou `switch`.
3. **Facade:** A classe `CheckoutFacade` atua orquestrando e encapsulando a enorme complexidade do sistema subjacente para a controller. Ela organiza as validações, comunicação HTTP, precificação via Strategy, persistência em banco e disparo assíncrono de eventos.
4. **Chain of Responsibility:** Criação de um robusto pipeline e encadeamento de validações (`OrderValidationChain`). Antes de gerar um pedido, o contexto é passado por uma série de validadores (`StockValidator`, `AntiFraudValidator`, `CustomerCreditValidator`). A esteira de aprovação é interrompida imediatamente caso alguma regra estrita de negócio falhe.
5. **Observer (Spring Domain Events):** Uso do `ApplicationEventPublisher` nativo do Spring para favorecer o baixo acoplamento e construir uma arquitetura orientada a eventos. Após a persistência do checkout, o núcleo emite um evento local de conclusão (`OrderProcessedEvent`), que é interceptado sem bloquear a requisição do usuário (`@Async` e `@EventListener`) pelo `OrderNotificationListener`, simulando processos complexos de backend como disparo de e-mails.

## Como Executar

1. Clone este repositório:
```bash
git clone https://github.com/guguim/project-dio.git
cd project-dio
```
2. Abra a pasta correspondente no IntelliJ IDEA, VS Code ou Eclipse.
3. Aguarde o download das dependências do `pom.xml` via Maven.
4. Rode o arquivo principal `PatternsApplication.java`.

### Acessos Importantes (Local)
Com a aplicação em execução na porta 8080, acesse pelo seu navegador:
- 📖 **Swagger UI (Documentação):** [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
- 🗄️ **H2 Console:** [http://localhost:8080/h2-console](http://localhost:8080/h2-console)
  - *JDBC URL:* `jdbc:h2:mem:patternsdb`
  - *User:* `sa` (senha em branco)

### Testando a API
Faça uma requisição REST POST para a rota de checkout utilizando ferramentas como Postman, Insomnia ou o próprio Swagger, usando um *payload* de exemplo:
**POST** `http://localhost:8080/api/v1/checkout`
```json
{
  "customerId": 1500,
  "cep": "01001000",
  "baseAmount": 100.00,
  "paymentType": "PIX"
}
```

