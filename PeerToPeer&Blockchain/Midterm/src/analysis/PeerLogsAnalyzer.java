/*
 * Copyright (C) 2019 Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package analysis;

import java.io.*;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;

import config.Alpha3;
import config.Configurations;

/** Use after the CmdLogger has finished its logging to store the results in a JS file */
public class PeerLogsAnalyzer {

    private static boolean isIPV4;
    private static String ipAddr;
    private static boolean isTCP;
    private static int port;
    private static String CID;
    private static int latency;
    private static boolean isOutgoing;

    /** Contains <country_name, num_of_peers> e.g. <"Italy", 30> */
    private static HashMap<String, Integer> countries;
    /** Contains <country_name, ISO 3166-1 alpha-2> e.g. <"Italy", "IT"> */
    private static HashMap<String, String> countriesAlpha2;


    public static void main(String[] args) {

        /*                                                  DECLARATIONS                                                            */

        // Vars used to have a general representation of the analyzed peers.
        int totalPeers = 0, peerSameAddress = 0;
        int ipv4Users = 0, ipv6Users = 0;
        int udpUsers = 0, tcpUsers = 0;
        int cidV0 = 0, cidV1 = 0;
        int outgoing = 0, incoming = 0;
        int latencyTot = 0, skippedLatency = 0, avgLatency;
        int fastPeers = 0, mediumPeers = 0, slowPeers = 0;
        int relayedPeers = 0, kadUsers = 0, bitswapUsers = 0;
        int churn, idx = 0;

        // Number of peers found in every log
        int newPeersThisFile, totPeersThisFile;

        // The command with "-v" sometimes returns double (or possibly more) "/ipfs/kad" for the same peer, so we skip these
        boolean skip = false;
        // Used for counting correctly the number of KAD etc users (counting twice the same peer would result in 2 KAD peers and 1 peer)
        boolean skipNextLines = false;

        // The number of peers retrieved per time i by the command
        int[] maxPeerPerTime;
        // The number of newly met peers per time i by the command
        int[] newPeerPerTime;

        // Every different IP Address + isTCP + port will be stored here to prevent the reappearance of the same peers over and over
        Set<String> metAddresses = new HashSet<>();
        // But we will save the logged peers that share the same IP address         < IpAddr, Peer1->Peer2->.. >
        HashMap<String, LinkedList<PeerInfo>> analyzedPeers = new HashMap<>();



        /*                                                  SETUP                                                            */

        // Make sure that the directory exists
        File dir = new File(Configurations.LOG_DIRECTORY);
        assertDirExistence(dir);

        // Get all the files from the directory and check that at least one file is there
        File[] files = dir.listFiles();
        assert files != null;
        if(files.length < 1) {
            print("There are no files in the Log directory");
            return;
        }
        maxPeerPerTime = new int[files.length];
        newPeerPerTime = new int[files.length];



        /*                                                  POPULATING                                                            */

        // Iterate over all the files in the given directory
        for(File f : files) {

            // Reset counters
            newPeersThisFile = 0;
            totPeersThisFile = 0;

            try {
                print("Reading from " + f.getName());

                // If there's a file that it's not a log we skip it
                if (!f.getName().endsWith(Configurations.LOG_EXTENSION))
                    continue;

                // Otherwise, read from it
                BufferedReader br = new BufferedReader(new FileReader(f));
                String line;

                while ((line = br.readLine()) != null) {

                    // Verbose will print also these types of lines so we take care of them here
                    if(line.startsWith("  ")) {

                        // Peer already met, so we don't count his stats again
                        if(skipNextLines)
                            continue;

                        // If we get here, then it's a newly met peer
                        if (line.contains("/ipfs/kad")) {
                            if (!skip) {
                                kadUsers++;
                                skip = true;
                            }
                            else
                                skip = false;
                        }

                        else if (line.contains("/ipfs/bitswap"))
                            bitswapUsers++;

                        else if (line.contains("/libp2p/circuit/relay/"))
                            relayedPeers++;

                        // In any case, go to next line
                        continue;
                    }

                    // If we get here, the line didn't start with indentation so it's a peer
                    totPeersThisFile++;

                    // See: https://github.com/libp2p/specs/tree/master/relay
                    if(line.contains("/p2p-circuit/")) {
                        relayedPeers++;
                        continue;
                    }

                    // See: https://github.com/ipfs/js-ipfs/tree/master/examples/circuit-relaying
                    else if (line.contains("/ws/")) {
                        relayedPeers++;

                        // Simply takes into account the relay part and removes it. Line will be the classic one
                        String[] tmp = line.split("/ws");
                        line = tmp[0] + tmp[1];
                    }

                    // If we get here, it's a normal peer of the swarm
                    if (line.startsWith("/ip4/") || line.startsWith("/ip6/")) {

                        /*
                         * Format:  r[0] /   r[1]   /   r[2]     /   r[3]    /    r[4]     / r[5] / r[6]    r[7]      r[8]
                         *               / ip{4, 6} / ip_address / {tcp,udp} / port_number / ipfs / CID     latency   direction
                         */
                        String[] res = line.trim()
                                .replace("n/a", "0")        // Latency may be unknown, so we set it to 0 (for parseInt exceptions)
                                .replace(" ", "/")          // We concatenate the verbose output to the string with the '/'
                                .split("/");                            // So that we can split all fields with only the '/' character
                        beautifyVars(res);

                        String address = ipAddr + isTCP + port;

                        // Avoid counting twice the exact same peer
                        if (!metAddresses.contains(address)) {

                            // If we reach here, it's a new peer so we save it
                            newPeersThisFile++;
                            PeerInfo peer = new PeerInfo(isIPV4, isTCP, port, CID, latency, isOutgoing);
                            analyzedPeers.computeIfAbsent(ipAddr, v -> new LinkedList<>()).add(peer);

                            // and prevent future adds
                            metAddresses.add(address);

                            // Since it's a new peer, we want to count its protocols etc
                            skipNextLines = false;
                            skip = false;
                        }
                        else    // We already met this peer, so we skip next lines
                            skipNextLines = true;
                    }

                    // Just checking that nothing gets left behind [it never gets printed]
                    else
                        print("Unknown: " + line);
                }
                br.close();
            }
            catch(IOException e) { print("Error try-catch: " + e.getMessage()); }

            // Store the result for this file
            newPeerPerTime[idx] = newPeersThisFile;
            maxPeerPerTime[idx] = totPeersThisFile;
            idx++;
        }



        /*                                                  ANALYSIS                                                            */

        // For each stored address we get: [...]
        Set<String> keySet = analyzedPeers.keySet();
        for(String address : keySet) {

            LinkedList<PeerInfo> listOfPeers = analyzedPeers.get(address);

            // The number of peers sharing the same address, but with different protocols and/or ports
            if(listOfPeers.size() > 1)
                peerSameAddress += listOfPeers.size();

            // For each peer
            for(PeerInfo p : listOfPeers) {

                // Counting the total number of analyzed peers
                totalPeers++;

                // Counting if it's TCP or UDP
                if (p.isTCP())
                    tcpUsers++;
                else
                    udpUsers++;

                // Counting if it's Ipv4 or Ipv6
                if(p.isIpv4())
                    ipv4Users++;
                else
                    ipv6Users++;

                // Counting if it's CID is Version 0 or Version 1
                if(p.isVersion0())
                    cidV0++;
                else
                    cidV1++;

                // Counting the connection's direction
                if(p.isOutgoing())
                    outgoing++;
                else
                    incoming++;

                /* Counting a general view of the peer's latency distribution */

                // If the latency resulted in "n/a", then we skip this in the avg counting
                if(p.getLatency() < 0) {
                    skippedLatency++;
                    continue;
                }
                // Otherwise we count it into this distinction
                if (p.getLatency() < Configurations.LATENCY_FAST)
                    fastPeers++;
                else if (p.getLatency() < Configurations.LATENCY_MEDIUM)
                    mediumPeers++;
                else
                    slowPeers++;
                // Then adding it to the total for the average count
                latencyTot += p.getLatency();
            }
        }



        /*                                                  GEOLOCALIZATION                                                            */

        if(Configurations.MAKE_HTTP_REQUESTS) {
            File dirGeo = new File(Configurations.IPSTACK_DIRECTORY);
            assertDirExistence(dirGeo);

            // Build a client to send the requests to the service
            HttpClient httpClient = HttpClient.newBuilder()
                    .version(HttpClient.Version.HTTP_2).build();

            // For each IP address that we met
            for (String metAddr : analyzedPeers.keySet()) {

                String uri = Configurations.URL_GEOLOC + metAddr + "?access_key=" + Configurations.YOUR_ACCESS_KEY;

                HttpRequest request = HttpRequest.newBuilder()
                        .GET()
                        .uri(URI.create(uri))
                        //.setHeader("User-Agent", "Java 12 HttpClient Bot")
                        .build();

                try {
                    HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

                    if (response.statusCode() == 200) {
                        // Saving it because there are 10'000 requests / month in the free plan!
                        File bodyLog = new File(Configurations.IPSTACK_DIRECTORY + metAddr + Configurations.LOG_EXTENSION);
                        assertFileExistence(bodyLog);

                        FileWriter fw = new FileWriter(bodyLog);
                        fw.write(response.body());
                        fw.close();
                    } else
                        print(metAddr + " didn't return 200");


                } catch (IOException | InterruptedException e) {
                    print("Missed " + metAddr + " due to: " + e.getMessage());
                }
            }
        }
        // Get the number of peers per country (into the 2 HashMaps)
        generateGeoLogs();


        /*                                                  SIMPLE PRINTS                                                            */

        print("Total peers: " + totalPeers);
        print("Addresses collisions: " + peerSameAddress);
        print("IPV4 peers: " + ipv4Users);
        print("IPV6 peers: " + ipv6Users);
        print("UDP users: " + udpUsers);
        print("TCP users: " + tcpUsers);
        print("Number of CID v.0: " +  cidV0);
        print("Number of CID v.1: " + cidV1);
        print("Number of outgoing connections: " + outgoing);
        print("Number of incoming connections: " + incoming);
        print("Number of kad: " + kadUsers);
        print("Number of bitswap: " + bitswapUsers);
        print("Number of Fast peers: " + fastPeers);
        print("Number of Ok peers: " + mediumPeers);
        print("Number of Slow peers: " + slowPeers);
        print("Number of unknown latency peers: " + skippedLatency);
        print("Number of relayed peers: " + relayedPeers);
        avgLatency = latencyTot / ( totalPeers - skippedLatency );
        print("Average latency: " + avgLatency + " ms");
        // Users at the beginning    +           users at the end              /    beginning            (in %)
        churn = (((newPeerPerTime[0] + newPeerPerTime[newPeerPerTime.length-1])/newPeerPerTime[0])*100)/getMax(newPeerPerTime);
        print("Churn %: " + churn);

        // Associate each ISO_3166-1_alpha-2 to it's corresponding ISO_3166-1_alpha-3
        idx = 0;
        Set<String> set = countries.keySet();
        String[] countriesFullNames = new String[countries.size()];
        String[] countriesCodes = new String[countries.size()];
        int[] countriesSizes = new int[countries.size()];

        for(String s : set) {
            // Ex. Italy
            countriesFullNames[idx] = s;
            // Ex. ITA
            countriesCodes[idx] = Alpha3.valueOf(countriesAlpha2.get(s).replace("\"", "")).getValue();
            // Ex. 30
            countriesSizes[idx] = countries.get(s);
            idx++;
        }

        String[] statsTogether = new String[] {"Total Peers", "Addresses collisions", "Ipv4 peers", "Ipv6 peers",
                        "UDP peers", "TCP peers", "Number of CID v.0", "Number of CID v.1",
                        "Number of outgoing connections", "Number of incoming connections",
                        "Number of KAD peers", "Number of BitSwap peers", "Number of Fast peers",
                        "Number of Ok peers", "Number of Slow peers", "Number of unknown latency peers",
                        "Number of relayed peers", "Average latency (ms)", "Churn (%)"};
        int[] valuesTogether = new int[] {totalPeers, peerSameAddress, ipv4Users, ipv6Users, udpUsers, tcpUsers,
                                        cidV0, cidV1, outgoing, incoming, kadUsers, bitswapUsers, fastPeers,
                                        mediumPeers, slowPeers, skippedLatency, relayedPeers, avgLatency, churn};

        /*                                                  JS HANDLER                                                            */

        jsMinWriter t = new jsMinWriter(countriesFullNames, countriesCodes, countriesSizes,
                                            statsTogether, valuesTogether, newPeerPerTime, maxPeerPerTime);
        t.start();
    }



