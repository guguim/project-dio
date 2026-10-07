import os

project_dir = r"C:\Users\Users\Documents\javaprojects\project-dio"

files = {
"pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>3.3.4</version>
		<relativePath/>
	</parent>
	<groupId>com.dio</groupId>
	<artifactId>patterns</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>patterns</name>
	<description>Design Patterns com Spring Boot</description>
	<properties>
		<java.version>21</java.version>
		<spring-cloud.version>2023.0.3</spring-cloud.version>
	</properties>
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-jpa</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-validation</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
		<dependency>
			<groupId>com.h2database</groupId>
			<artifactId>h2</artifactId>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
			<optional>true</optional>
		</dependency>
		<dependency>
			<groupId>org.springdoc</groupId>
			<artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
			<version>2.5.0</version>
		</dependency>
	</dependencies>
	<dependencyManagement>
		<dependencies>
			<dependency>
				<groupId>org.springframework.cloud</groupId>
				<artifactId>spring-cloud-dependencies</artifactId>
				<version>${spring-cloud.version}</version>
				<type>pom</type>
				<scope>import</scope>
			</dependency>
		</dependencies>
	</dependencyManagement>
	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>
</project>""",

"src/main/resources/application.yml": """spring:
  application:
    name: patterns
  datasource:
    url: jdbc:h2:mem:patternsdb
    driverClassName: org.h2.Driver
    username: sa
    password: 
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
  h2:
    console:
      enabled: true
      path: /h2-console
  cloud:
    openfeign:
      client:
        config:
          default:
            connectTimeout: 5000
            readTimeout: 5000
server:
  port: 8080
""",

"src/main/java/com/dio/patterns/PatternsApplication.java": """package com.dio.patterns;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.scheduling.annotation.EnableAsync;

@EnableFeignClients
@EnableAsync
@SpringBootApplication
public class PatternsApplication {
	public static void main(String[] args) {
		SpringApplication.run(PatternsApplication.class, args);
	}
}""",

"src/main/java/com/dio/patterns/model/enums/PaymentType.java": """package com.dio.patterns.model.enums;

public enum PaymentType {
    PIX,
    CREDIT_CARD,
    BOLETO
}""",

"src/main/java/com/dio/patterns/model/enums/OrderStatus.java": """package com.dio.patterns.model.enums;

public enum OrderStatus {
    PENDING,
    PROCESSED,
    FAILED,
    REJECTED
}""",

"src/main/java/com/dio/patterns/model/entity/Address.java": """package com.dio.patterns.model.entity;

import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Embeddable
public class Address {
    private String cep;
    private String logradouro;
    private String complemento;
    private String bairro;
    private String localidade;
    private String uf;
}""",

"src/main/java/com/dio/patterns/model/entity/OrderEntity.java": """package com.dio.patterns.model.entity;

import com.dio.patterns.model.enums.OrderStatus;
import com.dio.patterns.model.enums.PaymentType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "orders")
public class OrderEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long customerId;
    
    @Embedded
    private Address deliveryAddress;
    
    private BigDecimal baseAmount;
    private BigDecimal totalAmount;
    
    @Enumerated(EnumType.STRING)
    private PaymentType paymentType;
    
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    
    private LocalDateTime createdAt;
}""",

"src/main/java/com/dio/patterns/model/dto/CheckoutRequest.java": """package com.dio.patterns.model.dto;

import com.dio.patterns.model.enums.PaymentType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.math.BigDecimal;

public record CheckoutRequest(
    @NotNull Long customerId,
    @NotBlank String cep,
    @NotNull @Positive BigDecimal baseAmount,
    @NotNull PaymentType paymentType
) {}""",

"src/main/java/com/dio/patterns/model/dto/CheckoutResponse.java": """package com.dio.patterns.model.dto;

import com.dio.patterns.model.enums.OrderStatus;
import java.math.BigDecimal;

public record CheckoutResponse(
    Long orderId,
    OrderStatus status,
    BigDecimal baseAmount,
    BigDecimal finalAmount,
    String message
) {}""",

"src/main/java/com/dio/patterns/repository/OrderRepository.java": """package com.dio.patterns.repository;

