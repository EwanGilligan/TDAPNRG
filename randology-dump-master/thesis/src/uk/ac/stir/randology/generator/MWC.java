package uk.ac.stir.randology.generator;

/**
 * An implementation of the Multiply-With-Carry generator from Numerical Recipes.
 * @author zak
 */
public class MWC implements RNG {
	
	private long multiplier = 0xffffda61L;
	private long seed;
	
	public MWC(long seed) {
		this.seed = seed;
	}
	
	public String getName() {
		return "MWCNR";
	}
	
	private int nextInt() {
		seed = multiplier * ((int)seed) + (seed >>> 32);
		return (int)seed;
	}
	
	public long nextLong() {
		long left  = nextInt();
		long right = nextInt();
		return (left << 32) ^ right;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		return Math.abs( (double)nextInt() / Integer.MAX_VALUE );
	}
	
}