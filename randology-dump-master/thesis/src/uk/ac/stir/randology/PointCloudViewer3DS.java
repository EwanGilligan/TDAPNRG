package uk.ac.stir.randology;


import javax.swing.*;
import org.math.plot.*;

import uk.ac.stir.randology.generator.RNG;

public class PointCloudViewer3DS {
	
	public String name;
	public int numberOfPoints = 4096; //4096;
	public double[][] points;
	
	public double scale = 0.01;
	
	public PointCloudViewer3DS(String name, double[][] points) {
		this.name = name;
		this.points = points;
	}
	
	public PointCloudViewer3DS(RNG rng) {
		this.points = new double[numberOfPoints][3];
		
		int j = 0;
		while (j < numberOfPoints) {
			for(int k = 0; k < 3; k++) {
				points[j][k] = rng.nextDouble();
			}
			boolean correct = true;
			for(int k = 0; k < 3; k++) {
				correct &= (points[j][k] < scale);
			}
			if (correct && j % 200 == 0) { System.out.print("."); }
			if (correct) { j++; }
		}
		this.name = "output";// of " + rng.getName();
	}
	
    public void display() {
    
        double[] xs = new double[points.length];
        double[] ys = new double[points.length];
        double[] zs = new double[points.length];
        
        for(int k = 0; k < points.length; k++) {
        	xs[k] = points[k][0];
        	ys[k] = points[k][1];
        	zs[k] = points[k][2];
        }
        Plot3DPanel plot = new Plot3DPanel();
        plot.addLegend("SOUTH");
        plot.addScatterPlot(name, xs, ys, zs);
        
        JFrame frame = new JFrame("PlotApplet");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 800);
        frame.setContentPane(plot);
        frame.setVisible(true);
        
   }
}
