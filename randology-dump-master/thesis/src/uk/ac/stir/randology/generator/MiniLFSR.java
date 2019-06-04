package uk.ac.stir.randology.generator;


/**
 * A generator using a linear feedback shift register.
 * @author zak
 */
public class MiniLFSR implements RNG {

	private byte register;
	
	public MiniLFSR(long seed) {
		register = (byte)seed;
	}
	
	public String getName() {
		return "MiniLFSR";
	}
	
	private void rotate1() {
		byte b25 = (byte) ((register >> 3) & 1);
		byte b47 = (byte) ((register >> 6) & 1);
		byte bit = (byte) (b25 ^ b47);
		register = (byte) ((register << 1) | bit);
	}
	
	private void rotate() {
		for(int i = 0; i < 8; i++) rotate1();
	}
	
	public long nextLong() {
		rotate();
		return register % 256;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		return Math.abs( (double)nextLong() / 256 );
	}
}