package com.dio.patterns.service.chain;

import com.dio.patterns.model.dto.CheckoutRequest;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderValidationContext {
    private CheckoutRequest request;
    private boolean isValid;
    private String validationMessage;
}