    /*                                                 SUPPORT FUNCTIONS                                                          */


    /** Populates the two HashMaps with the results of the ipstack's requests */
    private static void generateGeoLogs() {

        File[] files = (new File(Configurations.IPSTACK_DIRECTORY)).listFiles();
        assert files != null;

        countries = new HashMap<>();
        countriesAlpha2 = new HashMap<>();
        BufferedReader br;

        // For each file in the directory
        for(File f : files) {

            try {
                br = new BufferedReader(new FileReader(f));
                String line, code = "", name = "";
                int value;

                // For each line (it will only be one line, but just in case someone manually tabs it to see better)
                while((line = br.readLine()) != null) {

                    if (!line.contains("country_name") && !line.contains("country_code"))
                        continue;

                    // Ex. "country_code":"US",
                    if (line.contains("_code")) {
                        code = line;
                        code = code.substring(code.indexOf("country_code\":\"") + 14);
                        code = code.substring(0, code.indexOf(','));        // removing the last ,
                    }

                    // Ex. "country_name":"United States",
                    if (line.contains("_name")) {
                        name = line;
                        name = name.substring(name.indexOf("country_name\":\"") + 14);
                        name = name.substring(0, name.indexOf(','));        // removing the last ,

                        try {
                            value = countries.get(name) + 1;
                        }
                        catch (NullPointerException e) { value = 1; }

                        // "United States" 1
                        countries.put(name, value);
                    }
                    // "United States" "US"
                    countriesAlpha2.put(name, code);
                }
                br.close();
            }
            catch(IOException e) { print("Error while creating report for " + f.getName()); }
        }
    }


