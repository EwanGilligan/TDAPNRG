package uk.ac.stir.randology;

import uk.ac.stir.randology.generator.*;

public class XRunExperiment {
	
	public static void main(String[] args) {
		long time = System.currentTimeMillis();
		TestLCSH1 test = new TestLCSH1();
		System.out.println(test);
		
		for(RNG rng : Generators.fullTest) {
			int result = test.performTest(rng);
			System.out.printf("%-32s %2d/10\n", rng.getName(), result);
		}
		
		System.out.printf("\nTook %dms\n",System.currentTimeMillis() - time);
		System.out.println("ALL DONE");
	}
	
}
