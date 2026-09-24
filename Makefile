# Define environment variables

export VERSION=0.1
export ACCOUNT=local:localhost
export APP_NAME=py-inventory-v2-a2a
export HOST=127.0.0.1
export PORT=7601

export URL_AGENT=http://127.0.0.1:7601
export SESSION_TIMEOUT=700
export VALIDATE_CONTEXT=false

export MCP_SERVER_INVENTORY_URL=http://127.0.0.1:7500/mcp
export MCP_SERVER_ORDER_URL=http://127.0.0.1:7501/mcp

export LOG_LEVEL=INFO
export OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4317
export OTEL_STDOUT_LOG_GROUP=True
export LOG_GROUP=/mnt/c/Eliezer/log/py-inventory-v2-a2a.log

# Default target
all: env activate run

# Show environment variables
env:
	@echo "Current Environment Variables:"
	@echo "VERSION=$(VERSION)"
	@echo "APP_NAME=$(APP_NAME)"
	@echo "LOG_LEVEL=$(LOG_LEVEL)"
	@echo "PORT=$(PORT)"
activate:
	@echo "Activate venv..."
	@bash -c "source ../../.venv/bin/activate"

# Run the Python application
run:
	@echo "Running application with environment variables..."
	@bash -c "source ../../.venv/bin/activate && python -m src.a2a_server.main"
   
.PHONY: all env activate run