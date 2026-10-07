package com.dio.patterns.service.strategy;

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
}
