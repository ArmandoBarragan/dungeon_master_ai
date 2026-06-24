# Dungeon Master AI
## Installation
1. Install Docker Compose
2. Copy / Update environment variables from example.env into .env
3. Run docker compose up --build

Endpoints can be interacted with trough Swagger by entering the /docs path

## Architecture
- config: The configuration folder contains the files necessary for the application to start.
- writting: Contains the files for example / real playable stories.
- src
    - controllers: The controller layer exposes the game logic for clients to interact with it.
    - game_engine: This is the core application layer. Here, every game concept is abstracted as an instantiable class.
    - models: This is the layer that defines the database schema.
    - repositories: This is the necessary interface to interact with the database. It stores and fetches information from the database.
    - schemas: It contains the classes that normalize the interaction with the controller layer
    - services: They orchestrate and execute the game logic depending on the input given to the controller layer
  
