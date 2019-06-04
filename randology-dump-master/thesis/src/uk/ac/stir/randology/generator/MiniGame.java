package uk.ac.stir.randology.generator;

// GameRand is an incredibly fast random number generator due to Stephan Schaem.
// see http://www.redditmirror.cc/cache/websites/mjolnirstudios.com_7yjlc/mjolnirstudios.com/IanBullard/files/79ffbca75a75720f066d491e9ea935a0-10.html
public class MiniGame implements RNG {
	
	private byte low;
	private byte high;
	
	public MiniGame(long seed) {
		high = (byte)seed;
		low  = (byte)(seed >> 8);
	};
	
	public long nextLong() {
		high = (byte) ((high << 4) + (high >> 4));
	    high += low;
	    low += high;
	    return high;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / 256 );
	}
	
	@Override
	public String getName() {
		return "GameRand";
	}

}
