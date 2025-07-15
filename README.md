# Ask DAN Anything 

Daily Assistant for Nutrition (Ask D.A.N.)


A self-hosting nutrition tracking webapp and assistant powered by edge AI.


This project is created for Qualcomm's ML Hackathon. Models are designed and optimized for the Snapdragon Xelite chips.

1. Frontend:
Created using streamlit and connects to the sqlite3 database for user data storage. 

2. Backend: 
Vectors are embedded in a FAISS index and uses CLIP vision model to process image data for querying. Vectors within the index is associated with an unique id to locate them within the database hosted by sqlite3 database for efficient retrieval and access.

Developers Contact Info:
- Alejandro Arteaga (ajarteag@usc.edu)
- Ashley Fu (yue.yang.fu@vanderbilt.edu)
- Daniel Arnold (danarnold38438@gmail.com)
- Katarina Duric (kd374@cornell.edu)
- Kerry Huang (yue.huang@nyu.edu)


Deployment: 
1. Clone the repository using: 
```
git clone https://github.com/ajarteag/qc-sandbox.git
```
2. Cd into the repository
```
cd qc-sandbox 
```

Run commands:
1. installs uv
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
2. installs dependencies in the packages 
```
uv run
```
3. activate the virtual environment 
```
.venv\scripts\activate

```
4. Download Ollama
```
Download Ollama for Windows from this website: https://ollama.com/download/windows
Run the installer *.exe file and follow the instructions.
Confirm Ollama is installed by running the following command in a terminal window:
ollama --version
In terminal, run the following command: ollama pull gemma3:4b

```
5. launches the webapp 
```
python -m streamlit run .\src\final_webApp.py
```



