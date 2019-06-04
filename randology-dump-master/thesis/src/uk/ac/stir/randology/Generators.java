package uk.ac.stir.randology;


import uk.ac.stir.randology.generator.RNG;

public class Generators {
	
	public static final long seed1 = 0x2197B942509FF4DBL;
	public static final long seed2 = 0xD978757273F2FCD2L;
	
	public static RNG[] fullTest = {
			// Linear Congruential Generators: 0-8
			//new uk.ac.stir.randology.generator.Randu(seed1),
			//new uk.ac.stir.randology.generator.Randu(seed2),
			//new uk.ac.stir.randology.generator.Minstd(seed1),
			//new uk.ac.stir.randology.generator.Minstd(seed2),
			//new uk.ac.stir.randology.generator.Glibc(seed1),
			//new uk.ac.stir.randology.generator.Glibc(seed2),
			//new uk.ac.stir.randology.generator.JavaRandom(seed1),
			//new uk.ac.stir.randology.generator.JavaRandom(seed2),
			//new uk.ac.stir.randology.generator.MWC(seed1),
			//new uk.ac.stir.randology.generator.MWC(seed2),
			//new uk.ac.stir.randology.generator.EICG1(seed1),
			//new uk.ac.stir.randology.generator.EICG1(seed2),
			// Linear Feedback Shift Registers: 8-12
			//new uk.ac.stir.randology.generator.LFSR(seed1),
			//new uk.ac.stir.randology.generator.LFSR(seed2),
			//new uk.ac.stir.randology.generator.XorShift32(seed1),
			//new uk.ac.stir.randology.generator.XorShift32(seed2),
			//new uk.ac.stir.randology.generator.XorShift64(seed1),
			//new uk.ac.stir.randology.generator.XorShift64(seed2),
			// WELL generators: 12-14
			//new uk.ac.stir.randology.generator.MersenneTwister(seed1),
			//new uk.ac.stir.randology.generator.MersenneTwister(seed2),
			// Cryptographically Secure Generators: 14-16
			//new uk.ac.stir.randology.generator.BlumBlumShub(seed1),
			//new uk.ac.stir.randology.generator.BlumBlumShub(seed2),
			//new uk.ac.stir.randology.generator.QCG631(seed1),
			//new uk.ac.stir.randology.generator.QCG651(seed1),
			//new uk.ac.stir.randology.generator.QCG981(seed1),
			new uk.ac.stir.randology.generator.Webkit2(seed1),
			//new uk.ac.stir.randology.generator.GameRand(seed1),
			//new uk.ac.stir.randology.generator.PCG32(seed2),
			//new uk.ac.stir.randology.generator.Ranrot(seed2),
			//new uk.ac.stir.randology.generator.Lamar((int)seed1),
			//new uk.ac.stir.randology.generator.Rule30(seed1),
			//new uk.ac.stir.randology.generator.Ranmar(seed1),
			// True Random Numbers: 16-18
			//new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series1-50M",640000),
			//new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series2-50M",640000),
			// Others: 18--
			//new uk.ac.stir.randology.generator.Quasirandom()
	};
	
	// True Random Number Generators
	public static RNG[] trngs = {
			new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-50M-R",640000),
			new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series1-50M",640000),
			new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series2-50M",640000),
	};
	
	public static RNG[] spectral = {
			//new uk.ac.stir.randology.generator.LCG("ANSIC",1103515245,12345,2147483648L,seed1),  // 0.84, 0.52, 0.43
			//new uk.ac.stir.randology.generator.LCG("Minstd",16807,0,2147483647L,seed1),          // 0.34, 0.44,	0.57
			//new uk.ac.stir.randology.generator.LCG("Minvar",48271,0,2147483647L,seed1),          // 0.90, 0.83, 0.59
			new uk.ac.stir.randology.generator.LCG("Simscript",630360016,0,2147483647L,seed1),   // 0.82, 0.43, 0.68
			//new uk.ac.stir.randology.generator.LCG("DERIVE",3141592653L,1,4294967296L,seed1),    // 0.10, 0.56, 0.52
			//new uk.ac.stir.randology.generator.LCG("Randu",65539,0,2147483648L,seed1)            // 0.93, 0.01, 0.45
	};
	
	public static RNG[] minitest = {
			new uk.ac.stir.randology.generator.MiniEICG(0),
			new uk.ac.stir.randology.generator.MiniEICG(seed1),
			/*new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series1-50M",640000),
			new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-Series2-50M",640000),
			new uk.ac.stir.randology.generator.MersenneTwister(seed1),
			new uk.ac.stir.randology.generator.MersenneTwister(seed2),
			new uk.ac.stir.randology.generator.MiniLCG(seed1),
			new uk.ac.stir.randology.generator.MiniLCG(seed2),
			new uk.ac.stir.randology.generator.MiniICG(seed1),
			new uk.ac.stir.randology.generator.MiniICG(seed2),*/
			//new uk.ac.stir.randology.generator.FromBinaryFile("res/RandomOrg-50M-R",640000),
	};
	
}