import com.dio.patterns.model.entity.OrderEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<OrderEntity, Long> {
}""",

"src/main/java/com/dio/patterns/client/ViaCepClient.java": """package com.dio.patterns.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "viacep", url = "https://viacep.com.br/ws")
public interface ViaCepClient {

    @GetMapping("/{cep}/json/")
    AddressDto getAddressByCep(@PathVariable("cep") String cep);
}""",

"src/main/java/com/dio/patterns/client/AddressDto.java": """package com.dio.patterns.client;

public record AddressDto(
    String cep,
    String logradouro,
    String complemento,
    String bairro,
    String localidade,
    String uf
) {}""",

"src/main/java/com/dio/patterns/service/chain/OrderValidationContext.java": """package com.dio.patterns.service.chain;

import com.dio.patterns.model.dto.CheckoutRequest;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderValidationContext {
    private CheckoutRequest request;
    private boolean isValid;
    private String validationMessage;
}""",

"src/main/java/com/dio/patterns/service/chain/OrderValidationHandler.java": """package com.dio.patterns.service.chain;

public interface OrderValidationHandler {
    void validate(OrderValidationContext context);
}""",

"src/main/java/com/dio/patterns/service/chain/StockValidator.java": """package com.dio.patterns.service.chain;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(1)
public class StockValidator implements OrderValidationHandler {
    @Override
    public void validate(OrderValidationContext context) {
        if (context.getRequest().baseAmount().doubleValue() < 0) {
            context.setValid(false);
            context.setValidationMessage("Items out of stock or invalid amount");
        }
    }
}""",

"src/main/java/com/dio/patterns/service/chain/AntiFraudValidator.java": """package com.dio.patterns.service.chain;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(2)
public class AntiFraudValidator implements OrderValidationHandler {
    @Override
    public void validate(OrderValidationContext context) {
        if (context.getRequest().baseAmount().doubleValue() > 10000) {
            context.setValid(false);
            context.setValidationMessage("Order rejected by Anti-Fraud System");
        }
    }
}""",

"src/main/java/com/dio/patterns/service/chain/CustomerCreditValidator.java": """package com.dio.patterns.service.chain;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(3)
public class CustomerCreditValidator implements OrderValidationHandler {
    @Override
    public void validate(OrderValidationContext context) {
        if (context.getRequest().customerId() == null || context.getRequest().customerId() <= 0) {
            context.setValid(false);
            context.setValidationMessage("Invalid customer or insufficient credit");
        }
    }
}""",

"src/main/java/com/dio/patterns/service/chain/OrderValidationChain.java": """package com.dio.patterns.service.chain;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class OrderValidationChain {

    private final List<OrderValidationHandler> validators;

    public OrderValidationChain(List<OrderValidationHandler> validators) {
        this.validators = validators;
    }

    public OrderValidationContext execute(OrderValidationContext context) {
        for (OrderValidationHandler validator : validators) {
            validator.validate(context);
            if (!context.isValid()) {
                break;
            }
        }
        return context;
    }
}""",

"src/main/java/com/dio/patterns/service/strategy/PaymentStrategy.java": """package com.dio.patterns.service.strategy;

import com.dio.patterns.model.enums.PaymentType;
import java.math.BigDecimal;

public interface PaymentStrategy {
    BigDecimal calculateFinalAmount(BigDecimal baseAmount);
    PaymentType getPaymentType();
}""",

"src/main/java/com/dio/patterns/service/strategy/PixPaymentStrategy.java": """package com.dio.patterns.service.strategy;

import com.dio.patterns.model.enums.PaymentType;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;

@Component
public class PixPaymentStrategy implements PaymentStrategy {
    @Override
    public BigDecimal calculateFinalAmount(BigDecimal baseAmount) {
        return baseAmount.multiply(BigDecimal.valueOf(0.95)); // 5% discount
    }

    @Override
    public PaymentType getPaymentType() {
        return PaymentType.PIX;
    }
}""",

"src/main/java/com/dio/patterns/service/strategy/CreditCardPaymentStrategy.java": """package com.dio.patterns.service.strategy;

