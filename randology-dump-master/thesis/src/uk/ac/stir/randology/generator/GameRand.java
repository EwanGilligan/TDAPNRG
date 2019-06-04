package uk.ac.stir.randology.generator;

// GameRand is an incredibly fast random number generator due to Stephan Schaem.
// see http://www.redditmirror.cc/cache/websites/mjolnirstudios.com_7yjlc/mjolnirstudios.com/IanBullard/files/79ffbca75a75720f066d491e9ea935a0-10.html
public class GameRand implements RNG {
	
	private long low;
	private long high;
	
	public GameRand(long seed) {
		high = seed;
		low = seed ^ 0xDEAFBABE49616E42L;
	};
	
	public long nextLong() {
		high = (high << 32) + (high >> 32);
	    high += low;
	    low += high;
	    return high;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "GameRand";
	}

}
