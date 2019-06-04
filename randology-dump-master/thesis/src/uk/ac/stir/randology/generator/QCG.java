package uk.ac.stir.randology.generator;

/**
 * An implementation of a Linear Congruential Generator with an arbitrary parameter set.
 * @author zak
 */
public class QCG implements RNG {
	
	private String name;
	
	private long multiplier;
	private long increment;
	private long seed;
	private long modulus;
	
	public QCG(long multiplier, long increment, long modulus, long seed) {
		this("QCG-" + multiplier + "-" + increment + "-" + modulus,multiplier,increment,modulus,seed);
	}
	
	public QCG(String name, long multiplier, long increment, long modulus, long seed) {
		this.multiplier = multiplier;
		this.increment = increment;
		this.modulus = modulus;
		this.seed = seed;
		setName(name);
	}
	
	public String getName() {
		return name;
	}
	
	private void setName(String name) {
		this.name = name;
	}
	
	public long nextLong() {
		seed = (seed*seed*multiplier + seed*(multiplier+1) + increment) % modulus;
		return seed;
	}
	
    public long next64bits() {
    	long high = nextLong();
    	long med  = nextLong();
    	long low  = nextLong();
    	long result = (high << 33) ^ (med << 2) ^ (low << 62 >> 62);
    	return result;
    }
	
	public double nextDouble() {
		return Math.abs( (double)nextLong() / modulus );
	}

}