package com.dio.patterns.service.strategy;

import com.dio.patterns.model.enums.PaymentType;
import java.math.BigDecimal;

public interface PaymentStrategy {
    BigDecimal calculateFinalAmount(BigDecimal baseAmount);
    PaymentType getPaymentType();
}
