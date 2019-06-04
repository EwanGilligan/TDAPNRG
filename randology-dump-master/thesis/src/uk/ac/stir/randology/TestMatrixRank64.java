package uk.ac.stir.randology;

import org.apache.commons.math3.stat.inference.ChiSquareTest;

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
public class TestMatrixRank64 {
	
	//--- Test configuration ---//
	
	int numberOfRuns = 10;
	int dimension = 64;
	int numberOfMatrices = 50;
	
	double[] filtrationValues = { 0, dimension - 3, dimension - 2, dimension - 1, dimension, dimension + 1 };
	double[] expectedValues = { 50, 43, 1, 1, 1, 1 };
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	private ChiSquareTest chi2 = new ChiSquareTest();
	//--- Implementation ---//
	
	private int getBit(long input, int position)
	{
	   return (int) ((input >> position) & 1);
	}
	
	private double singleRun(RNG rng) {
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
		
		VietorisRipsStream<Integer> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);
		long[] observedValues = new long[filtrationValues.length];
		
		for (int i = 0; i < filtrationValues.length; i++) {
			observedValues[i] = barcodes.getBettiNumbersMap(filtrationValues[i]).get(0);
			//System.out.print(observedValues[i] + " ");
		}
		
		// 4. Return chi^2 test result
		double result = chi2.chiSquareTest(expectedValues, observedValues);
		//System.out.printf("%.3f\n",result);
		return result;
	}
	
	public int performTest(RNG rng) {
		int passes = 0;
		for( int i = 0; i < numberOfRuns; i++ ) {
			if (singleRun(rng) > 0.01) passes++;
		}
		return passes;
	}
	
}
