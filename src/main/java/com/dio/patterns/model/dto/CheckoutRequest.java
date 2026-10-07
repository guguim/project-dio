package com.dio.patterns.model.dto;

import com.dio.patterns.model.enums.PaymentType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.math.BigDecimal;

public record CheckoutRequest(
    @NotNull Long customerId,
    @NotBlank String cep,
    @NotNull @Positive BigDecimal baseAmount,
    @NotNull PaymentType paymentType
) {}
