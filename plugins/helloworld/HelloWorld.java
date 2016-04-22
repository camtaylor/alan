import java.util.Scanner;

public class HelloWorld {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println(":speak:Hello, World");
        System.out.println(":listen:Give me a number");
        Scanner sc=new Scanner(System.in);
        int x = sc.nextInt();
        System.out.println(x);
    }

}
