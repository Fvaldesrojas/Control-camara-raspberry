from fastapi import FastAPI
import subprocess
import signal
import uvicorn

app = FastAPI()

# Variable global para almacenar la referencia al proceso en ejecución
proceso_en_ejecucion = None

def manejador_de_senal(signum, frame):
    global proceso_en_ejecucion
    if proceso_en_ejecucion and proceso_en_ejecucion.poll() is None:
        proceso_en_ejecucion.terminate()
        print("Programa detenido")
    exit(0)

# Asigna el manejador de señales
signal.signal(signal.SIGINT, manejador_de_senal)

@app.get("/start")
def ejecutar_programa():
    global proceso_en_ejecucion

    # Verifica si ya hay un proceso en ejecución
    if proceso_en_ejecucion and proceso_en_ejecucion.poll() is None:
        return {"message": "El programa ya está en ejecución"}

    # Coloca aquí el comando que deseas ejecutar
    comando = ["python3", "/home/citylabfrutilla/Desktop/Camera/Pancho/video_camera/capture.py"]
    proceso_en_ejecucion = subprocess.Popen(comando)
    return {"message": "Programa ejecutado"}

@app.get("/stop")
def detener_programa():
    global proceso_en_ejecucion

    # Verifica si hay un proceso en ejecución
    if not proceso_en_ejecucion or proceso_en_ejecucion.poll() is not None:
        return {"message": "No hay un programa en ejecución para detener"}

    # Termina el proceso
    proceso_en_ejecucion.terminate()
    proceso_en_ejecucion = None
    return {"message": "Programa detenido"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)