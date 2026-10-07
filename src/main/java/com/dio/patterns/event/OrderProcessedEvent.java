package com.dio.patterns.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class OrderProcessedEvent extends ApplicationEvent {
    private final Long orderId;
    private final String status;

    public OrderProcessedEvent(Object source, Long orderId, String status) {
        super(source);
        this.orderId = orderId;
        this.status = status;
    }
}
