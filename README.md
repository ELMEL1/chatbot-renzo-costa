# 🤖 Chatbot de Atención al Cliente — Renzo Costa
## Proyecto de Tesis | Universidad de Ciencias y Humanidades

---

## 📁 Estructura del Proyecto

```
/project
│
├── /backend
│   ├── app.py           ← Servidor Flask (API REST)
│   ├── chatbot.py       ← Motor del chatbot (detección de intenciones)
│   ├── intents.json     ← Base de conocimiento (patrones y respuestas)
│   └── requirements.txt ← Librerías Python necesarias
│
└── /frontend
    ├── index.html       ← Página web principal (interfaz del chat)
    ├── styles.css       ← Estilos visuales de la interfaz
    └── script.js        ← Lógica del chat (fetch, mensajes, eventos)
```

---

## 🚀 Instrucciones de Ejecución (Paso a Paso)

### REQUISITOS PREVIOS
Antes de empezar, asegúrate de tener instalado:
- **Python 3.8 o superior** → https://www.python.org/downloads/
- Un navegador web moderno (Chrome, Firefox, Edge)

---

### PASO 1: Descargar o copiar el proyecto
Coloca todos los archivos en tu computadora respetando la estructura de carpetas mostrada arriba.

---

### PASO 2: Abrir una terminal / símbolo del sistema
- **Windows**: Busca "cmd" o "PowerShell" en el menú inicio
- **Mac/Linux**: Abre la aplicación "Terminal"

---

### PASO 3: Navegar a la carpeta del backend
```bash
cd ruta/al/proyecto/backend
```
Por ejemplo:
```bash
cd C:\Users\TuNombre\proyecto\backend   # Windows
cd /home/tunombre/proyecto/backend       # Linux/Mac
```

---

### PASO 4: Instalar las dependencias de Python
```bash
pip install -r requirements.txt
```
Esto instalará Flask y Flask-CORS automáticamente.

Si `pip` no funciona, prueba con:
```bash
pip3 install -r requirements.txt
```

---

### PASO 5: Iniciar el servidor Flask
```bash
python app.py
```

Deberías ver en la terminal:
```
==================================================
  🤖 Chatbot Renzo Costa - Servidor Flask
==================================================
  ✅ Servidor iniciando...
  🌐 URL: http://localhost:5000
  📡 Endpoint del chat: http://localhost:5000/chat
  🛑 Presiona CTRL+C para detener el servidor
==================================================
 * Running on http://0.0.0.0:5000
```

⚠️ **Importante**: Mantén esta terminal abierta. Si la cierras, el servidor se detiene.

---

### PASO 6: Abrir el Frontend en el navegador
Abre el archivo `frontend/index.html` directamente en tu navegador:

- **Opción A**: Haz doble clic en el archivo `index.html`
- **Opción B**: Arrastra el archivo al navegador
- **Opción C**: En el navegador, escribe: `file:///ruta/al/proyecto/frontend/index.html`

---

### PASO 7: ¡Usar el chatbot!
- Escribe una pregunta en el campo de texto y presiona Enter o el botón de enviar
- O haz clic en los chips de preguntas frecuentes para probar rápidamente

---

## 🧪 Cómo Probar el Backend (Opcional)

Puedes probar el endpoint directamente desde la terminal:

```bash
# Con curl (Linux/Mac):
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"mensaje": "hola"}'
```

Respuesta esperada:
```json
{
  "respuesta": "¡Hola! Bienvenido a Renzo Costa 👋 ¿En qué puedo ayudarte hoy?",
  "intencion": "saludo"
}
```

---

## 💬 Intenciones del Chatbot

| Intención    | Ejemplos de preguntas                                      |
|--------------|-------------------------------------------------------------|
| saludo       | "hola", "buenos días", "qué tal"                           |
| productos    | "qué venden", "catálogo", "tienen bolsos"                  |
| precios      | "cuánto cuesta", "precio", "hay descuentos"                |
| horarios     | "a qué hora abren", "horario", "atienden domingos"         |
| ubicacion    | "dónde están", "tiendas", "dónde queda"                    |
| devoluciones | "cambios", "devolver producto", "garantía"                 |
| contacto     | "teléfono", "whatsapp", "email"                            |
| pagos        | "formas de pago", "tarjeta", "yape"                        |
| despedida    | "adiós", "gracias", "hasta luego"                          |
| desconocido  | Cualquier pregunta que no coincida con las anteriores      |

---

## 🔧 Cómo Agregar Nuevas Intenciones

Edita el archivo `backend/intents.json` y agrega un nuevo objeto con este formato:

```json
{
  "tag": "nombre_intencion",
  "patterns": [
    "frase de ejemplo 1",
    "frase de ejemplo 2",
    "palabra clave"
  ],
  "responses": [
    "Respuesta A del bot",
    "Respuesta B del bot (se elige aleatoriamente)"
  ]
}
```

No olvides agregar la coma al objeto anterior y reiniciar el servidor Flask.

---

## ❗ Solución de Problemas Comunes

| Problema | Solución |
|----------|----------|
| "No se pudo conectar con el servidor" | Verifica que `python app.py` esté corriendo en otra terminal |
| Error al instalar librerías | Prueba con `pip3` en lugar de `pip` |
| El chat no responde | Asegúrate de que el backend corre en el puerto 5000 |
| Módulo no encontrado | Ejecuta `pip install flask flask-cors` manualmente |

---

## 👨‍💻 Autores
- Gonzales Montenegro, Mattias
- Gómez Cortez, Gerald David

**Docente:** Laberiano Matias Andrade Arenas  
**Facultad:** Ingeniería de Sistemas e Informática  
**Universidad:** Universidad de Ciencias y Humanidades — 2025
