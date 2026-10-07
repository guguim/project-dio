package com.dio.patterns.service.strategy;

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
}
