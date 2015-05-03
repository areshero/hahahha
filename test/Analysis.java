package com.hw1;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.TreeMap;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import org.hsqldb.jdbc.jdbcDataSource;
import org.python.core.PyInstance;
import org.python.util.PythonInterpreter;


public class Analysis {

	public static final int width = 352;
	public static final int height = 288;

	Connection c;

	public Analysis() {

		try {
			jdbcDataSource dataSource = new jdbcDataSource();
			dataSource.setDatabase("jdbc:hsqldb:file:my576database1/data");
			c = dataSource.getConnection("SA", "");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void shutdown() throws SQLException {

		Statement st = c.createStatement();
		st.execute("SHUTDOWN");
		c.close(); // if there are no other open connection
	}

	public synchronized void query(String expression) throws SQLException {

		Statement st = null;
		ResultSet rs = null;
		st = c.createStatement();
		rs = st.executeQuery(expression);
		dump(rs);
		st.close();

	}

	public static void dump(ResultSet rs) throws SQLException {

		ResultSetMetaData meta = rs.getMetaData();
		int colmax = meta.getColumnCount();
		int i;
		Object o = null;

		for (; rs.next();) {
			for (i = 0; i < colmax; ++i) {
				o = rs.getObject(i + 1);
				System.out.print(o.toString() + " ");
			}
			System.out.println(" ");
		}
	}

	public synchronized void update(String expression) throws SQLException {

		Statement st = null;
		st = c.createStatement();
		int i = st.executeUpdate(expression);
		if (i == -1) {
			System.out.println("db error : " + expression);
		}
		st.close();
	}

	public void commit() throws SQLException {
		c.commit();
	}

	private static void run(String fileName) {

		// String fileName =
		// "/Users/chongli/Desktop/576/final/CSCI576_Project_Database/flowers/flowers001.rgb";

		BufferedImage img = new BufferedImage(width, height,
				BufferedImage.TYPE_INT_RGB);
		HashMap<String, Integer> dominColor = new HashMap<String, Integer>();

		try {
			byte[] bytes = readFile(fileName);
			dominColor = printOriginalImage(width, height, img, bytes);
			System.out.println(dominColor);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		JPanel panel = new JPanel();
		panel.add(new JLabel(new ImageIcon(img)));

		JFrame frame = new JFrame("Display images");

		frame.getContentPane().add(panel);
		frame.pack();
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	private static HashMap<String, Integer> printOriginalImage(int width,
			int height, BufferedImage img1, byte[] bytes) {

		HashMap<String, Integer> dominColor = new HashMap<String, Integer>();
		int ind1 = 0;
		dominColor.put("r", 0);
		dominColor.put("g", 0);
		dominColor.put("b", 0);

		HashMap<Integer, Integer> rMap = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> gMap = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> bMap = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> allMap = new HashMap<Integer, Integer>();

		ValueComparator bvcr = new ValueComparator(rMap);
		ValueComparator bvcg = new ValueComparator(gMap);
		ValueComparator bvcb = new ValueComparator(bMap);
		ValueComparator bvcall = new ValueComparator(allMap);

		TreeMap<Integer, Integer> srMap = new TreeMap<Integer, Integer>(bvcr);
		TreeMap<Integer, Integer> sgMap = new TreeMap<Integer, Integer>(bvcg);
		TreeMap<Integer, Integer> sbMap = new TreeMap<Integer, Integer>(bvcb);
		TreeMap<Integer, Integer> sallMap = new TreeMap<Integer, Integer>(
				bvcall);

		int rCount = 0;
		int rM = 0;
		int gCount = 0;
		int gM = 0;
		int bCount = 0;
		int bM = 0;

		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {

				byte a = 0;
				int r1 = bytes[ind1];
				int g1 = bytes[ind1 + height * width];
				int b1 = bytes[ind1 + height * width * 2];

				int r = r1;
				int b = b1;
				int g = g1;

				if (r < 0) {
					r += 256;

				}
				if (b < 0) {
					b += 256;
				}
				if (g < 0) {
					g += 256;
				}

				r = r >> 6;
				g = g >> 6;
				b = b >> 6;

				// r
				if (rMap.containsKey(r)) {
					rMap.put(r, rMap.get(r) + 1);
				} else {
					rMap.put(r, 1);
				}

				if (rCount <= rMap.get(r)) {
					rCount = rMap.get(r);
					rM = r;
				}

				// g
				if (gMap.containsKey(g)) {
					gMap.put(g, gMap.get(g) + 1);
				} else {
					gMap.put(g, 1);
				}

				if (gCount < gMap.get(g)) {
					gCount = gMap.get(g);
					gM = g;
				}

				// b
				if (bMap.containsKey(b)) {
					bMap.put(b, bMap.get(b) + 1);
				} else {
					bMap.put(b, 1);
				}

				if (bCount < bMap.get(b)) {
					bCount = bMap.get(b);
					bM = b;
				}

				// int pix = 0xff000000 | ((r & 0xff) << 16) | ((g & 0xff) << 8)
				// | (b &
				// 0xff);
				int pix = ((a << 24) + (r1 << 16) + (g1 << 8) + b1);

				if (allMap.containsKey(pix)) {
					allMap.put(pix, allMap.get(pix) + 1);
				} else {
					allMap.put(pix, 1);
				}

				img1.setRGB(x, y, pix);
				ind1++;
			}

		}
		srMap.putAll(rMap);
		sgMap.putAll(gMap);
		sbMap.putAll(bMap);
		sallMap.putAll(allMap);

		dominColor.put("r", rM + 128);
		dominColor.put("g", gM + 128);
		dominColor.put("b", bM + 128);
		System.out.println(srMap);
		System.out.println(sgMap);
		System.out.println(sbMap);
		// System.out.println(sallMap);

		return dominColor;
	}

	private static byte[] readFile(String fileName)
			throws FileNotFoundException, IOException {
		File file = new File(fileName);
		InputStream is = new FileInputStream(file);

		long len = file.length();
		byte[] bytes = new byte[(int) len];

		int offset = 0;
		int numRead = 0;
		while (offset < bytes.length
				&& (numRead = is.read(bytes, offset, bytes.length - offset)) >= 0) {
			offset += numRead;
		}

		is.close();
		return bytes;
	}

	public static void main(String[] args) throws InterruptedException {
		
		PythonInterpreter.initialize(System.getProperties(),System.getProperties(), new String[0]);
		PythonInterpreter interpreter =new PythonInterpreter();
		interpreter.exec("import sys");
		interpreter.exec("sys.path.append('/usr/local/Celler/opencv/2.4.11')");
		interpreter.exec("sys.path.append('/usr/local/lib/python2.7/site-packages')");
		
		interpreter.execfile("/Users/hehehehehe/Desktop/workspace/576python/test/test.py");
		PyInstance test = (PyInstance) interpreter.eval("Hello()");
		test.invoke("extractMotion");
		
		Process p;
		try {
			p = Runtime
					.getRuntime()
					.exec("python /Users/hehehehehe/Desktop/workspace/576python/test/test.py");
			BufferedReader in = new BufferedReader(new InputStreamReader(
					p.getInputStream()));
			String s = in.readLine();
			System.out.println("value is : " + s);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static void main1(String[] args) throws SQLException {
		Analysis a = new Analysis();

		// a.update("drop table dominColor");
		// a.update("drop table frame");
		// a.update("create table frame (frameid integer primary key , filename varchar(256))");
		// a.update("create table dominColor(id integer GENERATED by DEFAULT AS IDENTITY PRIMARY KEY,"
		// +
		// " r integer, g integer,b integer, frameid integer , pointcount integer, foreign key(frameid) references frame(frameid)) ");

		String base = "/Users/chongli/Desktop/576/final/CSCI576_Project_Database/";
		int i = 601;
		/*
		 * for(int k = 1; i <= 600;k++, i++){ TreeMap<MyCodeWord,
		 * HashSet<MyPoint>> result =
		 * ColorUtil.getDominateColor(base+"flowers/flowers"
		 * +String.format("%03d", i)+".rgb");
		 * a.update("insert into frame values("
		 * +i+", 'flowers"+String.format("%03d", i)+"')"); for(MyCodeWord code :
		 * result.keySet()){
		 * a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
		 * +code
		 * .getX()+","+code.getY()+","+code.getZ()+","+result.get(code).size
		 * ()+", "+i+")"); } a.commit(); }
		 */

		for (int k = 1; i <= 1200; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "interview/interview"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'interview"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
			a.commit();
		}

		for (int k = 1; i <= 1800; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "movie/movie"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'movie"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
			a.commit();
		}
		for (int k = 1; i <= 2400; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "musicvideo/musicvideo"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'musicvideo"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
			a.commit();
		}
		for (int k = 1; i <= 3000; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "sports/sports"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'sports"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
			a.commit();
		}
		for (int k = 1; i <= 3600; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "starcraft/starcraft"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'starcraft"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
		}
		for (int k = 1; i <= 4200; k++, i++) {
			TreeMap<MyCodeWord, HashSet<MyPoint>> result = ColorUtil
					.getDominateColor(base + "traffic/traffic"
							+ String.format("%03d", k) + ".rgb");
			a.update("insert into frame values(" + i + ", 'trafic"
					+ String.format("%03d", k) + "')");
			for (MyCodeWord code : result.keySet()) {
				a.update("insert into dominColor(r,g,b,pointcount, frameid) values("
						+ code.getX()
						+ ","
						+ code.getY()
						+ ","
						+ code.getZ()
						+ "," + result.get(code).size() + ", " + i + ")");
			}
			a.commit();
		}

		a.commit();
		a.shutdown();
		/*
		 * a.update("delete  from extractedColor"); a.update("CREATE TABLE ");
		 * 
		 * 
		 * File folder = new File(
		 * "/Users/chongli/Desktop/576/final/CSCI576_Project_Database/flowers");
		 * File files[] = folder.listFiles();
		 * 
		 * for (int i = 0; i < 600; i++) { TreeMap<MyCodeWord, HashSet<MyPoint>>
		 * result = ColorUtil.getDominateColor(files[i].getAbsolutePath());
		 * files[i].getName();
		 * 
		 * }
		 */

		// run("/Users/chongli/Desktop/576/final/CSCI576_Project_Database/flowers/flowers011.rgb");

		//
		// try {
		//
		// a.update("INSERT INTO extractedColor(colorvalue) VALUES(300)");
		// a.query("SELECT * FROM extractedColor");
		// a.commit();
		// a.shutdown();
		//
		// } catch (Exception ex3) {
		// ex3.printStackTrace();
		// }

	}

}

class ValueComparator implements Comparator<Integer> {

	Map<Integer, Integer> base;

	public ValueComparator(Map<Integer, Integer> base) {
		this.base = base;
	}

	// Note: this comparator imposes orderings that are inconsistent with
	// equals.
	public int compare(Integer a, Integer b) {
		if (base.get(a) >= base.get(b)) {
			return -1;
		} else {
			return 1;
		} // returning 0 would merge keys
	}
}