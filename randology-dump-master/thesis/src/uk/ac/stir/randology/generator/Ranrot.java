package uk.ac.stir.randology.generator;

// Implements the Ranrot algorithm of Agner Fog 
public class Ranrot implements RNG {
	
	private int[] randbuffer = {
			0x00000000, 0x9f392ae8, 0x881ca142, 0x900870db, 
			0x22226582, 0x67c98aea, 0x66b35d14, 0xc4e98bdf, 
			0xfd976f0e, 0x8a8bd962, 0x00000000, 0xd2eef179, 
			0x0aaff088, 0x823bed31, 0xf0f82685, 0xd8939479, 0x148c7af8, 
	};
	private int index1 = 0;
	private int index2 = 10;
	
	private int seed;
	
	
	public Ranrot(long seed) {
		randbuffer[index1] = (int)(seed);
		randbuffer[index2] = (int)(seed << 32);
		this.seed = randbuffer[index1];
	}
	
	public long nextLong() {
		int left  = nextInt();
		int right = nextInt();
		return (left << 32) ^ (right >>> 32);
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		nextInt();
	    return Math.abs( (double)seed / Integer.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "RANROT";
	}
	
	private int nextInt() {
		randbuffer[index1] = rotl(randbuffer[index2], 13) + rotr(randbuffer[index1], 9);
		seed = randbuffer[index1];
		if (--index1 < 0) index1 = 16;
		if (--index2 < 0) index2 = 16;
		return seed;
	}
	
	private int rotr(int bits, int shift) {
	     return (bits >>> shift) | (bits << (32 - shift));
	}
	private int rotl(int bits, int shift) {
	    return (bits << shift) | (bits >>> (32 - shift));
	}
	
}
