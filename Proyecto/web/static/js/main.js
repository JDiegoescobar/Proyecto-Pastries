// static/js/main.js
function actualizarEstadoNegocio() {
    const ahora = new Date();
    const hora = ahora.getHours();
    const badge = document.getElementById('estado-negocio');

    // Horario de atención para pedidos: 9:00 a 19:00 (7:00 p.m.)
    if (hora >= 9 && hora < 19) {
        badge.textContent = '🟢 ABIERTO';
        badge.classList.add('estado-abierto');
        badge.classList.remove('estado-cerrado');
    } else {
        badge.textContent = '🔴 CERRADO';
        badge.classList.add('estado-cerrado');
        badge.classList.remove('estado-abierto');
    }
}

// Ejecutar al cargar y verificar cada minuto
document.addEventListener('DOMContentLoaded', actualizarEstadoNegocio);
setInterval(actualizarEstadoNegocio, 60000);