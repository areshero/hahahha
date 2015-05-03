import java.io.*;
 
class test2{
    public static void main(String a[]){
        try{
         /*
        String prg = "import sys\nprint int(sys.argv[1])+int(sys.argv[2])\n";
        BufferedWriter out = new BufferedWriter(new FileWriter("test1.py"));
        out.write(prg);
        out.close();
        */
        int number1 = 10;
        int number2 = 32;
         
        //ProcessBuilder pb = new ProcessBuilder("python","client.py",String.valueOf(number1),String.valueOf(number2));
        ProcessBuilder pb = new ProcessBuilder("python","client.py","hahaha");
        Process p = pb.start();
         
        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        //System.out.println("ok");
        //Integer ret = new Integer(in.readLine()).intValue();
        //while (true)
            System.out.println(in.readLine());
        //System.out.println("value is : "+ret.toString());
        }catch(Exception e){
            System.out.println(e);
        }
    }
}