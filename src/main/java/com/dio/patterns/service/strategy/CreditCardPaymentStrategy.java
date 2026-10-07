package com.dio.patterns.service.strategy;

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
}
