from src.a2a_server.config.settings import settings

AGENT_CARD = {
  "name": settings.APP_NAME,
  "description": "Statistical inference agent (windowed data analysis)",
  "url": f"{settings.URL_AGENT}/a2a/message",
  "version": settings.VERSION,
  "provider": {
    "organization": "eliezer-junior",
    "url": f"{settings.URL_AGENT}"
  },
  "supportedInterfaces": [
    {
      "url": f"{settings.URL_AGENT}/a2a/message",
      "protocolBinding": "HTTP+JSON",
      "protocolVersion": settings.VERSION
    }
  ],
  "capabilities": {
    "streaming": False,
    "pushNotifications": False,
    "stateTransitionHistory": False,
    "extendedAgentCard": False,
  },
  "defaultInputModes": ["application/json"],
  "defaultOutputModes": ["application/json"],
  "skills": [
    {
      "id": "statistics.agent.status",
      "name": "Statistics Agent Status",
      "description": "Returns health status, version, capabilities and runtime information about this statistics agent.",
      "tags": ["health", "information", "status", "diagnostics", "metadata"],
      "additionalProperties": False,
      "inputSchema": {
        "title": "StatisticsStatusRequest",
        "type": "object",
          "properties": {}
        },
        "examples": [
          "Show statistics agent status.",
          "Get statistics agent version.",
          "Provide the information and health of the statistics agent.",
          "Give me the diagnostics and metadata of the statistics agent.",
        ],
        "outputModes": ["application/json"],
        "inputModes": ["application/json"]
    },
    {
      "id": "statistics.compute",
      "name": "Compute Statistics",
      "description": "Computes descriptive statistics and trend metrics from an input numeric array.",
      "tags": ["statistics","analytics","timeseries"],
      "additionalProperties": False,
      "inputSchema": {
        "type": "object",
        "title": "StatisticsComputeRequest",
        "properties": {
          "data": {
            "type": "array",
            "description":"Array of numeric values to analyze.",
            "items": {
              "type": "number",
              "description": "Numeric value for analysis"
            }
          }
        },
        "required": ["data"]
      },
      "examples": [
        "Show statistics agent status.",
        "Get statistics agent version.",
        "Provide the information and health of the statistics agent.",
        "Calculate the mean, median, and standard deviation of the input data.",
        "Analyze the trend of the input data and provide insights.",
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    }
  ]
}