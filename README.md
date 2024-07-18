# Resource Manager

This project is a application that provides infrastructure to users like cpu, gpu, ram and storages.
based on request_body, server creates resources and create container to execute the code.

## Getting Started

### Prerequisites

- Docker
- Python 3.9+

### Installation and Runing Application

1. Clone the repository:
   ```bash
   git clone https://github.com/Dastan1997/resource_manager
   cd resource_manager
2. install virtual env and requirements:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. run container:
   ```bash
   uvicorn app.main:app --reload

### Challenges

- creating container with given cpu, gpu, ram was challenge, I solved this by using aiodocker pkg.
- storage wasn't supported by aiodocker, so I created volume first and attached it to container.
- to validate the reqeust_body, I used regex built-in function of pydantic.
- I created middleware for timeout process for all api endpoints.
