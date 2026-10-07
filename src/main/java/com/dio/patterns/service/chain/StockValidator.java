package com.dio.patterns.service.chain;

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
}
