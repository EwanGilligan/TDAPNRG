package uk.ac.stir.randology;

import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.chain_basis.Simplex;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.metric.impl.ExplicitMetricSpace;
import edu.stanford.math.plex4.streams.impl.*;

import uk.ac.stir.randology.generator.RNG;
import gausselim.*;

/**
 * Matrix Rank Homology Test
 * @author zak
 *
 */
public class DeriveMatrixRank64 {
	
	//--- Test configuration ---//
	
	int numberOfRuns = 1;
	int dimension = 64;
	int numberOfMatrices = 50;

	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	double[] filtration = { 0, dimension - 3, dimension - 2, dimension - 1, dimension, dimension + 1 };
	
	//--- Implementation ---//
	
	private int getBit(long input, int position)
	{
	   return (int) ((input >> position) & 1);
	}
	
	private int getBetti(BarcodeCollection<Double> barcodes, double filter, int number) {
		return (barcodes.getBettiNumbersMap(filter).get(number) == null) ? 0 : barcodes.getBettiNumbersMap(filter).get(number);
	}
	
	private void testRun(RNG rng) {
		// 1. Generate matrices
		@SuppressWarnings("unchecked") Matrix<Integer>[] mats = (Matrix<Integer>[]) new Matrix[numberOfMatrices];
		
		
		for(int j = 0; j < numberOfMatrices; j++) {
			mats[j] = new Matrix<Integer>( dimension, dimension, new PrimeField(2) );
			for( int r = 0; r < dimension; r++ ) {
				long rowBase = rng.next64bits(); 
				for( int c = 0; c < dimension; c++ ) {
					mats[j].set(r, c, getBit(rowBase,c));
				}
			}
		}
		
		double[][] distance = new double[numberOfMatrices][numberOfMatrices];
		
		for(int j = 0; j < numberOfMatrices; j++) for(int k = 0; k <= j; k++) {
			Matrix<Integer> t = mats[j].add(mats[k]);
			distance[j][k] = t.rank();
			distance[k][j] = distance[j][k];
		}

		// 2. Create Vietoris-Rips complex
		ExplicitMetricSpace space = new ExplicitMetricSpace(distance);
		
		VietorisRipsStream<Integer> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtration);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);
		
		for (int i = 0; i < filtration.length; i++) {
			int observed = getBetti(barcodes, filtration[i], 0);
			System.out.print(observed + ",");
		}
		System.out.println( "x" );

	}
	
	public void perform() {
		System.out.println("Matrix Rank Test, d = 64, deriving phase START");
    	
    	// 2. Perform runs
    	for( RNG rng : Generators.fullTest ) {
    		for( int run = 0; run < numberOfRuns; run++ ) {
    			testRun(rng);
    		}
    	}

    	System.out.println("Matrix Rank Homology Test END");
	}
	
	public static void main(String[] args) {
		new DeriveMatrixRank64().perform();
	}
	
}
