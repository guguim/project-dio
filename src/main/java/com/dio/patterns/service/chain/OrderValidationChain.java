package com.dio.patterns.service.chain;

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
}
