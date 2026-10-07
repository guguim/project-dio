package com.dio.patterns.model.dto;

import com.dio.patterns.model.enums.OrderStatus;
import java.math.BigDecimal;

public record CheckoutResponse(
    Long orderId,
    OrderStatus status,
    BigDecimal baseAmount,
    BigDecimal finalAmount,
    String message
) {}
