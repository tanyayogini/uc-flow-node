def parameters_converter(parameters: dict) -> dict:
    customer_parameters = {}

    for param in parameters.values():
        if len(param) > 0:
            customer_parameters.update(param[0])
    
    return customer_parameters
