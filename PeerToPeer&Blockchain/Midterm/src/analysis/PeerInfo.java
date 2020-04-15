package analysis;

public class PeerInfo {

    private boolean isIPV4;
    private boolean isTCP;
    private int port;
    private String CID;
    private int latency;
    private boolean out;

    /**
     * Constructor
     *
     * @param ipv4 if it's ipv4 or ipv6
     * @param tcp if it's on tcp or udp
     * @param port its port
     * @param cid its related CID
     * @param laten the response time (in ms)
     * @param isOutgoing if it's outgoing or not
     */
    public PeerInfo(boolean ipv4, boolean tcp, int port, String cid, int laten, boolean isOutgoing) {
        isIPV4 = ipv4;
        isTCP = tcp;
        this.port = port;
        CID = cid;
        latency = laten;
        out = isOutgoing;
    }

    /** Returns if the CID stored for this peer is Version 0 or not.
     *
     * @return true if CID is version 0, false otherwise
     */
    public boolean isVersion0() {
        return getCID().startsWith("Qm") && getCID().length() == 46;
    }

    /**
     * A text version of this object.
     *
     * @return a string representing this object
     */
    public String toString() {
        return (isIPV4 ? "ip4" : "ip6") + (isTCP ? "/tcp" : "/udp") + "/" + String.valueOf(port) + "/" + CID;
    }

    /* Classic getters */

    public boolean isIpv4() {
        return isIPV4;
    }

    public boolean isTCP() {
        return isTCP;
    }

    public int getPort() {
        return port;
    }

    public String getCID() {
        return CID;
    }

    public int getLatency() {
        return latency;
    }

    public boolean isOutgoing() {
        return out;
    }

}
