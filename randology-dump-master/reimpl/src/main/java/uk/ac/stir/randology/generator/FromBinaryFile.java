package uk.ac.stir.randology.generator;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/**
 * Generator that takes consecutive bits from a binary file, returning ratios of 64-bit integers as double-precision floating point values.
 * 
 * @author zak
 */
public class FromBinaryFile implements RNG {
    
    private ByteBuffer byteBuffer;
    private byte[] buffer;
    private FileInputStream inputStream;
    
    private String name;
    
    public FromBinaryFile(String filePath, int size) {
        this.name = "File-" + filePath.replace('/', '-');
        this.buffer = new byte[size*64];
        try {
            this.inputStream = new FileInputStream(filePath);
            this.inputStream.read(buffer);
        } catch (IOException e) { e.printStackTrace(); }
        this.byteBuffer = ByteBuffer.wrap(buffer).order(ByteOrder.LITTLE_ENDIAN);
    }
    
    public long nextLong() {
        long b0 = 0xFFL & (long)(byteBuffer.get());
        long b1 = 0xFFL & (long)(byteBuffer.get());
        long b2 = 0xFFL & (long)(byteBuffer.get());
        long b3 = 0xFFL & (long)(byteBuffer.get());
        long b4 = 0xFFL & (long)(byteBuffer.get());
        long b5 = 0xFFL & (long)(byteBuffer.get());
        long b6 = 0xFFL & (long)(byteBuffer.get());
        long b7 = 0xFFL & (long)(byteBuffer.get());
        return (b7) | (b6 << 8) | (b5 << 16) | (b4 << 24) | (b3 << 32) | (b2 << 40) | (b1 << 48) | (b0 << 56);
    }
    
    public long next64bits() {
        return nextLong();
    }
    
    public double nextDouble() {
        return Math.abs((double)nextLong() / Long.MAX_VALUE);
    }
    
    public String getName() {
        return name;
    }
    
}
