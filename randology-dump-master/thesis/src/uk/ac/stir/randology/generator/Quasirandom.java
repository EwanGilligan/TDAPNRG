package uk.ac.stir.randology.generator;

/**
 * A three-dimensional high-discrepancy quasi-random sequence.
 * @author zak
 */
public class Quasirandom implements RNG {
	
	private final double C0 = 4.7596266423396880;
    private final double C1 = 5.3205298191322060;
    private final double C2 = 2.2419207148157443;
    private final double M0 = 0.9060939428196817;	
    private final double M1 = 0.5393446629166316;
    private final double M2 = 1.0471975511965976;
	
	private int seed = 0;
	
	public String getName() {
		return "Quasirandom";
	}
	
	public long nextLong() {
		return Math.round( nextDouble()*Long.MAX_VALUE );
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		int x = ++seed;
		switch(x % 3) {
		  case 0: return (C0+x*M0) % 1;
		  case 1: return (C1+x*M1) % 1;
		  case 2: return (C2+x*M2) % 1;
		}
		return -1; //this never happens
	}

}