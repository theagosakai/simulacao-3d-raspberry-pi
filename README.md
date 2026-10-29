# Simulacao 3D Raspberry Pi

Simulacao visual interativa de uma placa Raspberry Pi 5 para navegador e Android.

## Versao web

Abra `index.html` diretamente ou execute um servidor local:

```bash
python3 -m http.server 8080
```

Depois acesse `http://localhost:8080`.

Arraste sobre a placa para girar a visualizacao. Os botoes controlam energia, LEDs e reset da camera.

O seletor permite alternar entre Raspberry Pi 5, Raspberry Pi 4 Model B,
Raspberry Pi 3 Model B+ e Raspberry Pi Zero 2 W.

## Versao Android com Kivy

Instale as dependencias em um ambiente Python:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Para gerar um APK, use Buildozer:

```bash
pip install buildozer
buildozer init
buildozer -v android debug
```

## Arquivos

- `index.html`: estrutura da simulacao web
- `styles.css`: modelagem visual em CSS 3D
- `script.js`: rotacao e controles
- `main.py`: interface Kivy para Android e desktop
