% part 1
secFog(OpA, A, D) :-
    app(A, L),
    deployment(OpA, L, D).

% part 2
deployment(_,[],[]).
deployment(OpA, [C|Cs], [d(C, N, OpN)|D]) :-
    node(N, OpN),
    securityRequirements(C, N),
    trusts2(OpA, OpN),
    deployment(OpA, Cs, D).

% 2 fog nodes and 1 cloud node
node(fog1, fogOp1).
node(fog2, fogOp2).
node(cloud1, cloudOp).

% security part not specified
query(deployment(_, [iot_controller, data_storage, dashboard], _)).

% part 4, added securityRequirements to deployment (I want the securityrequirement C to hold on node N)

% part 5, specification of a whole application (1 single service)
% This service is secure when that node features antitampering OR access_control AND bla OR bla2
app(weatherApp, [weatherMonitor]).
securityRequirements(weatherMonitor, N) :-
    (anti_tampering(N); access_control(N)),
    (wireless_security(N); iot_data_encryption(N)).

% specify infrastructure (cloud and edge fog node, the cloud node features antitampering, access control and encryption)
% while the edge node a bit less in probs
node(cloud, cloudOp).
0.99::anti_tampering(cloud).
0.99::access_control(cloud).
0.99::iot_data_encryption(cloud).

node(edge, edgeOp).
0.8::anti_tampering(edge).
0.9::wireless_security(edge).
0.9::iot_data_encryption(edge).

query(secFog(appOp, weatherApp, D)).

% now we include trusts2, trust level between OpA and OpN
% and add the default trust model of trust (I trust myself)
trusts(X, X).
% between two others, I check that I am the same
trusts2(A, B) :-
    trusts(A, B).
% otherwise I check that I trust someone that directly or indirectly trustes B
trusts2(A, B) :-
    trusts(A, C),
    trusts2(C, B).

% 2 considerations: this default trust model combines all the direct trust relations in a graph with the missing ones
% 2 problems tho: opinions along paths are combined via multiplication (A -> C -> B == I trust C * C trust B)

0.9::trusts(srcOp, aOp).
0.2::trusts(srcOp, bOp).
0.1::trusts(aOp, dstOp).
0.8::trusts(bOp, dstOp).

query(trusts2(srcOp, dstOp)).


% next
%%% trust relations declared by appOp
.9::trusts(appOp, edgeOp).
.9::trusts(appOp, ispOp).

%%% trust relations declared by edgeOp
.7::trusts(edgeOp, cloudOp1).
.8::trusts(edgeOp, cloudOp2).

%%% trust relation declared by cloudOp1
.8::trusts(cloudOp1, cloudOp2).

%%% trust relation declared by cloudOp2
.2::trusts(cloudOp2, cloudOp).

%%% trust relations declared by ispOp
.8::trusts(ispOp, cloudOp).
.6::trusts(ispOp, edgeOp).

query(secFog(appOp,weatherApp,D)).

% TRUST IS NOT MONOTHONIC, in this model it is additive so...