import com.dio.patterns.model.enums.PaymentType;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;

@Component
public class CreditCardPaymentStrategy implements PaymentStrategy {
    @Override
    public BigDecimal calculateFinalAmount(BigDecimal baseAmount) {
        return baseAmount.multiply(BigDecimal.valueOf(1.03)); // 3% fee
    }

    @Override
    public PaymentType getPaymentType() {
        return PaymentType.CREDIT_CARD;
    }
}""",

"src/main/java/com/dio/patterns/service/strategy/BoletoPaymentStrategy.java": """package com.dio.patterns.service.strategy;

import com.dio.patterns.model.enums.PaymentType;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;

@Component
public class BoletoPaymentStrategy implements PaymentStrategy {
    @Override
    public BigDecimal calculateFinalAmount(BigDecimal baseAmount) {
        return baseAmount; // No discount, no fee
    }

    @Override
    public PaymentType getPaymentType() {
        return PaymentType.BOLETO;
    }
}""",

"src/main/java/com/dio/patterns/service/strategy/PaymentStrategyFactory.java": """package com.dio.patterns.service.strategy;

import com.dio.patterns.exception.BusinessException;
import com.dio.patterns.model.enums.PaymentType;
import org.springframework.stereotype.Component;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

@Component
public class PaymentStrategyFactory {

    private final Map<PaymentType, PaymentStrategy> strategies;

    public PaymentStrategyFactory(List<PaymentStrategy> strategyList) {
        strategies = new EnumMap<>(PaymentType.class);
        strategyList.forEach(strategy -> strategies.put(strategy.getPaymentType(), strategy));
    }

