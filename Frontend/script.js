const URL_BACKEND = "/chat";

const contenedorMensajes = document.getElementById("chatMensajes");
const inputMensaje = document.getElementById("inputMensaje");
const btnEnviar = document.getElementById("btnEnviar");
const indicadorEscribiendo = document.getElementById("indicadorEscribiendo");
const chatWidget = document.getElementById("chatWidget");
const btnAbrirChat = document.getElementById("btnAbrirChat");
const btnCerrarChat = document.getElementById("btnCerrarChat");
const btnMinimizarChat = document.getElementById("btnMinimizarChat");

let esperandoRespuesta = false;
let saludoMostrado = false;

function obtenerHora() {
  const ahora = new Date();
  return ahora.toLocaleTimeString("es-PE", {
    hour: "2-digit",
    minute: "2-digit"
  });
}

function crearIconoWhatsApp() {
  const icono = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  icono.setAttribute("viewBox", "0 0 24 24");
  icono.setAttribute("aria-hidden", "true");

  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute(
    "d",
    "M12.04 2a9.84 9.84 0 0 0-8.43 14.91L2 22l5.22-1.57A9.98 9.98 0 1 0 12.04 2Zm5.72 14.02c-.24.68-1.42 1.3-1.97 1.38-.5.08-1.14.12-1.84-.1-.43-.14-.98-.32-1.68-.62-2.96-1.28-4.89-4.27-5.04-4.47-.14-.2-1.2-1.6-1.2-3.05 0-1.46.76-2.17 1.04-2.47.27-.3.6-.37.8-.37h.58c.19 0 .44-.07.68.52.24.58.83 2.02.9 2.17.08.15.13.32.03.52-.1.2-.15.32-.3.5-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.76 1.26 1.64 2.04 1.13 1 2.08 1.31 2.38 1.46.3.15.48.13.66-.08.18-.2.76-.89.96-1.19.2-.3.4-.25.68-.15.28.1 1.76.83 2.06.98.3.15.5.22.58.35.07.12.07.72-.17 1.4Z"
  );
  icono.appendChild(path);
  return icono;
}

function agregarMensaje(texto, tipo, scroll = true, accion = null) {
  const mensajeDiv = document.createElement("div");
  mensajeDiv.classList.add("mensaje", tipo);

  if (tipo === "bot") {
    const avatarDiv = document.createElement("div");
    avatarDiv.classList.add("mensaje-avatar");
    const avatarImg = document.createElement("img");
    avatarImg.src = "logo1.jpg";
    avatarImg.alt = "";
    avatarDiv.appendChild(avatarImg);
    mensajeDiv.appendChild(avatarDiv);
  }

  const wrapperDiv = document.createElement("div");
  wrapperDiv.classList.add("mensaje-contenido");

  const burbujaDiv = document.createElement("div");
  burbujaDiv.classList.add("burbuja");
  burbujaDiv.textContent = texto;

  const tiempoDiv = document.createElement("div");
  tiempoDiv.classList.add("mensaje-tiempo");
  tiempoDiv.textContent = obtenerHora();

  wrapperDiv.appendChild(burbujaDiv);

  if (tipo === "bot" && accion?.tipo === "whatsapp") {
    const enlaceAccion = document.createElement("a");
    enlaceAccion.classList.add("mensaje-accion", "whatsapp");
    enlaceAccion.href = accion.url;
    enlaceAccion.target = "_blank";
    enlaceAccion.rel = "noopener noreferrer";
    enlaceAccion.appendChild(crearIconoWhatsApp());

    const textoAccion = document.createElement("span");
    textoAccion.textContent = accion.etiqueta;
    enlaceAccion.appendChild(textoAccion);
    wrapperDiv.appendChild(enlaceAccion);
  }

  wrapperDiv.appendChild(tiempoDiv);
  mensajeDiv.appendChild(wrapperDiv);
  contenedorMensajes.appendChild(mensajeDiv);

  if (scroll) {
    contenedorMensajes.scrollTop = contenedorMensajes.scrollHeight;
  }
}

