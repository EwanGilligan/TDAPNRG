package uk.ac.stir.randology.generator;

/**
 * An implementation of the mini Multiply-With-Carry generator.
 * @author zak
 */
public class MiniMWC implements RNG {
	
	private long multiplier = 61;
	private long seed;
	
	public MiniMWC(long seed) {
		this.seed = seed;
	}
	
	public String getName() {
		return "MWCNR";
	}
	
	private int nextInt() {
		seed = multiplier * ((byte)seed) + ((seed >>> 8) & 0xFF);
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