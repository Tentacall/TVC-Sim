# Simulation Module for Trust Vector Controlled Rocket 

### How to run ?
- Create Virtual Environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Make sure the esp32 reciver device is connected and that is printing ( serial output ) the quaternions and accl separeted by `','`
- RUN !

```
python3 main.py 
```