from transformers import pipeline

print("Iniciando el sistema y cargando el modelo de NLP...")
clasificador = pipeline(
    "zero-shot-classification", 
    model="Recognai/bert-base-spanish-wwm-cased-xnli"
)

# Etiquetas optimizadas con vocabulario más explícito para ayudar al modelo
etiquetas_candidatas = [
    "accidente de coche, golpe en el vehiculo o daños", 
    "duda sobre un pago, recibo o factura",
    "consultar coberturas de la poliza de seguro", 
    "dar datos personales como dni, telefono o cuenta bancaria", 
    "poner una queja, reclamacion o mal servicio"
]

print("-" * 50)
print("¡Chatbot SegurPlus v3 (Etiquetas Optimizadas) listo!")
print("Escribe 'salir' en cualquier momento para terminar.")
print("-" * 50)

while True:
    texto_usuario = input("\nTú: ")
    
    if texto_usuario.strip().lower() in ['salir', 'exit', 'quit']:
        print("Chatbot: ¡Hasta pronto! Cerrando sesión segura.")
        break
        
    if not texto_usuario.strip():
        continue

    # Clasificar la intención
    resultado = clasificador(texto_usuario, candidate_labels=etiquetas_candidatas)
    intent_detectado = resultado['labels'][0]
    confianza = resultado['scores'][0]

    # Respuestas prácticas + Guardrails de Compliance
    if intent_detectado == "dar datos personales como dni, telefono o cuenta bancaria":
        respuesta = "⚠️ [BLOQUEO DE SEGURIDAD]: Por normativas de protección de datos, no puedo recoger información personal. Por favor, reformula tu consulta sin incluir DNI, teléfonos o cuentas bancarias."
    
    elif intent_detectado == "consultar coberturas de la poliza de seguro":
        respuesta = "Para confirmarte las coberturas exactas de tu póliza y no generarte confusiones, te voy a derivar con un agente especializado que revisará tu contrato en detalle. ¿Te parece bien?"
    
    elif confianza < 0.45:
        # Si la confianza sigue siendo baja, entra la red de seguridad
        respuesta = "Perdona, no he captado bien tu necesidad. ¿Me escribes por un siniestro, un problema con un recibo, o necesitas hablar con un agente?"
    
    elif intent_detectado == "accidente de coche, golpe en el vehiculo o daños":
        respuesta = "Lamento que hayas tenido un percance. Para abrir el parte, indícame solo la matrícula del vehículo o el número de tu póliza (recuerda no darme nombres ni DNI)."
        
    elif intent_detectado == "duda sobre un pago, recibo o factura":
        respuesta = "Entiendo que tienes una consulta sobre facturación. ¿Se trata de un recibo devuelto, un doble cargo o quieres cambiar la cuenta de cobro? (No escribas tu IBAN por aquí)."
        
    elif intent_detectado == "poner una queja, reclamacion o mal servicio":
        respuesta = "Siento mucho que tu experiencia no haya sido buena. Tomo nota de tu reclamación. Cuéntame brevemente qué ha ocurrido para adjuntarlo a tu expediente."

    # Mostrar la respuesta y el log de auditoría
    print(f"Chatbot: {respuesta}")
    print(f"  [Auditoría interna -> Intent: '{intent_detectado}' | Confianza: {confianza:.2f}]")