package uk.ac.stir.randology.generator;

// XorShift64 is due to Marsaglia http://www.jstatsoft.org/article/view/v008i14
// it passes all of DieHard
public class XorShift32 implements RNG {
	
	private int state;
	
	public XorShift32(long seed) {
		state = (int)seed;
	};
	
	private int nextInt() {
		state ^= (state << 13);
		state ^= (state >>> 17);
		state ^= (state << 5);
		return state;
	}
	
	public long nextLong() {
		long a = (long)nextInt();
		long b = (long)nextInt();
		return (a << 32) ^ b;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextInt() / Integer.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "XorShift32";
	}

}