function mostrarEscribiendo(mostrar) {
  indicadorEscribiendo.classList.toggle("activo", mostrar);

  if (mostrar) {
    contenedorMensajes.scrollTop = contenedorMensajes.scrollHeight;
  }
}

function actualizarEstadoEntrada(deshabilitar) {
  esperandoRespuesta = deshabilitar;
  inputMensaje.disabled = deshabilitar;
  btnEnviar.disabled = deshabilitar;
  btnEnviar.setAttribute("aria-busy", String(deshabilitar));

  if (!deshabilitar) {
    inputMensaje.focus();
  }
}

function mostrarSaludoInicial() {
  if (saludoMostrado) return;

  saludoMostrado = true;
  setTimeout(function() {
    agregarMensaje(
      "Hola, soy el asistente virtual de Renzo Costa. Puedo ayudarte con productos, precios, promociones, delivery, reclamos, seguimiento de pedidos, garantias, tallas y materiales. ¿En que puedo ayudarte hoy?",
      "bot"
    );
  }, 250);
}

function abrirChat() {
  chatWidget.classList.add("is-open");
  chatWidget.classList.remove("is-minimized");
  btnAbrirChat.setAttribute("aria-expanded", "true");
  mostrarSaludoInicial();
  setTimeout(() => inputMensaje.focus(), 120);
}

window.abrirChat = abrirChat;

function cerrarChat() {
  chatWidget.classList.remove("is-open", "is-minimized");
  btnAbrirChat.setAttribute("aria-expanded", "false");
}

function minimizarChat() {
  chatWidget.classList.remove("is-open");
  chatWidget.classList.add("is-minimized");
  btnAbrirChat.setAttribute("aria-expanded", "false");
}

async function enviarMensaje() {
  if (esperandoRespuesta) return;

  const textoUsuario = inputMensaje.value.trim();

  if (!textoUsuario) {
    inputMensaje.focus();
    return;
  }

  agregarMensaje(textoUsuario, "usuario");
  inputMensaje.value = "";
  actualizarEstadoEntrada(true);
  mostrarEscribiendo(true);

  try {
    const respuesta = await fetch(URL_BACKEND, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mensaje: textoUsuario
      })
    });

    if (!respuesta.ok) {
      throw new Error(`Error HTTP: ${respuesta.status}`);
    }

    const datos = await respuesta.json();
    await new Promise(resolve => setTimeout(resolve, 350));

    mostrarEscribiendo(false);
    agregarMensaje(datos.respuesta, "bot", true, datos.accion);
  } catch (error) {
    console.error("Error al comunicarse con el servidor:", error);
    mostrarEscribiendo(false);
    agregarMensaje(
      "No pude conectar con el servidor. Verifica que Flask este activo en http://localhost:5000 y vuelve a intentarlo.",
      "bot"
    );
  } finally {
    actualizarEstadoEntrada(false);
  }
}

function enviarDesdeChip(texto) {
  if (esperandoRespuesta) return;

  abrirChat();
  inputMensaje.value = texto;
  enviarMensaje();
}

window.addEventListener("DOMContentLoaded", function() {
  btnAbrirChat.setAttribute("aria-expanded", "false");

  btnEnviar.addEventListener("click", enviarMensaje);
  btnCerrarChat.addEventListener("click", cerrarChat);
  btnMinimizarChat.addEventListener("click", minimizarChat);

  document.addEventListener("click", function(evento) {
    const botonAbrir = evento.target.closest("[data-open-chat]");
    const chip = evento.target.closest("[data-chip]");

    if (botonAbrir) {
      abrirChat();
    }

    if (chip) {
      enviarDesdeChip(chip.dataset.chip);
    }
  });

  inputMensaje.addEventListener("keydown", function(evento) {
    if (evento.key === "Enter" && !evento.shiftKey) {
      evento.preventDefault();
      enviarMensaje();
    }
  });
});
