package com.dio.patterns.event;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class OrderNotificationListener {

    @Async
    @EventListener
    public void handleOrderProcessedEvent(OrderProcessedEvent event) {
        log.info("Async Notification: Order {} processed with status: {}", event.getOrderId(), event.getStatus());
        try {
            Thread.sleep(2000); // Simulate email/SMS notification delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        log.info("Async Notification: Email sent to customer for Order {}", event.getOrderId());
    }
}
