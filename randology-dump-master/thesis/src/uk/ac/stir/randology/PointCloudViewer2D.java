package uk.ac.stir.randology;


import javax.swing.*;
import org.math.plot.*;

import uk.ac.stir.randology.generator.RNG;

public class PointCloudViewer2D {
	
	public String name;
	public int numberOfPoints = 2000;
	public double[][] points;
	
	public PointCloudViewer2D(String name, double[][] points) {
		this.name = name;
		this.points = points;
	}
	
	public PointCloudViewer2D(RNG rng) {
		this.points = new double[numberOfPoints][2];
		//for( int j = 0; j < numberOfPoints; j++ ) for( int k = 0; k < 2; k++ ) {
		//	points[j][k] = rng.nextDouble();
		//}
		int j = 0;
		while (j < numberOfPoints) {
			for(int k = 0; k < 2; k++) {
				points[j][k] = rng.nextDouble();
			}
			boolean correct = true;
			for(int k = 0; k < 2; k++) {
				correct &= (points[j][k] < 1);
			}
			if (correct) { j++; System.out.print("."); if (j % 100 == 0) System.out.println(); }
		}
		this.name = "output";// of " + rng.getName();
	}
	
    public void display() {
    
        double[] xs = new double[points.length];
        double[] ys = new double[points.length];
        
        for(int k = 0; k < points.length; k++) {
        	xs[k] = points[k][0];
        	ys[k] = points[k][1];
        }
        Plot2DPanel plot = new Plot2DPanel();
        plot.addLegend("SOUTH");
        plot.addScatterPlot(name, xs, ys);
        
        JFrame frame = new JFrame("PlotApplet");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 600);
        frame.setContentPane(plot);
        frame.setVisible(true);
        
   }
}
