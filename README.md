---
layout: post
title:  "ICT Infrastructure Course Notes"
date:   2017-12-14
excerpt: "Just try to recap all the topic debated in the ICT Infrastructure Course"
tag:
- english
- ICT Infrastructure
- University 
- Notes
feature: http://www.arabianoilandgas.com/pictures/gallery/ICTinfrastructure.jpg
comments: true
---
_Since there is no material on ICT Infastructure course, I'm trying to recap all lessons done in this page. The notes are written trying to remember the contents of the course (in accordance with the OneNote Notebook published on course page) and then expanding that contents with structured resources found online. Thanks to anyone that will help me to expand this note (download source [here]({{ site.url }}/assets/2017-12-13-presentations.md) and send me update version)._

# Introduction
The world is changing and a lots of axiom are becaming false. Some example? In the bechelor course (and not, sigh), the teachers say: "The main bottleneck is the disk", and so all the performance are evalueted with reference to disk usage, number of IOs operations and so on... This, nowdaays, is false.  Just thing of [Intel Optane SSD](https://www.anandtech.com/show/11702/intel-introduces-new-ruler-ssd-for-servers) where the new SSD tecnologie based on 3D NAND permits to write and read more fast then previous SSD (the disk that we have installed on our system, sigh number 2), and so we have to redesign the system. Some distributed file system, written in '90s, are crashing due the axiom that the disks are slower than CPU and so you have enough time to do all the computation needed. False! 

Anothe example is in application and server distribution. In the past many application was managed on each server with a shared storage, nowadays we have deploy a large application on a custers of server with local storage, so new system to develop and manage distributed computing application is needed (Hadoop, cassandra (distributed DB), Spark (Computation)...).

The world is evolving faster than I can write this notes, so maybe some things written here are already obsolete, so we can not waste any more time on introduction to avoid to need to rewrite the introduction. 

Let's start to see how a datacenter is build to support new requests. 

# Fabric
The fabric is the interconnection of node in a datacenter. We can think this level as a bunch of switch and wires. 

#### Ethernet
The connection can be performed with various technologies, the most famous is **Ethernet**, commonly used in Local Area Networks (LAN) and Wide Area Networks (WAN). Ethernet use twisted pair and fiber optic links. Ethernet as some famous features such as 48-bit MAC address and Ethernet frame format that influenced other networking protocols.

#### Infiniband
Even if Ethernet is so famous, there are other standard to communicate. **InfiniBand (IB)** is another standard used in high-performance computing (HPC) that features very high throughtput and very low latency. InfiniBand is a protocol and a physical infrastructure and it can send up to 2GB massages with 16 priorities level.
The [RFC 4391](https://tools.ietf.org/html/rfc4391) specifies a method for encapsulating and transmitting IPv4/IPv6 and Address Resolution Protocol (ARP) packets over InfiniBand (IB).

InfiniBand trasmits data in packets up to 4KB. A massage can be:
 - a direct memory access read from or write to a remote node (RDMA)
 - a channel send or receive
 - a transaction-based operation (that can be reversed)
 - a multicast trasmission
 - an atomic operation

#### Omni-Path
Moreover, another communication architecture that exist and is interested to see is Omni-Path. This architecture is owned by Intel and performs high-performance communication. Production of Omni-Path products started in 2015 and a mass delivery of these products started in the first quarted of 2016 (you can insert here some more stuff written on [Wikipedia](https://en.wikipedia.org/wiki/Omni-Path)). 
The interest of this architecture is that Intel plans to develop technologiy based on that will serve as the on-ramp to exascale computing (a computing system capacle of the least one exaFLOPS). 

##### RDMA
If you read wikipedia pages about IB and OmniPath you will find a acronym: RDMA. This acronym means **Remote Direct Memory Access**, a direct memory access (really!) from one computer into that of another without involving either one's OS, this permits high-throuhput, low-latency networking performing.

### Some consideration about numbers
Start think about real world. We have some server with 1 Gbps (not so high speed, just think that is the speed you can reach with your laptop attaching a cable that is in classroom in the univesity). We have to connects this servers to each other, using a switches (each of them has 48 ports). We have a lots of servers... The computation is done.

 ![server speed]({{ site.url }}/speed-required.png)

#### Real use case
As we see we need a lots of bandwith to manage a lots of service (you don't say?) and even if the north-south traffic (the traffic that goes outsite from our datacenter) can be relatively small (the university connection exits on the world with 40 Gbps), the east-west traffic (the traffic inside the datacenter) can reach a very huge number of Gbps. [Aruba datacenter](https://www.arubacloud.com/infrastructures/italy-dc-it1.aspx) (called IT1) with another Aruba datacenter (IT2) reach a bandwidth of 82 Gbps of Internet connection.

Yesterday I went to master degree thesis discussion of my friend. He is a physicist and his experiment requires 2.2Tbps of bandwidth to store produced data, so public cloud is impossible to use. How can manage 2.2 Tbps? Maybe we can reply to this answer (hopefully, otherwise the exam is failed :/ ).

## Connectors
Now we try to analyse the problem from the connector point of view. The fastest wire technology avaiable is the optic fiber. It can be divided into two categories: monomodal (1250 nm) or multimodal (850 nm). Of course, the wire is a wire, and we need something to connect it to somewhere. One of them is the Small form-factor pluggable transceiver (SFP), a compact, hot-pluggable optical module transceiver. The upgrade of this connector is the SFP+ that supports data rates up to 16 Gbps. It supports 10 Gigabit ethernet and can be combined with some other SFP+ with QSFP to reach 4x10Gbps. If combined with QSFP28 we can reach 100 Gbps on the ethernet that is the upper limit nowadays for the data rate.

## Software Defined __ 
The Software Defined something, where something is Networking (**SDN**) or Storage (**SDS**), is a novel approch to cloud computing. 
### SDN
SDN is an architecture purpoting to be dynamic, manageable, cost-effective and some more nice attribute readable [here](https://en.wikipedia.org/wiki/Software-defined_networking#Concept). This type of software create a virtual network to manage the network with more simplicity.

The main concept are the following:
 - Network control is directly programmable
 - The infrastructure is agile, since it can be dynamically adjustable
 - It is programmatically configured and is managed by managed by a software-based SDN controller
 - It is Open Standard-based and Vendor-neutral

### SDS
Software-defined Storage is a term fro computer data storage software for policy-based provisioning and management of data storage independent of the underlying hardware. This type of software includes a storage virtualization to separate storage hardware from the software that manages it.

### Software-defined data center
Software-defined data center is a sort of upgrade of the previous term and indicate a series of virtualization concepts such as abstraction, pooling and automation to all data center resources and services to achieve IT as a service.

## Hyperconvergence
So we virtualize the networking, the storage, the data center... and the cloud! Some tools, as [Nutanix(https://www.nutanix.com/hyperconverged-infrastructure/) build the hyperconverged infrastructure ([HCI](https://en.wikipedia.org/wiki/Hyper-converged_infrastructure)) technology.

## Network topologies
### Spanning Tree Protocol (STP) 
The spanning Tree Protocol is a network protocol that builds a logical loop-free topology for Ethernet networks. The spanning tree is built using some Bridge Protocol Data Units (BPDUs) frames. In 2001 the IEEE introduced Rapid Spanning Tree Protocol (RSTP) that provides significantly faster spanning tree convergence after a topology change.

![Spine-Leaf VS Traditional 3-tier](https://media.licdn.com/mpr/mpr/AAEAAQAAAAAAAAhHAAAAJGI4NmQ3ZDkzLTA2MzUtNGY2MC1hZWMzLTZhMDZkNGEwZTU3Nw.png)
### Three-tier design
This architecture is simple architecture where each component has a redundant unit to replace it in case of failure.

### Spine and leaf Architecture
With the increased focus on east-west data transfer the three-tier design architecture is being replaced with Spine-Leaf design. The switches are diveded into 2 groups, the leaf switches and spine switches. Every leaf switch in a leaf-spine architecture connects to every switch in the network fabric. 
In that topoligy the Link Aggregation Control Protocol (LACP) is used. It provides a method to control the bundling of several physical ports together to form a single logical channel.

### Full Fat Tree
In this network topology, the link that are nearer the top of the hierarchy are "fatter" (thicker) than the link further down the hierarchy. 
![Full Fat Tree](https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Fat_tree_network.svg/220px-Fat_tree_network.svg.png)

## VLAN
Now, the problem is that every switch can be connected to each other and so there is no more LANs separation in the datacenter, every packet can go wherever it wants and some problems may appear. For this problem the VLAN is invented. It partition a broadcast domain and create a isolated computer network.

It works by applying _tags_ to network packets (in Ethernet frame) and handling these tags in the networking systems. 
![Ethernet Frame](https://adelzalok.files.wordpress.com/2011/09/figure-13-ieee-8021q-vlan1.png)

A switch can be configured to accept some tags on some ports and some other tags on some other ports. 

VLAN are useful to manage the access control to some resources (and avoid to access to some subnetwork from other subnetwork).

## Switch Anatomy
A switch is an ASIC (application-specific integrated circuit). It can be proprietary architecture or non-proprietary.

It can be see as two plane that cooperate, the control plane and the data plane. The first runs an OS (Linux, BSD...) and expose a CLI to configure it. The second plana manges the data.

Now some standard are trying to impose a common structure to the network elements (switch included) to facilitate the creation of standard ochestration and automation tools.
![Future of networking](http://en.community.dell.com/cfs-file/__key/communityserver-blogs-components-weblogfiles/00-00-00-00-11/5611.futurenetworking.png)

# Storage
After the fabric, another fondamental component of a datacenter is the storage. The storage can be provided with various tecnologies. 
The simple one is that the disk are put inside each servers and are used as we use the disk on our laptop. Of course it is not useful is we have a bunch of data to manage, and some networking solution can be better to use.

# References
 - https://tools.ietf.org/html/rfc4391
 - https://en.wikipedia.org/wiki/Omni-Path
 - https://en.wikipedia.org/wiki/Remote_direct_memory_access
 - https://www.arubacloud.com/infrastructures/italy-dc-it1.aspx
 - https://en.wikipedia.org/wiki/Software-defined_networking
 - https://en.wikipedia.org/wiki/Software-defined_storage
 - https://en.wikipedia.org/wiki/Software-defined_data_center
 - https://en.wikipedia.org/wiki/Spanning_Tree_Protocol#Rapid_Spanning_Tree_Protocol
 - https://en.wikipedia.org/wiki/Multitier_architecture
 - https://blog.westmonroepartners.com/a-beginners-guide-to-understanding-the-leaf-spine-network-topology/
 - http://searchdatacenter.techtarget.com/definition/Leaf-spine