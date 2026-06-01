# 🌷 YT Descargas by p0u

Una herramienta ligera, estética y ultraeficiente para descargar videos de YouTube en la máxima calidad disponible. Desarrollada en Python utilizando **CustomTkinter** para una interfaz gráfica moderna y **yt-dlp** como motor de descarga asíncrono.

![Versión](https://img.shields.io/badge/version-1.0.0-ff69b4)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

---

## 📸 Vista Previa

<p align="center">
  <img src="https://i.imgur.com/vHqBvIu.png" alt="YT Descargas Interface" width="550">
</p>

---

## ✨ Características

* **Máxima Calidad Automática:** Si el script detecta **FFmpeg** en el sistema, fusionará de forma automática el mejor video y audio disponibles (1080p, 2K, 4K).
* **Modo de Compatibilidad Intuitivo:** En caso de no contar con FFmpeg, el script se adapta dinámicamente limitando la descarga al mejor formato único pre-fusionado (máximo 720p) y mostrando una advertencia visual.
* **Interfaz Estética y Compacta:** Diseño optimizado en modo oscuro con una paleta de colores personalizada en tonos rosa (`#ff69b4`, `#ff1493`). La ventana ajusta su altura automáticamente según el estado.
* **Descargas Asíncronas (Multihilo):** El proceso de descarga se ejecuta en un hilo (`threading`) secundario, evitando que la interfaz gráfica se congele o deje de responder.
* **Monitoreo en Tiempo Real:** Barra de progreso dinámica que detalla el porcentaje actual, el estado del proceso y la velocidad de descarga.
* **Gestión de Rutas:** Permite cambiar la carpeta de destino de forma sencilla y cuenta con un sistema de recorte visual para que las rutas largas no rompan la interfaz.

---

## 🚀 Requisitos e Instalación

Antes de ejecutar el script, asegúrate de tener instalado Python 3.8 o superior y las dependencias del proyecto.
pip install customtkinter yt-dlp

## 🌷 FFmpeg (Altamente Recomendado)
Para poder descargar videos en calidades superiores a 720p (1080p, 2K, 4K), yt-dlp necesita FFmpeg para fusionar las pistas de audio y video:

Windows: Puedes descargarlo desde el sitio oficial o usar winget install Gyan.FFmpeg. Asegúrate de añadirlo al PATH del sistema.

Windows: Instálalo rápidamente con Chocolatey ejecutando choco install ffmpeg, tambien puedes descárgarlo manualmente o usar winget install Gyan.FFmpeg. Asegúrate de añadirlo al PATH del sistema.

Linux (Ubuntu/Debian): sudo apt install ffmpeg

macOS: brew install ffmpeg

Nota: Si no deseas instalar FFmpeg, la app funcionará de todos modos, pero limitada a un máximo de 720p.
