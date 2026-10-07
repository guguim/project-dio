package com.dio.patterns.service.facade;

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
                .valid(true)
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
}
