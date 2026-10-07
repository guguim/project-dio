package com.dio.patterns.controller;

import com.dio.patterns.model.dto.CheckoutRequest;
import com.dio.patterns.model.dto.CheckoutResponse;
import com.dio.patterns.service.facade.CheckoutFacade;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/checkout")
@RequiredArgsConstructor
@Tag(name = "Checkout API", description = "Endpoints for order processing and checkout")
public class CheckoutController {

    private final CheckoutFacade checkoutFacade;

    @PostMapping
    @Operation(summary = "Process a new order checkout", description = "Executes validations, calculates payment strategies, fetches address and publishes events.")
    public ResponseEntity<CheckoutResponse> processCheckout(@RequestBody @Valid CheckoutRequest request) {
        CheckoutResponse response = checkoutFacade.processCheckout(request);
        return ResponseEntity.ok(response);
    }
}
