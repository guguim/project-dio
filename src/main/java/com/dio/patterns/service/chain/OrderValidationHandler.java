package com.dio.patterns.service.chain;

public interface OrderValidationHandler {
    void validate(OrderValidationContext context);
}
