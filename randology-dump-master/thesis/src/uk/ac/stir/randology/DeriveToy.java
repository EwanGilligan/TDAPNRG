package uk.ac.stir.randology;

import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.chain_basis.Simplex;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.metric.impl.EuclideanMetricSpace;
import edu.stanford.math.plex4.streams.impl.*;

import org.apache.commons.math3.stat.inference.*;

import uk.ac.stir.randology.generator.RNG;

/**
 * Unit Cube Homology Test
 * @author zak
 *
 */
@SuppressWarnings("unused")
public class DeriveToy {
	
	//--- Test configuration ---//
	
	private int numberOfRuns = 5;
	private int numberOfPoints = 64;
	private int dimension = 2;
	
	private double[] filtrationValues = {0.0, 0.01, 0.04, 0.05, 0.08, 0.09, 0.11, 0.12 };
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 2;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	//--- Implementation ---//
	
	private int getBetti(BarcodeCollection<Double> barcodes, double filter, int number) {
		return (barcodes.getBettiNumbersMap(filter).get(number) == null) ? 0 : barcodes.getBettiNumbersMap(filter).get(number);
	}
	
	private void testRun(RNG rng) {
		// 1. Generate points
		double[][] points = new double[numberOfPoints][dimension];
		for(int j = 0; j < numberOfPoints; j++) for(int k = 0; k < dimension; k++) {
			points[j][k] = rng.nextDouble();
		}
		
		// 2. Create Vietoris-Rips complex
		EuclideanMetricSpace space = Plex4.createEuclideanMetricSpace(points);
		VietorisRipsStream<double[]> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);

		long[] observedValues = new long[filtrationValues.length];
		for (int i = 0; i < filtrationValues.length; i++) {
			observedValues[i] = getBetti(barcodes,filtrationValues[i],0);
			System.out.print(observedValues[i] + ",");
		}
		System.out.println( "x" );
		/*for (int i = 1; i < filtrationValues.length-1; i++) {
			observedValues[i] = (barcodes.getBettiNumbersMap(filtrationValues[i]).get(1) == null) ? 0 : barcodes.getBettiNumbersMap(filtrationValues[i]).get(1);
			System.out.print(observedValues[i] + ",");
		}
    	System.out.println( "x" );
    	*/
	}
	
	public void perform() {
		System.out.println("Hypercube Test, d = 2, proof of concept, deriving phase START");
		
		// 1. Print csv header
    	for( double value : filtrationValues ) {
    		System.out.print(value + ",");
    	}
    	System.out.println("x");
    	
    	// 2. Perform runs
    	for( RNG rng : Generators.minitest ) {
    		for( int run = 0; run < numberOfRuns; run++ ) {
    			testRun(rng);
    		}
    	}

    	System.out.println("END");
	}
	
	public static void main(String[] args) {
		new DeriveToy().perform();
	}
	
	
}
