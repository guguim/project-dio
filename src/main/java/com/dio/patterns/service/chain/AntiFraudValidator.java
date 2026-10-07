package com.dio.patterns.service.chain;

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
}
