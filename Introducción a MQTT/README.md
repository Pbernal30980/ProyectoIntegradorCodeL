# Proyecto MQTT con Java

Este proyecto contiene ejemplos de publicador (Publisher) y suscriptor (Subscriber) usando el protocolo MQTT con Eclipse Paho.

## Requisitos previos

1. **Java JDK 11 o superior**
2. **Maven** (para gestionar dependencias)
3. **Broker MQTT** corriendo en `localhost:1883` (por ejemplo, Mosquitto)

## Configuración del proyecto

### 1. Instalar Mosquitto (Broker MQTT)

**Windows:**
```powershell
# Descargar desde: https://mosquitto.org/download/
# O instalar con chocolatey:
choco install mosquitto
```

**Iniciar el broker:**
```powershell
mosquitto -v
```

### 2. Instalar las dependencias de Maven

Desde la carpeta del proyecto, ejecutar:

```powershell
mvn clean install
```

Esto descargará la librería `org.eclipse.paho.client.mqttv3` automáticamente.

## Estructura del proyecto

```
Introducción a MQTT/
├── pom.xml                              # Archivo de configuración de Maven
├── src/
│   └── main/
│       └── java/
│           ├── MQTTPublisher.java       # Publicador de mensajes
│           └── MQTTSubscriber.java      # Suscriptor de mensajes
└── README.md                            # Este archivo
```

## Compilar el proyecto

```powershell
mvn clean compile
```

**Nota importante**: Después de compilar, recargar VS Code (Ctrl+Shift+P → "Developer: Reload Window") para que reconozca las dependencias de Maven.

## Ejecutar los ejemplos

### 1. Primero, ejecutar el Suscriptor (en una terminal):

```powershell
mvn exec:java -Dexec.mainClass="MQTTSubscriber"
```

O compilar y ejecutar manualmente:
```powershell
javac -cp "target/classes;%USERPROFILE%\.m2\repository\org\eclipse\paho\org.eclipse.paho.client.mqttv3\1.2.5\org.eclipse.paho.client.mqttv3-1.2.5.jar" MQTTSubscriber.java
java -cp ".;%USERPROFILE%\.m2\repository\org\eclipse\paho\org.eclipse.paho.client.mqttv3\1.2.5\org.eclipse.paho.client.mqttv3-1.2.5.jar" MQTTSubscriber
```

### 2. Luego, ejecutar el Publicador (en otra terminal):

```powershell
mvn exec:java -Dexec.mainClass="MQTTPublisher"
```

O compilar y ejecutar manualmente:
```powershell
javac -cp "target/classes;%USERPROFILE%\.m2\repository\org\eclipse\paho\org.eclipse.paho.client.mqttv3\1.2.5\org.eclipse.paho.client.mqttv3-1.2.5.jar" MQTTPublisher.java
java -cp ".;%USERPROFILE%\.m2\repository\org\eclipse\paho\org.eclipse.paho.client.mqttv3\1.2.5\org.eclipse.paho.client.mqttv3-1.2.5.jar" MQTTPublisher
```

## Características del código

### MQTTPublisher.java
- Publica un mensaje con QoS 1
- El mensaje es retenido (retained)
- Se desconecta después de publicar

### MQTTSubscriber.java
- Se suscribe al tema "test/tema"
- Mantiene una sesión persistente
- Recibe mensajes en tiempo real
- Se queda escuchando indefinidamente

## Configuración

Puedes modificar estos parámetros en los archivos Java:

- **broker**: Dirección del broker MQTT (por defecto: `tcp://localhost:1883`)
- **topic**: Tema MQTT (por defecto: `test/tema`)
- **qos**: Quality of Service (por defecto: 1)
- **clientId**: Identificador único del cliente

## Solución de problemas

### Error: "The import org.eclipse cannot be resolved"
**Solución**: Ejecutar `mvn clean install` para descargar las dependencias.

### Error: "Connection refused"
**Solución**: Asegurarse de que Mosquitto esté corriendo en el puerto 1883:
```powershell
mosquitto -v
```

### Error en VS Code: "The public type MQTTPublisher must be defined in its own file"
**Solución**: Este es un warning de VS Code. El código funcionará correctamente. Para eliminarlo, asegúrate de que:
- El archivo se llame exactamente `MQTTPublisher.java`
- El archivo se llame exactamente `MQTTSubscriber.java`

## Testing

1. Inicia el broker Mosquitto
2. Ejecuta el suscriptor (debe mostrar "Conectado" y "Suscrito al tema: test/tema")
3. Ejecuta el publicador (debe mostrar "Mensaje publicado" y "Desconectado")
4. El suscriptor debe mostrar: "Mensaje recibido: Mensaje con QoS 1 y retenido en el tema test/tema"
