ResQChain is a disaster response platform that connects civilians to nearby safety shelters and helps first responders decide where to go first.  
It uses AI-based impact assessment, live geospatial data, and priority mapping to support faster decisions during emergencies, while also guiding civilians to safety in real time.

One of the main problems during disasters is loss of internet connectivity.  
ResQChain addresses this by providing basic guidance even when there is little or no connectivity.

## Architecture
- FastAPI backend  
- Offline fallback logic  
- Geospatial mapping (Leaflet + OpenStreetMap)  
- OpenWeather API (live weather details)  
- Random Forest model for AI-based decision making  
- HTML, CSS, JavaScript (frontend)

## Dataset
The raw datasets are **not included** due to size constraints.  
The xView2 dataset was used for model training.

## Warning
**This project was made under strict time constraints.**  
Some parts of the code may be hardcoded.

## Current Status
Hackathon prototype.

## Future Goals
- Remove hardcoded paths  
- Improve file structure  
- Build a better offline-first interface  

## Team & Contribution
This project was built as part of a duo team.

**Teammate:** https://github.com/devkohli1129-hash

**My contributions:**
- Backend logic and API development  
- ML model training and priority logic  
- Offline fallback design and integration  
