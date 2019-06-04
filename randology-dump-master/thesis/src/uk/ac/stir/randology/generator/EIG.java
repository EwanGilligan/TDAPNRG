package uk.ac.stir.randology.generator;

/**
 * An implementation of an Explicit Inversive Congruential Generator with an arbitrary parameter set. Use a prime modulus.
 * @author zak
 */
public class EIG implements RNG {
	
	private String name;
	
	private long multiplier;
	private long increment;
	private long seed;
	private long modulus;
	
	public EIG(long multiplier, long increment, long modulus, long seed) {
		this("EIG-" + multiplier + "-" + increment + "-" + modulus,multiplier,increment,modulus,seed);
	}
	
	public EIG(String name, long multiplier, long increment, long modulus, long seed) {
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
		seed = (seed + 1) % modulus;
		return inverseMod((seed*multiplier + increment) % modulus,modulus);
	}
	
    public long next64bits() {
    	long high = nextLong();
    	long med  = nextLong();
    	long low  = nextLong();
    	long result = (high << 33) ^ (med << 2) ^ (low << 62 >> 62);
    	return result;
    }
	
	public double nextDouble() {
		double b = (double)nextLong() / modulus;
		return Math.abs( b );
	}

	long inverseMod(long a, long b) {
		long b0 = b;
		long t = 0;
		long q = 0;
		long x0 = 0;
		long x1 = 1;
		if (b == 1) return 1;
		while (a < 0) a = a + modulus;
		while (a > 1 && b > 0) {
			q = a / b;
			t = b;
			b = a % b;
			a = t;
			t = x0;
			x0 = x1 - q * x0;
			x1 = t;
		}
		if (x1 < 0) x1 += b0;
		return x1;
	}
	
}