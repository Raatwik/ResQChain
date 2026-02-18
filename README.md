ResQChain is a disaster response platform that connects civilians to nearby safety shelters and helps first responders decide where to go first.
It uses AI-based impact assessment, live geospatial data, and priority mapping to support faster decisions during emergencies, while also guiding civilians to safety in real time.

One of the main problems during disasters is loss of internet connectivity.
ResQChain addresses this by providing basic guidance even when there is little or no connectivity.

## Architecture
- FastAPI backend 
- Fallback logic(Offline mode)
- Geospatial mapping(Leaflet + OSM)
- OpenWeather API(Live weather details) 
- Random Forest(AI decision making)
- HTML, CSS, JavaScript(frontend)

## Dataset
The raw datasets are **not included** due to size constraints. xView2 was used for model training.

## WARNING
**This project was made under time constraints! Some parts may be hardcoded.**

## Current Status
This is a hackathon prototype

## Future Goals
- Remove hardcoded paths
- Improve file structure
- Build a better offline interface

## Team & Contribution
This project was built as a part of a duo team. 
**TEAM: https://github.com/devkohli1129-hash**

My contributions:
- backend logic and API development
- ML model training and priority logic 
- offline fallback design and integration 
