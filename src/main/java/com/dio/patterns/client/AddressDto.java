package com.dio.patterns.client;

public record AddressDto(
    String cep,
    String logradouro,
    String complemento,
    String bairro,
    String localidade,
    String uf
) {}
