package uk.ac.stir.randology.generator;

/**
 * Wraps Melissa O'Neill's PCG32 implementation in an RNG. 
 * @author zak
 */
public class PCG32 implements RNG {
	
	private PCG32Impl rng;
	
	public PCG32(long seed) {
		rng = new PCG32Impl(seed,0x1234);
	}
	
	public String getName() {
		return "PCG32";
	}
	
	public long nextLong() {
		long a = rng.nextLong();
		return a;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		int a = rng.nextInt();
		return Math.abs((double)(a&0xFFFFFF)/0xFFFFFF);
	}
	
}
