For General information, platform overview and system architecture please see: 00_system_architecture/quant_mamangement_platform_architecture.pptx

To Run the services:
run .\run_all.bat

This will open four command prompts and spin up the Data Service, Portfolio Service, Execution Service and the MarketData Service.

To examine and playaround with the REST endpoints for each service go to:
http://localhost:8001/docs => Data Service
http://localhost:8002/docs => Portfolio Service
http://localhost:8003/docs => Execution Service
http://localhost:8004/docs => MarketData Service
http://localhost:8010/docs => IPO_Strategy Service

These services are built using FastAPI, at /docs you are able to try out the endpoints for yourself, read any documentation and examine the schemas associated with these routers. To try out an endpoint, click the drop down arrow on the desired route handler and click "try it out" in the top right hand corner. It will provide details on the input schema and output schema.