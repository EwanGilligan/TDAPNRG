package uk.ac.stir.randology.generator;

import java.util.Random;

// The Lamar genetic programming evolved RNG by Lamenca-Martinez et al.
public class MiniLamar implements RNG {
	
	private byte[] counter = new byte[8];
	
	private long rotdk(long x, long moves) { // multi-bit right shift
		 return (x >> moves);
	}
	private long vrotdk(long x, long moves) { // multi-bit right rotation
		 return (x >> moves) | (x << (Long.SIZE - moves));
	}
	private long vrotik(long x, long moves) { // multi-bit left rotation
		 return (x << moves) | (x >> (Long.SIZE - moves));
	}
	private long vrotd(long x) { // one bit right rotation
		return vrotdk(x,1);
	}
	private long vroti(long x) {
		return vrotik(x,1);
	}
	
	
	public long nextLong() {
		// output
		long nonce;
		long aux1;
		long aux2;
		long aux3;
		aux1 = ((vroti(counter[6] ^ counter[1]) ^ counter[2] ^ counter[4] ^ counter[6]) * 99) + counter[3];
		aux2 = rotdk(aux1, vrotd(99)) ^ (counter[1]<<1);
		aux1 = (99 * aux2) + counter[5];
		aux2 = rotdk(aux1, 99) ^ counter[1] ^ (counter[3] * counter[6]);
		aux1 = rotdk(aux2, 99) ^ counter[1] ^ ((counter[1]<<1) * counter[3]);
		aux2 = ((counter[0] ^ counter[1] ^ counter[3] ^ counter[7]) * 99) + counter[5];
		aux3 = ((rotdk(aux2, vrotd(99)) ^ counter[0]) * 99) + counter[5];
		aux2 = rotdk(aux3, vrotd(99)) ^ counter[0] ^ counter[2];
		aux3 = (counter[2] ^ counter[6]) + (vroti(aux2)>>1);
		aux2 = vrotdk(aux1,99) ^ counter[3] ^ aux3;
		aux1 = ((aux2 * 99) + counter[5] + counter[7]) * 99;
		aux2 = (counter[6] ^ counter[1]) + counter[5] + vrotd(99);
		nonce = ((aux1 + counter[5]) * 99) + aux2;
		
		// counter feedback
		for(int i = 0; i < 7; i++) {
			counter[i] = counter[i+1];
		}
		counter[7] = (byte) nonce;
		
		return nonce;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public MiniLamar(int seed) {
		Random r = new Random(seed);
		for( int i = 0; i < 8; i++ ) {
			counter[i] = (byte) r.nextLong();
		}
	}
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "Lamar";
	}

}
