package uk.ac.stir.randology;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import uk.ac.stir.randology.generator.RNG;

public class XRunOutput {
	
	public static void main(String[] args) {
		System.out.println("Starting...");
	    new ToBinaryFile(new uk.ac.stir.randology.generator.GameRand(0xDEAFBABEDEADBEEFL),"Gamerand",125);
		System.out.println("ALL DONE");
	}
	
}

class ToBinaryFile {

	private RNG rng;
	private FileOutputStream output;
	
	public ToBinaryFile(RNG rng, int rounds) {
		this(rng,rng.getName(),rounds);
	}
	
	public ToBinaryFile(RNG rng, String filename, int rounds) {
		this.rng = rng;
		try {
			File file = new File("out" + filename);
			file.createNewFile();
			this.output = new FileOutputStream(file);
			for(int i = 0; i < rounds; i++) { writeRound(); }
			output.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private void writeRound() throws IOException {
		byte[] buffer = new byte[80000];
		// fill buffer
		for (int i = 0; i < 80000; i += 8) {
			long out = rng.next64bits();
			buffer[i+7] = (byte)(out     );
			buffer[i+6] = (byte)(out >> 8);
			buffer[i+5] = (byte)(out >> 16);
			buffer[i+4] = (byte)(out >> 24);
			buffer[i+3] = (byte)(out >> 32);
			buffer[i+2] = (byte)(out >> 40);
			buffer[i+1] = (byte)(out >> 48);
			buffer[i+0] = (byte)(out >> 56);
		}
		output.write(buffer);
	}
	
	
}