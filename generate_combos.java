public class Combinations{

     public static void main(String []args){
        combine("ACGLT", new StringBuffer(), 0);
     }
     
     public static void combine(String instr, StringBuffer outstr, int index) {
        for (int i = index; i < instr.length(); i++) {
            outstr.append(instr.charAt(i));
            System.out.print(outstr);
            System.out.println(",");
            combine(instr, outstr, i + 1);
            outstr.deleteCharAt(outstr.length() - 1);
        }
    } 
}