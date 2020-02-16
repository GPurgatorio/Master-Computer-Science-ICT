secFog(OpA, A, D) :-
    app(A, L),			
    deployment(OpA, L, D).

deployment(_,[],[]).
deployment(OpA,[C|Cs],[d(C,N,OpN)|D]) :-
    node(N,OpN),
    securityRequirements(C,N),
    trusts2(OpA, OpN),
    deployment(OpA,Cs,D).

trusts(X,X).

trusts2(A,B) :-
    trusts(A,B).
trusts2(A,B) :-
    trusts(A,C),
    trusts2(C,B).

query(secFog(appOp,smartbuilding,D)).

%%%info provided by app operator
app(smartbuilding, [iot_controller, data_storage, dashboard]).

%%% security requirements
securityRequirements(iot_controller, N) :-
    physical_security(N),
    public_key_cryptography(N),
    authentication(N).

securityRequirements(data_storage, N) :-
    secure_storage(N),
    access_logs(N),
    network_ids(N),
    public_key_cryptography(N),
    authentication(N).

securityRequirements(dashboard, N) :-
    %TODO
    
%%% custom policies
physical_security(N) :- 
    anti_tampering(N); access_control(N).

secure_storage(N) :- 
    backup(N), 
    (encrypted_storage(N); obfuscated_storage(N)).


%%% trust relations declared by appOp
0.9::trusts(appOp, edgeOp).
0.8::trusts(appOp, cloudOp2).

%%% trust relations declared by edgeOp
0.9::trusts(edgeOp, cloudOp2).
0.7::trusts(edgeOp, cloudOp1).

%%% trust relations declared by cloudOp2
0.1::trusts(cloudOp1, cloudOp2).

%%% trust relations declared by cloudOp2
0.8::trusts(cloudOp2, edgeOp).
0.5::trusts(cloudOp2, cloudOp1).


%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% cloud1 %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
node(cloud1, cloudOp1).

%virtualisation
0.9999::access_logs(cloud1). 
0.9999::authentication(cloud1).
0.9999::host_ids(cloud1).
0.9999::process_isolation(cloud1).
0.9999::permission_model(cloud1).
0.9999::resource_monitoring(cloud1).
0.9999::restore_points(cloud1).
0.9999::user_data_isolation(cloud1).

%comms
0.9999::certificates(cloud1).
%iot_data_encryption(node).
0.9999::firewall(cloud1).
0.9999::node_isolation_mechanism(cloud1).
0.9999::network_ids(cloud1).
0.9999::public_key_cryptography(cloud1).
%wireless_security(node).

%data
0.9999::backup(cloud1).
0.9999::encrypted_storage(cloud1).
%obfuscated_storage(cloud1).

%physical
0.9999::access_control(cloud1).
%anti_tampering(node).

%other
0.9999::audit(cloud1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% cloud2 %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
node(cloud2, cloudOp2).

%virtualisation
0.999::access_logs(cloud2). 
0.999::authentication(cloud2).
0.999::host_ids(cloud2).
0.999::process_isolation(cloud2).
0.999::permission_model(cloud2).
0.999::resource_monitoring(cloud2).
0.999::restore_points(cloud2).
0.999::user_data_isolation(cloud2).

%comms
0.999::certificates(cloud2).
%iot_data_encryption(node).
0.999::firewall(cloud2).
0.999::node_isolation_mechanism(cloud2).
0.999::network_ids(cloud2).
0.999::public_key_cryptography(cloud2).
%wireless_security(node).

%data
%backup(node).
%encrypted_storage(node).
%obfuscated_storage(node).

%physical
0.999::access_control(cloud2).
%anti_tampering(node).

%other
0.999::audit(cloud2).

%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% edge1 %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%

node(edge1, appOp).

%virtualisation
%access_logs(node). 
0.9::authentication(edge1).
%host_ids(node).
%process_isolation(node).
%permission_model(node).
resource_monitoring(edge1).
%restore_points(node).
%user_data_isolation(node).

%comms
%certificates(node).
iot_data_encryption(edge1).
0.95::firewall(edge1).
%node_isolation_mechanism(node).
%network_ids(node).
public_key_cryptography(edge1).
0.95::wireless_security(edge1).

%data
%backup(node).
%encrypted_storage(node).
obfuscated_storage(edge1).

%physical
%access_control(node).
%0.8::anti_tampering(edge1).

%other
%audit(node).

%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% edge2 %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%

node(edge2, edgeOp).

%virtualisation
%access_logs(node). 
0.9::authentication(edge2).
%host_ids(node).
%process_isolation(node).
%permission_model(node).
resource_monitoring(edge2).
%restore_points(node).
%user_data_isolation(node).

%comms
%certificates(node).
%iot_data_encryption(node).
0.9::firewall(edge2).
%node_isolation_mechanism(node).
%network_ids(node).
public_key_cryptography(edge2).
0.8::wireless_security(edge2).

%data
%backup(node).
%encrypted_storage(node).
obfuscated_storage(edge2).

%physical
%access_control(node).
0.9::anti_tampering(edge2).

%other
%audit(node).

%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% edge3 %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%

node(edge3, edgeOp).

%virtualisation
0.99::access_logs(edge3). 
0.99::authentication(edge3).
0.99::host_ids(edge3).
0.99::process_isolation(edge3).
0.99::permission_model(edge3).
0.99::resource_monitoring(edge3).
%restore_points(node).
0.99::user_data_isolation(edge3).

%comms
0.99::certificates(edge3).
0.99::iot_data_encryption(edge3).
0.99::firewall(edge2).
%node_isolation_mechanism(node).
0.99::network_ids(edge3).
0.99::public_key_cryptography(edge3).
%wireless_security(node).

%data
0.99::backup(edge3).
0.99::encrypted_storage(edge3).
%obfuscated_storage(edge2).

%physical
0.99::access_control(edge3).
0.99::anti_tampering(edge3).

%other
0.99::audit(edge3).
