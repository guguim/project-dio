package com.test;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class OrderValidationContext {
    private boolean isValid;
}
