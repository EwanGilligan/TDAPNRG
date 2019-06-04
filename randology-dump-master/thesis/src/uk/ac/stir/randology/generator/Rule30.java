package uk.ac.stir.randology.generator;

// Wolfram's Rule 30 generator from RngPack
public class Rule30 implements RNG {

    private long s0;
    private long s1;
    private long s2;


    public Rule30(long seed) {
	    //s0 = 0;
	    //s1 = seed;
	    //s2 = 0;
    	setSeed(0,seed,0);
    }

    private void setSeed(final long w0, final long w1, final long w2) {
		final int BLOCKS = 3;
		final int BITS_PER_BLOCK = 64;
	
		// this loop can certainly be unrolled, and the use of array eliminated
		// however this isn't critical and this shows how to extend
		// the algorithm for more blocks
		long input[] = {w0, w1, w2};      // pack into array to simply algorithm below
		long output[] = new long[BLOCKS]; // tmp variable for holding state
	
		for (int j = 0; j < BLOCKS * BITS_PER_BLOCK; ++j) {
		    int inputBlock = j / BITS_PER_BLOCK;
		    int inputPos = j % BITS_PER_BLOCK;
		    int outputBlock = j % BLOCKS;
		    int outputPos = j / BLOCKS;
	
		    // get the bit we are working on
		    // if it's 0, nothing to do
		    // if it's 1, set the appropriate bit
		    // MAYBE: use table instead of shifting.
		    if ((input[inputBlock] & (1L << inputPos)) != 0L) {
			output[outputBlock] |= (1L << outputPos);
		    }
		}
		this.s0 = output[0];
		this.s1 = output[1];
		this.s2 = output[2];
    }

    private long getBits(int bits) {
		long result = 0;
		long t0, t1, t2;
		for (int j = bits; j != 0; --j) {
		    result = (result << 1) | ((s0 >>> 32) & 1L);
		    t0 = ((s2 >>> 1) | (s2 << 63)) ^ (s0 | s1);
		    t2 = s1 ^ (s2 | ((s0 << 1) | (s0 >>> 63)));
		    t1 = s0 ^ (s1 | s2);
		    s0 = t0; s1 = t1; s2 = t2;
		}
		return result;
    }

	@Override
	public String getName() {
		return "Rule30";
	}

	public long nextLong() {
		long x = getBits(64);
		return x;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	@Override
	public double nextDouble() {
		return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
}
