package com.test;
public class TestLombok {
    public static void main(String[] args) {
        OrderValidationContext ctx = OrderValidationContext.builder()
                .isValid(true)
                .build();
    }
}