    public PaymentStrategy getStrategy(PaymentType paymentType) {
        PaymentStrategy strategy = strategies.get(paymentType);
        if (strategy == null) {
            throw new BusinessException("Payment strategy not found for: " + paymentType);
        }
        return strategy;
    }
}""",

"src/main/java/com/dio/patterns/event/OrderProcessedEvent.java": """package com.dio.patterns.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class OrderProcessedEvent extends ApplicationEvent {
    private final Long orderId;
    private final String status;

    public OrderProcessedEvent(Object source, Long orderId, String status) {
        super(source);
        this.orderId = orderId;
        this.status = status;
    }
}""",

"src/main/java/com/dio/patterns/event/OrderNotificationListener.java": """package com.dio.patterns.event;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class OrderNotificationListener {

    @Async
    @EventListener
    public void handleOrderProcessedEvent(OrderProcessedEvent event) {
        log.info("Async Notification: Order {} processed with status: {}", event.getOrderId(), event.getStatus());
        try {
            Thread.sleep(2000); // Simulate email/SMS notification delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        log.info("Async Notification: Email sent to customer for Order {}", event.getOrderId());
    }
}""",

"src/main/java/com/dio/patterns/service/facade/CheckoutFacade.java": """package com.dio.patterns.service.facade;

import com.dio.patterns.client.AddressDto;
import com.dio.patterns.client.ViaCepClient;
import com.dio.patterns.event.OrderProcessedEvent;
import com.dio.patterns.exception.BusinessException;
import com.dio.patterns.model.dto.CheckoutRequest;
import com.dio.patterns.model.dto.CheckoutResponse;
import com.dio.patterns.model.entity.Address;
import com.dio.patterns.model.entity.OrderEntity;
import com.dio.patterns.model.enums.OrderStatus;
import com.dio.patterns.repository.OrderRepository;
import com.dio.patterns.service.chain.OrderValidationChain;
import com.dio.patterns.service.chain.OrderValidationContext;
import com.dio.patterns.service.strategy.PaymentStrategy;
import com.dio.patterns.service.strategy.PaymentStrategyFactory;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class CheckoutFacade {

    private final OrderValidationChain validationChain;
    private final PaymentStrategyFactory paymentStrategyFactory;
    private final ViaCepClient viaCepClient;
    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public CheckoutResponse processCheckout(CheckoutRequest request) {
        log.info("Starting checkout process for customer: {}", request.customerId());

        // 1. Chain of Responsibility: Validations
        OrderValidationContext validationContext = OrderValidationContext.builder()
                .request(request)
                .isValid(true)
                .build();
                
        validationChain.execute(validationContext);

        if (!validationContext.isValid()) {
            throw new BusinessException("Validation Failed: " + validationContext.getValidationMessage());
        }

        // 2. Fetch external data (ViaCEP)
        AddressDto addressDto = viaCepClient.getAddressByCep(request.cep());
        if (addressDto == null || addressDto.cep() == null) {
            throw new BusinessException("Invalid CEP");
        }
        Address deliveryAddress = Address.builder()
                .cep(addressDto.cep())
                .logradouro(addressDto.logradouro())
                .complemento(addressDto.complemento())
                .bairro(addressDto.bairro())
                .localidade(addressDto.localidade())
                .uf(addressDto.uf())
                .build();

        // 3. Strategy: Calculate final amount based on payment type
        PaymentStrategy paymentStrategy = paymentStrategyFactory.getStrategy(request.paymentType());
        BigDecimal finalAmount = paymentStrategy.calculateFinalAmount(request.baseAmount());

        // 4. Save to Database
        OrderEntity order = OrderEntity.builder()
                .customerId(request.customerId())
                .deliveryAddress(deliveryAddress)
                .baseAmount(request.baseAmount())
                .totalAmount(finalAmount)
                .paymentType(request.paymentType())
                .status(OrderStatus.PROCESSED)
                .createdAt(LocalDateTime.now())
                .build();
        
        order = orderRepository.save(order);

        // 5. Observer: Publish Domain Event
        eventPublisher.publishEvent(new OrderProcessedEvent(this, order.getId(), order.getStatus().name()));

        log.info("Checkout completed successfully. Order ID: {}", order.getId());

        return new CheckoutResponse(
                order.getId(),
                order.getStatus(),
                order.getBaseAmount(),
                order.getTotalAmount(),
                "Order processed successfully"
        );
    }
}""",

"src/main/java/com/dio/patterns/controller/CheckoutController.java": """package com.dio.patterns.controller;

import com.dio.patterns.model.dto.CheckoutRequest;
import com.dio.patterns.model.dto.CheckoutResponse;
import com.dio.patterns.service.facade.CheckoutFacade;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/checkout")
@RequiredArgsConstructor
@Tag(name = "Checkout API", description = "Endpoints for order processing and checkout")
public class CheckoutController {

    private final CheckoutFacade checkoutFacade;

    @PostMapping
    @Operation(summary = "Process a new order checkout", description = "Executes validations, calculates payment strategies, fetches address and publishes events.")
    public ResponseEntity<CheckoutResponse> processCheckout(@RequestBody @Valid CheckoutRequest request) {
        CheckoutResponse response = checkoutFacade.processCheckout(request);
        return ResponseEntity.ok(response);
    }
}""",

"src/main/java/com/dio/patterns/exception/BusinessException.java": """package com.dio.patterns.exception;

public class BusinessException extends RuntimeException {
    public BusinessException(String message) {
        super(message);
    }
}""",

"src/main/java/com/dio/patterns/exception/ErrorResponse.java": """package com.dio.patterns.exception;

import java.time.LocalDateTime;

public record ErrorResponse(
    LocalDateTime timestamp,
    int status,
    String error,
    String message,
    String path
) {}""",

"src/main/java/com/dio/patterns/exception/GlobalExceptionHandler.java": """package com.dio.patterns.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(
                LocalDateTime.now(),
                HttpStatus.BAD_REQUEST.value(),
                "Business Rule Violation",
                ex.getMessage(),
                request.getDescription(false)
        );
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(
                LocalDateTime.now(),
                HttpStatus.BAD_REQUEST.value(),
                "Validation Error",
                ex.getBindingResult().getFieldError().getDefaultMessage(),
                request.getDescription(false)
        );
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneralException(Exception ex, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(
                LocalDateTime.now(),
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                ex.getMessage(),
                request.getDescription(false)
        );
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}"""
}

for filepath, content in files.items():
    full_path = os.path.join(project_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Project generated successfully!")
