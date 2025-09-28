# Code Structure

The code has the following structure:

```
jetweb/
|-- tests/                # Automated tests
|-- docs/                 # Documentation
|-- jetweb/               # Main code
|---- application.py      # JetWeb application, main WSGI entrypoint
|---- context.py          # Request context with dependency injection
|---- converters.py       # Path parameter converters
|---- exceptions.py       # HTTP exception representation
|---- handler.py          # Base class for class-based routes
|---- http/               # HTTP request and response representation
|---- routing/            # Routing system (router, routes and route table)
|---- utils/              # Utility functions and datastructures
```
