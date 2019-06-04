package uk.ac.stir.randology.generator;


public class BlumBlumShub implements RNG {

        private long pq = 50159L * 50207L;
        private long state;
        
        public BlumBlumShub(long seed) {
        	state = seed % pq;
        }
        
        
        public long nextLong() {
        	long result = 0;
        	for (int i = 0; i < 64; i++) {
        		state = state*state % pq;
        		result = 2*result + (state % 2);
        	}
        	return result;
        }
        
        
        public double nextDouble() {
        	return Math.abs((double)nextLong()/Long.MAX_VALUE);
        }
        
        public long next64bits() {
        	return nextLong();
        }
        
        @Override
        public String getName() {
        	return "BlumBlumShub";
        }
}

