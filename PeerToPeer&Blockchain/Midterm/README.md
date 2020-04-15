# MidTerm P2PBC

This MidTerm involved the monitoring of the IPFS network and the logging of some stats.
You can find the requests in the attached pdf.

*Idea: store swarm's result into files, parse ip addresses and request to some service for geolocalization purposes and create some JavaScript code depending on the results.*

- **src/logging** The first main class. It allows to execute shell/bash commands through Java. It has been used to log data from the IPFS.
- **src/analysis** The second main class. Once the logger finishes its iterations, PeerLogsAnalyzer can be executed and it will generate some stats and write some minified JS code, depending on the logged data. The result can be then pasted in the final html.
- **src/config** Classes used to either config (what command to execute, how many cycles, ..) and to support ISO 3166-1 alpha-3 coding convention
- **resources** It contains the css and automatically generated JS used in *index.html*

