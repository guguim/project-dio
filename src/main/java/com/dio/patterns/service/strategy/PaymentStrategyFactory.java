package com.dio.patterns.service.strategy;

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
}
