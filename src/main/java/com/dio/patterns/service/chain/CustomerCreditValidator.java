package com.dio.patterns.service.chain;

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
}
