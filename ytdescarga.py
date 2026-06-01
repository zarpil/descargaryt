import os
import shutil
import threading
from pathlib import Path
import customtkinter as ctk
import yt_dlp

# Configuración visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue") 

class AppDescargador(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ruta por defecto segura: La carpeta "Descargas"
        self.carpeta_guardado = str(Path.home() / "Downloads")
        if not os.path.exists(self.carpeta_guardado):
            self.carpeta_guardado = str(Path.home() / "Desktop")

        # Detectar FFmpeg en el sistema
        self.tiene_ffmpeg = shutil.which('ffmpeg') is not None

        # Configuración dinámica de la ventana (ajustada para evitar espacio sobrante)
        self.title("YT descargas by p0u")
        self.alto_inicial = 285 if not self.tiene_ffmpeg else 260
        self.alto_progreso = self.alto_inicial + 85
        self.geometry(f"550x{self.alto_inicial}")  
        self.resizable(False, False)

        # --- COMPONENTES DE LA INTERFAZ ---
        
        # Título
        self.titulo = ctk.CTkLabel(self, text="Descargas de Video en Máxima Calidad", font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=(15, 10))

        # Campo de texto para la URL
        self.entry_url = ctk.CTkEntry(self, placeholder_text="Introduce la URL del video de YouTube aquí...", width=450, border_color="#ff69b4")
        self.entry_url.pack(pady=5)

        # SECCIÓN DE CARPETA
        self.marco_carpeta = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_carpeta.pack(pady=5)

        # Botón Cambiar Carpeta
        self.btn_carpeta = ctk.CTkButton(self.marco_carpeta, text="Cambiar carpeta", command=self.seleccionar_carpeta, width=120, fg_color="#ff8da1", hover_color="#ff69b4", text_color="#000000")
        self.btn_carpeta.pack(side="left", padx=10)

        self.lbl_ruta_actual = ctk.CTkLabel(self.marco_carpeta, text=self.recortar_ruta(self.carpeta_guardado), font=ctk.CTkFont(size=12))
        self.lbl_ruta_actual.pack(side="left")

        # Botón de descarga
        self.btn_descargar = ctk.CTkButton(self, text="Descargar Video", command=self.iniciar_descarga_hilo, font=ctk.CTkFont(weight="bold"), fg_color="#ff1493", hover_color="#c71585")
        self.btn_descargar.pack(pady=(10, 15))

        # --- SECCIÓN DE PROGRESO (OCULTA AL INICIO) ---
        self.barra_progreso = ctk.CTkProgressBar(self, width=450, progress_color="#ff69b4")
        self.barra_progreso.set(0)

        self.lbl_estado = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.lbl_porcentaje = ctk.CTkLabel(self, text="0%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ff69b4")

        # --- CRÉDITOS / FOOTER ---
        self.lbl_credits = ctk.CTkLabel(self, text="🌷 Made by @p0u 🌷", font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
        self.lbl_credits.pack(side="bottom", pady=10)

        # Advertencia si FFmpeg no está instalado
        if not self.tiene_ffmpeg:
            self.lbl_warning_ffmpeg = ctk.CTkLabel(self, text="⚠️ FFmpeg no detectado. La calidad se limitará a un máximo de 720p.", font=ctk.CTkFont(size=11), text_color="#ffcc00")
            self.lbl_warning_ffmpeg.pack(side="bottom", pady=2)

    def seleccionar_carpeta(self):
        carpeta = ctk.filedialog.askdirectory(initialdir=self.carpeta_guardado)
        if carpeta:
            self.carpeta_guardado = carpeta
            self.lbl_ruta_actual.configure(text=self.recortar_ruta(carpeta))

    def recortar_ruta(self, ruta):
        if len(ruta) > 40:
            return "..." + ruta[-37:]
        return ruta

    def mostrar_progreso(self):
        self.geometry(f"550x{self.alto_progreso}") 
        self.lbl_credits.pack_forget()
        if not self.tiene_ffmpeg:
            self.lbl_warning_ffmpeg.pack_forget()
        
        self.barra_progreso.pack(pady=5)
        self.lbl_estado.pack(pady=2)
        self.lbl_porcentaje.pack(pady=2)
        
        self.lbl_credits.pack(side="bottom", pady=8)
        if not self.tiene_ffmpeg:
            self.lbl_warning_ffmpeg.pack(side="bottom", pady=2)

    def ocultar_progreso(self):
        self.barra_progreso.pack_forget()
        self.lbl_estado.pack_forget()
        self.lbl_porcentaje.pack_forget()
        self.geometry(f"550x{self.alto_inicial}")

    def progreso_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            descargado = d.get('downloaded_bytes', 0)
            
            if total:
                porcentaje_float = descargado / total
                porcentaje_texto = f"{int(porcentaje_float * 100)}%"
                velocidad = d.get('_speed_str', 'N/A')
                
                self.barra_progreso.set(porcentaje_float)
                self.lbl_porcentaje.configure(text=porcentaje_texto)
                self.lbl_estado.configure(text=f"Descargando pista actual... ({velocidad})", text_color="#e6a100")
                
        elif d['status'] == 'finished':
            self.lbl_estado.configure(text="[+] Descarga de pista finalizada. Procesando...", text_color="#e6a100")

    def iniciar_descarga_hilo(self):
        url = self.entry_url.get().strip()
        if not url:
            self.mostrar_progreso()
            self.lbl_estado.configure(text="[!] Por favor, introduce una URL válida.", text_color="red")
            self.barra_progreso.set(0)
            self.lbl_porcentaje.configure(text="")
            return
        
        self.mostrar_progreso()
        self.barra_progreso.set(0)
        self.lbl_porcentaje.configure(text="0%")
        
        self.btn_descargar.configure(state="disabled")
        self.btn_carpeta.configure(state="disabled")
        self.lbl_estado.configure(text="[+] Conectando con YouTube...", text_color="#e6a100")
        
        hilo = threading.Thread(target=self.proceso_descarga, args=(url,))
        hilo.start()

    def proceso_descarga(self, url):
        ydl_opts = {
            'outtmpl': os.path.join(self.carpeta_guardado, '%(title)s.%(ext)s'),
            'noplaylist': True, 
            'verbose': False,
            'progress_hooks': [self.progreso_hook],
        }

        if self.tiene_ffmpeg:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessor_args': {
                    'ExtractAudio': ['-c:a', 'aac'],
                    'Merger': ['-c:v', 'copy', '-c:a', 'aac']
                }
            })
        else:
            # Sin FFmpeg: Descargar el mejor formato único pre-fusionado (usualmente MP4 <= 720p)
            ydl_opts.update({
                'format': 'best[ext=mp4]/best'
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.barra_progreso.set(1.0)
            self.lbl_porcentaje.configure(text="100%")
            self.lbl_estado.configure(text="[✔] ¡Video descargado con éxito!", text_color="green")
            self.entry_url.delete(0, 'end')
            
        except Exception as e:
            self.lbl_estado.configure(text=f"[❌] Error en la descarga. Verifica la URL.", text_color="red")
            self.barra_progreso.set(0)
            self.lbl_porcentaje.configure(text="0%", text_color="red")
            print(f"Error detallado: {e}")
            
        finally:
            self.btn_descargar.configure(state="normal")
            self.btn_carpeta.configure(state="normal")

if __name__ == "__main__":
    app = AppDescargador()
    app.mainloop()