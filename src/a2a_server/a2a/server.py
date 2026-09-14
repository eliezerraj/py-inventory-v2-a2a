import logging
import json

from src.a2a_server.a2a.exception import A2ARequestError, A2ARouterError

from opentelemetry.trace.status import Status, StatusCode
from opentelemetry import trace

#---------------------------------
# Configure logging and tracer
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class A2AServer:
    
    def __init__(self, settings, orchestrator):
        self.settings = settings
        self.orchestrator = orchestrator
        logger.info("A2AServer initialized.")
    
    def router(self, envelope):
        with tracer.start_as_current_span("a2a.server.router") as span:
            span.set_attribute("envelope.id", getattr(envelope, "message_id", "unknown"))
            
            try:
                if envelope.message_type == "inventory.product.check":
                    logger.info("Handling inventory.product.check message type.")
                    
                    response = {"message": "check ok" }
                                        
                    return response
                
                if envelope.message_type == "inventory.agent.status":
                    logger.info("Handling inventory.agent.status message type.")
                    
                    response = {"message": "agent status ok",
                                "data": json.dumps(self.settings.dict() if hasattr(self.settings, "dict") else self.settings.__dict__),
                            }
                    
                    return response
                if envelope.message_type == "inventory.monitor":
                    logger.info("Handling inventory.monitor message type.")
                    
                    response = self.orchestrator.monitor(envelope.payload["product"])
                    
                    return response
                else:
                    logger.error("Handling unsupported message type.")
                    message = f"Unsupported message type: {envelope.message_type}"
                    raise A2ARouterError(message)

            except A2ARouterError as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Error A2ARouterError message", exc_info=e)
                raise e
            
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error("Error uncaught Exception", exc_info=e)
                raise e
