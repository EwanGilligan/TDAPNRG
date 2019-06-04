package uk.ac.stir.randology.generator;


/**
 * A generator using a linear feedback shift register.
 * @author zak
 */
public class LFSR implements RNG {

	private long register;
	
	public LFSR(long seed) {
		register = seed;
	}
	
	public String getName() {
		return "LFSR2547";
	}
	
	private void rotate1() {
		long b25 = (register >>> 25) & 1;
		long b47 = (register >>> 47) & 1;
		long bit = b25 ^ b47;
		register = (register << 1) | bit;
	}
	
	private void rotate() {
		for(int i = 0; i < 64; i++) rotate1();
	}
	
	public long nextLong() {
		rotate();
		return register;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
}