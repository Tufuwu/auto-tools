public class Leetcode {
    public static void main(String[] args) {
        String a ="1001101";
        Leetcode solution = new Leetcode();
        int result = solution.maxOperations(a);
        System.out.println(result);
    }

    public int maxOperations(String s) {
        int i = 0;
        int j = s.length()-1;
        int t = 0;
        while(i<j){
            while(true && i<=j){
                if(s.charAt(i)=='1'){
                    break;
                }
                i++;
                System.out.println(i);
            }
            while(true && j>=i){
                if(s.charAt(j) =='0'){
                    break;
                }
                j--;
                // System.out.println(j);
            }
            if(i<j){
                i++;
                j--;
                t++;
            }
        }
        return t;
    }
}