    /**
     * Helps visualizing what the res array stores by assigning values to variables with meaningful names.
     *
     * @param res the array of splitted infos
     */
    private static void beautifyVars(String[] res) {
        isIPV4 = res[1].equals("ip4");
        ipAddr = res[2];
        isTCP = res[3].equals("tcp");
        port = Integer.parseInt(res[4]);
        CID = res[6];
        isOutgoing = res[8].equals("outbound");

        try {
            String tmp = res[7];
            if(tmp.equals("0"))     // I replaced the 'n/a' with 0 when parsing
                latency = -1;       // We do not count it into stats

            else if (tmp.contains("ms"))
                latency = Math.round(Float.parseFloat(tmp.substring(0, tmp.indexOf("m"))));

            else if (tmp.contains("s"))       // converts seconds into milliseconds
                latency = Math.round(Float.parseFloat(tmp.substring(0, tmp.length() - 1)) * 1000);

            else        // Never printed
                print("Skipped latency: " + tmp);
        }
        catch(NumberFormatException e) { print("Error in latency"); latency = -1; }
    }


    /**
     * Simple (because no checks on array) getMax for an int array
     *
     * @param array the array to analyze
     * @return the maximum value of the array
     */
    private static int getMax(int[] array) {
        int max = array[0];
        for (int value : array)
            if (value > max)
                max = value;

        return max;
    }


    /** Assures that a dir exists after this */
    private static void assertDirExistence(File dir) {
        if(!dir.exists())
            dir.mkdir();
    }


    /** Assures that given file will exist after this */
    private static void assertFileExistence(File file) {
        try {
            if (!file.exists())
                file.createNewFile();
        }
        catch(IOException e) { e.printStackTrace(); }
    }


    /**
     * Simple print to stdout if the boolean DEBUG in Configurations.java is True
     *
     * @param s the string to print
     */
    private static void print(String s) {
        if(Configurations.DEBUG)
            System.out.println(s);
    }
}
