//Java programming Assignment

//Assignment instructions:
//1. Create a new class called CalculateG. 
/2. Copy and paste the following initial version of the code. Note variables declaration and the types. 
class CalculateG { 
    public static void main(String[] arguments){ 
    (datatype) gravity =-9.81; // Earth's gravity in m/s^2
    (datatype) fallingTime = 30; 
    (datatype)initialVelocity = 0.0; 
    (datatype) finalVelocity = ; 
    (datatype) initialPosition = 0.0; 
    (datatype) finalPosition = ;
    // Add the formulas for position and velocity 
    //finalVelocity
    finalVelocity = gravity * fallingTime ;
    //distance
    m = 0.5 * gravity * fallingTime*fallingTime;
    
    System.out.println("The object's position after " + fallingTime + " seconds is " 
    + finalPosition + " m."); 
    // Add output line for velocity (similar to position) 
    System.out.println("The object's finalVelocity after " + fallingTime + " seconds is " 
    + finalVelocity + initialVelocity);
    
} 
}
//3. Modify the example program to compute the position and velocity of an object after 
  falling for 30 seconds, outputting the position in meters. The formula in Math 
  notation is: 
  𝑥(𝑡) = 0.5 ∗𝑎𝑡2 + 𝑣𝑖𝑡 + 𝑥𝑖 
  𝑣(𝑡) = 𝑎𝑡 + 𝑣𝑖 
  
  class CalculateG { 
    public static void main(String[] arguments){ 
    a =-9.81; // Earth's gravity in m/s^2
    t = 30; 
    vi = 0.0; 
    v = ; 
    x = 0.0; 
    xi = ;
    // Add the formulas for position and velocity 
    //finalVelocity
    v(t) = a * t * vi ;
    //distance
    m = 0.5 * a * t*t + 𝑣𝑖𝑡 + 𝑥𝑖;
    
    System.out.println("The object's position after " + t + " seconds is " 
    + xi + " m."); 
    // Add output line for velocity (similar to position) 
    System.out.println("The object's finalVelocity after " + t + " seconds is " 
    + v + xi);
    
} 
}

4. Run the completed code in Eclipse (Run → Run As → Java Application). 5.
Extend datatype class with the following code: 
public class CalculateG { 
public static double multi(……){ 
// method for multiplication
} 
// add 2 more methods for powering to square and summation (similar to multiplication)
public static void outline(……){ 
// method for printing out a result
} 
public static void main(String[] args) { 
// compute the position and velocity of an object with defined methods and print out the 
result 
} 
} 
6. Create methods for multiplication, powering to square, summation and printing out a result in 
CalculateG class.
