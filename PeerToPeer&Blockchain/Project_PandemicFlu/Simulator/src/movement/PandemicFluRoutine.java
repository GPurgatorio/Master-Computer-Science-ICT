package movement;

import core.Coord;
import core.Settings;

import java.util.LinkedList;
import java.util.List;

public class PandemicFluRoutine extends MovementModel {
    /** how many waypoints should there be per path */
    private static final int PATH_LENGTH = 1;
    private Coord lastWaypoint;

    protected List<Coord> pois = new LinkedList<Coord>();

    public PandemicFluRoutine(Settings settings) {
        super(settings);
        initPois();
    }

    protected PandemicFluRoutine(PandemicFluRoutine rwp) {
        super(rwp);
        pois = rwp.pois;
    }

    /**
     * Returns a possible (random) placement for a host
     * @return Random position on the map
     */
    @Override
    public Coord getInitialLocation() {
        assert rng != null : "MovementModel not initialized!";
        Coord c = randomCoord();

        this.lastWaypoint = c;
        return c;
    }

    @Override
    public Path getPath() {
        Path p;
        p = new Path(generateSpeed());
        p.addWaypoint(lastWaypoint.clone());
        Coord c = lastWaypoint;

        for (int i=0; i<PATH_LENGTH; i++) {
            c = randomPoi();
            p.addWaypoint(c);
        }

        this.lastWaypoint = c;
        return p;
    }

    @Override
    public PandemicFluRoutine replicate() {
        return new PandemicFluRoutine(this);
    }

    protected Coord randomCoord() {
        return new Coord(rng.nextDouble() * getMaxX(),
                rng.nextDouble() * getMaxY());
    }

    private void initPois() {
        Settings s = new Settings("PandemicFlu");
        int nrOfPois = s.getInt("nrOfPois");
        assert(nrOfPois > 0);

        for(int i=0; i < nrOfPois; i++) {
            pois.add(randomCoord());
        }
    }

    private Coord randomPoi() {
        return pois.get(rng.nextInt(pois.size()));
    }

    public List<Coord> getPois() {
        return this.pois;
    }
}
